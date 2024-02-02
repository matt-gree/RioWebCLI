import requests
import json
import os


def create_community(community_name, type, private, global_link, desc, RIOKEY):
    headers = {'Content-Type': 'application/json'}

    community_data = {
        "community_name": community_name,
        "type": type,
        "private": private,       
        "global_link": global_link,  
        "desc": desc,
        "rio_key": RIOKEY
    }

    response = requests.post('https://api.projectrio.app/community/create', json=community_data, headers=headers)

    if response.status_code == 200:
        print("Community created successfully!")
        print(response.text)
    else:
        print(f"Failed to create community. Status code: {response.status_code}")
        print(response.text)


def check_sponsored_community(community_name, RIOKEY):
    url = "https://api.projectrio.app/community/sponsor"
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "community_name": community_name,
        "action": "get",
        "rio_key": RIOKEY
    }

    response = requests.post(url, json=data, headers=headers)

    if response.status_code == 200:
        result = response.json()
        sponsor_username = result.get('sponsor')
        print(f"{sponsor_username} is currently sponsoring the {community_name} community")
    else:
        print(f"Error: {response.status_code} - {response.text}")


def invite_users_to_community(community_name, users_to_invite):
    # Non Functional ATM
    """
    Invite users to a community.

    Args:
    - community_name (str): The name of the community to invite users to.
    - users_to_invite (list): List of usernames to invite.

    Returns:
    - dict: A dictionary containing information about the invited users.
    """

    # Prepare the payload
    payload = {
        'community_name': community_name,
        'invite_list': users_to_invite,
        'rio_key': RIOKEY
    }

    # Make the API request
    response = requests.post('https://api.projectrio.app/community/invite', json=payload)

    # Check the response
    if response.status_code == 200:
        invited_users = response.json()['Invited Users']
        print(f"Invited users to community '{community_name}': {invited_users}")
    else:
        error_message = f"Failed to invite users to community '{community_name}'. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def print_community_members(community_name, RIOKEY):
    """
    Print information about the members of a specified community.

    Args:
    - community_name (str): The name of the community to get members from.
    """

    # Prepare the payload
    payload = {
        'community_name': community_name,
        'rio_key': RIOKEY
    }

    # Make the API request
    response = requests.post('https://api.projectrio.app/community/members', json=payload)

    # Check the response
    if response.status_code == 200:
        members_list = response.json().get('Members', [])
        print(f"Members of community '{community_name}': ")
        for member in members_list:
            print(member)
    else:
        error_message = f"Failed to get members of community '{community_name}'. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def print_community_tags(community_name, RIOKEY):
    """
    Print information about the tags of a specified community.

    Args:
    - community_name (str): The name of the community to get tags from.
    - api_base_url (str): The base URL of the API. Default is 'https://api.projectrio.app'.
    - rio_key (str): The RioKey for authentication. Default is 'your_rio_key_here'.
    """

    # Prepare the payload
    payload = {
        'community_name': community_name,
        'rio_key': RIOKEY
    }

    # Make the API request
    response = requests.post('https://api.projectrio.app/community/tags', json=payload)

    # Check the response
    if response.status_code == 200:
        tags_info_list = response.json().get('Tags', [])
        print(f"Tags of community '{community_name}':" )
        for tag in tags_info_list:
            print(tag)
    else:
        error_message = f"Failed to get tags of community '{community_name}'. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def update_user_admin_status(community_name, username, RIOKEY, make_admin=True):
    """
    Update the admin status of a user within a community.

    Args:
    - community_name (str): The name of the community.
    - username (str): The username of the user to update admin status.
    - make_admin (bool): True to make the user an admin, False to remove admin status.
    """
    # Prepare the payload
    payload = {
        'community_name': community_name,
        'user_list': [
            {
                'username': username,
                'admin': make_admin
            }
        ],
        'rio_key': RIOKEY
    }

    # Make the API request
    response = requests.post('https://api.projectrio.app/community/manage', json=payload)

    # Check the response
    if response.status_code == 200:
        result = response.json().get('members', [])[0]
        action = "made an admin" if make_admin else "removed admin status"
        print(f"User {username} is now {action} in {community_name}")
    else:
        action = "make an admin" if make_admin else "remove admin status"
        error_message = f"Failed to {action} for {username} in {community_name}. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def print_all_tags(RIOKEY, tag_types=None, community_ids=None):
    """
    Print information about all tags or filtered tags based on type and communities.

    Args:
    - client (bool): Whether the request is made from a client (default is False).
    - tag_types (list): List of tag types to filter (optional).
    - community_ids (list): List of community IDs to filter (optional).
    """

    # Prepare the payload
    payload = {
    }
    if tag_types is not None:
        payload['tag_types'] = tag_types

    if community_ids is not None:
        payload['community_ids'] = community_ids

    # Make the API request
    print(payload)
    response = requests.post('https://api.projectrio.app/tag/list', json=payload)

    # Check the response
    if response.status_code == 200:
        tags_list = response.json().get('Tags', [])
        for tag in tags_list:
            print(tag)
    else:
        error_message = f"Failed to get tags. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def create_tag_set(name, desc, type, community_name, tags, start_date, end_date, RIOKEY, tag_set_id=None):
    """
    Create a new tag set.

    Args:
    - name (str): Name of the tag set.
    - desc (str): Description of the tag set.
    - type (str): Type of the tag set.
    - community_name (str): Name of the community associated with the tag set.
    - tags (list): List of tag IDs to be associated with the tag set.
    - start_date (str): Start date of the tag set.
    - end_date (str): End date of the tag set.
    - tag_set_id (int, optional): Tag Set ID to copy tags from (default is None).
    """

    # Prepare the payload
    payload = {
        'name': name,
        'desc': desc,
        'type': type,
        'community_name': community_name,
        'tags': tags,
        'start_date': start_date,
        'end_date': end_date,
        'rio_key': RIOKEY
    }
    if tag_set_id is not None:
            payload['tag_set_id']: tag_set_id
            payload = payload.pop('tags')

    # Make the API request
    response = requests.post('https://api.projectrio.app/tag_set/create', json=payload)

    # Check the response
    if response.status_code == 200:
        tag_set_info = response.json()
        print(f"Tag Set created successfully: {tag_set_info}")
    else:
        error_message = f"Failed to create tag set. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def get_tag_set_tags(tag_set_id):
    """
    Get the tags from a specified tag set.

    Args:
    - tag_set_id (int): ID of the tag set to retrieve tags from.
    """

    # Make the API request
    response = requests.get(f'https://api.projectrio.app/tag_set/{tag_set_id}')

    # Check the response
    if response.status_code == 200:
        tag_set_info = response.json().get('Tag Set', [])
        if tag_set_info:
            tags = tag_set_info[0].get('tags', [])
            print(f"Tags from Tag Set {tag_set_id}: {tags}")
        else:
            print(f"No information found for Tag Set {tag_set_id}")
    else:
        error_message = f"Failed to get tags from Tag Set {tag_set_id}. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def get_tag_sets(RIOKEY, active_only='n', communities=None):
    """
    Get information about all tag sets.

    Args:
    - client (bool): Whether the request is from a client.
    - active_only (bool): Whether to include only active tag sets.
    - communities (list): List of community IDs to filter tag sets.
    - rio_key (str): Rio Key for authentication.

    Returns:
    - dict: Information about the tag sets.
    """

    # Prepare the payload
    payload = {
        'Active': active_only,
        #'Rio Key': RIOKEY
    }

    if communities is not None:
        payload['Communities'] = communities

    # Make the API request
    response = requests.post('https://api.projectrio.app/tag_set/list', json=payload)

    # Check the response
    if response.status_code == 200:
        tag_sets_info = response.json().get('Tag Sets', [])
        if tag_sets_info:
            print("Tag Sets:")
            for tag_set_info in tag_sets_info:
                tag_set_id = tag_set_info.get('id')
                tag_set_name = tag_set_info.get('name')
                tag_set_type = tag_set_info.get('type')
                print(f"Tag Set ID: {tag_set_id}, Name: {tag_set_name}, Type: {tag_set_type}")
        else:
            print("No tag sets found.")
    else:
        error_message = f"Failed to get tag sets. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def delete_tag_set(RIOKEY, tag_set_name):
    """
    Delete a tag set by name.

    Args:
    - tag_set_name (str): Name of the tag set to delete.
    """

    # Prepare the payload
    payload = {
        'name': tag_set_name,
        'rio_key': RIOKEY
    }

    # Make the API request
    response = requests.post('https://api.projectrio.app/tag_set/delete', json=payload)

    # Check the response
    if response.status_code == 200:
        success_message = response.json().get('msg', '')
        print(success_message)
    else:
        error_message = f"Failed to delete tag set. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")


