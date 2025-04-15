import sys

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter

from pyRio.api_manager import APIManager
from pyRio.web_caching import CompleterCache
from comm_manager_functions import community_functions, tag_functions, game_mode_functions, rio_mod_functions, data_endpoints
from prompt_validators import OptionValidator
from api_parameters import APIParameter
from function_executer import ParameterProcessor

manager = APIManager()
cache = CompleterCache(manager)

formatted_text = '''
     _____  _   __          __  _      _____ _      _____ 
    |  __ \(_)  \ \        / / | |    / ____| |    |_   _|
    | |__)| _  __\ \  /\  / /__| |__ | |    | |      | |  
    |  _  /| |/ _ \ \/  \/ / _ \ '_ \| |    | |      | |  
    | | \ \| | (_) \  /\  /  __/ |_) | |____| |____ _| |_ 
    |_|  \_\_|\___/ \/  \/ \___|_.__/ \_____|______|_____|
         
    '''

function_groups = {
    'Manage Communities': community_functions,
    'Manage Game Modes': game_mode_functions,
    'Manage Tags': tag_functions,
    'Rio Mod Functions': rio_mod_functions,
    'Data Endpoints': data_endpoints,
    'Update Cache': cache.refresh_cache
}

print(formatted_text)

while True:
    print(f'\nMenu Options: ')
    for key in function_groups.keys():
        print(f'    {key}')
    print()

    selected_function_group = prompt('What would you like to do (or "q" to quit): ',
                                     completer=FuzzyCompleter(WordCompleter(list(function_groups.keys()) + ['q'], ignore_case=True)),
                                     validator=OptionValidator(list(function_groups.keys()) + ['q']))

    if selected_function_group.lower() == 'q':
        break

    if selected_function_group == 'Update Cache':
        cache.refresh_cache()
        continue

    print()
    print(f'{selected_function_group}: ')
    selected_function_group_dict = function_groups[selected_function_group]

    while True:
        for key in selected_function_group_dict:
            print(f'    {key}')
        print()

        selected_function_str = prompt('What would you like to do ("b" to go back): ',
                                       completer=FuzzyCompleter(WordCompleter(list(selected_function_group_dict.keys()), ignore_case=True)),
                                       validator=OptionValidator(list(selected_function_group_dict.keys()) + ['b']))

        if selected_function_str.lower() == 'b':
            break

        executor = ParameterProcessor()
        selected_function = selected_function_group_dict[selected_function_str]
        function_args = executor.gather_function_args(selected_function.inputs)

        function_args['api_manager'] = manager

        if selected_function.constant_inputs:
            function_args = function_args | selected_function.constant_inputs

        output = selected_function.func(**function_args)
        if selected_function.parse_data:
            result = selected_function.parse_data(cache, output)
            if isinstance(result, (list, tuple, set)):
                for item in result:
                    print(item, '\n')
            else:
                print(result)

        if selected_function.refresh_cache:
            cache.refresh_cache()
