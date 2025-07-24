from collections import defaultdict
import json
import pandas as pd
import os

CARD_JSON_FILE_PATH = "data/cardinfo.json"


def get_all_cards_dataframe() -> pd.DataFrame:
    with open(CARD_JSON_FILE_PATH, "r") as f:
        data = json.load(f)
    card_dataset_json = data["data"]
    cards = [
        {
            "id": card["id"],
            "name": card["name"],
            "type": card["type"],
            "desc": card["desc"],
            "race": card["race"],
            "url": card["ygoprodeck_url"],
            "atk": card.get("atk", 0),
            "def": card.get("def", 0),
        }
        for card in card_dataset_json
    ]
    return pd.DataFrame(cards)


def parse_deck_file(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as f:
        ids = [int(line.strip()) for line in f if line.strip().isdigit()]
    return pd.DataFrame(ids, columns=["id"])


DECKS_PATH = "data/decks"


def get_all_decks():
    all_decks = defaultdict(dict)
    for filename in os.listdir(DECKS_PATH):
        if filename.endswith(".ydk"):
            deck_name = os.path.splitext(filename)[0]
            if "_" in deck_name:
                character, deck_number = deck_name.split("_", 1)
                deck_path = os.path.join(DECKS_PATH, filename)
                all_decks[character][deck_number] = parse_deck_file(deck_path)
    return all_decks
