from prompt_toolkit import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.key_binding import KeyBindings, merge_key_bindings
from prompt_toolkit.key_binding.bindings.completion import display_completions_like_readline
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.widgets import TextArea
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.filters import Condition
from datetime import datetime
import re

class DateValidator(Validator):
    def validate(self, document):
        text = document.text
        try:
            if text:
                datetime.strptime(text, '%Y-%m-%d')
        except ValueError:
            raise ValidationError(message='Invalid date format. Use YYYY-MM-DD')

class UsernameValidator(Validator):
    def validate(self, document):
        text = document.text
        if not re.match(r'^[a-zA-Z0-9_]{3,}$', text):
            raise ValidationError(message='Username must be alphanumeric with underscores, min 3 chars')

class CLIInterface:
    def __init__(self):
        self.current_focus = 0
        self.kb = KeyBindings()
        self.done = False
        
        # Sample completers - replace these with your actual options
        self.tag_completer = WordCompleter(['important', 'urgent', 'low-priority', 'bug', 'feature'])
        self.username_completer = WordCompleter(['admin', 'user1', 'user2'])

        # Create input fields
        self.username_field = TextArea(
            height=1,
            prompt='Username: ',
            completer=self.username_completer,
            validator=UsernameValidator(),
            multiline=False,
            complete_while_typing=True
        )
        
        self.date_field = TextArea(
            height=1,
            prompt='Date: ',
            validator=DateValidator(),
            multiline=False
        )
        
        self.tag_field = TextArea(
            height=1,
            prompt='Tag: ',
            completer=self.tag_completer,
            multiline=False,
            complete_while_typing=True
        )

        self.fields = [self.username_field, self.date_field, self.tag_field]
        self.setup_keybindings()

    def setup_keybindings(self):
        @self.kb.add('up')
        def _(event):
            self.current_focus = (self.current_focus - 1) % len(self.fields)
            self.app.layout.focus(self.fields[self.current_focus])

        @self.kb.add('down')
        def _(event):
            self.current_focus = (self.current_focus + 1) % len(self.fields)
            self.app.layout.focus(self.fields[self.current_focus])

        @self.kb.add('enter')
        def _(event):
            try:
                # Validate all fields
                self.username_field.buffer.validate()
                self.date_field.buffer.validate()
                # Tag validation is optional
                self.done = True
                event.app.exit()
            except ValidationError:
                # If validation fails, don't exit
                pass

        @self.kb.add('c-c')
        def _(event):
            self.done = False
            event.app.exit()

        # Add completion key bindings
        @self.kb.add('tab')
        def _(event):
            buff = event.current_buffer
            if buff.completer:
                buff.complete_next()

        @self.kb.add('s-tab')
        def _(event):
            buff = event.current_buffer
            if buff.completer:
                buff.complete_previous()

    def create_layout(self):
        return Layout(HSplit([
            Window(height=1),  # Top padding
            *self.fields,
            Window(height=1),  # Middle padding
            Window(
                content=FormattedTextControl(
                    text="Press Enter to submit (Tab for completions), Ctrl-C to cancel"
                ),
                height=1
            ),
            Window(height=1),  # Bottom padding
        ]))

    def run(self):
        # Merge our key bindings with the default ones
        kb = merge_key_bindings([
            load_key_bindings(),  # Default bindings
            self.kb              # Our custom bindings
        ])

        self.app = Application(
            layout=self.create_layout(),
            key_bindings=kb,
            full_screen=True,
            mouse_support=True
        )
        
        self.app.layout.focus(self.fields[0])
        self.app.run()
        return self.done

    def get_values(self):
        return {
            'username': self.username_field.text,
            'date': self.date_field.text,
            'tag': self.tag_field.text
        }

if __name__ == '__main__':
    interface = CLIInterface()
    if interface.run():
        values = interface.get_values()
        print("\nSubmitted values:", values)
    else:
        print("\nCancelled by user")