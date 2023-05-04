## NS2K Sample Sheet Validator
This Python script validates the contents of a Nextseq 2k sample sheet, ensuring that it meets the expected format. It includes several features for processing and modifying the data, including:

Replacing special characters in the sample IDs with hyphens
Removing Unicode characters from all columns in the sample sheet
Converting column names to title case
Generating a processed sample sheet with headers in the expected format
Providing a link to download the processed sample sheet in CSV format

[![.github/workflows/test.yml](https://github.com/thanhleviet/sample_sheet_validator/actions/workflows/test.yml/badge.svg)](https://github.com/thanhleviet/sample_sheet_validator/actions/workflows/test.yml)
## Installation
This script requires Python 3 and several third-party libraries to run. You can install the required dependencies using poetry by running the following command:

```
poetry install
```

## Usage
To use this script, run the following command:

```
streamlit run app.py
```

This will launch a web interface that allows you to upload a sample sheet file and configure various options for processing the data.

See live version at <https://thanhleviet-sample-sheet-validator-app-22jf26.streamlit.app/>

## Authors

Thanh Le-Viet