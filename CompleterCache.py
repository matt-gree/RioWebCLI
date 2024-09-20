from web_functions import list_tags, list_users, list_game_modes
from APIManager import APIManager

class CompleterCache:
    def __init__(self, manager: APIManager):
        self.manager = manager
        self.communities_list = []
        self.users_dict = {}
        self.users_list = []
        self.tags_dict = {}
        self.game_mode_dict = {}
    
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
    
    def tags_dictionary(self):
        if not self.tags_dict:
            self.tags_dict = {tag['name']: tag['id'] for tag in list_tags(self.manager, ['Gecko Code', 'Component'])['Tags']}

        return self.tags_dict
    
    def game_mode_dictionary(self):
        if not self.game_mode_dict:
            self.game_mode_dict = {tag['name']: tag['id'] for tag in list_game_modes(self.manager)['Tag Sets']}

        return self.game_mode_dict