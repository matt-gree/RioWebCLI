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
    return f'Community Sponsor: {community_sponsor['sponsor']}'

def community_user_keys_to_dataframe(cache, community_user_keys_data):
    return pd.DataFrame(community_user_keys_data)