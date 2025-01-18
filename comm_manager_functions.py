from typing import List, Optional, Callable
import project_rio_lib.web_functions as web_func
import api_parameters as param
import data_parsing
from functools import partial

class FunctionHandler:
    def __init__(
        self,
        func: Callable,
        inputs: List[param.APIParameter],
        parse_data: Optional[Callable] = None,
        constant_inputs: Optional[dict] = None
    ):
        """
        Represents a handler for a specific function.

        Parameters:
        - func (Callable): The function to execute.
        - inputs (List[APIParameter]): A list of input parameters required for the function.
        - parse_data (Optional[Callable]): A function to parse the output data.
        - constant_inputs (Optional[dict]): A dictionary of fixed inputs to supply to the function.
        """
        self.func = func
        self.inputs = inputs
        self.parse_data = parse_data
        self.constant_inputs = constant_inputs or {}


# Community Functions
community_functions = {
    'Create Community': FunctionHandler(
        func=web_func.create_community,
        inputs=[
            param.community_name_free,
            param.comm_type,
            param.private,
            param.global_link,
            param.comm_desc,
        ],
    ),
    'Add Community Members': FunctionHandler(
        func=web_func.community_invite,
        inputs=[
            param.community_name_closed,
            param.invite_list,
        ],
    ),
    'List Community Members': FunctionHandler(
        func=web_func.community_members,
        inputs=[
            param.community_name_closed,
        ],
        parse_data=data_parsing.community_members_to_dataframe,
    ),
    'List Community Tags': FunctionHandler(
        func=web_func.community_tags,
        inputs=[
            param.community_name_closed,
        ],
        parse_data=data_parsing.community_tags_to_dataframe,
    ),
    'Add or Remove Community Bans': FunctionHandler(
        func=web_func.community_manage,
        inputs=[
            param.community_name_closed,
            param.community_manage_bans,
        ],
    ),
    'Remove Community Members': FunctionHandler(
        func=web_func.community_manage,
        inputs=[
            param.community_name_closed,
            param.community_remove_users,
        ],
    ),
    'Manage Community User Keys': FunctionHandler(
        func=web_func.community_manage,
        inputs=[
            param.community_name_closed,
            param.manage_user_community_keys,
        ],
    ),
    'Manage Community Admins': FunctionHandler(
        func=web_func.community_manage,
        inputs=[
            param.community_name_closed,
            param.manage_community_admins,
        ],
    ),
    'List Community Sponsor': FunctionHandler(
        func=web_func.community_sponsor,
        inputs=[
            param.community_name_closed,
        ],
        constant_inputs={'action': 'get'},
        parse_data=data_parsing.print_community_sponsor,
    ),
    'Community-Wide User Keys': FunctionHandler(
        func=web_func.community_key,
        inputs=[
            param.community_name_closed,
            param.key_action,
        ],
        parse_data=data_parsing.community_user_keys_to_dataframe,
    ),
    'Update Community Type': FunctionHandler(
        func=web_func.community_update,
        inputs=[
            param.community_id,
            param.comm_type
        ],
    ),
    'Remove All Users from Community': FunctionHandler(
        func=web_func.community_manage,
        inputs=[
            param.community_name_closed,
            param.community_remove_all_users,
        ],
    )
}

# Tag Functions
tag_functions = {
    'Create Component Tag': FunctionHandler(
        func=partial(web_func.create_tag, tag_type='Component'),
        inputs=[
            param.community_name_closed,
            param.tag_name_free,
            param.tag_desc,
        ],
    ),
    'Create Gecko Code Tag': FunctionHandler(
        func=partial(web_func.create_tag, tag_type='Gecko Code'),
        inputs=[
            param.community_name_closed,
            param.tag_name_free,
            param.tag_desc,
            param.gecko_code,
            param.gecko_code_desc,
        ],
    ),
    'Update Tag Name': FunctionHandler(
        func=web_func.update_tag,
        inputs=[
            param.tag_id,
            param.tag_name_free,
        ],
    ),
    'Update Tag Description': FunctionHandler(
        func=web_func.update_tag,
        inputs=[
            param.tag_id,
            param.tag_desc,
        ],
    ),
    'Update Tag Type': FunctionHandler(
        func=web_func.update_tag,
        inputs=[
            param.tag_id,
            param.tag_type,
        ],
    ),
    'Update Tag Gecko Code Desc': FunctionHandler(
        func=web_func.update_tag,
        inputs=[
            param.tag_id,
            param.gecko_code_desc,
        ],
    ),
    'Update Tag Gecko Code': FunctionHandler(
        func=web_func.update_tag,
        inputs=[
            param.tag_id,
            param.gecko_code,
        ],
    ),
}

