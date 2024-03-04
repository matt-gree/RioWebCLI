import requests
import web_functions
import argparse
from prompt_toolkit import prompt

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.validation import Validator, ValidationError
from datetime import datetime, timezone, timedelta
import os
import json
import string
end_completer =  WordCompleter([], ignore_case=True)

class CommaSeparatedIntegersValidator(Validator):
            def validate(self, document):
                text = document.text

                if not text:
                    # Empty input is allowed
                    return

                try:
                    # Attempt to convert each part to an integer
                    integers = [int(part.strip()) for part in text.split(',')]
                except ValueError:
                    raise ValidationError(message='Invalid input. Use comma-separated integers.')
    
class OptionValidator(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, document):
        text = document.text.strip()

        if text not in self.options:
            raise ValidationError(message=f'Valid options are: {", ".join(self.options)}')

def manage_community():
    print()
    history = InMemoryHistory()
    session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())

    tags_list = web_functions.get_tags(RIOKEY, tag_types=['Community'])
    community_names_list = []

    for tag in tags_list:
        community_names_list.append(tag['name'])
    
    community_names_completer = WordCompleter(community_names_list, ignore_case=True)

    community_manage_completer = WordCompleter(['Create Community', 'Check Community Sponsor', 'Invite Users to Community', 'Update Community Admins', 'Display Community Members', 'List Community Tags', 'Exit'], ignore_case=True)
    user_input = session.prompt('What would you like to do?\nCreate Community, Check Community Sponsor, Invite Users to Community, Update Community Admins, Display Community Members, List Community Tags\nSelection: ', completer=community_manage_completer)

    user_input = user_input.lower().replace(" ", "")

    def create_community():
        print("-----------------------------------------------\n Welcome to the RioWeb Community Creation Tool! \n-----------------------------------------------")

        community_type_completer = WordCompleter(['Official', 'Unofficial'], ignore_case=True)
        end_completer =  WordCompleter([], ignore_case=True)

        community_name = prompt('Enter the name for your community: ')
        community_type = prompt('Enter the type of community (Official, Unofficial): ', completer=community_type_completer, validator=OptionValidator(['Official', 'Unofficial']))
        is_private = prompt('Would you like the community to be private? (y/n): ', validator=OptionValidator(['y','n']))
        global_link = prompt('Would you like a global join link for your community? (y/n): ', validator=OptionValidator(['y','n']))
        description = prompt('Enter a description for your community: ')

        # Display information for confirmation
        print("\nPlease review the information:")
        print(f"Community Name: {community_name}")
        print(f"Community Type: {community_type}")
        print(f"Is Private: {is_private}")
        print(f"Global Link: {global_link}")
        print(f"Description: {description}")

        # Confirm submission
        confirmation = prompt('Do you want to submit this information? (y/n): \n')

        if confirmation.lower() == 'y':
            web_functions.create_community(community_name, community_type, is_private, global_link, description, RIOKEY)
        else:
            print("Community creation canceled.")

    def check_community_sponsor():
        community_name = prompt('Enter the name of the community: ', completer=community_names_completer)
        print()
        web_functions.check_sponsored_community(community_name, RIOKEY)

    def invite_users_to_community():
        print('Not yet functional')

    def update_community_admins():
        print('Not yet functional')

    def display_community_members():
        community_name = prompt('Enter the name of the community: ', completer=community_names_completer)
        print()
        web_functions.print_community_members(community_name, RIOKEY)

    def list_community_tags():
        community_name = prompt('Enter the name of the community: ', completer=community_names_completer)
        print()
        web_functions.print_community_tags(community_name, RIOKEY)

    if user_input == 'createcommunity':
        create_community()
    elif user_input == 'checkcommunitysponsor':
        check_community_sponsor()
    elif user_input == 'inviteuserstocommunity':
        invite_users_to_community()
    elif user_input == 'updatecommunityadmins':
        update_community_admins()
    elif user_input == 'displaycommunitymembers':
        display_community_members()
    elif user_input == 'listcommunitytags':
        list_community_tags()
    elif user_input == 'exit':
        return
    else:
        print("Invalid option. Please choose Create Community, Check Community Sponsor, Invite Users to Community, Update Community Admins, Display Community Members, List Community Tags")
        