def update_tag_set(RIOKEY, tag_set_id, new_name=None, new_desc=None, new_type=None, new_start_date=None, new_end_date=None, new_tag_ids=None):
    """
    Update parameters of a tag set.

    Args:
    - tag_set_id (int): The ID of the tag set to update.
    - new_name (str, optional): New name for the tag set.
    - new_desc (str, optional): New description for the tag set.
    - new_type (str, optional): New type for the tag set.
    - new_start_date (int, optional): New start date for the tag set.
    - new_end_date (int, optional): New end date for the tag set.
    - new_tag_ids (list, optional): List of new tag IDs for the tag set.
    """

    # Prepare the payload
    payload = {
        'tag_set_id': tag_set_id,
        'rio_key': RIOKEY
    }

    # Add optional parameters to the payload
    if new_name:
        payload['name'] = new_name
    if new_desc:
        payload['desc'] = new_desc
    if new_type:
        payload['type'] = new_type
    if new_start_date:
        payload['start_date'] = new_start_date
    if new_end_date:
        payload['end_date'] = new_end_date
    if new_tag_ids:
        payload['tag_ids'] = new_tag_ids

    # Make the API request
    response = requests.post('https://api.projectrio.app/tag_set/update', json=payload)

    # Check the response
    if response.status_code == 200:
        success_message = response.json()
        print(success_message)
    else:
        error_message = f"Failed to update tag set. Status code: {response.status_code}"
        print(f"Error: {error_message}\nDetails: {response.text}")

if __name__ == "__main__":
    if os.path.exists('rio_key.json'):
        with open('rio_key.json', "r") as config_file:
            RIOKEY = json.load(config_file)['rio_key']
    else:
        raise Exception('No file named rio_key.json. Please rename the template json and input your rio key')

    # create_community(community_data)
    # check_sponsored_community("PJandFriends")
    # invite_users_to_community("PJandFriends", ['MattGree'])
    # print_community_members('PJandFriends')
    # update_user_admin_status('PJandFriends', 'VicklessFalcon', make_admin=False)
    # print_community_members('PJandFriends')
    # print_community_tags('PJandFriends')
    # print_all_tags(tag_types='Competition')
    # get_tag_set_tags(51)
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

