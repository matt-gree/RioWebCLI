from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.widgets import RadioList, Button, Label
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit import print_formatted_text as print_formatted

# Define the dropdown options
function_groups = [
    ('manage_communities', 'Manage Communities'),
    ('manage_game_modes', 'Manage Game Modes'),
    ('manage_tags', 'Manage Tags'),
    ('rio_mod_functions', 'Rio Mod Functions'),
]

functions = {
    'manage_communities': [
        ('add_community', 'Add Community'),
        ('remove_community', 'Remove Community'),
        ('edit_community', 'Edit Community')
    ],
    'manage_game_modes': [
        ('add_game_mode', 'Add Game Mode'),
        ('remove_game_mode', 'Remove Game Mode'),
        ('edit_game_mode', 'Edit Game Mode')
    ],
    'manage_tags': [
        ('add_tag', 'Add Tag'),
        ('remove_tag', 'Remove Tag'),
        ('edit_tag', 'Edit Tag')
    ],
    'rio_mod_functions': [
        ('update_rio', 'Update Rio Mod'),
        ('rollback_rio', 'Rollback Rio Mod'),
        ('configure_rio', 'Configure Rio Mod')
    ]
}


def _create_app(dialog, style):
    """Create an application for the dialog."""
    return Application(
        layout=Layout(dialog),
        full_screen=True,
        style=style,
    )


def radiolist_dialog(
    title: str = "",
    text: str = "",
    ok_text: str = "Ok",
    cancel_text: str = "Cancel",
    values: list = None,
    default: str = None,
    style: Style = None,
):
    """
    Display a simple list of elements the user can choose amongst, and handles two menus.
    """
    if values is None:
        values = []

    selected_category = None
    selected_function = None

    def ok_handler() -> None:
        """Handler when the user selects 'OK'"""
        get_app().exit(result=selected_function)

    def _return_none() -> None:
        """Cancel handler"""
        get_app().exit(result=None)

    # Create the first menu (category selection)
    def create_category_menu():
        nonlocal selected_category
        radio_list = RadioList(values=values, default=default)

        def on_category_selected() -> None:
            selected_category = radio_list.current_value[0]
            create_function_menu(selected_category)
            get_app().exit()

        radio_list.on_select = on_category_selected

        dialog = Dialog(
            title=title,
            body=HSplit([Label(text=text), radio_list]),
            buttons=[
                Button(text=ok_text, handler=ok_handler),
                Button(text=cancel_text, handler=_return_none),
            ]
        )

        return dialog

    # Create the second menu (function selection based on category)
    def create_function_menu(category):
        nonlocal selected_function
        function_values = functions.get(category, [])
        radio_list = RadioList(values=function_values)

        def on_function_selected() -> None:
            selected_function = radio_list.current_value[0]
            get_app().exit()

        radio_list.on_select = on_function_selected

        dialog = Dialog(
            title=title,
            body=HSplit([Label(text=f"Select function for {category}:"), radio_list]),
            buttons=[
                Button(text=ok_text, handler=ok_handler),
                Button(text=cancel_text, handler=_return_none),
            ]
        )

        return dialog

    # Create and show the first menu dialog
    dialog = create_category_menu()

    return _create_app(dialog, style)


def _return_none() -> None:
    """No action"""
    pass


class Dialog:
    def __init__(self, title, body, buttons):
        self.title = title
        self.body = body
        self.buttons = buttons


def run_two_page_dialog():
    # Call the radiolist_dialog with two menus
    result = radiolist_dialog(
        title="Select a Function",
        text="Choose a category and then select a function",
        values=function_groups,
    )
    print(result)  # The selected option


if __name__ == "__main__":
    run_two_page_dialog()