import pytest
import json
from unittest.mock import patch, mock_open
from ..identify_runtime_from_lock import extract_deps

# Mock data
mock_data = {
    "packages": {
        "packageA": {"dev": None, "version": "1.0.0"},
        "packageB": {"dev": None, "version": "2.0.0"},
        "packageC": {"dev": True, "version": "3.0.0"},
        "packageD": {"dev": None, "version": "4.0.0"}
    }
}


def test_extract_deps():
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = extract_deps("dummy_path")
        assert result == ["packageA", "packageB", "packageD"], f"Expected ['packageA', 'packageB', 'packageD'], got {result}"


def test_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        with pytest.raises(FileNotFoundError):
            extract_deps("non_existent_path")


def test_empty_json():
    empty_data = {"packages": {}}
    with patch("builtins.open", mock_open(read_data=json.dumps(empty_data))):
        result = extract_deps("dummy_path")
        assert result == [], f"Expected an empty list, got {result}"


def test_no_runtime_deps():
    no_runtime_data = {
        "packages": {
            "packageA": {"dev": True, "version": "1.0.0"},
            "packageB": {"dev": True, "version": "2.0.0"}
        }
    }
    with patch("builtins.open", mock_open(read_data=json.dumps(no_runtime_data))):
        result = extract_deps("dummy_path")
        assert result == [], f"Expected an empty list, got {result}"