# Game Mode Functions
game_mode_functions = {
    'Create Game Mode': FunctionHandler(
        func=web_func.create_game_mode,
        inputs=[
            param.game_mode_name_free,
            param.game_mode_desc,
            param.game_mode_type,
            param.community_name_closed,
            param.start_date,
            param.end_date,
            param.add_tag_ids,
            param.game_mode_to_mirror_tags_from,
        ],
    ),
    'Update Game Mode Name': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.game_mode_name_free,
        ],
    ),
    'Update Game Mode Description': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.game_mode_desc,
        ],
    ),
    'Update Game Mode Type': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.game_mode_type,
        ],
    ),
    'Add Tags to Game Mode': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.add_tag_ids,
        ],
    ),
    'Remove Tags from Game Mode': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.remove_tag_ids,
        ],
    ),
    'Update Game Mode End Date': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.end_date,
        ],
    ),
    'Update Game Mode Start Date': FunctionHandler(
        func=web_func.update_game_mode,
        inputs=[
            param.tag_set_id,
            param.start_date,
        ],
    ),
    'List Game Mode Tags': FunctionHandler(
        func=web_func.list_game_mode_tags,
        inputs=[
            param.tag_set_id,
        ],
        parse_data=data_parsing.game_mode_tags_to_dataframe,
    ),
    'Show Game Mode Ladder': FunctionHandler(
        func=web_func.game_mode_ladder,
        inputs=[
            param.game_mode_name_closed,
        ],
        parse_data=data_parsing.ladder_to_dataframe,
    ),
    'Delete Game Mode': FunctionHandler(
        func=web_func.delete_game_mode,
        inputs=[
            param.game_mode_name_closed,
        ],
    )
}

# Rio Mod Functions
rio_mod_functions = {
    'Delete Game': FunctionHandler(
        func=web_func.delete_game,
        inputs=[
            param.game_id_dec,
        ],
    ),
    'Manual Game Submission From Statfile': FunctionHandler(
        func=web_func.manual_game_submit,
        inputs=[
            param.manual_submission_stat_file,
        ],
        parse_data=data_parsing.print_data,
    ),
    'Add User to User Group (Ban Users)': FunctionHandler(
        func=web_func.add_user_to_user_group,
        inputs=[
            param.username,
            param.user_group,
        ],
    ),
    'Remove User from User Group': FunctionHandler(
        func=web_func.remove_user_from_user_group,
        inputs=[
            param.username,
            param.user_group,
        ],
        parse_data=data_parsing.print_data,
    ),
    'Check Membership in User Group': FunctionHandler(
        func=web_func.check_for_member_in_user_group,
        inputs=[
            param.username,
            param.user_group,
        ],
        parse_data=data_parsing.print_data,
    ),
    'Check Members of User Group': FunctionHandler(
        func=web_func.check_members_of_user_groups,
        inputs=[
            param.user_group,
        ],
        parse_data=data_parsing.print_data,
    ),
}


data_endpoints = {
    'Games Endpoint': FunctionHandler(
        func=web_func.games_endpoint,
        inputs=[
            param.data_tag,
            param.data_exclude_tag,
            param.data_username,
            param.data_vs_username,
            param.data_exclude_username,
            param.data_captain,
            param.data_vs_captain,
            param.data_stadium,
            param.data_limit_games
        ],
        parse_data=data_parsing.games_endpoint_to_excel
    )
}