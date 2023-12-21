import re
from typing import Any, Dict, List
import requests


VERSION_REGEX = re.compile(r"\b\d+(\.\d+)*\b")
SPLIT_REGEX = re.compile("==|<=|>=")

class RequirementsUpdater:
    @staticmethod
    def get_package_versions(package_name: Any) -> List[Any]:
        # make sure we don't get any rc's, etc
        try:
            response = requests.get(
                f"https://pypi.org/simple/{package_name}",
                headers={"Accept": "application/vnd.pypi.simple.v1+json"},
            )
            response.raise_for_status()
            versions = response.json().get("versions")
            return list(
                reversed(
                    [version for version in versions if VERSION_REGEX.fullmatch(version)]
                )
            )
        except requests.exceptions.RequestException as e:
            print(f"Error fetching package versions for {package_name}: {e}")
            return []
    
    @staticmethod
    def semver_to_dict(version: str) -> Dict:
        holder_versions = ["0", "0", "0"]
        semver_versions = version.split(".")
        for i, v in enumerate(semver_versions):
            holder_versions[i] = v
        major, minor, patch = holder_versions
        return {"major": major, "minor": minor, "patch": patch}
    
    
    @staticmethod
    def is_newer_version(
        available_version: Dict, current_version: Dict, semver_type: str
    ) -> Any:
        if semver_type == "major":
            return available_version["major"] >= current_version["major"]
        elif semver_type == "minor":
            return (
                available_version["major"] == current_version["major"]
                and available_version["minor"] >= current_version["minor"]
            )
        elif semver_type == "patch":
            return (
                available_version["major"] == current_version["major"]
                and available_version["minor"] == current_version["minor"]
                and available_version["patch"] >= current_version["patch"]
            )
        return False
    
    @staticmethod 
    def get_latest_version(
        current_version: Any, available_versions: List[str], semver_type: str
    ) -> Any:
        current_version_semver = RequirementsUpdater.semver_to_dict(current_version)
        for version in available_versions:
            available_version_semver = RequirementsUpdater.semver_to_dict(version)
            if RequirementsUpdater.is_newer_version(
                available_version_semver, current_version_semver, semver_type
            ):
                return version
        return current_version
    
    
    @staticmethod
    def format_package_string(package: str, version: str) -> str:
        parts = package.split("[")
        return f"{parts[0]}=={version}" + (f"[{parts[1]}" if len(parts) > 1 else "")
    
    @staticmethod
    def split_package_name(package: str) -> Dict:
        package_splits = package.split("[")
        package_name, *specification = package_splits
        return {
            "package_name": package_name,
            "specification": specification[0] if specification else "",
        }
    
    
    @staticmethod
    def update_requirements(file_path, semver_type) -> None:
        with open(file_path) as file:
            updated_packages = []
            for line in file.readlines():
                if not line.startswith("#"):
                    package, current_version = re.split(SPLIT_REGEX, line)
                    package_split = RequirementsUpdater.split_package_name(package)
                    package_name = package_split.get("package_name")
                    latest_version = RequirementsUpdater.get_latest_version(
                        current_version,
                        RequirementsUpdater.get_package_versions(package_name),
                        f"{semver_type}",
                    )
                    updated_package_name = f"{package_name}{('[' + package_split.get('specification')) if package_split.get('specification') else ''}"  # type: ignore[operator]
                    updated_packages.append(
                        f"{RequirementsUpdater.format_package_string(updated_package_name, latest_version)}\n"
                    )
                else:
                    updated_packages.append(line)
            with open("./updated-requirements.txt", mode="w") as updated_file:
                updated_file.writelines(updated_packages)
                print(
                    "Requirements updated in updated_requirements.txt file. Make sure you check the versions"
                )
 
