import project_rio_lib.web_functions as web_func
import api_parameters as param
import data_parsing
from functools import partial

community_functions = {
    'Create Community': {
        'func': web_func.create_community,
        'inputs': [
            param.community_name_free,
            param.comm_type,
            param.private,
            param.global_link,
            param.comm_desc
        ]
    },
    'Remove Members': {
        'unsupported': True
        # Endpoint is unnecessary, use update_community
    },
    'Add Members': {
        'unsupported': True
        # Endpoint is unnecessary, use invite_members
    },
    'Community Join': {
        'unsupported': True
        # Endpoint is not needed for a community admin
    },
    'Community Invite': {
        'func': web_func.community_invite,
        'inputs': [
            param.community_name_closed,
            param.invite_list
        ]
    },
    'Community Members': {
        'func': web_func.community_members,
        'inputs': [
            param.community_name_closed
        ],
        'parse_data': data_parsing.community_members_to_dataframe
    },
    'Community Tags': {
        'func': web_func.community_tags,
        'inputs': [
            param.community_name_closed
        ],
        'parse_data': data_parsing.community_tags_to_dataframe
    },
    'Manage Community Bans': {
        'func': web_func.community_manage,
        'inputs': [
            param.community_name_closed,
            param.community_manage_bans
        ]
    },
    'Remove Community Users': {
        'func': web_func.community_manage,
        'inputs': [
            param.community_name_closed,
            param.community_remove_users
        ]
    },
    'Manage Community User Keys': {
        'func': web_func.community_manage,
        'inputs': [
            param.community_name_closed,
            param.manage_user_community_keys
        ]
    },
    'Manage Community Admins': {
        'func': web_func.community_manage,
        'inputs': [
            param.community_name_closed,
            param.manage_community_admins
        ]
    },
    'Get Community Sponsor': {
        'func': web_func.community_sponsor,
        'inputs': [
            param.community_name_closed
        ],
        'fixed_inputs': {
            'action': 'get'
        },
        'parse_data': data_parsing.print_community_sponsor
    },
    'Community-Wide User Keys': {
        'func': web_func.community_key,
        'inputs': [
            param.community_name_closed,
            param.key_action
        ],
        'parse_data': data_parsing.community_user_keys_to_dataframe
    }
}

tag_functions = {
    'Create Component Tag': {
        'func': partial(web_func.create_tag, tag_type='Component'),
        'inputs': [
            param.community_name_closed,
            param.tag_name_free,
            param.tag_desc
        ]
    },
    'Create Gecko Code Tag': {
        'func': partial(web_func.create_tag, tag_type='Gecko Code'),
        'inputs': [
            param.community_name_closed,
            param.tag_name_free,
            param.tag_desc,
            param.gecko_code,
            param.gecko_code_desc
        ]
    },
    'Update Tag Name': {
        'func': web_func.update_tag,
        'inputs': [
            param.tag_id,
            param.tag_name_free
        ]
    },
    'Update Tag Description': {
        'func': web_func.update_tag,
        'inputs': [
            param.tag_id,
            param.tag_desc
        ]
    },
    'Update Tag Type': {
        'func': web_func.update_tag,
        'inputs': [
            param.tag_id,
            param.tag_type
        ]
    },
    'Update Tag Gecko Code Desc': {
        'func': web_func.update_tag,
        'inputs': [
            param.tag_id,
            param.gecko_code_desc
        ]
    },
    'Update Tag Gecko Code': {
        'func': web_func.update_tag,
        'inputs': [
            param.tag_id,
            param.gecko_code
        ]
    },
}

game_mode_functions = {
    'Create Game Mode': {
        'func': web_func.create_game_mode,
        'inputs': [
            param.game_mode_name_free,
            param.game_mode_desc,
            param.game_mode_type,
            param.community_name_closed,
            param.start_date,
            param.end_date,
            param.add_tag_ids,
            param.game_mode_to_mirror_tags_from
        ]
    },
    'Update Game Mode Name': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.game_mode_name_free
        ]
    },
    'Update Game Mode Description': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.game_mode_desc
        ]
    },
    'Update Game Mode Type': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.game_mode_type
        ]
    },
    'Add Tags to Game Mode': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.add_tag_ids
        ]
    },
    'Remove Tags from Game Mode': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.remove_tag_ids
        ]
    },
    'Update Game Mode End Date': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.end_date
        ]
    },
    'Update Game Mode Start Date': {
        'func': web_func.update_game_mode,
        'inputs': [
            param.tag_set_id,
            param.start_date
        ]
    },
    'List Game Mode Tags': {
        'func': web_func.list_game_mode_tags,
        'inputs': [
            param.tag_set_id
        ],
        'parse_data': data_parsing.game_mode_tags_to_dataframe
    },
    'Show Game Mode Ladder': {
        'func': web_func.game_mode_ladder,
        'inputs': [
            param.game_mode_name_closed
        ],
        'parse_data': data_parsing.ladder_to_dataframe
    },
    'Delete Game Mode': {
        'func': web_func.delete_game_mode,
        'inputs': [
            param.game_mode_name_closed
        ]
    },
}

rio_mod_functions = {
    'Delete Game': {
        'func': web_func.delete_game,
        'inputs': [
            param.game_id_dec
        ]
    },
    'Manual Game Submission From Statfile': {
        'func': web_func.manual_game_submit,
        'inputs': [
            param.manual_submission_stat_file
        ],
        'parse_data': data_parsing.print_data
    },
    'Add User to User Group (Ban Users)': {
        'func': web_func.add_user_to_user_group,
        'inputs' : [
            param.username,
            param.user_group
        ]
    },
    'Remove User from User Group': {
        'func': web_func.remove_user_from_user_group,
        'inputs': [
            param.username,
            param.user_group
        ],
        'parse_data': data_parsing.print_data
    },
    'Check Membership in User Group': {
        'func': web_func.check_for_member_in_user_group,
        'inputs' : [
            param.username,
            param.user_group
        ],
        'parse_data': data_parsing.print_data
    },
    'Check Members of User Group': {
        'func': web_func.check_members_of_user_groups,
        'inputs': [
            param.user_group
        ],
        'parse_data': data_parsing.print_data
    }
}

