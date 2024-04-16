import os
import json
import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))


def get_local_test_data():
    with open(os.path.join(__location__, "test_data.json"), "rb") as f:
        data = json.load(f)
        game_information = {
            "date": datetime.date(2022, 9, 17),
            "game_id": "LqzTy7nxHCCAMU5I"
        }
        return data, game_information


def get_local_test_data_2():
    with open(os.path.join(__location__, "test_data_2.json"), "rb") as f:
        data = json.load(f)
        game_information = {
            "date": datetime.date(2022, 9, 17),
            "game_id": "wmaH8zFegtFblYHJ"
        }
        return data, game_information

def get_html_test_data():
    with open(os.path.join(__location__, "test.html"), "r", encoding="UTF-8") as f:
        return f.read()