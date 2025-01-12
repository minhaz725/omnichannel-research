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


def clean_data(df):
    cleaned_df = df.copy()
    
    # Remove unnecessary columns
    cleaned_df = cleaned_df.drop(['Timestamp', '1. Your name (optional)'],  axis=1)

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
        '11. How familiar are you with using the following device(s)? [Desktop Computer / iMac / Mac mini ]',
        '12. How familiar are you with using the Internet? [Your opinion]',
        '13. How is the quality of your overall Internet access according to you? [Your opinion]'
    ]].copy()

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
        'Devices_familiarity',
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
    
    
    return demographics
    # return {
    #     'clean_data': cleaned_df,
    #     'demographics': demographics
    # }

def generate_quality_report(df_dict):
    report = {}
    for name, df in df_dict.items():
        report[name] = {
            'missing_values': df.isnull().sum(),
            'value_counts': {col: df[col].value_counts() for col in df.columns}
        }
    return report

if __name__ == "__main__":
    df = pd.read_csv('data_v0.csv')
    #print(df.columns)
    print("\n=== Dataset Overview ===")
    print(f"Number of responses: {len(df)}")
    print(f"Number of questions: {len(df.columns)}")
    demographics_cleaned = clean_data(df)
    print("\nCleaning complete. Cleaned data saved in 'cleaned' dictionary.")
    print("\nKeys available:")

    demographics_cleaned.to_csv('demographics_cleaned.csv', index=False)

    # for key in cleaned.keys():
    #     print(f"- {key}")

    #quality_report = generate_quality_report(cleaned)
    # print(quality_report)