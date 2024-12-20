from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from project_rio_lib.api_manager import APIManager
from project_rio_lib.web_caching import CompleterCache
from comm_manager_functions import community_functions, tag_functions, game_mode_functions, rio_mod_functions
from prompt_validators import OptionValidator
from api_parameters import APIParameter

manager = APIManager()
cache = CompleterCache(manager)

formatted_text = '''
    ______ _         _    _      _       _____                            ___  ___                                  
    | ___ (_)       | |  | |    | |     /  __ \\                           |  \\/  |                                  
    | |_/ /_  ___   | |  | | ___| |__   | /  \\/ ___  _ __ ___  _ __ ___   | .  . | __ _ _ __   __ _  __ _  ___ _ __ 
    |    /| |/ _ \\  | |/\\| |/ _ \\ '_ \\  | |    / _ \\| '_ ` _ \\| '_ ` _ \\  | |\\/| |/ _` | '_ \\ / _` |/ _` |/ _ \\ '__|
    | |\\ \\| | (_) | \\  /\\  /  __/ |_) | | \\__/\\ (_) | | | | | | | | || |  | |  | | (_| | | | | (_| | (_| |  __/ |   
    \\_| \\_|_|\\___/   \\/  \\/ \\___|_.__/   \\____/\\___/|_| |_| |_|_| |_||_|  \\_|  |_|\\__,_|_| |_|\\__,_|\\__, |\\___|_|   
                                                                                                    __/  |          
                                                                                                    |___/           
    '''

print(formatted_text)

function_groups = {
    'Manage Communities': community_functions,
    'Manage Game Modes': game_mode_functions,
    'Manage Tags': tag_functions,
    'Rio Mod Functions': rio_mod_functions
}
print(f'\nMenu Options: ')
for key in function_groups.keys():
    print(f'    {key}')
print()

selected_function_group = prompt('What would you like to do: ',
                                 completer=WordCompleter(list(function_groups.keys()), ignore_case=True),
                                 validator=OptionValidator(list(function_groups.keys())))

print()
print(f'{selected_function_group}: ')
selected_function_group = function_groups[selected_function_group]

supported_functions = []
# Iterate through the dictionary
for key, value in selected_function_group.items():
    if 'unsupported' not in value or value['unsupported'] is not True:
        supported_functions.append(key)


for item in supported_functions:
    print(f'    {item}')
print()

selected_function = prompt('What would you like to do: ',
                                 completer=WordCompleter(supported_functions, ignore_case=True),
                                 validator=OptionValidator(supported_functions))


def prompt_for_input(parameter: APIParameter, break_key='q'):
    """
    Displays a prompt for user input based on the given APIParameter.
    Processes the input if a processing function is provided.
    
    Args:
        parameter (APIParameter): The parameter containing the prompt configuration.
        break_key (str): Key to exit the input loop (default is 'q').
    
    Returns:
        str: User input after optional processing, or the break_key if entered.
    """
    completer = WordCompleter(parameter.completer, ignore_case=True)
    user_input = prompt(parameter.prompt, completer=completer, validator=parameter.validator, multiline=parameter.multiline)
    if user_input == break_key:
        return break_key
    if parameter.input_processing:
        user_input = parameter.input_processing(user_input)
    return user_input


def has_subparameters(user_input, parameter):
    """
    Checks if the given input corresponds to a valid subparameter key.
    
    Args:
        user_input (str): The user's input.
        parameter (APIParameter): The parameter to check for subparameters.
    
    Returns:
        bool: True if the input matches a subparameter key, False otherwise.
    """
    return parameter.subparameters and user_input in parameter.subparameters


def execute_prompt(parameter: APIParameter):
    """
    Recursively prompts the user for input for the given parameter and its subparameters, if applicable.
    
    Args:
        parameter (APIParameter): The parameter to process.
    
    Returns:
        Union[str, list, dict]: User input, processed recursively if subparameters are present.
    """
    if parameter.loop:
        inputs = []
        while True:
            user_input = prompt_for_input(parameter)
            if user_input == 'q':
                break
            if has_subparameters(user_input, parameter):
                subparam_value = execute_prompt(parameter.subparameters[user_input])
                inputs.append(subparam_value)
            else:
                inputs.append(user_input)
        return inputs

    user_input = prompt_for_input(parameter)
    if has_subparameters(user_input, parameter):
        return execute_prompt(parameter.subparameters[user_input])

    return user_input

function_args = {}

for parameter in selected_function_group[selected_function]['inputs']:
    input = execute_prompt(parameter)
    arg_name = parameter.arg_name

    if arg_name == '_dict':
        for key in input:
            function_args[key] = input[key]
    else:
        function_args[arg_name] = input
    
function_args['api_manager'] = manager
if selected_function_group[selected_function].get('fixed_inputs'):
    function_args = function_args | selected_function_group[selected_function]['fixed_inputs']

output = selected_function_group[selected_function]['func'](**function_args)
if selected_function_group[selected_function].get('parse_data'):
    result = selected_function_group[selected_function]['parse_data'](cache, output)
    if isinstance(result, (list, tuple, set)):  
        for item in result:
            print(item, '\n')
    else:
        print(result)
