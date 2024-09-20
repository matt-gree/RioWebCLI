from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter
import string

from datetime import datetime
import pytz

from functools import partial

from APIManager import APIManager
from CompleterCache import CompleterCache

from comm_manager_functions import community_endpoints, supported_endpoints


manager = APIManager()
cache = CompleterCache(manager)


class OptionValidator(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, document):
        text = document.text.strip()

        if text not in self.options:
            raise ValidationError(message=f'Valid options are: {", ".join(self.options)}')
        

class GeckoCodeValidator(Validator):
    def validate(self, document):
        in_str = document.text
        index = 0
        
        for char in in_str:
            if index == 17:
                if char != '\n':
                    raise ValidationError(
                        message="Invalid Gecko Code: Each line of 17 characters must be separated by a newline",
                        cursor_position=index
                    )
                index = 0
            elif index == 8:
                if char != ' ':
                    raise ValidationError(
                        message="Invalid Gecko Code: There must be a space between memory address and value",
                        cursor_position=index
                    )
                index += 1
            elif index <= 16:
                if char not in string.hexdigits:
                    raise ValidationError(
                        message="Invalid Gecko Code: Gecko code must be made of hex values only",
                        cursor_position=index
                    )
                index += 1
        
        # After the loop, check if we ended in the middle of a line
        if index != 0: 
            raise ValidationError(
                message="Invalid Gecko Code: Gecko code must end at the end of a line",
                cursor_position=len(in_str)
            )
        
class DateValidator(Validator):
    def validate(self, document):
        text = document.text

        if text == '':
            return

        try:
            datetime.strptime(text, '%m-%d-%Y')
        except ValueError as e:
            raise ValidationError(message='Invalid date format. Use MM-DD-YYYY.') from e

def create_list_from_txt(txt_path):
    try:
        with open(txt_path, 'r') as file:
            content = file.read().strip()
            username_list = content.split(',')
            username_list = [username.strip() for username in username_list]  # Remove any extra whitespace
        return username_list
    except FileNotFoundError:
        print(f"File not found: {txt_path}")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def yes_to_1_converter(y_or_n):
    conversion_dict = {
        'y': 1,
        'n': 0
    }

    return conversion_dict[y_or_n]

def yes_no_to_t_f(y_or_n):
    conversion_dict = {
        'y': True,
        'n': False
    }

    return conversion_dict[y_or_n]

def dictionary_conversion(key, dictionary):
    return dictionary[key]

def community_manager_converter(user, ban=None, remove=None, key=None, admin=None):
    user_action_dict = {}
    action_values  = [True, False]
    user_action_dict['username'] = user

    if ban in action_values:
        user_action_dict['ban'] = ban

    if remove in action_values:
        user_action_dict['remove'] = remove

    if key in action_values:
        user_action_dict['key'] = key
    
    if admin in action_values:
        user_action_dict['admin'] = admin

    return user_action_dict

def date_processing(date_string, eod=False):
    # Define the EST timezone
    est = pytz.timezone('America/New_York')
    
    # Parse the date string and set time to 11:59:59 PM
    naive_datetime = datetime.strptime(date_string, '%m-%d-%Y')
    est_datetime = est.localize(naive_datetime)
    if eod:
        est_datetime = est.localize(naive_datetime.replace(hour=23, minute=59, second=59))
    
    # Return the timestamp
    return int(est_datetime.timestamp())

