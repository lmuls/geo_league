import os
import json
import datetime
from geo_league_vars import BASE_DIR


def get_local_test_data():
    with open("test_data.json", "rb") as f:
        data = json.load(f)
        game_information = {
            "date": datetime.date(2022, 9, 17),
            "game_id": "LqzTy7nxHCCAMU5I"
        }
        return data, game_information


def get_local_test_data_2():
    with open("test_data_2.json", "rb") as f:
        data = json.load(f)
        game_information = {
            "date": datetime.date(2022, 9, 17),
            "game_id": "wmaH8zFegtFblYHJ"
        }
        return data, game_information
