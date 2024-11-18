import pandas as pd

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None) 

def community_members_to_dataframe(cache, community_members_data):
    members_list = community_members_data['Members']
    df = pd.DataFrame(members_list)
    df2 = pd.DataFrame(list(cache.users_dict.items()), columns=['user_id', 'username'])
    df2['user_id'] = pd.to_numeric(df2['user_id'])
    df = df.merge(df2, on='user_id', how='left')
    df = df.set_index('username')

    return df

def community_tags_to_dataframe(cache, community_tags_data):
    return pd.DataFrame(community_tags_data['Tags']).set_index('id')

def print_community_sponsor(cache, community_sponsor):
    return f'Community Sponsor: {community_sponsor["sponsor"]}'

def community_user_keys_to_dataframe(cache, community_user_keys_data):
    return pd.DataFrame(community_user_keys_data)

def game_mode_tags_to_dataframe(cache, game_mode_tags):
    game_mode_info = game_mode_tags['Tag Set'][0]
    game_mode_tags_df = pd.DataFrame(game_mode_info['tags']).set_index('id')
    game_mode_info.pop('tags')
    game_mode_info_df = pd.DataFrame([game_mode_info]).set_index('comm_id')
    
    return game_mode_info_df, game_mode_tags_df

def ladder_to_dataframe(cache, ladder):
    return pd.DataFrame.from_dict(ladder, orient='index')

def tags_list_to_dataframe(cache, tags):
    return pd.DataFrame(tags['Tags']).set_index('id')

def print_df_columns_by_row(cache, df):
    output = []
    for index, row in df.iterrows():
        output.append(f"ID: {index}:")
        for column, value in row.items():
            if isinstance(value, str) and '\n' in value:
                # Add value starting on a new line if it contains a newline
                output.append(f"{column}:\n{value[:-1]}")
            else:
                output.append(f"{column}: {value}")
    return "\n".join(output)


def print_data(cache, data):
    return data