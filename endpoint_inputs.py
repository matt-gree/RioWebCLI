import web_functions as web_func

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
    }
}

supported_endpoints = []

# Iterate through the dictionary
for key, value in community_endpoints.items():
    if 'unsupported' not in value or value['unsupported'] is not True:
        supported_endpoints.append(key)
