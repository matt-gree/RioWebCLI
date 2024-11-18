from APIManager import include_rio_key, APIManager

def get_tag_info(api_manager: APIManager, tags_df, tag_name_closed):
    return tags_df[tags_df['name'] == tag_name_closed]
