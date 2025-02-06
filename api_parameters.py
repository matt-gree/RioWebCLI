from typing import List, Optional, Union, Callable
from functools import partial

from prompt_toolkit.validation import Validator
from prompt_validators import OptionValidator, GeckoCodeValidator, DateValidator, IntValidator
from pyRio.web_caching import CompleterCache
from pyRio.api_manager import APIManager

from input_conversion import InputConverters

manager = APIManager()
cache = CompleterCache(manager)

class APIParameter:
    def __init__(
        self,
        prompt: str,
        arg_name: str,
        completer: Optional[List[str]] = None,
        validator: Optional[Union[Callable, List[str]]] = None,
        input_processing: Optional[Callable] = None,
        loop: bool = False,
        subparameters: Optional[dict] = None,
        multiline: bool = False,
        optional: bool = False
    ):
        """
        Represents an individual API parameter used in prompts.
        Parameters:
        - prompt (str): The text that prompts the user for input.
        - arg_name (str): The name of the web_functions argument
        - completer (Optional[Union[List[str], Callable]]): A list of valid options to complete input or a callable that returns a list.
        - validator (Optional[Union[List[str], Callable]]): A list of valid options or a callable for input validation.
        - input_processing (Optional[Callable]): A function to process the input before or after validation.
        - subparameters (Optional[dict]): A dictionary of subparameters that can be nested under the current parameter.
        - loop (bool): Whether to continue prompting for input in a loop.
        - multiline (bool): Whether the input should support multiple lines (for example, for code input).
        """
        self.prompt = prompt
        self.arg_name = arg_name
        self.loop = loop
        self.optional = optional
        self.completer = self._validate_completer(completer)
        self.validator = self._process_validator(validator)
        self.input_processing = input_processing
        self.subparameters = subparameters or {}
        self.multiline = multiline

    def _validate_completer(self, completer: Optional[List[str]]) -> Optional[List[str]]:
        """
        Ensures that the completer is always a list of strings.
        """
        if completer is None:
            return None
        if not isinstance(completer, list):
            raise TypeError("Completer must be a list of strings.")
        if not all(isinstance(item, str) for item in completer):
            raise TypeError("All items in completer must be strings.")
        if self.loop or self.optional:
            completer += ['q']
        return completer

    def _process_validator(self, validator: Optional[Union[Callable, List[str]]]) -> Optional[Callable]:
        """
        Converts a list into an OptionValidator or validates if the input is callable.
        """
        if isinstance(validator, list):
            if self.loop or self.optional:
                validator += ['q']
            return OptionValidator(validator)
        if isinstance(validator, Validator):
            return validator
        if validator is not None:
            raise TypeError("Validator must be a callable or a list.")
        return None
    

community_name_free = APIParameter(
    prompt = 'Enter the name for your community: ',
    arg_name = 'community_name_free'
)

community_name_closed = APIParameter(
    prompt='Enter the name of the community: ',
    arg_name = 'community_name_closed',
    completer=cache.communities(),
    validator=cache.communities()
)

comm_type = APIParameter(
    prompt='Enter the type of community (Official, Unofficial): ',
    arg_name = 'comm_type',
    completer=['Official', 'Unofficial'],
    validator=['Official', 'Unofficial']
)

private = APIParameter(
    prompt='Would you like the community to be private? (y/n):  ',
    arg_name = 'private',
    validator=['y', 'n'],
    input_processing=InputConverters.yes_to_1_converter
)

global_link = APIParameter(
    prompt='Would you like a global join link for your community? (y/n): ',
    arg_name = 'global_link',
    validator=['y', 'n'],
    input_processing=InputConverters.yes_to_1_converter
)

comm_desc = APIParameter(
    prompt='Enter a description for your community: ',
    arg_name = 'comm_desc'
)

user_list = APIParameter(
    prompt='Enter a list of users to add: ',
    arg_name = 'user_list'
)

action = APIParameter(
    prompt='Enter the action you would like to take (Add, Get, Remove): ',
    arg_name = 'action',
    completer=['Add', 'Get', 'Remove'],
    validator=['Add', 'Get', 'Remove']
)

invite_list = APIParameter(
    prompt='How would you like to enter usernames (input or txt): ',
    arg_name = 'invite_list',
    completer=['input', 'txt'],
    validator=['input', 'txt'],
    subparameters={
        'input': APIParameter(
            arg_name = None,
            prompt='Enter the Rio username to add to the community (q to finish): ',
            completer=cache.users(),
            validator=cache.users(),
            loop=True
        ),
        'txt': APIParameter(
            prompt='Enter the path to the comma separated username .txt file: ',
            arg_name = None,
            input_processing=InputConverters.create_list_from_txt
        )
    }
)

