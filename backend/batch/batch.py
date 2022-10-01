import requests

from batch.parse_input import parse
from database.schemas import GameInformation

BASE_URL = "https://www.geoguessr.com/api/v3/results/scores/"
COOKIE_CONTENT = "devicetoken=8A0A21555D; snconsent=eyJwdWJsaXNoZXIiOjMsInZlbmRvciI6MywiZ2xDb25zZW50cyI6IiIsImN2Q29uc2VudHMiOnsiMSI6dHJ1ZSwiMiI6dHJ1ZX19.AngAJwArAC4ANwA9AEYAUwBZAF0AbAB1AHoAfACDAIcAiACPAJAAkwCVAJ8AogCnAKsAwADEAMoA0wDaAOQA5gDvAPEBAwEKARABHgEjATcBPQFCAUMBRgFHAVIBbwFzAYEBhQGKAY0BlwGdAZ8BqAGuAbQBuAG9AcEBxQHiAeYB6wHuAe8B9QH3AfkCCgILAhwCJgIvAjACOAI-AkACSAJLAk8C3QLhAukDEwMiAyMDMQM0AzUDPQNHA2ADYwNqA4MDiAOaA6MDqgPTA9UD2QPrBAAEAwQHBAkEEAQWBBsEHQQrBD0ERARHBEkESwRTBGcEbwR3BH0EgASKBI4EogSkBLEEtQS7BL8EygTLBM4E5AT0BPYE_AUEB…BHggEQBEAgABAAqEQgAI2AQUAFgYBAAKAaFijFAEIEhBkQERSmBARIkFBPZUIJQd6GmEIdZYAUGj_ioQESgBCsCISFg5DgiQEvFkgWYo3yAEYIUAolQqAAA.YAAAAAAAAKA; _ga_7YENZ2KY0B=GS1.1.1663400243.2.1.1663400289.0.0.0; _ga=GA1.2.394915699.1663183308; _ncfa=tUMDdCcVN0KaQWP%2BEqDnNlyOLgrSDjTLlV9wOx7Sx%2Fc%3DKqBt%2Fe2qGhyoRayYHDzOypmICYw5JzprQB3mTBDAmXCEFJ4F8kTv9dCEv8kPG53H; __stripe_mid=04dd7333-74f8-4a5c-9e4c-20f7399f1a63dd9875; _gid=GA1.2.1925714442.1663400243; _gat_UA-40205730-2=1; __stripe_sid=8066870d-1942-4dd2-bfa9-1f73bcaf62c4153630"


def import_data(game_information: GameInformation, db):
    url = BASE_URL + game_information.game_id
    res = requests.get(url, headers={
        "cookie": COOKIE_CONTENT.encode()})

    if res.status_code == 200:
        data = res.json()
        # game_information = {"game_id": game_information.game_id, "date": game_information.date}
        parse(data, game_information.dict(), db)
    else:
        raise Exception("Ble ikke noe henting av den urlen gitt")
