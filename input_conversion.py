from typing import List, Optional, Union, Callable
from datetime import datetime
import pytz
import json

from project_rio_lib.web_functions import community_members


class InputConverters:
    @staticmethod
    def create_list_from_txt(txt_path):
        try:
            with open(txt_path, 'r') as file:
                content = file.read().strip()
                username_list = content.split(',')
                username_list = [username.strip() for username in username_list]  # Remove extra whitespace
            return username_list
        except FileNotFoundError:
            print(f"File not found: {txt_path}")
            return []
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
        
    @staticmethod
    def yes_to_1_converter(y_or_n):
        conversion_dict = {
            'y': 1,
            'n': 0
        }

        return conversion_dict[y_or_n]
    
    @staticmethod
    def yes_no_to_t_f(y_or_n):
        conversion_dict = {
            'y': True,
            'n': False
        }

        return conversion_dict[y_or_n]
    
    @staticmethod
    def dictionary_conversion(key, dictionary):
        return dictionary[key]
    
    @staticmethod
    def community_manager_converter(user, ban=None, remove=None, key=None, admin=None):
        user_action_dict = {}
        action_values  = [True, False]
        user_action_dict['username'] = user

        if ban in action_values:
            user_action_dict['ban'] = ban

        if remove in action_values:
            user_action_dict['remove'] = remove

        if key in action_values:
            user_action_dict['key'] = key
        
        if admin in action_values:
            user_action_dict['admin'] = admin

        return user_action_dict
    
    @staticmethod
    def stat_file_converter(stat_file_path, cache_instance):
        with open(stat_file_path) as f:
            hud_data = json.load(f)

        game_id_hex = int(hud_data['GameID'].replace(",", ""))
        away_score = hud_data['Away Score']
        home_score = hud_data['Home Score']
        tag_set_id = hud_data['TagSetID']

        reversed_dict = {v: k for k, v in cache_instance.game_mode_dictionary().items()}
        tag_set_name = reversed_dict[tag_set_id]
        
        try:
            date = int(hud_data['Date - End'])
        except:
            datetime_format = "%a %b %d %H:%M:%S %Y"
            est_time = datetime.strptime(hud_data['Date - End'], datetime_format).replace(tzinfo=pytz.timezone("America/New_York"))
            date = int(est_time.timestamp())

        if away_score > home_score:
            winner_username = hud_data['Away Player']
            loser_username = hud_data['Home Player']
            winner_score = away_score
            loser_score = home_score
        elif home_score > away_score:
            winner_username = hud_data['Home Player']
            loser_username = hud_data['Away Player']
            winner_score = home_score
            loser_score = away_score
        else:
            raise Exception('Stat file supplied has no winner')
        
        manual_submit_dict = {
            #'game_id_hex': game_id_hex,
            'winner_username': winner_username,
            'winner_score': winner_score,
            'loser_username': loser_username,
            'loser_score': loser_score,
            'date': date,
            'tag_set': tag_set_name
        }

        return manual_submit_dict
    
    @staticmethod
    def date_processing(date_string, eod=False):
        # Define the EST timezone
        est = pytz.timezone('America/New_York')
        
        # Parse the date string and set time to 11:59:59 PM
        naive_datetime = datetime.strptime(date_string, '%m-%d-%Y')
        est_datetime = est.localize(naive_datetime)
        if eod:
            est_datetime = est.localize(naive_datetime.replace(hour=23, minute=59, second=59))
        
        # Return the timestamp
        return int(est_datetime.timestamp())
    
    @staticmethod
    def remove_all_users_list(y_or_n, cache_instance, manager):
        print(y_or_n)
        if y_or_n == 'y':
            user_list = []
            for user_dict in community_members(manager, 'Rookie Rumble')['Members']:
                try:
                    user_name = InputConverters.dictionary_conversion(str(user_dict['user_id']), cache_instance.users_dictionary())
                except:
                    continue
                user_list.append(InputConverters.community_manager_converter(user_name, remove=True))
            return user_list
        else:
            return None