api_inputs = {
    'community_name_free': {
        'prompt': 'Enter the name for your community: '
    },
    'community_name_closed': {
        'prompt': 'Enter the name of the community: ',
        'completer': cache.communities(),
        'validator': OptionValidator(cache.communities())
    },
    'comm_type': {
        'prompt': 'Enter the type of community (Official, Unofficial): ',
        'completer': ['Official', 'Unofficial'],
        'validator': OptionValidator(['Official', 'Unofficial'])
    },
    'private': {
        'prompt': 'Would you like the community to be private? (y/n):  ',
        'validator': OptionValidator(['y', 'n']),
        'input_processing': yes_to_1_converter
    },
    'global_link': {
        'prompt': 'Would you like a global join link for your community? (y/n): ',
        'validator': OptionValidator(['y', 'n']),
        'input_processing': yes_to_1_converter
    },
    'comm_desc': {
        'prompt': 'Enter a description for your community: '
    },
    'user_list': {
        'prompt': 'Enter a list of users to add: '
    },
    'action': {
        'prompt': 'Enter the action you would like to take (Add, Get, Remove): ',
        'completer': ['Add', 'Get', 'Remove'],
        'validator': OptionValidator(['Add', 'Get', 'Remove'])
    },
    'invite_list': {
        'prompt': 'How would you like to enter usernames (input or txt): ',
        'completer': ['input', 'txt'],
        'validator': OptionValidator(['input', 'txt']),
        'subprompt': True,
        'input': {
            'loop': True,
            'prompt': 'Enter the Rio username to add to the community (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q'])
        },
        'txt': {
            'prompt': 'Enter the path to the comma seperated username .txt file: ',
            'input_processing': create_list_from_txt
        }
    },
    'community_manage_bans': {
        'prompt': 'Would you like to ban or unban members?: ',
        'completer': ['ban', 'unban'],
        'validator': OptionValidator(['ban', 'unban']),
        'subprompt': True,
        'ban': {
            'loop': True,
            'prompt': 'Enter the Rio username to ban (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q']),
            'input_processing': partial(community_manager_converter, ban=True)
        },
        'unban': {
            'loop': True,
            'prompt': 'Enter the Rio username to unban (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q']),
            'input_processing': partial(community_manager_converter, ban=False)
        },
        'rename_arg': 'user_list'
    },
    'community_remove_users': {
        'loop': True,
        'prompt': 'Enter the Rio username to remove (q to finish): ',
        'completer': cache.users() +['q'],
        'validator': OptionValidator(cache.users() +['q']),
        'input_processing': partial(community_manager_converter, remove=True),
        'rename_arg': 'user_list'
    },
    'manage_user_community_keys': {
        'prompt': 'Would you like to create or delete member keys?: ',
        'completer': ['create', 'delete'],
        'validator': OptionValidator(['create', 'delete']),
        'subprompt': True,
        'create': {
            'loop': True,
            'prompt': 'Enter the Rio username to create a key for (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q']),
            'input_processing': partial(community_manager_converter, key=True)
        },
        'delete': {
            'loop': True,
            'prompt': 'Enter the Rio username to delete a key for (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q']),
            'input_processing': partial(community_manager_converter, key=False)
        },
        'rename_arg': 'user_list'
    },
    'manage_community_admins': {
        'prompt': 'Would you like to add or remove community admins?: ',
        'completer': ['add', 'remove'],
        'validator': OptionValidator(['add', 'remove']),
        'subprompt': True,
        'add': {
            'loop': True,
            'prompt': 'Enter the Rio username to make an admin (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q']),
            'input_processing': partial(community_manager_converter, admin=True)
        },
        'remove': {
            'loop': True,
            'prompt': 'Enter the Rio username to remove as admin (q to finish): ',
            'completer': cache.users() +['q'],
            'validator': OptionValidator(cache.users() +['q']),
            'input_processing': partial(community_manager_converter, admin=False)
        },
        'rename_arg': 'user_list'
    },
    'key_action': {
        'prompt': 'What action would you like to take (generate, revoke, generate_all): ',
        'completer': ['generate', 'revoke', 'generate_all'],
        'validator': OptionValidator(['generate', 'revoke', 'generate_all']),
    },
    'tag_name_free': {
        'prompt': 'Enter the name for your tag: '
    },
    'tag_desc': {
        'prompt': 'Enter a description for your new tag: '
    },
    'gecko_code': {
        'prompt': 'Enter the gecko code: ',
        'validator': GeckoCodeValidator(),
    },
    'gecko_code_desc':{
        'prompt': 'Enter a description for your new tag: '
    },
    'game_mode_name_free': {
        'prompt': 'Enter the name for your game mode: '
    },
    'game_mode_desc': {
        'prompt': 'Enter a description for your community: '
    },
    'game_mode_type': {
        'prompt': 'Enter the game mode type (Season, League, Tournament): ',
        'completer': ['Season', 'League', 'Tournament'],
        'validator': OptionValidator(['Season', 'League', 'Tournament'])
    },
    'start_date': {
        'prompt': 'Enter the start date (MM-DD-YYYY): ',
        'validator': DateValidator(),
        'input_processing': date_processing
    },
    'end_date': {
        'prompt': 'Enter the end date (EOD) (MM-DD-YYYY): ',
        'validator': DateValidator(),
        'input_processing': partial(date_processing, eod=True)
    },
    'add_tag_ids': {
        'loop': True,
        'prompt': 'Enter the tags to add to this community (optional): ',
        'completer': list(cache.tags_dictionary().keys()) + ['q'],
        'validator': OptionValidator(list(cache.tags_dictionary().keys()) + ['q']),
        'input_processing': partial(dictionary_conversion, dictionary=cache.tags_dictionary())
    },
    'remove_tag_ids': {
        'loop': True,
        'prompt': 'Enter the tags to add to remove from this community (optional): ',
        'completer': list(cache.tags_dictionary().keys()) + ['q'],
        'validator': OptionValidator(list(cache.tags_dictionary().keys()) + ['q']),
        'input_processing': partial(dictionary_conversion, dictionary=cache.tags_dictionary())
    },
    'game_mode_to_mirror_tags_from': {
        'prompt': 'Enter the game mode to mirror tags from in this new game mode (enter to skip): ',
        'completer': list(cache.game_mode_dictionary().keys()) + [''],
        'validator': OptionValidator(list(cache.game_mode_dictionary().keys()) + ['']),
        'input_processing': partial(dictionary_conversion, dictionary=cache.game_mode_dictionary())
    },
    'tag_set_id': {
        'prompt': 'Enter the name of the game mode: ',
        'completer': list(cache.game_mode_dictionary().keys()) + [''],
        'validator': OptionValidator(list(cache.game_mode_dictionary().keys()) + ['']),
        'input_processing': partial(dictionary_conversion, dictionary=cache.game_mode_dictionary())
    }

}


