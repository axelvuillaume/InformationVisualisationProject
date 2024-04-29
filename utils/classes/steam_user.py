from utils.data_processing import get_game_list_from_api, get_friends_list_from_api

class Steam_User:
    def __init__(self, steamid, fetch_friends=True):
        self._steamid = steamid
        self._games = get_game_list_from_api(steamid)
        self._fetch_friends = fetch_friends
        self._friends = None
        
        if self._fetch_friends:
            self._friends = get_friends_list_from_api(steamid)

    @property
    def games(self):
        return self._games

    @property
    def steamid(self):
        return self._steamid
    
    @property
    def friends(self):
        return self._friends

    # Setting steamid will cause the games df to be updated
    @steamid.setter
    def steamid(self, value):
        self._steamid = value
        self._update_user_data(value)

    # Get friend games
    def get_friend_games(self, friend):
        return get_game_list_from_api(friend.steamid)

    def _update_user_data(self, steamid):
        self._games = get_game_list_from_api(steamid)

        if self._fetch_friends:
            self._friends = get_friends_list_from_api(steamid)
        # Update other fields related to user data from steam api here