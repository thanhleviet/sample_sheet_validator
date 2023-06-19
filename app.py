# -*- coding: utf-8 -*-
"""
@author: thanh-le-viet <thanh.le-viet@quadram.ac.uk>
@date: 2023-05-01
"""
import pandas as pd
import streamlit as st
import re
import os
from PIL import Image
import datetime

def replace_special_characters(text):
    """
    Replaces multiple special characters in a string with a single hyphen.
    
    Parameters:
        text (str): The input string to modify.
        
    Returns:
        str: The modified string with multiple special characters replaced by a single hyphen.
    """
    # replace multiple special characters with a single hyphen
    text = re.sub(r'[\W_]+', '-', text)
    # replace multiple hyphens with a single hyphen
    text = re.sub(r'-+', '-', text)
    # replace multiple underscores with a single underscore
    text = re.sub(r'_+', '_', text)
    return text

def remove_unicode(df):
    """
    Remove all Unicode characters from all columns in a pandas DataFrame.
    
    Parameters:
        df (pandas.DataFrame): The DataFrame to modify.
        
    Returns:
        pandas.DataFrame: The modified DataFrame with Unicode characters removed.
    """
    # Iterate over each column in the DataFrame
    for col in df.columns:
        # Replace all Unicode characters like "\U" with an empty string
        df[col] = df[col].str.replace(r"\\U[a-zA-Z0-9]{8}", "", regex=True)
    return df

def rename_duplicates(df, column):
    """
    Rename duplicated values in a column of a DataFrame.

    Args:
        df (pandas.DataFrame): The DataFrame containing the column to rename.
        column (str): The name of the column to process.

    Returns:
        pandas.DataFrame: A copy of the input DataFrame with duplicated values in the specified column renamed.

    """

    duplicates = df.duplicated(column)
    new_df = df.copy()

    for index, row in df.iterrows():
        if duplicates[index]:
            count = duplicates[:index].sum()
            new_value = f'{row[column]}_{count + 1}'
            new_df.loc[index, column] = new_value

    return new_df

def columns_to_title_case(df):
    """
    Returns a new DataFrame with column names in title case format.
    
    Parameters:
        df (pandas.DataFrame): The input DataFrame to modify.
        
    Returns:
        pandas.DataFrame: A new DataFrame with column names in title case format.
    """
    # Create a dictionary of old column names to new column names in title case format
    new_columns = {col: col.title() for col in df.columns}
    
    # Use the rename() method to rename the columns with the new titles
    df = df.rename(columns=new_columns)
    
    # Return the modified DataFrame
    return df

def process_data(data,HEADER_TEXT):
    today = datetime.date.today()
    formatted_date = today.strftime('%Y-%m-%d')
    # Replace multiple special characters in Sample_ID with a single hyphen
    data["Sample_Id"] = data["Sample_Id"].apply(replace_special_characters)
    # Rename duplicate sample id
    data = rename_duplicates(data, "Sample_Id")
    # Append processed data to headers
    headers = HEADER_TEXT + "\n" + data.to_csv(index=False)
    # Show link to download processed file
    st.download_button(label="Download Processed Data", data=headers.encode(), file_name=f"sample_sheet_{st.session_state.run_name}_{formatted_date}.csv", mime="text/csv")

def main():
    # Set the page title and icon
    st.set_page_config(page_title="NS2K Sample_Sheet Validator", page_icon=":smiley:")
    # Define the required columns
    required_cols = ["Sample_ID", "index", "index2", "Sample_Project"]
    st.title('Nextseq 2k Sample Sheet Validator')
    uploaded_file = st.file_uploader(
            "Upload XLS or CSV file",
            type=["xls", "xlsx", "csv"],
            key="uploaded_file",
            help="To activate 'wide mode', go to the hamburger menu > Settings > turn on 'wide mode'",
        )

    file_uploaded = False
    if uploaded_file is not None:
        file_uploaded = True
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xls') or uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        # Check if the expected columns are present in the DataFrame
        missing_columns = set(required_cols) - set(df.columns)
        if missing_columns:
            st.error(f"Missing columns: {', '.join(missing_columns)}")
        else:
            df = columns_to_title_case(df)
    else:
        st.info(
            f"""
            👆 Upload a file to get started! See the example below for the expected format.
            """
        )
        image = Image.open('./static/table.png')
        st.image(image, caption='Example of a valid sample sheet', use_column_width=False)

    st.text_input('Run name', key='run_name', value='nextseq2000', help='Run name')
    st.text_input('Adapter Read 1', key='adapter_read1', value='AGATCGGAAGAGCACACGTCTGAACTCCAGTCA', help='Adapter sequence of Read 1')
    st.text_input('Adapter Read 2', key='adapter_read2', value='AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGT', help='Adapter sequence of Read 2')
    st.text_input('BCL Convert version', key='bcl_version', value='3.10.11', help='BCL Convert version')

    col_read1cycle, col_read2cycle = st.columns(2, gap='medium')
    with col_read1cycle:
        st.number_input('Read1 Cycle', key='read1_cycle', value=151)

    with col_read2cycle:
        st.number_input('Read2 Cycle', key='read2_cycle', value=151)

    col_index1cycle, col_index2cycle = st.columns(2, gap='medium')
    with col_index1cycle:
        st.number_input('Index1 Cycle', key='index1_cycle', value=10)

    with col_index2cycle:
        st.number_input('Index2 Cycle', key='index2_cycle', value=10)

    col_BarcodeMismatchesIndex1, col_BarcodeMismatchesIndex2 = st.columns(2, gap='medium')
    with col_BarcodeMismatchesIndex1:
        st.number_input('Barcode Mismatches Index1', key='BarcodeMismatchesIndex1', value=0)
    with col_BarcodeMismatchesIndex2:
        st.number_input('Barcode Mismatches Index2', key='BarcodeMismatchesIndex2', value=0)

    no_lane_splitting = st.checkbox("No lane splitting", key='no_lane_splitting', value=True)

    if no_lane_splitting:
        _no_lane_splitting = 'TRUE'
    else:
        _no_lane_splitting = 'FALSE'

    # Define header text
    HEADER_TEXT = f"""[Header],,,
    FileFormatVersion,2,,
    RunName,{st.session_state.run_name},,
    InstrumentPlatform,NextSeq1k2k,,
    InstrumentType,NextSeq2000,,
    ,,,
    [Reads],,,
    Read1Cycles,{st.session_state.read1_cycle},,
    Read2Cycles,{st.session_state.read2_cycle},,
    Index1Cycles,{st.session_state.index1_cycle},,
    Index2Cycles,{st.session_state.index2_cycle},,
    ,,,
    [BCLConvert_Settings],,,
    SoftwareVersion,{st.session_state.bcl_version},,
    BarcodeMismatchesIndex1,{st.session_state.BarcodeMismatchesIndex1},,
    BarcodeMismatchesIndex2,{st.session_state.BarcodeMismatchesIndex2},,
    AdapterRead1,{st.session_state.adapter_read1},,
    AdapterRead2,{st.session_state.adapter_read2},,
    NoLaneSplitting,{_no_lane_splitting},,
    ,,,
    [BCLConvert_Data],,,"""
    HEADER_TEXT = '\n'.join([line.lstrip() for line in HEADER_TEXT.split('\n')])

    if st.button("Process data") and file_uploaded:
        # Perform data processing
        process_data(df,HEADER_TEXT)
    else:
        st.error("Please upload a file to process.")
    # Set the footer text
    st.markdown("Sample Sheet Validator by Thanh Le-Viet")

if __name__ == "__main__":
    main()
