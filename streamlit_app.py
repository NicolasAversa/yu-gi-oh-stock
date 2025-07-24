import streamlit as st
import pandas as pd
from lib.yu_gi_oh_editor import get_all_decks, get_all_cards_dataframe

cards_df = get_all_cards_dataframe()
all_decks = get_all_decks()


character_options = sorted([key.capitalize() for key in all_decks.keys()])
selected_character = st.selectbox("Select a character", character_options)

character_deck_dfs = all_decks[selected_character.lower()]
sorted_deck_numbers = sorted(character_deck_dfs.keys(), key=lambda x: int(x))

deduplicated_decks = []
seen_ids = set()

for deck_number in sorted_deck_numbers:
    deck_df = character_deck_dfs[deck_number]
    filtered_df = deck_df[~deck_df["id"].isin(seen_ids)].copy()
    deduplicated_decks.append((deck_number, filtered_df))
    seen_ids.update(filtered_df["id"].tolist())

for deck_number, deck_df in deduplicated_decks:
    st.write(f"Deck {deck_number}")
    merged_deck_df = pd.merge(how="left", left=deck_df, right=cards_df, on="id")
    merged_deck_sorted_df = merged_deck_df.sort_values(
        by=["type", "race", "atk", "def", "id"], ascending=[True, True, False, False, True]
    ).reset_index(drop=True)
    st.dataframe(merged_deck_sorted_df, column_config={"url": st.column_config.LinkColumn()})