community_manage_bans = APIParameter(
    prompt='Would you like to ban or unban members?: ',
    arg_name = 'user_list',
    completer=['ban', 'unban'],
    validator=['ban', 'unban'],
    subparameters={
        'ban': APIParameter(
            prompt='Enter the Rio username to ban (q to finish): ',
            arg_name=None,
            completer=cache.users(),
            validator=cache.users(),
            input_processing=partial(InputConverters.community_manager_converter, ban=True),
            loop=True
        ),
        'unban': APIParameter(
            prompt='Enter the Rio username to unban (q to finish): ',
            arg_name=None,
            completer=cache.users(),
            validator=cache.users(),
            input_processing=partial(InputConverters.community_manager_converter, ban=False),
            loop=True
        )
    }
)

community_remove_users = APIParameter(
    loop=True,
    arg_name = 'user_list',
    prompt='Enter the Rio username to remove (q to finish): ',
    completer=cache.users(),
    validator=cache.users(),
    input_processing=partial(InputConverters.community_manager_converter, remove=True),
)

community_remove_all_users = APIParameter(
    arg_name = 'user_list',
    prompt='Please confirm you would like to remove all users from this community: ',
    validator=['y', 'n'],
    input_processing=InputConverters.remove_all_users_list
)

manage_user_community_keys = APIParameter(
    prompt='Would you like to create or delete member keys?: ',
    arg_name = 'manage_user_community_keys',
    completer=['create', 'delete'],
    validator=['create', 'delete'],
    subparameters={
        'create': APIParameter(
            prompt='Enter the Rio username to create a key for (q to finish): ',
            arg_name=None,
            completer=cache.users(),
            validator=cache.users(),
            input_processing=partial(InputConverters.community_manager_converter, key=True),
            loop=True
        ),
        'delete': APIParameter(
            prompt='Enter the Rio username to delete a key for (q to finish): ',
            arg_name=None,
            completer=cache.users(),
            validator=cache.users(),
            input_processing=partial(InputConverters.community_manager_converter, key=False),
            loop=True
        )
    }
)

manage_community_admins = APIParameter(
    prompt='Would you like to add or remove community admins?: ',
    arg_name = 'user_list',
    completer=['add', 'remove'],
    validator=['add', 'remove'],
    subparameters={
        'add': APIParameter(
            prompt='Enter the Rio username to make an admin (q to finish): ',
            arg_name='None',
            completer=cache.users(),
            validator=cache.users(),
            input_processing=partial(InputConverters.community_manager_converter, admin=True),
            loop=True
        ),
        'remove': APIParameter(
            prompt='Enter the Rio username to remove as admin (q to finish): ',
            arg_name='None',
            completer=cache.users(),
            validator=cache.users(),
            input_processing=partial(InputConverters.community_manager_converter, admin=False),
            loop=True,
        )
    }
)

key_action = APIParameter(
    prompt='What action would you like to take (generate, revoke, generate_all): ',
    arg_name = 'key_action',
    completer=['generate', 'revoke', 'generate_all'],
    validator=['generate', 'revoke', 'generate_all']
)

tag_name_free = APIParameter(
    prompt='Enter the name for your tag: ',
    arg_name = 'tag_name_free'
)

tag_name_closed = APIParameter(
    prompt='Enter the tag name: ',
    arg_name='tag_name_closed',
    completer=list(cache.tags_dictionary().keys()),
    validator=list(cache.tags_dictionary().keys())
)

tag_desc = APIParameter(
    prompt='Enter a description for your new tag: ',
    arg_name = 'tag_desc'
)

gecko_code = APIParameter(
    prompt='Enter the gecko code (option-enter to submit on Mac, ESC-enter on Windows):\n',
    arg_name = 'gecko_code',
    validator=GeckoCodeValidator(),
    multiline=True
)

gecko_code_desc = APIParameter(
    prompt='Enter a description for your new gecko code: ',
    arg_name = 'gecko_code_desc',
)

game_mode_name_free = APIParameter(
    prompt='Enter the name for your game mode: ',
    arg_name = 'game_mode_name_free'
)

game_mode_desc = APIParameter(
    prompt='Enter a description for your game mode: ',
    arg_name = 'game_mode_desc',
)

game_mode_type = APIParameter(
    prompt='Enter the game mode type (Season, League, Tournament): ',
    completer=['Season', 'League', 'Tournament'],
    validator=['Season', 'League', 'Tournament'],
    arg_name = 'game_mode_type',
)

start_date = APIParameter(
    prompt='Enter the start date (MM-DD-YYYY): ',
    arg_name = 'start_date',
    validator=DateValidator(),
    input_processing=InputConverters.date_processing
)

end_date = APIParameter(
    prompt='Enter the end date (EOD) (MM-DD-YYYY): ',
    arg_name = 'end_date',
    validator=DateValidator(),
    input_processing=partial(InputConverters.date_processing, eod=True)
)

add_tag_ids = APIParameter(
    prompt='Enter the tags to add to this community (optional): ',
    arg_name = 'add_tag_ids',
    completer=list(cache.tags_dictionary().keys()),
    validator=list(cache.tags_dictionary().keys()),
    input_processing=partial(InputConverters.dictionary_conversion, dictionary=cache.tags_dictionary()),
    loop=True
)

