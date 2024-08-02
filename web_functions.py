import json
from APIManager import include_rio_key, APIManager

with open('rio_key.json', "r") as config_file:
    global RIO_KEY
    RIO_KEY = json.load(config_file)['rio_key']

### example of including the decorator. I'd also like to think that you could streamline the params part too but I didn't have anything come to mind right now
@include_rio_key(RIO_KEY)
def create_community(api_manager: APIManager, community_name_free, private, global_link, desc, comm_type="Unofficial", data=None):
    ### this is because of the decorator, by using it, the args for the function get kinda wonky, so the way to fix it is to pass it data so that what it is expecting is there
    if data is None:
        data = {}

    ### because of above, just update data, not create new one
    data.update({
        "community_name": community_name_free,
        "type": comm_type,
        "private": private,       
        "global_link": global_link,  
        "desc": desc,
    })

    ### calls api manager and sends the request
    return api_manager.send_request("/community/create", method="POST", data=data)

@include_rio_key(RIO_KEY)
def community_invite(api_manager: APIManager, community_name_closed, invite_list, data=None):
    if data is None:
        data = {}

    data.update({
        "community_name": community_name_closed,
        "invite_list": invite_list
    })

    return api_manager.send_request("/community/invite", method="POST", data=data)

@include_rio_key(RIO_KEY)
def list_tags(api_manager: APIManager, tag_types=None, community_ids=None, data=None):
    if data is None:
        data = {}

    if tag_types:
        data['Types'] = tag_types

    if community_ids:
        data['community_ids'] = community_ids

    # Make the API request
    return api_manager.send_request("/tag/list", method="POST", data=data)

def list_users(api_manager: APIManager):
    return api_manager.send_request('/user/all')