def manage_tagset():
    print()
    history = InMemoryHistory()
    session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())

    community_manage_completer = WordCompleter(['Create Tag Set', 'Update Tag Set', 'Delete Tag Set', 'Print Tag Sets', 'Show TagSet Tags', 'Exit'], ignore_case=True)
    user_input = prompt('What would you like to do?\nCreate Tag Set, Update Tag Set, Delete Tag Set, Print Tag Sets, Show TagSet Tags, \nSelection: ', completer=community_manage_completer)

    user_input = user_input.lower().replace(" ", "")

    tagset_list = web_functions.get_tag_sets(RIOKEY)
    tagset_names_dict= {}

    for tagset in tagset_list:
        tagset_names_dict[tagset['name']] = tagset['id']
    
    tagset_names_completer = WordCompleter(tagset_names_dict.keys(), ignore_case=True)

    tagset_type_completer = WordCompleter(['Season', 'League', 'Tournament'], ignore_case=True)

    class DateValidator(Validator):
        def validate(self, document):
            text = document.text

            if text == '':
                return

            try:
                datetime.strptime(text, '%m-%d-%Y')
            except ValueError:
                raise ValidationError(message='Invalid date format. Use MM-DD-YYYY.')
            
    def tag_search_completion():
        tags_list = web_functions.get_tags(RIOKEY, tag_types=['Gecko Code', 'Component'])
        tags_dict = {}
        tag_completer_list = []
        for tag in tags_list:
            tag_completer_list.append(tag['name'])
            tags_dict[tag['name']] = tag

        tag_input_list = []
        while True: 
            tag_name_completer = prompt('\nWhich tags would you like to add? (Search by name)\nInput: ', completer=WordCompleter(tag_completer_list, ignore_case=True))
            date_string = datetime.utcfromtimestamp(tags_dict[tag_name_completer]['date_created']).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-5))).strftime('%Y-%m-%d %H:%M:%S')
            print(f'\nName: {tags_dict[tag_name_completer]["name"]}\nDescription: {tags_dict[tag_name_completer]["desc"]}\nTag ID: {tags_dict[tag_name_completer]["id"]}\nCommunity ID: {tags_dict[tag_name_completer]["comm_id"]}\nTag Type: {tags_dict[tag_name_completer]["type"]}\nDate Created: {date_string} EST\n')
            tag_input_list.append(tags_dict[tag_name_completer]["id"])
            continue_prompt = prompt('Tag Added! Would you like to add another? (y/n): ', validator=OptionValidator(['y','n']))
            if continue_prompt == 'n':
                break

        return tag_input_list
        
    def create_tag_set():
        print("Welcome to the Tag Set Creation Tool!")
        name = prompt('Enter the name of the tag set: ')
        desc = prompt('Enter the description of the tag set: ')
        type = prompt('Enter the type of the tag set (Season, League, Tournament): ', completer=tagset_type_completer, validator=OptionValidator(['Season', 'League', 'Tournament']))
        community_name = prompt('Enter the name of your community: ', completer=end_completer)
        
        # Prompt for tags (assuming comma-separated tag IDs)
        tags_input = tag_search_completion()
        if ',' in tags_input:
            tags = [int(tag_id.strip()) for tag_id in tags_input.split(',')]
        else:
            tags = None

        # Prompt for start date with validation
        start_date_str = prompt('Enter the start date (MM-DD-YYYY) of the tag set: ',
                            validator=DateValidator(),
                            validate_while_typing=True)
        
        start_date = int(datetime.strptime(start_date_str, '%m-%d-%Y').timestamp())

        # Prompt for end date with validation
        end_date_str = prompt('Enter the end date (MM-DD-YYYY) of the tag set: ',
                        validator=DateValidator(),
                        validate_while_typing=True)
        
        end_date = int(datetime.strptime(end_date_str, '%m-%d-%Y').timestamp())

        # Optional: Prompt for tag_set_id (if needed)
        tag_set_id = prompt('Enter the optional Tag Set ID to mirror (will overwrite the specified tags) (press Enter to skip): ')
        tag_set_id = int(tag_set_id) if tag_set_id.strip() else None

        # Display entered inputs and ask for confirmation
        print("\nPlease review your inputs:")
        print(f"Name: {name}")
        print(f"Description: {desc}")
        print(f"Type: {type}")
        print(f"Community Name: {community_name}")
        print(f"Tags: {tags}")
        print(f"Start Date: {start_date_str}")
        print(f"End Date: {end_date_str}")
        print(f"Tag Set ID: {tag_set_id}")

        confirmation = prompt('Do you want to submit this information? (y/n): \n')

        if confirmation.lower() == 'y':
             web_functions.create_tag_set(name, desc, type, community_name, tags, start_date, end_date, RIOKEY, tag_set_id)
        else:
            print("Tagset creation canceled.")

    def update_tag_set():

        tag_set_id = (prompt('Enter the ID or name of the tag set to update: ', completer=tagset_names_completer))

        if tag_set_id in tagset_names_dict.keys():
            tag_set_id =  tagset_names_dict[tag_set_id]
        elif tag_set_id not in tagset_names_dict.values():
            print('Invalid Tag Input')
            return
        
        for tag in tagset_list:
            if (tag['id'] == tag_set_id):
                current_tag_info = tag
                break


        print(f'\nCurrent Name: {current_tag_info["name"]}')
        new_name = prompt('Enter new name for the tag set (press Enter to skip): ')
        print()

        #print(f'Current Description: {current_tag_info["desc"]}')
        new_desc = prompt('Enter new description for the tag set (press Enter to skip): ')
        print()

        print(f'Current Tag Type: {current_tag_info["type"]}')
        new_type = prompt('Enter the new type of the tag set (Season, League, Tournament) (press Enter to skip): ', completer=tagset_type_completer, validator=OptionValidator(['Season', 'League', 'Tournament', '']))
        print()

        print(f'Current Start Date: {datetime.utcfromtimestamp(current_tag_info["start_date"]).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d %H:%M:%S")} EST')
        new_start_date = prompt('Enter new start date for the tag set (MM-DD-YYYY, press Enter to skip): ', validator=DateValidator())
        new_start_date = datetime.strptime(new_start_date, '%m-%d-%Y').timestamp() if new_start_date else None
        print()

        print(f'Current End Date: {datetime.utcfromtimestamp(current_tag_info["end_date"]).replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=-5))).strftime("%Y-%m-%d %H:%M:%S")} EST')
        new_end_date = prompt('Enter new end date for the tag set (MM-DD-YYYY, press Enter to skip): ', validator=DateValidator())
        new_end_date = datetime.strptime(new_end_date, '%m-%d-%Y').timestamp() if new_end_date else None
        print()

        applied_tags = {}
        for tag in current_tag_info['tags']:
            if tag['type'] in ['Gecko Code', 'Compettion']:
                applied_tags[tag['name']] = tag['id']

        print(f'Current Tags in Tagset:')
        for tag, id in applied_tags.items():
            print(f'Name: {tag}, ID: {id}')

        tags_edit = prompt('\nWould you like to ADD to the current tags or START OVER? (press Enter to skip): ', completer=WordCompleter(['Add', 'Start Over'], ignore_case=True), validator=OptionValidator(['Add', 'Start Over', '']))

        if tags_edit != '':
            new_tags = tag_search_completion()
            if tags_edit == 'Add':
                new_tags.extend(applied_tags.values())
        else:
            new_tags = None

        

        web_functions.update_tag_set(RIOKEY, tag_set_id, new_name, new_desc, new_type, new_start_date, new_end_date, new_tags)

    def print_tag_sets():

        active_input = prompt('Would you like to search for active tag sets only? (y/n): ', validator=OptionValidator(['y','n']))

        community_ids_input = prompt('Enter community IDs to search from (comma-separated, press Enter to skip): ', validator=CommaSeparatedIntegersValidator())
        community_ids_list = [int(community_id.strip()) for community_id in community_ids_input.split(',') if community_id.strip()] if community_ids_input else None

        web_functions.get_tag_sets(RIOKEY, active_only=active_input, communities=community_ids_list, print_option=True)

    def delete_tag_set():
        tag_set_name_input = prompt('Enter the name of the tagset: ', completer=tagset_names_completer)
        web_functions.delete_tag_set(RIOKEY, tag_set_name_input)

    def show_tag_set_tags():
        tag_set_id = prompt('Enter the name or ID of the tag set to show the tags of: ', completer=tagset_names_completer)

        if tag_set_id in tagset_names_dict.keys():
            tag_set_id = tagset_names_dict[tag_set_id]
        elif tag_set_id not in tagset_names_dict.values():
            print('Invalid Tag Input')
            return

        web_functions.get_tag_set_tags(tag_set_id, print_option=True)

    if user_input == 'createtagset':
        create_tag_set()
    elif user_input == 'updatetagset':
        update_tag_set()
    elif user_input == 'printtagsets':
        print_tag_sets()
    elif user_input == 'deletetagset':
        delete_tag_set()
    elif user_input == 'showtagsettags':
        show_tag_set_tags()
    elif user_input == 'exit':
        return
    else:
        print("Invalid option. Please choose \nCreate Tag Set, Update Tag Set, Delete Tag Set, Print Tag Sets, Show Tag Set Tags")
    
