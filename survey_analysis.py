import pandas as pd
import numpy as np

def clean_survey_data(df):
    clean_df = df.copy()
    
    # Remove unnecessary columns
    clean_df = clean_df.drop(['Timestamp', '1. Your name (optional)'],  axis=1)
    
    # Standardize values for Likert scales
    likert_mapping = {
        'Very satisfied': 5, 'Very good': 5, 'Strongly agree': 5, 'Very concerned': 5,
        'Satisfied': 4, 'Good': 4, 'Agree': 4, 'Concerned': 4,
        'Neither satisfied nor dissatisfied': 3, 'Acceptable': 3, 'Neutral': 3,
        'Dissatisfied': 2, 'Poor': 2, 'Disagree': 2, 'Unconcerned': 2,
        'Very dissatisfied': 1, 'Very poor': 1, 'Strongly disagree': 1, 'Very unconcerned': 1,
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

    demographics = clean_df[[
        '2. Your age range by generation',
        '3. Your gender',
        '4. Language(s) you speak (please select all that apply)',
        '5. Country you live in',
        '6. Your nationality',
        '7. Your highest educational qualification (please select only one option)'
        '8. What is the major (e.g., Computer Science/IT, Engineering, Medical, General Science, Arts, Commerce etc.) of your study?'
        '9. Your occupation (please select all that apply)'
        '10. Which electronic device(s) do you use normally for communication with others? (please select all that apply)'
        '11. How familiar are you with using the following device(s)?'
        '12. How familiar are you with using the Internet?'
        '13. How is the quality of your overall Internet access according to you?'
    ]].copy()

    demographics.columns = [
        'age_range',
        'gender',
        'languages',
        'country',
        'nationality',
        'education',
        'major',
        'occupation',
        'devices',
        'internet_familiarity',
        'internet_quality'
    ]
    
    # Apply value mappings to relevant columns
    for col in clean_df.columns:
        if clean_df[col].dtype == 'object':
            if any(val in clean_df[col].fillna('').values for val in likert_mapping.keys()):
                clean_df[col] = clean_df[col].map(likert_mapping)
            elif any(val in clean_df[col].fillna('').values for val in frequency_mapping.keys()):
                clean_df[col] = clean_df[col].map(frequency_mapping)
    
    return {
        'clean_data': clean_df,
        'demographics': demographics
    }

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
    print("\n=== Dataset Overview ===")
    print(f"Number of responses: {len(df)}")
    print(f"Number of questions: {len(df.columns)}")
    cleaned = clean_survey_data(df)
    print("\nCleaning complete. Cleaned data saved in 'cleaned' dictionary.")
    print("\nKeys available:")
    print(cleaned)
    for key in cleaned.keys():
        print(f"- {key}")

    quality_report = generate_quality_report(cleaned)
    # print(quality_report)