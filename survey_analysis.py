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


def handle_matrix_questions(df):
    """
    Handle all matrix-style questions where multiple items are rated on the same scale.

    Parameters:
    df (pandas.DataFrame): The input dataframe
    likert_mapping (dict): Mapping for Likert scale values
    frequency_mapping (dict): Mapping for frequency scale values

    Returns:
    dict: Dictionary with each item as a key and its processed values as values
    """
    results = {}
    for col in df.columns:
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

def raname_columns(df, col_start_idx):
    renamed_df = df.copy()

    short_names = [
        '1. name',
        '2. age_generation',
        '3. gender',
        '4. languages',
        '5. residence_country',
        '6. nationality',
        '7. education',
        '8. study_major',
        '9. occupation',
        '10. devices_used',
        '11. desktop_familiarity',
        '11. laptop_familiarity',
        '11. smartphone_familiarity',
        '11. featurephone_familiarity',
        '11. tablet_familiarity',
        '11. smartwatch_familiarity',
        '12. internet_familiarity',
        '13. internet_quality',
        '14. whatsapp_usage',
        '14. messenger_usage',
        '14. discord_usage',
        '14. skype_usage',
        '14. msteams_usage',
        '14. slack_usage',
        '14. instagram_usage',
        '14. snapchat_usage',
        '14. telegram_usage',
        '14. reddit_usage',
        '14. imo_usage',
        '14. viber_usage',
        '15. other_apps',
        '16. communication_targets',
        '17. whatsapp_ui_organization',
        '17. messenger_ui_organization',
        '17. discord_ui_organization',
        '17. skype_ui_organization',
        '17. msteams_ui_organization',
        '17. slack_ui_organization',
        '17. instagram_ui_organization',
        '17. snapchat_ui_organization',
        '17. telegram_ui_organization',
        '17. reddit_ui_organization',
        '17. imo_ui_organization',
        '17. viber_ui_organization',
        '18. whatsapp_response_speed',
        '18. messenger_response_speed',
        '18. discord_response_speed',
        '18. skype_response_speed',
        '18. msteams_response_speed',
        '18. slack_response_speed',
        '18. instagram_response_speed',
        '18. snapchat_response_speed',
        '18. telegram_response_speed',
        '18. reddit_response_speed',
        '18. imo_response_speed',
        '18. viber_response_speed',
        '19. whatsapp_feature_satisfaction',
        '19. messenger_feature_satisfaction',
        '19. discord_feature_satisfaction',
        '19. skype_feature_satisfaction',
        '19. msteams_feature_satisfaction',
        '19. slack_feature_satisfaction',
        '19. instagram_feature_satisfaction',
        '19. snapchat_feature_satisfaction',
        '19. telegram_feature_satisfaction',
        '19. reddit_feature_satisfaction',
        '19. imo_feature_satisfaction',
        '19. viber_feature_satisfaction',
        '20. ui_ux_problems',
        '21. whatsapp_privacy_invasion',
        '21. messenger_privacy_invasion',
        '21. discord_privacy_invasion',
        '21. skype_privacy_invasion',
        '21. msteams_privacy_invasion',
        '21. slack_privacy_invasion',
        '21. instagram_privacy_invasion',
        '21. snapchat_privacy_invasion',
        '21. telegram_privacy_invasion',
        '21. reddit_privacy_invasion',
        '21. imo_privacy_invasion',
        '21. viber_privacy_invasion',
        '22. whatsapp_cyberbullying',
        '22. messenger_cyberbullying',
        '22. discord_cyberbullying',
        '22. skype_cyberbullying',
        '22. msteams_cyberbullying',
        '22. slack_cyberbullying',
        '22. instagram_cyberbullying',
        '22. snapchat_cyberbullying',
        '22. telegram_cyberbullying',
        '22. reddit_cyberbullying',
        '22. imo_cyberbullying',
        '22. viber_cyberbullying',
        '23. whatsapp_ad_personalization',
        '23. messenger_ad_personalization',
        '23. discord_ad_personalization',
        '23. skype_ad_personalization',
        '23. msteams_ad_personalization',
        '23. slack_ad_personalization',
        '23. instagram_ad_personalization',
        '23. snapchat_ad_personalization',
        '23. telegram_ad_personalization',
        '23. reddit_ad_personalization',
        '23. imo_ad_personalization',
        '23. viber_ad_personalization',
        '24. whatsapp_misinformation',
        '24. messenger_misinformation',
        '24. discord_misinformation',
        '24. skype_misinformation',
        '24. msteams_misinformation',
        '24. slack_misinformation',
        '24. instagram_misinformation',
        '24. snapchat_misinformation',
        '24. telegram_misinformation',
        '24. reddit_misinformation',
        '24. imo_misinformation',
        '24. viber_misinformation',
        '25. whatsapp_identity_theft',
        '25. messenger_identity_theft',
        '25. discord_identity_theft',
        '25. skype_identity_theft',
        '25. msteams_identity_theft',
        '25. slack_identity_theft',
        '25. instagram_identity_theft',
        '25. snapchat_identity_theft',
        '25. telegram_identity_theft',
        '25. reddit_identity_theft',
        '25. imo_identity_theft',
        '25. viber_identity_theft',
        '26. whatsapp_location_tracking',
        '26. messenger_location_tracking',
        '26. discord_location_tracking',
        '26. skype_location_tracking',
        '26. msteams_location_tracking',
        '26. slack_location_tracking',
        '26. instagram_location_tracking',
        '26. snapchat_location_tracking',
        '26. telegram_location_tracking',
        '26. reddit_location_tracking',
        '26. imo_location_tracking',
        '26. viber_location_tracking',
        '27. whatsapp_data_misuse',
        '27. messenger_data_misuse',
        '27. discord_data_misuse',
        '27. skype_data_misuse',
        '27. msteams_data_misuse',
        '27. slack_data_misuse',
        '27. instagram_data_misuse',
        '27. snapchat_data_misuse',
        '27. telegram_data_misuse',
        '27. reddit_data_misuse',
        '27. imo_data_misuse',
        '27. viber_data_misuse',
        '28. privacy_problem_reasons',
        '29. legal_framework_adequacy',
        '30. personal_data_concerns',
        '31. privacy_improvement_suggestions',
        '32. privacy_violation_experience',
        '33. whatsapp_content_findability',
        '33. messenger_content_findability',
        '33. discord_content_findability',
        '33. skype_content_findability',
        '33. msteams_content_findability',
        '33. slack_content_findability',
        '33. instagram_content_findability',
        '33. snapchat_content_findability',
        '33. telegram_content_findability',
        '33. reddit_content_findability',
        '33. imo_content_findability',
        '33. viber_content_findability',
        '34. whatsapp_content_loss',
        '34. messenger_content_loss',
        '34. discord_content_loss',
        '34. skype_content_loss',
        '34. msteams_content_loss',
        '34. slack_content_loss',
        '34. instagram_content_loss',
        '34. snapchat_content_loss',
        '34. telegram_content_loss',
        '34. reddit_content_loss',
        '34. imo_content_loss',
        '34. viber_content_loss',
        '35. data_loss_reasons',
        '36. whatsapp_login_issues',
        '36. messenger_login_issues',
        '36. discord_login_issues',
        '36. skype_login_issues',
        '36. msteams_login_issues',
        '36. slack_login_issues',
        '36. instagram_login_issues',
        '36. snapchat_login_issues',
        '36. telegram_login_issues',
        '36. reddit_login_issues',
        '36. imo_login_issues',
        '36. viber_login_issues',
        '37. whatsapp_unintended_sharing',
        '37. messenger_unintended_sharing',
        '37. discord_unintended_sharing',
        '37. skype_unintended_sharing',
        '37. msteams_unintended_sharing',
        '37. slack_unintended_sharing',
        '37. instagram_unintended_sharing',
        '37. snapchat_unintended_sharing',
        '37. telegram_unintended_sharing',
        '37. reddit_unintended_sharing',
        '37. imo_unintended_sharing',
        '37. viber_unintended_sharing',
        '38. whatsapp_spam_frequency',
        '38. messenger_spam_frequency',
        '38. discord_spam_frequency',
        '38. skype_spam_frequency',
        '38. msteams_spam_frequency',
        '38. slack_spam_frequency',
        '38. instagram_spam_frequency',
        '38. snapchat_spam_frequency',
        '38. telegram_spam_frequency',
        '38. reddit_spam_frequency',
        '38. imo_spam_frequency',
        '38. viber_spam_frequency',
        '39. security_problem_reasons',
        '40. whatsapp_missed_notifications',
        '40. messenger_missed_notifications',
        '40. discord_missed_notifications',
        '40. skype_missed_notifications',
        '40. msteams_missed_notifications',
        '40. slack_missed_notifications',
        '40. instagram_missed_notifications',
        '40. snapchat_missed_notifications',
        '40. telegram_missed_notifications',
        '40. reddit_missed_notifications',
        '40. imo_missed_notifications',
        '40. viber_missed_notifications',
        '41. whatsapp_notification_satisfaction',
        '41. messenger_notification_satisfaction',
        '41. discord_notification_satisfaction',
        '41. skype_notification_satisfaction',
        '41. msteams_notification_satisfaction',
        '41. slack_notification_satisfaction',
        '41. instagram_notification_satisfaction',
        '41. snapchat_notification_satisfaction',
        '41. telegram_notification_satisfaction',
        '41. reddit_notification_satisfaction',
        '41. imo_notification_satisfaction',
        '41. viber_notification_satisfaction',
        '42. notification_problem_reasons',
        '43. app_availability_comparison',
        '44. switching_problems',
        '45. others_switching_problems',
        '46. omnichannel_productivity',
        '46. omnichannel_time_saving',
        '46. omnichannel_collaboration',
        '46. omnichannel_communication_gap',
        '46. omnichannel_app_switching',
        '46. omnichannel_conversation_tracking',
        '47. omnichannel_dependency',
        '47. omnichannel_info_overload',
        '47. omnichannel_downtime_effect',
        '47. omnichannel_feature_limitation',
        '47. omnichannel_adoption_difficulty',
        '48. omnichannel_work_life_balance',
        '48. omnichannel_privacy',
        '48. omnichannel_security',
        '48. omnichannel_data_loss',
        '48. omnichannel_integration',
        '49. omnichannel_adoption_likelihood',
        '50. omnichannel_adoption_prediction',
        '51. omnichannel_suggestions'
    ]

    # Function to extract question number from column name
    def get_question_number(col_name):
        # Extract the number at the start of the column name
        match = re.match(r'^(\d+[a-z]?\.) ', col_name)
        return match.group(1) if match else None

    # Create a mapping of original columns to new names
    column_mapping = {}
    current_std_name_idx = col_start_idx
    # Sort columns by question number to ensure correct mapping
    sorted_columns = sorted(renamed_df.columns,
                            key=lambda x: (int(get_question_number(x).split('.')[0])
                                           if get_question_number(x) else float('inf')))


    # Create mapping for each column
    for col in sorted_columns:
        # int(get_question_number(col))
        # question_number = int(get_question_number(short_names[current_std_name_idx]))
        if current_std_name_idx < len(short_names):
                long_idx_str = col.split('.')[0]
                short_idx_str = short_names[current_std_name_idx].split('.')[0]

                if col_start_idx == 18:
                    short_idx = int(short_idx_str)
                    long_idx = int(long_idx_str)
                    if short_idx != long_idx:
                        current_std_name_idx += 1
                        continue
                # print(f"Mapping: {col} -> {short_names[current_std_name_idx]}")
                column_mapping[col] = short_names[current_std_name_idx]
                current_std_name_idx += 1


    # Rename all columns using the mapping
    renamed_df = renamed_df.rename(columns=column_mapping)

    return renamed_df

