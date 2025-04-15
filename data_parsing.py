import pandas as pd
import os
from datetime import datetime
import pytz

from pyRio.web_caching import CompleterCache
from pyRio.endpoint_handling import games_endpoints

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None) 

def community_members_to_dataframe(cache: CompleterCache, community_members_data):
    members_list = community_members_data['Members']
    df = pd.DataFrame(members_list)
    df2 = pd.DataFrame(list(cache.users_dictionary().items()), columns=['user_id', 'username'])
    df2['user_id'] = pd.to_numeric(df2['user_id'])
    df = df.merge(df2, on='user_id', how='left')
    df = df.set_index('username')

    est = pytz.timezone('US/Eastern')
    df['date_joined'] = pd.to_datetime(df['date_joined'], unit='s').dt.tz_localize('UTC').dt.tz_convert(est)
    df['date_joined'] = df['date_joined'].dt.strftime('%Y-%m-%d %H:%M:%S')

    return df

def community_tags_to_dataframe(cache, community_tags_data):
    return pd.DataFrame(community_tags_data['Tags']).set_index('id')

def print_community_sponsor(cache, community_sponsor):
    return f'Community Sponsor: {community_sponsor["sponsor"]}'

def user_keys_to_dataframe(cache, community_user_keys_data):
    df2 = pd.DataFrame(list(cache.users_dictionary().items()), columns=['user_id', 'username'])
    df2['user_id'] = pd.to_numeric(df2['user_id'])
    return pd.DataFrame(community_user_keys_data['members']).merge(df2, on='user_id', how='left').set_index('username')

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

def games_endpoint_to_excel(cache: CompleterCache, games_endpoint):
    df = games_endpoints(games_endpoint, cache)

    # Specify the folder path in the same directory
    folder_path = "endpoint_data"
    os.makedirs(folder_path, exist_ok=True)  # Create the folder if it doesn't exist

    # Generate a filename with the current date
    current_date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_name = f"games_data_{current_date_time}.xlsx"
    file_path = os.path.join(folder_path, file_name)

    # Save to Excel
    df.to_excel(file_path, index=False)
    return file_path

def game_mode_list_to_dataframe(cache: CompleterCache, games_list_data):
    df = pd.DataFrame(games_list_data['Tag Sets'])

    # Drop the 'tag_ids' and 'tags' columns
    df = df.drop(columns=['tag_ids', 'tags'])

    print(df)