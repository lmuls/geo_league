import pytest
from batch.parse_html import parse
from test_data.provider import get_html_test_data, get_html_test_data_202603


# ---------------------------------------------------------------------------
# Original results page (results_table / results_row_ / results_column)
# ---------------------------------------------------------------------------

def test_parse_game_id():
    game_id, _, _ = parse(get_html_test_data())
    assert game_id == "6wH0fIB2VabiBp3j"


def test_parse_map_name():
    _, map_name, _ = parse(get_html_test_data())
    assert map_name == "Oslo"


def test_parse_player_count():
    _, _, results = parse(get_html_test_data())
    assert len(results) == 10


def test_parse_total_score():
    _, _, results = parse(get_html_test_data())
    assert sum(score for _, score in results) == 198389


# ---------------------------------------------------------------------------
# Newer results page (coordinate-results_table / coordinate-results_row_ / etc.)
# ---------------------------------------------------------------------------

def test_parse_202603_game_id():
    game_id, _, _ = parse(get_html_test_data_202603())
    assert game_id == "xLTUgE1GAVTaIOhm"


def test_parse_202603_map_name():
    _, map_name, _ = parse(get_html_test_data_202603())
    assert map_name == "Norske Byer, tettsteder og bygda"


def test_parse_202603_player_count():
    _, _, results = parse(get_html_test_data_202603())
    assert len(results) == 6


def test_parse_202603_total_score():
    _, _, results = parse(get_html_test_data_202603())
    assert sum(score for _, score in results) == 126511


def test_parse_202603_players():
    _, _, results = parse(get_html_test_data_202603())
    names = [name for name, _ in results]
    assert "Lmulsnes" in names
    assert "Magnus Kongshem" in names
