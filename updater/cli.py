import argparse

from .script import update_requirements

def main():
    parser = argparse.ArgumentParser(
        description="A very simple requirements updater for python packages"
    )
    parser.add_argument(
        "file", type=str, 
        help="The requirements file that you need to update"
    )
    parser.add_argument(
        "--semver", "-s",
        type=str, help="The semver type you need to update (major, minor, patch)"
    )

    args = parser.parse_args()
    update_requirements(
        args.file, args.semver
    )


if __name__ == "__main__":
    main()