import os
import json
import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_html_test_data():
    with open(os.path.join(__location__, "test.html"), "r", encoding="UTF-8") as f:
        return f.read()