remove_tag_ids = APIParameter(
    prompt='Enter the tags to remove from this community (optional): ',
    arg_name = 'remove_tag_ids',
    completer=list(cache.tags_dictionary().keys()),
    validator=list(cache.tags_dictionary().keys()),
    input_processing=partial(InputConverters.dictionary_conversion, dictionary=cache.tags_dictionary()),
    loop=True
)

game_mode_to_mirror_tags_from = APIParameter(
    prompt='Enter the game mode to mirror tags from in this new game mode (q to skip): ',
    arg_name = 'game_mode_to_mirror_tags_from',
    completer=list(cache.game_mode_dictionary().keys()),
    validator=list(cache.game_mode_dictionary().keys()),
    input_processing=partial(InputConverters.dictionary_conversion, dictionary=cache.game_mode_dictionary()),
    optional=True
)

tag_set_id = APIParameter(
    prompt='Enter the name of the game mode: ',
    arg_name = 'tag_set_id',
    completer=list(cache.game_mode_dictionary().keys()),
    validator=list(cache.game_mode_dictionary().keys()),
    input_processing=partial(InputConverters.dictionary_conversion, dictionary=cache.game_mode_dictionary())
)

community_id = APIParameter(
    prompt='Enter the community id: ',
    arg_name='community_id',
    input_processing=int
)

game_mode_name_closed = APIParameter(
    prompt='Enter the name of the game mode: ',
    arg_name = 'game_mode_name_closed',
    completer=list(cache.game_mode_dictionary().keys()),
    validator=list(cache.game_mode_dictionary().keys())
)

tag_id = APIParameter(
    prompt='Enter the name of the tag: ',
    arg_name = 'tag_id',
    completer=list(cache.tags_dictionary().keys()),
    validator=list(cache.tags_dictionary().keys()),
    input_processing=partial(InputConverters.dictionary_conversion, dictionary=cache.tags_dictionary())
)

tag_type = APIParameter(
    prompt='Enter the tag type: ',
    arg_name = 'tag_type',
    completer=['Component', 'Gecko Code'],
    validator=['Component', 'Gecko Code']
)

game_id_dec = APIParameter(
    prompt='Enter the GameID in decimal form (They are Hex in Rio Stat Files, Decimal on Rio Web): ',
    arg_name = 'game_id_dec'
)

manual_submission_stat_file = APIParameter(
    prompt='Enter the path to the stat file of the game to submit: ',
    arg_name = '_dict',
    input_processing=partial(InputConverters.stat_file_converter, cache_instance=cache)
)

username = APIParameter(
    prompt = "Enter the player's username: ",
    arg_name='username',
    completer = cache.users(),
    validator = cache.users()
)

user_group = APIParameter(
    prompt= 'Enter the name of the user group: ',
    arg_name='group_name',
    completer=['Banned'],
    validator=['Banned']
)

data_tag = APIParameter(
    prompt = 'Enter the tag name(s) to filter by: ',
    arg_name='tag',
    completer=list(cache.game_mode_dictionary().keys()),
    validator=list(cache.game_mode_dictionary().keys()),
    loop=True,
    optional=True
)

data_exclude_tag = APIParameter(
    prompt = 'Enter the tag name(s) to exclude: ',
    arg_name='exclude_tag',
    completer=list(cache.game_mode_dictionary().keys()),
    validator=list(cache.game_mode_dictionary().keys()),
    loop=True,
    optional=True
)

data_username = APIParameter(
    prompt='Enter the username(s) to filter by: ',
    arg_name='username',
    completer=cache.users(),
    validator=cache.users(),
    loop=True,
    optional=True
)

data_vs_username = APIParameter(
    prompt='Enter the usernames(s) to filter opponents by: ',
    arg_name='vs_username',
    completer=cache.users(),
    validator=cache.users(),
    loop=True,
    optional=True
)

data_exclude_username = APIParameter(
    prompt='Enter the usernames(s) to exclude: ',
    arg_name='exclude_username',
    completer=cache.users(),
    validator=cache.users(),
    loop=True,
    optional=True
)

# Add completers
data_captain = APIParameter(
    prompt='Enter the captain(s) to filter by: ',
    arg_name='captain',
    loop=True,
    optional=True
)

data_vs_captain = APIParameter(
    prompt='Enter the captain(s) to filter opponents by: ',
    arg_name='vs_captain',
    loop=True,
    optional=True
)

data_stadium = APIParameter(
    prompt='Enter the stadium(s) to filter by: ',
    arg_name='stadium',
    loop=True,
    optional=True
)

data_limit_games = APIParameter(
    prompt='Enter the number of games to look at: ',
    arg_name='limit_games',
    optional=True
)

game_mode_limit = APIParameter(
    prompt='Enter the new active tag set limit: ',
    arg_name='active_tag_set_limit',
    validator=IntValidator(),
    input_processing=int
)

