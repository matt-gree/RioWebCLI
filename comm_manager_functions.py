import web_functions as web_func
import data_parsing

community_endpoints = {
    'Create Community': {
        'func': web_func.create_community,
        'inputs': [
            'community_name_free',
            'comm_type',
            'private',
            'global_link',
            'comm_desc'
        ]
    },
    'Remove Members': {
        'unsupported': True
        # Endpoint is unecessary, use update_community
    },
    'Add Members': {
        'unsupported': True
        # Endpoint is unecessary, use invite_members
    },
    'Community Join': {
        'unsupported': True
        # Endpoint is not needed for a community admin
    },
    'Community Invite': {
        'func': web_func.community_invite,
        'inputs': [
            'community_name_closed',
            'invite_list'
        ]
    },
    'Community Members': {
        'func': web_func.community_members,
        'inputs': [
            'community_name_closed'
        ],
        'parse_data': data_parsing.community_members_to_dataframe
    },
    'Community Tags': {
        'func': web_func.community_tags,
        'inputs': [
            'community_name_closed'
        ],
        'parse_data': data_parsing.community_tags_to_dataframe
    },
    'Manage Community Bans': {
        'func': web_func.community_manage,
        'inputs': [
            'community_name_closed',
            'community_manage_bans',
        ]
    },
    'Remove Community Users': {
        'func': web_func.community_manage,
        'inputs': [
            'community_name_closed',
            'community_remove_users',
        ]
    },
    'Manage Community User Keys': {
        'func': web_func.community_manage,
        'inputs': [
            'community_name_closed',
            'manage_user_community_keys',
        ]
    },
    'Manage Community Admins': {
        'func': web_func.community_manage,
        'inputs': [
            'community_name_closed',
            'manage_community_admins',
        ]
    },
    'Get Community Sponsor': {
        'func': web_func.community_sponsor,
        'inputs': [
            'community_name_closed',
        ],
        'fixed_inputs': {
            'action': 'get'
        },
        'parse_data': data_parsing.print_community_sponsor
    },
    'Manage Community User Keys': {
        'func': web_func.community_key,
        'inputs': [
            'community_name_closed',
            'key_action'
        ],
        'parse_data': data_parsing.community_user_keys_to_dataframe
    }
}

supported_endpoints = []

# Iterate through the dictionary
for key, value in community_endpoints.items():
    if 'unsupported' not in value or value['unsupported'] is not True:
        supported_endpoints.append(key)
