import datetime

import pandas as pd
import numpy as np

# Standardize values for Likert scales
likert_mapping = {
        'Very satisfied': 5, 'Very good': 5, 'Strongly agree': 5, 'Very concerned': 5, 'Very familiar': 5,
        'Satisfied': 4, 'Good': 4, 'Agree': 4, 'Concerned': 4, 'Familiar': 4,
        'Neither satisfied nor dissatisfied': 3, 'Acceptable': 3, 'Neutral': 3, 'Somewhat familiar': 3,
        'Dissatisfied': 2, 'Poor': 2, 'Disagree': 2, 'Unconcerned': 2, 'Unfamiliar': 2,
        'Very dissatisfied': 1, 'Very poor': 1, 'Strongly disagree': 1, 'Very unconcerned': 1, 'Very unfamiliar': 1,
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


def handle_matrix_question(df, base_column_name):
    """
    Handle matrix-style questions where multiple items are rated on the same scale.

    Parameters:
    df (pandas.DataFrame): The input dataframe
    base_column_name (str): The base name of the matrix question

    Returns:
    dict: Dictionary with each item as a key and its processed values as values
    """
    # Find all columns that belong to this matrix question
    matrix_columns = [col for col in df.columns if base_column_name in col]

    results = {}
    for col in matrix_columns:
        # Extract the specific item name (e.g., "Desktop Computer" from the full column name)
        item_name = col.split('[')[-1].strip(']') if '[' in col else col

        # Process the values using the appropriate mapping
        if any(val in df[col].fillna('').values for val in likert_mapping.keys()):
            results[item_name] = map_values(df[col], likert_mapping)
        elif any(val in df[col].fillna('').values for val in frequency_mapping.keys()):
            results[item_name] = map_values(df[col], frequency_mapping)
        else:
            results[item_name] = df[col]

    return results


def clean_data(df):
    cleaned_df = df.copy()

    # Remove unnecessary columns
    cleaned_df = cleaned_df.drop(['Timestamp', '1. Your name (optional)'], axis=1)

    # Handle the device familiarity matrix question
    device_familiarity = handle_matrix_question(
        cleaned_df,
        '11. How familiar are you with using the following device(s)?'
    )

    # Create a new dataframe with the processed matrix questions
    device_familiarity_df = pd.DataFrame(device_familiarity)

    # Rename columns to be more concise
    device_familiarity_df.columns = [
        'Desktop_familiarity',
        'Laptop_familiarity',
        'Phone_familiarity',
        'Feature_phone_familiarity',
        'Tablet_familiarity',
        'Smartwatch_familiarity'
    ]

    # Handle other demographic columns as before
    demographics = cleaned_df[[
        '2. Your age range by generation',
        '3. Your gender',
        '4. Language(s) you speak (please select all that apply)',
        '5. Country you live in',
        '6. Your nationality',
        '7. Your highest educational qualification (please select only one option)',
        '8. What is the major (e.g., Computer Science/IT, Engineering, Medical, General Science, Arts, Commerce etc.) of your study?',
        '9. Your occupation (please select all that apply)',
        '10. Which electronic device(s) do you use normally for communication with others? (please select all that apply)',

        '12. How familiar are you with using the Internet? [Your opinion]',
        '13. How is the quality of your overall Internet access according to you? [Your opinion]'
    ]].copy()

    # Rename demographic columns
    demographics.columns = [
        'Age_range',
        'Gender',
        'Languages',
        'Country',
        'Nationality',
        'Education',
        'Major',
        'Occupation',
        'Devices',

        'Internet_familiarity',
        'Internet_quality'
    ]

    # Iterate through the columns in the demographics DataFrame and Apply value mappings to relevant columns
    for col in demographics.columns:
        if demographics[col].dtype == 'object':
            col_values = demographics[col].fillna('').values
            if any(val in col_values for val in likert_mapping.keys()):
                demographics[col] = map_values(demographics[col], likert_mapping)
        elif any(val in col_values for val in frequency_mapping.keys()):
            demographics[col] = map_values(demographics[col], frequency_mapping)

    # Combine demographic data with device familiarity data
    final_df = pd.concat([demographics, device_familiarity_df], axis=1)

    return final_df


def generate_quality_report(df):
    return {
        'missing_values': df.isnull().sum(),
        'value_counts': {col: df[col].value_counts() for col in df.columns}
    }


if __name__ == "__main__":
    df = pd.read_csv('data_v0.csv')
    print("\n=== Dataset Overview ===")
    print(f"Number of responses: {len(df)}")
    print(f"Number of questions: {len(df.columns)}")

    cleaned_data = clean_data(df)
    print("\nCleaning complete. Saving cleaned data...")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    cleaned_data.to_csv('cleaned_survey_data'+ timestamp +'.csv', index=False)

    quality_report = generate_quality_report(cleaned_data)
    print("\nQuality report generated.")