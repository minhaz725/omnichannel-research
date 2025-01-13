import datetime

import pandas as pd
import numpy as np
from fontTools.misc.cython import returns

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

def raname_columns(df):
    renamed_df = df.copy()

    short_names = [
        'name',
        'age_generation',
        'gender',
        'languages',
        'residence_country',
        'nationality',
        'education',
        'study_major',
        'occupation',
        'devices_used',
        'desktop_familiarity',
        'laptop_familiarity',
        'smartphone_familiarity',
        'featurephone_familiarity',
        'tablet_familiarity',
        'smartwatch_familiarity',
        'internet_familiarity',
        'internet_quality',
        'whatsapp_usage',
        'messenger_usage',
        'discord_usage',
        'skype_usage',
        'msteams_usage',
        'slack_usage',
        'instagram_usage',
        'snapchat_usage',
        'telegram_usage',
        'reddit_usage',
        'imo_usage',
        'viber_usage',
        'other_apps',
        'communication_targets',
        'whatsapp_ui_organization',
        'messenger_ui_organization',
        'discord_ui_organization',
        'skype_ui_organization',
        'msteams_ui_organization',
        'slack_ui_organization',
        'instagram_ui_organization',
        'snapchat_ui_organization',
        'telegram_ui_organization',
        'reddit_ui_organization',
        'imo_ui_organization',
        'viber_ui_organization',
        'whatsapp_response_speed',
        'messenger_response_speed',
        'discord_response_speed',
        'skype_response_speed',
        'msteams_response_speed',
        'slack_response_speed',
        'instagram_response_speed',
        'snapchat_response_speed',
        'telegram_response_speed',
        'reddit_response_speed',
        'imo_response_speed',
        'viber_response_speed',
        'whatsapp_feature_satisfaction',
        'messenger_feature_satisfaction',
        'discord_feature_satisfaction',
        'skype_feature_satisfaction',
        'msteams_feature_satisfaction',
        'slack_feature_satisfaction',
        'instagram_feature_satisfaction',
        'snapchat_feature_satisfaction',
        'telegram_feature_satisfaction',
        'reddit_feature_satisfaction',
        'imo_feature_satisfaction',
        'viber_feature_satisfaction',
        'ui_ux_problems',
        'whatsapp_privacy_invasion',
        'messenger_privacy_invasion',
        'discord_privacy_invasion',
        'skype_privacy_invasion',
        'msteams_privacy_invasion',
        'slack_privacy_invasion',
        'instagram_privacy_invasion',
        'snapchat_privacy_invasion',
        'telegram_privacy_invasion',
        'reddit_privacy_invasion',
        'imo_privacy_invasion',
        'viber_privacy_invasion',
        'whatsapp_cyberbullying',
        'messenger_cyberbullying',
        'discord_cyberbullying',
        'skype_cyberbullying',
        'msteams_cyberbullying',
        'slack_cyberbullying',
        'instagram_cyberbullying',
        'snapchat_cyberbullying',
        'telegram_cyberbullying',
        'reddit_cyberbullying',
        'imo_cyberbullying',
        'viber_cyberbullying',
        'whatsapp_ad_personalization',
        'messenger_ad_personalization',
        'discord_ad_personalization',
        'skype_ad_personalization',
        'msteams_ad_personalization',
        'slack_ad_personalization',
        'instagram_ad_personalization',
        'snapchat_ad_personalization',
        'telegram_ad_personalization',
        'reddit_ad_personalization',
        'imo_ad_personalization',
        'viber_ad_personalization',
        'whatsapp_misinformation',
        'messenger_misinformation',
        'discord_misinformation',
        'skype_misinformation',
        'msteams_misinformation',
        'slack_misinformation',
        'instagram_misinformation',
        'snapchat_misinformation',
        'telegram_misinformation',
        'reddit_misinformation',
        'imo_misinformation',
        'viber_misinformation',
        'whatsapp_identity_theft',
        'messenger_identity_theft',
        'discord_identity_theft',
        'skype_identity_theft',
        'msteams_identity_theft',
        'slack_identity_theft',
        'instagram_identity_theft',
        'snapchat_identity_theft',
        'telegram_identity_theft',
        'reddit_identity_theft',
        'imo_identity_theft',
        'viber_identity_theft',
        'whatsapp_location_tracking',
        'messenger_location_tracking',
        'discord_location_tracking',
        'skype_location_tracking',
        'msteams_location_tracking',
        'slack_location_tracking',
        'instagram_location_tracking',
        'snapchat_location_tracking',
        'telegram_location_tracking',
        'reddit_location_tracking',
        'imo_location_tracking',
        'viber_location_tracking',
        'whatsapp_data_misuse',
        'messenger_data_misuse',
        'discord_data_misuse',
        'skype_data_misuse',
        'msteams_data_misuse',
        'slack_data_misuse',
        'instagram_data_misuse',
        'snapchat_data_misuse',
        'telegram_data_misuse',
        'reddit_data_misuse',
        'imo_data_misuse',
        'viber_data_misuse',
        'privacy_problem_reasons',
        'legal_framework_adequacy',
        'personal_data_concerns',
        'privacy_improvement_suggestions',
        'privacy_violation_experience',
        'whatsapp_content_findability',
        'messenger_content_findability',
        'discord_content_findability',
        'skype_content_findability',
        'msteams_content_findability',
        'slack_content_findability',
        'instagram_content_findability',
        'snapchat_content_findability',
        'telegram_content_findability',
        'reddit_content_findability',
        'imo_content_findability',
        'viber_content_findability',
        'whatsapp_content_loss',
        'messenger_content_loss',
        'discord_content_loss',
        'skype_content_loss',
        'msteams_content_loss',
        'slack_content_loss',
        'instagram_content_loss',
        'snapchat_content_loss',
        'telegram_content_loss',
        'reddit_content_loss',
        'imo_content_loss',
        'viber_content_loss',
        'data_loss_reasons',
        'whatsapp_login_issues',
        'messenger_login_issues',
        'discord_login_issues',
        'skype_login_issues',
        'msteams_login_issues',
        'slack_login_issues',
        'instagram_login_issues',
        'snapchat_login_issues',
        'telegram_login_issues',
        'reddit_login_issues',
        'imo_login_issues',
        'viber_login_issues',
        'whatsapp_unintended_sharing',
        'messenger_unintended_sharing',
        'discord_unintended_sharing',
        'skype_unintended_sharing',
        'msteams_unintended_sharing',
        'slack_unintended_sharing',
        'instagram_unintended_sharing',
        'snapchat_unintended_sharing',
        'telegram_unintended_sharing',
        'reddit_unintended_sharing',
        'imo_unintended_sharing',
        'viber_unintended_sharing',
        'whatsapp_spam_frequency',
        'messenger_spam_frequency',
        'discord_spam_frequency',
        'skype_spam_frequency',
        'msteams_spam_frequency',
        'slack_spam_frequency',
        'instagram_spam_frequency',
        'snapchat_spam_frequency',
        'telegram_spam_frequency',
        'reddit_spam_frequency',
        'imo_spam_frequency',
        'viber_spam_frequency',
        'security_problem_reasons',
        'whatsapp_missed_notifications',
        'messenger_missed_notifications',
        'discord_missed_notifications',
        'skype_missed_notifications',
        'msteams_missed_notifications',
        'slack_missed_notifications',
        'instagram_missed_notifications',
        'snapchat_missed_notifications',
        'telegram_missed_notifications',
        'reddit_missed_notifications',
        'imo_missed_notifications',
        'viber_missed_notifications',
        'whatsapp_notification_satisfaction',
        'messenger_notification_satisfaction',
        'discord_notification_satisfaction',
        'skype_notification_satisfaction',
        'msteams_notification_satisfaction',
        'slack_notification_satisfaction',
        'instagram_notification_satisfaction',
        'snapchat_notification_satisfaction',
        'telegram_notification_satisfaction',
        'reddit_notification_satisfaction',
        'imo_notification_satisfaction',
        'viber_notification_satisfaction',
        'notification_problem_reasons',
        'app_availability_comparison',
        'switching_problems',
        'conversation_tracking_difficulty',
        'miscommunication_issues',
        'communication_delays',
        'generational_difference',
        'unified_app_desire',
        'others_switching_problems',
        'others_tracking_difficulty',
        'others_miscommunication',
        'others_communication_delays',
        'others_generational_difference',
        'others_unified_desire',
        'omnichannel_productivity',
        'omnichannel_time_saving',
        'omnichannel_collaboration',
        'omnichannel_communication_gap',
        'omnichannel_app_switching',
        'omnichannel_conversation_tracking',
        'omnichannel_dependency',
        'omnichannel_info_overload',
        'omnichannel_downtime_effect',
        'omnichannel_feature_limitation',
        'omnichannel_adoption_difficulty',
        'omnichannel_work_life_balance',
        'omnichannel_privacy',
        'omnichannel_security',
        'omnichannel_data_loss',
        'omnichannel_integration',
        'omnichannel_adoption_likelihood',
        'omnichannel_adoption_prediction',
        'omnichannel_suggestions'
    ]

    # Function to extract question number from column name
    def get_question_number(col_name):
        # Extract the number at the start of the column name
        import re
        match = re.match(r'^(\d+[a-z]?\.) ', col_name)
        return match.group(1) if match else None

    # Create a mapping of original columns to new names
    column_mapping = {}
    current_std_name_idx = 0

    # Sort columns by question number to ensure correct mapping
    sorted_columns = sorted(renamed_df.columns,
                            key=lambda x: (int(get_question_number(x).split('.')[0])
                                           if get_question_number(x) else float('inf')))


    # Create mapping for each column
    for col in sorted_columns:
        if current_std_name_idx < len(short_names):
            column_mapping[col] = short_names[current_std_name_idx]
            current_std_name_idx += 1

    # Rename all columns using the mapping
    renamed_df = renamed_df.rename(columns=column_mapping)

    return renamed_df

