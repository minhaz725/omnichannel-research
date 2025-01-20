import pandas as pd
import numpy as np


def add_new_colums(input_df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """
    Adds a new column to the DataFrame and returns the updated DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame to which the column will be added.
        column_name (str): The name of the new column to add.

    Returns:
        pd.DataFrame: The updated DataFrame with the new column added.
    """
    df = input_df.copy()

    all_options = df[column_name].dropna().str.split(';').explode()
    print(all_options)

    unique_options = sorted(all_options.unique())
    print(unique_options)
    
    # for option in unique_options:
    #     new_column_name = f"{column_name}_{option.strip()}"
    #     df[new_column_name] = df[column_name].apply(
    #         lambda x: 1 if pd.notna(x) and option in x.split(';') else 0
    #         )
    
    return df

likert_mapping = {
    'Very satisfied': 5, 'Very good': 5, 'Strongly agree': 5, 'Very concerned': 5, 'Very familiar': 5, 'Always': 5, 'Very likely' : 5,
    'Satisfied': 4, 'Good': 4, 'Agree': 4, 'Concerned': 4, 'Familiar': 4, 'Often' : 4, 'Likely' : 4,
    'Neither satisfied nor dissatisfied': 3, 'Acceptable': 3, 'Neutral': 3, 'Somewhat familiar': 3, 'Sometimes': 3, 'Normal' :3,
    'Dissatisfied': 2, 'Poor': 2, 'Disagree': 2, 'Unconcerned': 2, 'Unfamiliar': 2, 'Rarely': 2, 'Unlikely' : 2,
    'Very dissatisfied': 1, 'Very poor': 1, 'Strongly disagree': 1, 'Very unconcerned': 1, 'Very unfamiliar': 1, 'Never': 1, 'Very unlikely' : 1,
    'Not applicable': np.nan
}

age_mapping = {
    'Generation Alpha: Born after 2012': 4,
    'Generation X: Born 1965-1980' : 1,
    'Generation Z: Born 1997-2012' : 3,
    'Millennials: Born 1981-1996' : 2
}
gender_mapping = {
    'Male': 1,
    'Female': 2,
    'Preferred not to disclose': 3
}
highest_education_mapping = {
    'Below High School/SSC/O-level/Equivalent Degree' : 1,
    'High School/SSC/O-level/Equivalent Degree': 2,
    'College/HSC/A-level/Equivalent Degree': 3,
    'Above College/Diploma/Equivalent Degree': 4,
    'University/Higher Degree': 5
}



# Define a function to map values based on the provided mappings
def map_values(column, mappings):
    return column.map(mappings)

def replace_likert_values(df):
    cleaned_df = df.copy()

    # Iterate through the columns in the demographics DataFrame and Apply value mappings to relevant columns
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            col_values = cleaned_df[col].fillna('').values
            if any(val in col_values for val in age_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], age_mapping)
            elif any(val in col_values for val in gender_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], gender_mapping)
            elif any(val in col_values for val in highest_education_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], highest_education_mapping)
            elif any(val in col_values for val in likert_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], likert_mapping)

    return cleaned_df




input_file = 'updated_file_with_demographic.xlsx'
df = pd.read_excel(input_file, sheet_name='Sheet1')
#demographic_df = df.copy()

#temp = add_new_colums(df, "education")


# demographic_df = add_new_colums(demographic_df, "languages")
# print(demographic_df.columns)
# demographic_df = add_new_colums(demographic_df, "devices_used")
# print(demographic_df.columns)
# demographic_df = add_new_colums(demographic_df, "age_generation")
# print(demographic_df.columns)


temp = replace_likert_values(df)

# Save the updated DataFrame to a new Excel file
# output_path = 'updated_file_with_demographic.xlsx'
# demographic_df.to_excel(output_path, index=False)

with pd.ExcelWriter('data_v3.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
        temp.to_excel(writer, sheet_name='Demographic_Cleaned_v3', index=False)

