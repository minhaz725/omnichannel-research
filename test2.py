import pandas as pd

df_demo = pd.read_excel("updated_file.xlsx") #("data_v3.xlsx", index_col=0, sheet_name='Demographic_Cleaned_v3')

all_options = df_demo["study_major"].dropna().str.split(';').explode()
#print(all_options)

unique_options = sorted(all_options.unique())
print(len(unique_options))

groups = {
    'Arts': ['Arts', 'Arts ', 'Social Science','Economics ', 'Law', 'N'],
    'Commerce': ['Commerce', 'Business Administration '],
    'CS/IT': ['Software Engineering', 'BSc in Software Engineering', 'Bsc in Computer Science adn Engineering', 'CS', 'CSE','Computer Science', 'Computer Science ', 'Computer Science & Engineering', 'Computer Science and Engineering', 'IT',
    'Computer Science and Engineering ', 'Computer Science/IT', 'Computer science', 'Computer science ', 'Computer science and Engineering ', 'Computing ', 'Data science ', 'Information and Communication Engineering '],
    'Other_Engg': ['Biochemistry and Molecular Biology ', 'Biomedical Engineering',   
    'Civil Engineering',  'EEE',  'Electrical & Electronic Engineering', 'Electrical Engineering', 'Electrical Engineering ', 'Electrical and Electronic Engineering', 'Electrical engineering', 'Engineering', 'Engineering ',   'Industrial Engineering ',  'BSc Engineering ',
    'Maritime science', 'Materials Science and Engineering', 'Mechanical Engineering', 'Mechanical Engineering ', 'Urban and Regional Planning', 'Water Resources Engineering'],
    'Medical': ['Medical', 'Medical ', 'Nursing'],
    'General_Science': ['Science', 'Chemistry', 'General Science ', 'General science', 'Agricultural Economics', 'Agriculture', 'Fisheries']
}

study_major_mapping = {
    'Arts': 1,
    'Commerce': 2,
    'CS/IT': 3,
    'Other_Engg': 4,
    'Medical': 5,
    'General_Science': 6
}


# Define a function to map values based on the provided mappings
def map_values(column, mappings):
    return column.map(mappings)


mapping = {}
for group_name, group_items in groups.items():
    for item in group_items:
        mapping[item] = group_name

def replace_likert_values(df):
    cleaned_df = df.copy()

    # Iterate through the columns in the demographics DataFrame and Apply value mappings to relevant columns
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            col_values = cleaned_df[col].fillna('').values
            if any(val in col_values for val in study_major_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], study_major_mapping)
    return cleaned_df

df_demo = replace_likert_values(df_demo)

output_path = 'updated_file2.xlsx'
df_demo.to_excel(output_path, index=False)

# with pd.ExcelWriter('data_v4.xlsx', mode='a', engine='openpyxl', if_sheet_exists='replace') as writer:
#         df_demo.to_excel(writer, sheet_name='Demographic_Cleaned_v3', index=False)
