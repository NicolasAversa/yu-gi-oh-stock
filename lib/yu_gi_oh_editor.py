import json
import streamlit as st
import pandas as pd
import os

CARD_JSON_FILE_PATH = "data/cardinfo.json"


def read_card_dataset():
    with open(CARD_JSON_FILE_PATH, "r") as f:
        data = json.load(f)
    final_data = data["data"]
    return final_data


def create_cards_dataset(card_json) -> pd.DataFrame:
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
        for card in card_json
    ]
    cards_df = pd.DataFrame(cards)
    # st.dataframe(cards_df)
    return cards_df


def parse_deck_file(file_path: str) -> pd.DataFrame:
    with open(file_path, "r") as f:
        ids = [int(line.strip()) for line in f if line.strip().isdigit()]

    return pd.DataFrame(ids, columns=["id"])


DECKS_PATH = "data/decks"

""" def get_decks_by_stock_generation"""
all_decks = {
    os.path.splitext(filename)[0]: parse_deck_file(os.path.join(DECKS_PATH, filename))
    for filename in os.listdir(DECKS_PATH)
    if filename.endswith(".ydk")
}
