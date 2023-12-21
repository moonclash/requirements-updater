import pytest
from updater.script import RequirementsUpdater


@pytest.mark.parametrize(
    "input,expected",
    [
        ("14.12.34", {"major": "14", "minor": "12", "patch": "34"}),
        ("10.20.101", {"major": "10", "minor": "20", "patch": "101"}),
        ("08.23.45", {"major": "08", "minor": "23", "patch": "45"}),
        ("02.17.56", {"major": "02", "minor": "17", "patch": "56"}),
        ("19.05.28", {"major": "19", "minor": "05", "patch": "28"}),
        ("11.33.22", {"major": "11", "minor": "33", "patch": "22"}),
        ("07.14.39", {"major": "07", "minor": "14", "patch": "39"}),
    ],
)
def test_semver_to_dict(input, expected):
    semver_dict = RequirementsUpdater.semver_to_dict(input)
    assert semver_dict == expected


@pytest.mark.parametrize(
    "available_version,current_version,semver_type,expected",
    [
        (
            {"major": "14", "minor": "12", "patch": "34"},
            {"major": "14", "minor": "12", "patch": "12"},
            "patch",
            True,
        ),
        (
            {"major": "14", "minor": "12", "patch": "34"},
            {"major": "100", "minor": "5000", "patch": "0"},
            "major",
            True,
        ),
        (
            {"major": "3000", "minor": "12", "patch": "34"},
            {"major": "100", "minor": "5000", "patch": "0"},
            "minor",
            False,
        ),
        (
            {"major": "12", "minor": "12", "patch": "100"},
            {"major": "12", "minor": "12", "patch": "150"},
            "minor",
            True,
        )
    ],
)
def test_is_newer_version(available_version, current_version, semver_type, expected):
    is_newer_version = RequirementsUpdater.is_newer_version(
        available_version, current_version, semver_type
    )
    assert is_newer_version == expected