def replace_likert_values(df):
    cleaned_df = df.copy()

    # Remove unnecessary columns
    # cleaned_df = cleaned_df.drop(['Timestamp', '1. name'], axis=1)

    # Handle the device familiarity matrix question
    # todo: do we need this
    # todo: handle ; or , separated values
    matrix_vals = handle_matrix_questions(cleaned_df)


    # Iterate through the columns in the demographics DataFrame and Apply value mappings to relevant columns
    for col in cleaned_df.columns:
        if cleaned_df[col].dtype == 'object':
            col_values = cleaned_df[col].fillna('').values
            if any(val in col_values for val in likert_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], likert_mapping)
            elif any(val in col_values for val in frequency_mapping.keys()):
                cleaned_df[col] = map_values(cleaned_df[col], frequency_mapping)

    # Combine demographic data with device familiarity data
    # final_df = pd.concat([cleaned_df], axis=1)
    return cleaned_df

def generate_quality_report(df):
    return {
        'missing_values': df.isnull().sum(),
        'value_counts': {col: df[col].value_counts() for col in df.columns}
    }


if __name__ == "__main__":
    input_file = 'data_v2.xlsx'
    demographic_df = pd.read_excel(input_file, sheet_name='Demographic')
    print("\n=== Raw Demographic Dataset Overview ===")
    print(f"Number of responses: {len(demographic_df)}")
    print(f"Number of questions: {len(demographic_df.columns)}")

    dm_cleaned_data = raname_columns(demographic_df,0)
    print("\nCleaning complete. Saving cleaned data...")
    print("\n=== Demographic Cleaned Dataset Overview ===")
    print(f"Number of responses: {len(dm_cleaned_data)}")
    print(f"Number of questions: {len(dm_cleaned_data.columns)}")

    quantitative_df = pd.read_excel(input_file, sheet_name='Quantitative')
    print("\n=== Raw Quantitative Dataset Overview ===")
    print(f"Number of responses: {len(quantitative_df)}")
    print(f"Number of questions: {len(quantitative_df.columns)}")

    qn_cleaned_data = raname_columns(quantitative_df, 18)
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