from prompt_toolkit import PromptSession
from prompt_toolkit.validation import Validator, ValidationError
import string

# Define the GeckoCodeValidator
class GeckoCodeValidator(Validator):
    def validate(self, document):
        in_str = document.text
        index = 0
        
        for i, char in enumerate(in_str):
            if index == 17:
                if char != '\n':
                    raise ValidationError(
                        message="Invalid Gecko Code: Each line of 17 characters must be separated by a newline",
                        cursor_position=i
                    )
                index = 0
            elif index == 8:
                if char != ' ':
                    raise ValidationError(
                        message="Invalid Gecko Code: There must be a space between memory address and value",
                        cursor_position=i
                    )
                index += 1
            elif index <= 16:
                if char not in string.hexdigits:
                    raise ValidationError(
                        message="Invalid Gecko Code: Gecko code must be made of hex values only",
                        cursor_position=i
                    )
                index += 1
        
        # After the loop, check if we ended in the middle of a line
        if index == 17:
            if char != '\n':
                raise ValidationError(
                    message="Invalid Gecko Code: Add a newline to the end of the gecko code",
                    cursor_position=len(in_str)
                )
        elif index != 0:
            raise ValidationError(
                message=f"Invalid Gecko Code: The final line must have 17 characters but only has {index} characters",
                cursor_position=len(in_str)
            )

# Create a PromptSession with the GeckoCodeValidator
session = PromptSession(multiline=True, validator=GeckoCodeValidator())

print("Enter your Gecko code (Ctrl+D to finish):")

try:
    # Read multiline input
    user_input = session.prompt(">>> ")
    print("\nYou entered valid Gecko code:\n")
    print(user_input)
except EOFError:
    print("\nInput ended (Ctrl+D detected).")
except ValidationError as e:
    print(f"\nValidation Error: {e}")