import os
import json
import datetime

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def get_html_test_data():
    with open(os.path.join(__location__, "test.html"), "rb") as f:
        return f.read()


def get_html_test_data_202603():
    with open(os.path.join(__location__, "202603.html"), "rb") as f:
        return f.read()