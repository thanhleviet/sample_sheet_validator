import io
import pandas as pd
from app import replace_special_characters, remove_unicode, columns_to_title_case, process_data

def test_replace_special_characters():
    # Test that multiple special characters are replaced with a single hyphen
    input_text = "PID-1453-LCP21S3-B1@!$%"
    expected_output = "PID-1453-LCP21S3-B1-"
    assert replace_special_characters(input_text) == expected_output
    
    # Test that multiple hyphens are replaced with a single hyphen
    input_text = "PID-1453-LCP21S3-B1---"
    expected_output = "PID-1453-LCP21S3-B1-"
    assert replace_special_characters(input_text) == expected_output
    
    # Test that multiple underscores are replaced with a single underscore
    input_text = "PID_1453_LCP21S3_B1___"
    expected_output = "PID-1453-LCP21S3-B1-"
    assert replace_special_characters(input_text) == expected_output
    
def test_remove_unicode():
    # Test that Unicode characters are removed from a DataFrame
    input_data = pd.DataFrame({
        "Sample_Id": ["PID-1453-LCP21S3-B1", "\\U0001F600"],
        "Index": ["TAACTTGGTC", "CGTAGAACAG"],
        "Index2": ["GATTCACGAC", "\\U0001F600"],
        "Sample_Project": ["A", "B"]
    })
    expected_output = pd.DataFrame({
        "Sample_Id": ["PID-1453-LCP21S3-B1", ""],
        "Index": ["TAACTTGGTC", "CGTAGAACAG"],
        "Index2": ["GATTCACGAC", ""],
        "Sample_Project": ["A", "B"]
    })
    assert remove_unicode(input_data).equals(expected_output)
    
def test_columns_to_title_case():
    # Test that column names are converted to title case format
    input_data = pd.DataFrame({
        "Sample_Id": ["PID-1453-LCP21S3-B1"],
        "index": ["TAACTTGGTC"],
        "index2": ["GATTCACGAC"],
        "Sample_Project": ["A"]
    })
    expected_output = pd.DataFrame({
        "Sample_Id": ["PID-1453-LCP21S3-B1"],
        "Index": ["TAACTTGGTC"],
        "Index2": ["GATTCACGAC"],
        "Sample_Project": ["A"]
    })
    assert columns_to_title_case(input_data).equals(expected_output)