def clean_data(df):
    cleaned_df = df.copy()

    # Remove unnecessary columns
    # cleaned_df = cleaned_df.drop(['Timestamp', '1. Your name (optional)'], axis=1)

    # Handle the device familiarity matrix question
    device_familiarity = handle_matrix_question(
        cleaned_df,
        '11. How familiar are you with using the following device(s)?'
    )

    # Create a new dataframe with the processed matrix questions
    # device_familiarity_df = pd.DataFrame(device_familiarity)


    # Handle other demographic columns as before
    # demographics = cleaned_df[[
    #     '2. Your age range by generation',
    #     '3. Your gender',
    #     '4. Language(s) you speak (please select all that apply)',
    #     '5. Country you live in',
    #     '6. Your nationality',
    #     '7. Your highest educational qualification (please select only one option)',
    #     '8. What is the major (e.g., Computer Science/IT, Engineering, Medical, General Science, Arts, Commerce etc.) of your study?',
    #     '9. Your occupation (please select all that apply)',
    #     '10. Which electronic device(s) do you use normally for communication with others? (please select all that apply)',
    #
    #     '12. How familiar are you with using the Internet? [Your opinion]',
    #     '13. How is the quality of your overall Internet access according to you? [Your opinion]'
    # ]].copy()


    # for orig, new in column_mapping.items():
    #     print(f"Original: {orig:<80} New: {new}")

    # Iterate through the columns in the demographics DataFrame and Apply value mappings to relevant columns
    # for col in cleaned_df.columns:
    #     if cleaned_df[col].dtype == 'object':
    #         col_values = cleaned_df[col].fillna('').values
    #         if any(val in col_values for val in likert_mapping.keys()):
    #             cleaned_df[col] = map_values(cleaned_df[col], likert_mapping)
    #         elif any(val in col_values for val in frequency_mapping.keys()):
    #             cleaned_df[col] = map_values(cleaned_df[col], frequency_mapping)

    # Combine demographic data with device familiarity data
    final_df = pd.concat([cleaned_df], axis=1)

    return final_df

def generate_quality_report(df):
    return {
        'missing_values': df.isnull().sum(),
        'value_counts': {col: df[col].value_counts() for col in df.columns}
    }


if __name__ == "__main__":
    # xlsx = pd.ExcelFile('data_v0.xlsx')
    # print(xlsx.sheet_names)
    raw_df = pd.read_excel('data_v1.xlsx', sheet_name='Demographic')
    print("\n=== Raw Dataset Overview ===")
    print(f"Number of responses: {len(raw_df)}")
    print(f"Number of questions: {len(raw_df.columns)}")

    cleaned_data = raname_columns(raw_df)
    print("\nCleaning complete. Saving cleaned data...")

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    cleaned_data.to_excel('cleaned_survey_data'+ timestamp +'.xlsx', index=False)

    print("\n=== Cleaned Dataset Overview ===")
    print(f"Number of responses: {len(cleaned_data)}")
    print(f"Number of questions: {len(cleaned_data.columns)}")

    quality_report = generate_quality_report(cleaned_data)
    print("\nQuality report generated.")