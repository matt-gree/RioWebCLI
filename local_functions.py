from pyRio.api_manager import APIManager

def get_tag_info(api_manager: APIManager, tags_df, tag_name_closed):
    return tags_df[tags_df['name'] == tag_name_closed]

#def get_game_mode_info