def manage_tags():
    user_input = prompt('What would you like to do?\nPrint Tags, Create Tag, Update Tag: ')
    user_input = user_input.lower().replace(" ", "")

    tag_type_completer = WordCompleter(["Component", "Competition", "Community", "Gecko Code"], ignore_case=True)
    tag_type_create_completer = WordCompleter(["Component", "Gecko Code"], ignore_case=True)

    def print_tags(): 
        tag_types_input = prompt('Enter tag types (comma-separated, press Enter to skip)\nComponent, Competition, Community, Gecko Code: ', completer=tag_type_completer)
        tag_types_list = [tag_type.strip() for tag_type in tag_types_input.split(',') if tag_type.strip()] if tag_types_input else None

        print(tag_types_list)

        community_ids_input = prompt('Enter community IDs (comma-separated, press Enter to skip): ', validator=CommaSeparatedIntegersValidator())
        community_ids_list = [int(community_id.strip()) for community_id in community_ids_input.split(',') if community_id.strip()] if community_ids_input else None

        web_functions.get_tags(RIOKEY, tag_types=tag_types_list, community_ids=community_ids_list, print_option=True)

    def create_tag():
        tag_name = prompt('Enter a name for the new tag: ')
        desc = prompt('Enter a description for the new tag: ')
        community_name = prompt('Enter the community name where the new tag will be created: ')
        tag_type = prompt('Enter tag type (Component, Gecko Code): ', completer=tag_type_create_completer)

        if tag_type == 'Gecko Code':
            gecko_code = prompt('Enter the gecko code: ')
            if gecko_code[-1] != '\n':
                gecko_code += '\n'
            gecko_code_desc = prompt('Enter a description of the Gecko Code: ')
        else:
            gecko_code = None
            gecko_code_desc = None

        def validate_gecko_code(in_str):
            index = 0
            for char in in_str:
                if index == 17:
                    if char != '\n':
                        return (False, "Invalid Gecko Code: Each line of 17 charccters must be seperated by a newline")
                    index = 0
                elif index == 8:
                    if char != ' ':
                        return (False, "Invalid Gecko Code: There must be a space between memory address and value")   
                    index+=1
                elif index <= 16:
                    if char not in string.hexdigits:
                        return (False, "Invalid Gecko Code: Gecko code must be made of hexvalues only")
                    index+=1
                #After the for loop 
            if (index != 0): #Loop ended in the middle of a line
                return (False, "Gecko code must end at the end of a line")
            return (True, "Gecko Code Validated!")
        
        print(validate_gecko_code(gecko_code)[1])
        if not validate_gecko_code(gecko_code)[0]:
            print("Please try again")
            return

        # Print out all inputs
        print("\nPlease confirm the information provided is correct:")
        print(f"Tag Name: {tag_name}")
        print(f"Description: {desc}")
        print(f"Community Name: {community_name}")
        print(f"Tag Type: {tag_type}")
        if tag_type == 'Gecko Code':
            print(f"Gecko Code:\n{gecko_code}")
            print(f"Gecko Code Description: {gecko_code_desc}")

        # Prompt the user to confirm
        confirmation = prompt("Confirm creation of the tag (y/n): ").lower()
        if confirmation != 'y':
            print("Tag creation aborted.")
            return

        web_functions.create_tag(RIOKEY, tag_name, desc, community_name, tag_type, gecko_code, gecko_code_desc)

    if user_input == 'printtags':
        print_tags()
    elif user_input == 'createtag':
        create_tag()
    elif user_input == 'updatetag':
        print('Not yet available')
    elif user_input == 'exit':
        return
    else:
        print("Invalid option. Please choose \nCreate Tag Set, Update Tag Set, Delete Tag Set, Print Tag Sets, Show Tag Set Tags")

if __name__ == "__main__":
    if os.path.exists('rio_key.json'):
        with open('rio_key.json', "r") as config_file:
            global RIOKEY
            RIOKEY = json.load(config_file)['rio_key']
    else:
        raise Exception('No file named rio_key.json. Please rename the template JSON and input your Rio key')

    history = InMemoryHistory()
    session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())

                
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

    while True:
        initial_completer = WordCompleter(['Community', 'Tagset', 'Tags', 'Exit'], ignore_case=True)
        user_input = prompt('\nChoose what to manage:\nCommunity, TagSet, Tags\nManage: ', completer=initial_completer)

        user_input = user_input.lower().strip()
        
        if user_input == 'community':
            manage_community()
        elif user_input == 'tagset':
            manage_tagset()
        elif user_input == 'tags':
            manage_tags()
        elif user_input == 'exit':
            break
        else:
            print("Invalid option. Please choose \nManage Community\nManage TagSet\nManage Tags")
