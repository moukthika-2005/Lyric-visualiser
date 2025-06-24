import streamlit as st
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Get your Genius token from secrets
GENIUS_API_TOKEN = st.secrets["GENIUS_API_TOKEN"]

def search_genius_song(query):
    headers = {"Authorization": f"Bearer {GENIUS_API_TOKEN}"}
    params = {"q": query}
    response = requests.get("https://api.genius.com/search", params=params, headers=headers)
    if response.status_code != 200:
        return None
    hits = response.json()["response"]["hits"]
    for hit in hits:
        if hit["result"]["primary_artist"]["name"].lower() == "taylor swift":
            return hit["result"]["url"]
    return None

def get_lyrics_from_url(song_url):
    page = requests.get(song_url)
    soup = BeautifulSoup(page.text, "html.parser")
    lyrics_div = soup.find("div", class_="Lyrics__Root-sc-1ynbvzw-0")
    if not lyrics_div:
        # fallback for older layout
        lyrics_div = soup.find("div", class_="lyrics")
    if lyrics_div:
        return lyrics_div.get_text(separator="\n").strip()
    return "Lyrics not found."

st.title("🎤 Taylor Swift Lyrics & WordCloud")

song_title = st.text_input("Enter a Taylor Swift song title")

if st.button("Get Lyrics"):
    with st.spinner("Searching and fetching lyrics..."):
        song_url = search_genius_song(song_title)
        if song_url:
            lyrics = get_lyrics_from_url(song_url)
            st.text_area("Lyrics", lyrics, height=400)

            # Word Cloud
            wordcloud = WordCloud(width=800, height=300, background_color="white").generate(lyrics)
            st.subheader("Word Cloud")
            fig, ax = plt.subplots()
            ax.imshow(wordcloud, interpolation="bilinear")
            ax.axis("off")
            st.pyplot(fig)
        else:
            st.error("Song not found or lyrics not available.")
