import os

TEST_HTML = os.path.join(os.path.dirname(__file__), "../test_data/test.html")


def _upload_game(client, date="2023-01-01"):
    with open(TEST_HTML, "rb") as f:
        return client.post(
            "/new-game/",
            files={"file": ("test.html", f.read(), "text/html")},
            data={"date": date},
        )


# ---------------------------------------------------------------------------
# GET /players
# ---------------------------------------------------------------------------

def test_get_players_empty(client):
    response = client.get("/players")
    assert response.status_code == 200
    assert response.json() == []


def test_get_players_after_new_game(client):
    _upload_game(client)

    response = client.get("/players")
    assert response.status_code == 200
    players = response.json()
    assert len(players) > 0
    assert all("id" in p and "name" in p for p in players)


# ---------------------------------------------------------------------------
# GET /players/{player_id}
# ---------------------------------------------------------------------------

def test_get_player_by_id(client):
    _upload_game(client)

    players = client.get("/players").json()
    first_id = players[0]["id"]

    response = client.get(f"/players/{first_id}")
    assert response.status_code == 200
    assert response.json()["id"] == first_id


def test_get_player_by_id_not_found(client):
    response = client.get("/players/99999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# GET /leaderboard/
# ---------------------------------------------------------------------------

def test_get_leaderboard_empty(client):
    response = client.get("/leaderboard/")
    assert response.status_code == 200
    assert response.json() == {"players": []}


def test_get_leaderboard_after_new_game(client):
    _upload_game(client)

    response = client.get("/leaderboard/")
    assert response.status_code == 200
    data = response.json()
    assert len(data["players"]) > 0

    for player in data["players"]:
        assert "name" in player
        assert "points" in player
        assert "games" in player
        assert len(player["games"]) > 0


def test_leaderboard_sorted_by_points_descending(client):
    _upload_game(client)

    data = client.get("/leaderboard/").json()
    points = [p["points"] for p in data["players"]]
    assert points == sorted(points, reverse=True)


def test_leaderboard_game_fields(client):
    _upload_game(client)

    data = client.get("/leaderboard/").json()
    game = data["players"][0]["games"][0]
    assert "id" in game
    assert "map_name" in game
    assert "points" in game
    assert "date" in game


# ---------------------------------------------------------------------------
# POST /new-game/
# ---------------------------------------------------------------------------

def test_post_new_game(client):
    response = _upload_game(client)
    assert response.status_code == 200


def test_post_new_game_idempotent(client):
    """Uploading the same game twice should not create duplicate players/scores."""
    _upload_game(client)
    _upload_game(client)

    data = client.get("/leaderboard/").json()
    # Each player should still have exactly one game entry
    for player in data["players"]:
        assert len(player["games"]) == 1


def test_post_new_game_returns_filename(client):
    response = _upload_game(client)
    body = response.json()
    assert "filename" in body


# ---------------------------------------------------------------------------
# DELETE /delete-game/{game_id}
# ---------------------------------------------------------------------------

def test_delete_game(client):
    _upload_game(client)

    lb = client.get("/leaderboard/").json()
    game_id = lb["players"][0]["games"][0]["id"]

    response = client.delete(f"/delete-game/{game_id}")
    assert response.status_code == 200


def test_delete_game_removes_from_leaderboard(client):
    _upload_game(client)

    lb = client.get("/leaderboard/").json()
    game_id = lb["players"][0]["games"][0]["id"]

    client.delete(f"/delete-game/{game_id}")

    lb_after = client.get("/leaderboard/").json()
    all_game_ids = [g["id"] for p in lb_after["players"] for g in p["games"]]
    assert game_id not in all_game_ids


def test_delete_game_removes_playerless_players(client):
    """Players whose only game is deleted should be removed from the leaderboard."""
    _upload_game(client)

    lb = client.get("/leaderboard/").json()
    game_id = lb["players"][0]["games"][0]["id"]

    client.delete(f"/delete-game/{game_id}")

    lb_after = client.get("/leaderboard/").json()
    # All remaining players should have at least one game
    for player in lb_after["players"]:
        assert len(player["games"]) > 0
