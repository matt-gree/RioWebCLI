from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from project_rio_lib.api_manager import APIManager
from project_rio_lib.web_caching import CompleterCache
from comm_manager_functions import community_endpoints, supported_endpoints
from prompt_validators import OptionValidator, GeckoCodeValidator, DateValidator
from api_parameters import APIParameter

manager = APIManager()
cache = CompleterCache(manager)

community_endpoints_prompt = APIParameter(
    prompt = 'What would you like to do: ',
    arg_name=None,
    completer =  supported_endpoints,
    validator = OptionValidator(supported_endpoints)
)

def get_prompt_input(parameter: APIParameter, break_key='q'):
    completer = WordCompleter(parameter.completer, ignore_case=True)
    input = prompt(parameter.prompt, completer=completer, validator=parameter.validator, multiline=parameter.multiline)
    if input == break_key:
        return break_key
    if parameter.input_processing:
        input = parameter.input_processing(input)

    return input

def run_prompt(parameter: APIParameter):
    if parameter.loop:
        input = []
        while True:
            add_item = get_prompt_input(parameter,)
            if add_item == 'q':
                break
            input.append(add_item)
        return input

    return get_prompt_input(parameter)        

function_args = {}

user_endpoint_choice = run_prompt(community_endpoints_prompt)
for parameter in community_endpoints[user_endpoint_choice]['inputs']:
    input = run_prompt(parameter)

    if parameter.subparameters:
        input = run_prompt(parameter.subparameters[input])

    arg_name = parameter.arg_name

    if arg_name == '_dict':
        for key in input:
            function_args[key] = input[key]
    else:
        function_args[arg_name] = input
    
function_args['api_manager'] = manager
if community_endpoints[user_endpoint_choice].get('fixed_inputs'):
    function_args = function_args | community_endpoints[user_endpoint_choice]['fixed_inputs']

output = community_endpoints[user_endpoint_choice]['func'](**function_args)
if community_endpoints[user_endpoint_choice].get('parse_data'):
    result = community_endpoints[user_endpoint_choice]['parse_data'](cache, output)
    if isinstance(result, (list, tuple, set)):  
        for item in result:
            print(item, '\n')
    else:
        print(result)
