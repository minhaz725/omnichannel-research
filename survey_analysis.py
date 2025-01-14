import datetime

import pandas as pd
import numpy as np
import re

# Standardize values for Likert scales
likert_mapping = {
    'Very satisfied': 5, 'Very good': 5, 'Strongly agree': 5, 'Very concerned': 5, 'Very familiar': 5, 'Always': 5, 'Very likely' : 5,
    'Satisfied': 4, 'Good': 4, 'Agree': 4, 'Concerned': 4, 'Familiar': 4, 'Often' : 4, 'Likely' : 4,
    'Neither satisfied nor dissatisfied': 3, 'Acceptable': 3, 'Neutral': 3, 'Somewhat familiar': 3, 'Sometimes': 3, 'Normal' :3,
    'Dissatisfied': 2, 'Poor': 2, 'Disagree': 2, 'Unconcerned': 2, 'Unfamiliar': 2, 'Rarely': 2, 'Unlikely' : 2,
    'Very dissatisfied': 1, 'Very poor': 1, 'Strongly disagree': 1, 'Very unconcerned': 1, 'Very unfamiliar': 1, 'Never': 1, 'Very unlikely' : 1,
    'Not applicable': np.nan
}

frequency_mapping = {
    'Always': 5,
    'Often': 4,
    'Sometimes': 3,
    'Rarely': 2,
    'Never': 1,
    'Not applicable': np.nan
}

# Define a function to map values based on the provided mappings
def map_values(column, mappings):
    return column.map(mappings)


def raname_columns(df, mapping_dict):
    renamed_df = df.copy()

    # Create a mapping of original columns to new names
    column_mapping = {}

    # Create mapping for each column
    for col in renamed_df.columns:
        column_mapping[col] = mapping_dict[col]

    # Rename all columns using the mapping
    renamed_df = renamed_df.rename(columns=column_mapping)

    return renamed_df

def replace_likert_values(df):
    cleaned_df = df.copy()

    # Iterate through the columns in the demographics DataFrame and Apply value mappings to relevant columns
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            col_values = cleaned_df[col].fillna('').values
            if any(val in col_values for val in likert_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], likert_mapping)
            elif any(val in col_values for val in frequency_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], frequency_mapping)

    return cleaned_df

def generate_quality_report(df):
    return {
        'missing_values': df.isnull().sum(),
        'value_counts': {col: df[col].value_counts() for col in df.columns}
    }


if __name__ == "__main__":
    input_file = 'data_v3.xlsx'

    mapping_sheet = pd.read_excel(input_file, sheet_name='Original to Short name map')
    mapping_dict = mapping_sheet.set_index('Orignal Name')['Short Name'].to_dict()

    demographic_df = pd.read_excel(input_file, sheet_name='Demographic')
    print("\n=== Raw Demographic Dataset Overview ===")
    print(f"Number of responses: {len(demographic_df)}")
    print(f"Number of questions: {len(demographic_df.columns)}")

    dm_cleaned_data = raname_columns(demographic_df, mapping_dict)
    print("\nCleaning complete. Saving cleaned data...")
    print("\n=== Demographic Cleaned Dataset Overview ===")
    print(f"Number of responses: {len(dm_cleaned_data)}")
    print(f"Number of questions: {len(dm_cleaned_data.columns)}")

    quantitative_df = pd.read_excel(input_file, sheet_name='Quantitative')
    print("\n=== Raw Quantitative Dataset Overview ===")
    print(f"Number of responses: {len(quantitative_df)}")
    print(f"Number of questions: {len(quantitative_df.columns)}")

    qn_cleaned_data = raname_columns(quantitative_df, mapping_dict)
    print("\nData Cleaning complete. Saving cleaned data...")
    print("\n=== Quantitative Cleaned Dataset Overview ===")
    print(f"Number of responses: {len(qn_cleaned_data)}")
    print(f"Number of questions: {len(qn_cleaned_data.columns)}")

    with pd.ExcelWriter(input_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        dm_cleaned_data.to_excel(writer, sheet_name='Demographic_Cleaned', index=False)
        qn_cleaned_data.to_excel(writer, sheet_name='Quantitative_Cleaned', index=False)
        # quality_df.to_excel(writer, sheet_name='Quality_Report', index=False)

    quantitative_cleaned_df = pd.read_excel(input_file, sheet_name='Quantitative_Cleaned')
    likert_df = replace_likert_values(quantitative_cleaned_df)

    with pd.ExcelWriter(input_file, mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        likert_df.to_excel(writer, sheet_name='Quantitative_Likert', index=False)

    # quality_report = generate_quality_report(cleaned_data)
    # quality_df = pd.DataFrame(quality_report.items(), columns=['Metric', 'Value'])
    # print("\nQuality report generated.")