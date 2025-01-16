import pytest
import json
from ..debloat_lock_file import remove_directs, remove_indirect, collect_keys, reg_names  

# Test for `remove_directs` function
def test_remove_directs():
    mock_data = {
        "packages": {
            "": {
                "dependencies": {
                    "packageA": "^1.0.0",
                    "packageB": "^2.0.0"
                }
            }
        }
    }
    directs = ["node_modules/packageA"]

    result = remove_directs(mock_data, directs)

    assert "packageA" not in result["packages"][""]["dependencies"], "Expected packageA to be removed"
    assert "packageB" in result["packages"][""]["dependencies"], "packageB should not be removed"

def test_remove_indirect():
    mock_data = {
        "packages": {
            "node_modules/packageA": {
                "dependencies": {
                    "packageB": "^1.0.0"
                }
            },
            "node_modules/packageB": {
                "dev": False,
                "dependencies": {}
            }
        }
    }
    key = "node_modules/packageB"
    result = remove_indirect(mock_data, key)

    assert "packageB" not in result["packages"]["node_modules/packageA"]["dependencies"], "packageB should be removed"
    assert "node_modules/packageB" not in result["packages"], "node_modules/packageB should be removed"

def test_remove_indirect_dev():
    mock_data = {
        "packages": {
            "node_modules/packageA": {
                "dependencies": {
                    "packageB": "^1.0.0"
                }
            },
            "node_modules/packageB": {
                "dev": False,
                "dependencies": {}
            }
        }
    }
    key = "node_modules/packageB"
    result = remove_indirect(mock_data, key)

    assert "packageB" not in result["packages"]["node_modules/packageA"]["dependencies"], "packageB should be removed"
    assert result["packages"]["node_modules/packageB"]["dev"] is True, "packageB should be marked as dev"

def test_collect_keys():
    mock_data = {
        "packages": {
            "node_modules/packageA": {
                "dependencies": {}
            },
            "node_modules/packageB": {
                "dependencies": {}
            },
            "src/packageA": {
                "dependencies": {}
            }
        }
    }

    result = collect_keys(mock_data, "node_modules/", "packageA")
    assert "node_modules/packageA" in result, "Expected node_modules/packageA to be matched"
    assert "node_modules/packageB" in result, "Expected node_modules/packageB to be matched"
    assert "src/packageA" not in result, "src/packageA should not be matched"

def test_reg_names():
    result = reg_names("node_modules/packageA")
    assert result == {"folder": "", "dep": "packageA"}, f"Expected {{'folder': '', 'dep': 'packageA'}}, got {result}"

def test_reg_names_invalid():
    result = reg_names("packageA")
    assert result == {"folder": "", "dep": "packageA"}, f"Expected {{'folder': '', 'dep': 'packageA'}}, got {result}"

def test_remove_indirect_file_not_found():
    mock_data = {
        "packages": {
            "node_modules/packageA": {
                "dependencies": {
                    "packageB": "^1.0.0"
                }
            }
        }
    }
    key = "node_modules/packageC"  
    result = remove_indirect(mock_data, key)

    assert mock_data == result, "The data should remain unchanged when no matching dependency is found"
