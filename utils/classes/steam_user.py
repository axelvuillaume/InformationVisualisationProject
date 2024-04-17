from utils.data_processing import get_game_list_from_api

class Steam_User:
    def __init__(self, steamid):
        self._steamid = steamid
        self._games = get_game_list_from_api(steamid)

    @property
    def games(self):
        return self._games

    @property
    def steamid(self):
        return self._steamid

    # Setting steamid will cause the games df to be updated
    @steamid.setter
    def steamid(self, value):
        self._steamid = value
        self._update_user_data(value)

    def _update_user_data(self, steamid):
        self._games = get_game_list_from_api(steamid)
        # Update other fields related to user data from steam api here
