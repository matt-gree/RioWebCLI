from prompt_toolkit.validation import Validator, ValidationError
from datetime import datetime
import string

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
        if index == 17:
            if char != '\n':
                raise ValidationError(
                    message="Invalid Gecko Code: Add a newline to the end of the gecko code",
                    cursor_position=index
                    )
        elif index != 0: 
            raise ValidationError(
                message=f'Invalid Gecko Code: The final line must have 17 characters but only has {index} characters',
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