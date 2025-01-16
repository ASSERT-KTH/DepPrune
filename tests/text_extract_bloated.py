import pytest
import json
from unittest.mock import mock_open, patch
from ..extract_bloated_candidates import get_run_deps, collect_files, extract_direct_deps  


def test_get_run_deps():
    mock_data = "packageA__1.0.0\npackageB__2.0.0\npackageC__3.0.0"
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_run_deps("dummy_path")
        assert result == ["packageA", "packageB", "packageC"], f"Expected ['packageA', 'packageB', 'packageC'], got {result}"


def test_get_run_deps_empty():
    mock_data = ""
    
    with patch("builtins.open", mock_open(read_data=mock_data)):
        result = get_run_deps("dummy_path")
        assert result == [], f"Expected [], got {result}"


def test_collect_files():
    dependencies = ["packageA", "packageB"]
    files = [
        "src/packageA/file1.js",
        "src/packageB/file2.js",
        "node_modules/packageC/file3.js"
    ]
    
    result = collect_files(dependencies, files)
    
    assert result["reachable_files"] == [
        "src/packageA/file1.js", "src/packageB/file2.js"
    ], f"Expected reachable files, got {result['reachable_files']}"
    
    assert result["reachable_deps"] == ["packageA", "packageB"], f"Expected reachable deps, got {result['reachable_deps']}"


def test_collect_files_no_match():
    dependencies = ["packageA"]
    files = [
        "src/packageB/file1.js",
        "src/packageC/file2.js"
    ]
    
    result = collect_files(dependencies, files)
    
    assert result["reachable_files"] == [], f"Expected no reachable files, got {result['reachable_files']}"
    assert result["reachable_deps"] == [], f"Expected no reachable deps, got {result['reachable_deps']}"


def test_extract_direct_deps():
    mock_data = {
        "dependencies": {
            "packageA": "^1.0.0",
            "packageB": "^2.0.0"
        }
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = extract_direct_deps("dummy_path")
        assert result == ["packageA", "packageB"], f"Expected ['packageA', 'packageB'], got {result}"


def test_extract_direct_deps_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = extract_direct_deps("non_existent_path")
        assert result == [], f"Expected [], got {result}"


def test_extract_direct_deps_invalid_json():
    with patch("builtins.open", mock_open(read_data="Invalid JSON")):
        with pytest.raises(json.JSONDecodeError):
            extract_direct_deps("dummy_path")


def test_extract_direct_deps_no_dependencies():
    mock_data = {}
    
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_data))):
        result = extract_direct_deps("dummy_path")
        assert result == [], f"Expected [], got {result}"