community_endpoints_prompt = {
    'prompt': 'What would you like to do: ',
    'completer': supported_endpoints,
    'validator': OptionValidator(supported_endpoints)
}

def get_prompt_input(prompt_dictionary, break_key='q'):
    completer = WordCompleter(prompt_dictionary.get('completer', []), ignore_case=True)
    input = prompt(prompt_dictionary['prompt'], completer=completer, validator=prompt_dictionary.get('validator'), bottom_toolbar=prompt_dictionary.get('toolbar'))
    if input == break_key:
        return break_key
    if prompt_dictionary.get('input_processing'):
        input = prompt_dictionary['input_processing'](input)

    return input

def run_prompt(prompt_dictionary):
    if prompt_dictionary.get('loop'):
        input = []
        while True:
            add_item = get_prompt_input(prompt_dictionary,)
            if add_item == 'q':
                break
            input.append(add_item)
        return input

    return get_prompt_input(prompt_dictionary)        

function_args = {}

user_endpoint_choice = run_prompt(community_endpoints_prompt)
for key in community_endpoints[user_endpoint_choice]['inputs']:
    build_prompt = api_inputs[key]
    input = run_prompt(build_prompt)

    if build_prompt.get('subprompt'):
        input = run_prompt(build_prompt[input])

    arg_name = key
    if build_prompt.get('rename_arg'):
        arg_name = build_prompt['rename_arg']

    function_args[arg_name] = input
    
function_args['api_manager'] = manager
if community_endpoints[user_endpoint_choice].get('fixed_inputs'):
    function_args = function_args | community_endpoints[user_endpoint_choice]['fixed_inputs']

output = community_endpoints[user_endpoint_choice]['func'](**function_args)
if community_endpoints[user_endpoint_choice].get('parse_data'):
    print(community_endpoints[user_endpoint_choice]['parse_data'](cache, output))
