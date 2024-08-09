from web_functions import list_tags, list_users
from APIManager import APIManager

class CompleterCache:
    def __init__(self, manager: APIManager):
        self.manager = manager
        self.communities_list = []
        self.users_dict = {}
        self.users_list = []
    
    def communities(self):
        if not self.communities_list:
            self.communities_list = [tag['name'] for tag in list_tags(self.manager, ['Community'])['Tags']]
        
        return self.communities_list
    
    def users_dictionary(self):
        if not self.users_dict:
            self.users_dict = list_users(self.manager)['users']
        
        return self.users_dict
    
    def users(self):
        if not self.users_dict:
            self.users_dict = list_users(self.manager)['users']
        if not self.users_list:
            self.users_list = list(self.users_dict.values())

        return self.users_list