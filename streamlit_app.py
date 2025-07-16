import streamlit as st
from lib.yu_gi_oh_editor import create_cards_dataset, read_card_dataset, all_decks
import pandas as pd

cards = read_card_dataset()
cards_df = create_cards_dataset(cards)

decks_options = sorted(all_decks.keys())

selected_deck = st.selectbox(label="Select your deck", options=decks_options)
selected_deck_df = all_decks[selected_deck]
merged_deck_df = pd.merge(how="left", left=selected_deck_df, right=cards_df, on="id")

merged_deck_sorted_df = merged_deck_df.sort_values(
    by=["type", "id"], ascending=[True, True]
).reset_index(drop=True)

st.dataframe(merged_deck_sorted_df)
