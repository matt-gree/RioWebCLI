from typing import List, Union, Dict, Optional
from prompt_toolkit.completion import WordCompleter, FuzzyCompleter
from prompt_toolkit import prompt


class ParameterProcessor:
    def __init__(self, break_key: str = 'q'):
        """
        Initializes the parameter processor.
        
        Args:
            break_key (str): Key to exit input loops (default is 'q').
        """
        self.break_key = break_key

    def prompt_for_input(self, parameter):
        """
        Displays a prompt for user input based on the given APIParameter.
        Processes the input if a processing function is provided.

        Args:
            parameter (APIParameter): The parameter containing the prompt configuration.

        Returns:
            str: User input after optional processing, or the break key if entered.
        """
        completer = WordCompleter(parameter.completer, ignore_case=True) if parameter.completer else None
        completer = FuzzyCompleter(completer) if completer else None
        user_input = prompt(parameter.prompt, completer=completer, validator=parameter.validator, multiline=parameter.multiline)
        
        if user_input == self.break_key:
            return self.break_key
        
        if parameter.input_processing:
            user_input = parameter.input_processing(user_input)
        
        return user_input

    def has_subparameters(self, user_input: str, parameter) -> bool:
        """
        Checks if the given input corresponds to a valid subparameter key.

        Args:
            user_input (str): The user's input.
            parameter (APIParameter): The parameter to check for subparameters.

        Returns:
            bool: True if the input matches a subparameter key, False otherwise.
        """
        return parameter.subparameters and user_input in parameter.subparameters

    def execute_prompt(self, parameter):
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
                user_input = self.prompt_for_input(parameter)
                if user_input == self.break_key:
                    break
                
                if self.has_subparameters(user_input, parameter):
                    subparam_value = self.execute_prompt(parameter.subparameters[user_input])
                    inputs.append({parameter.subparameters[user_input].arg_name: subparam_value})
                else:
                    inputs.append(user_input)
            return inputs

        user_input = self.prompt_for_input(parameter)

        if self.has_subparameters(user_input, parameter):
            return self.execute_prompt(parameter.subparameters[user_input])
        
        if user_input == self.break_key:
            return None
        
        return user_input

    def gather_function_args(self, parameters: List) -> Dict:
        """
        Iterates over a list of parameters, prompting the user for inputs and assembling arguments.

        Args:
            parameters (List[APIParameter]): A list of input parameters.

        Returns:
            Dict: A dictionary of argument names and their corresponding user inputs.
        """
        function_args = {}
        for parameter in parameters:
            user_input = self.execute_prompt(parameter)
            arg_name = parameter.arg_name

            if arg_name == '_dict':
                for key, value in user_input.items():
                    function_args[key] = value
            elif parameter.data_params_dict:
                merged = {}
                print(user_input)
                for d in user_input:
                    for key, value in d.items():
                        # If the key already exists in merged
                        if key in merged:
                            # Only merge list-type values
                            if isinstance(merged[key], list) and isinstance(value, list):
                                merged[key].extend(value)
                            elif isinstance(merged[key], list):
                                merged[key].append(value)
                            else:
                                # Don't try to merge non-list values (e.g., bool, str) — overwrite or raise warning
                                merged[key] = value
                        else:
                            # First time seeing the key
                            merged[key] = value if not isinstance(value, list) else list(value)
                function_args[arg_name] = merged
            else:
                function_args[arg_name] = user_input
        
        return function_args