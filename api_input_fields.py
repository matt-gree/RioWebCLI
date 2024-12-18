from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.completion import WordCompleter

from project_rio_lib.api_manager import APIManager
from project_rio_lib.web_caching import CompleterCache

manager = APIManager()
cache = CompleterCache(manager)


class OptionValidator(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, document):
        text = document.text.strip()

        if text not in self.options:
            raise ValidationError(message=f'Valid options are: {", ".join(self.options)}')
        
            
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
        'validator': OptionValidator(['y', 'n'])
    },
    'global_link': {
        'prompt': 'Would you like a global join link for your community? (y/n): ',
        'validator': OptionValidator(['y', 'n'])
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
}