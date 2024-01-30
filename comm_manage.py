import requests
import web_functions
import argparse
from prompt_toolkit import prompt

from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
import os
import json

def manage_community():
    print()
    history = InMemoryHistory()
    session = PromptSession(history=history, auto_suggest=AutoSuggestFromHistory())

    community_manage_completer = WordCompleter(['Create Community', 'Check Community Sponsor', 'Invite Users to Community', 'Update Community Admins', 'Display Community Members', 'List Community Tags', 'Exit'], ignore_case=True)
    user_input = session.prompt('What would you like to do?\nCreate Community, Check Community Sponsor, Invite Users to Community, Update Community Admins, Display Community Members, List Community Tags\nSelection: ', completer=community_manage_completer)

    user_input = user_input.lower().replace(" ", "")

    def create_community():
        print("-----------------------------------------------\n Welcome to the RioWeb Community Creation Tool! \n-----------------------------------------------")

        community_type_completer = WordCompleter(['Official', 'Unofficial'], ignore_case=True)
        end_completer =  WordCompleter([], ignore_case=True)

        community_name = session.prompt('Enter the name for your community: ')
        community_type = session.prompt('Enter the type of community (Official, Unofficial): ', completer=community_type_completer)
        is_private = session.prompt('Would you like the community to be private? (y/n): ', completer=end_completer)
        global_link = session.prompt('Would you like a global join link for your community? (y/n): ')
        description = session.prompt('Enter a description for your community: ')

        # Display information for confirmation
        print("\nPlease review the information:")
        print(f"Community Name: {community_name}")
        print(f"Community Type: {community_type}")
        print(f"Is Private: {is_private}")
        print(f"Global Link: {global_link}")
        print(f"Description: {description}")

        # Confirm submission
        confirmation = session.prompt('Do you want to submit this information? (y/n): \n')

        if confirmation.lower() == 'y':
            web_functions.create_community(community_name, community_type, is_private, global_link, description, RIOKEY)
        else:
            print("Community creation canceled.")

    def check_community_sponsor():
        community_name = session.prompt('Enter the name of the community: ')
        print()
        web_functions.check_sponsored_community(community_name, RIOKEY)

    def invite_users_to_community():
        print('Not yet functional')

    def update_community_admins():
        print('Not yet functional')

    def display_community_members():
        community_name = session.prompt('Enter the name of the community: ')
        print()
        web_functions.print_community_members(community_name, RIOKEY)

    def list_community_tags():
        community_name = session.prompt('Enter the name of the community: ')
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
        print("Invalid option. Please choose \nManage Community\nManage TagSet\nManage Tags")
        
def manage_tagset():
    community_name = session.prompt('Enter the name of the community to edit (TagSet): ')
    print(f"Editing community (TagSet): {community_name}")

def manage_tags():
    community_name = session.prompt('Enter the name of the community to edit (Tags): ')
    print(f"Editing community (Tags): {community_name}")

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
        user_input = session.prompt('\nChoose what to manage:\nCommunity, TagSet, Tags\nManage: ', completer=initial_completer)

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

    
    # create_community(community_data)
    # check_sponsored_community("PJandFriends")
    # invite_users_to_community("PJandFriends", ['MattGree'])
    # print_community_members('PJandFriends')
    # update_user_admin_status('PJandFriends', 'VicklessFalcon', make_admin=False)
    # print_community_members('PJandFriends')
    # print_community_tags('PJandFriends')
    # print_all_tags(tag_types='Competition')
    # get_tag_set_tags(59)
    # get_tag_sets()
    # create_tag_set("NNL Training",
    #                "NNL Season 5 Spring Training mode for non-league scheduled games",
    #                "League",
    #                "PJandFriends",
    #                [14, 22, 44, 4, 50, 66, 24],
    #                1706497388,
    #                1706600000,
    #                59)
    # delete_tag_set("NNL Training")
    
    #update_tag_set(61, new_end_date=1714971600)
