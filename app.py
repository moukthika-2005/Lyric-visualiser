import streamlit as st
import lyricsgenius
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# Genius API
genius = lyricsgenius.Genius(st.secrets["GENIUS_API_TOKEN"],timeout=15)
genius.skip_non_songs = True
genius.excluded_terms = ["(Remix)", "(Live)"]

# Streamlit App
st.title("🎤 Taylor Swift Lyrics Explorer")

song_title = st.text_input("Enter a Taylor Swift song title")
def clean_lyrics(raw_lyrics):
    # Find the first [Verse ...] or [Intro] or similar section
    match = re.search(r"\[.*?\]", raw_lyrics)
    if match:
        start_index = match.start()
        return raw_lyrics[start_index:].strip()
    return raw_lyrics.strip()  # fallback if no section headings found
if st.button("Get Lyrics"):
    with st.spinner("Fetching lyrics..."):
        try:
            song = genius.search_song(song_title, artist="Taylor Swift")
            if song:
                lyrics = clean_lyrics(song.lyrics)
                st.subheader("Lyrics for: " + song.title)
                st.text_area("Lyrics", lyrics, height=400)


                # Generate word cloud
                wordcloud = WordCloud(width=800, height=400, background_color="white").generate(song.lyrics)
                st.subheader("Word Cloud")
                fig, ax = plt.subplots()
                ax.imshow(wordcloud, interpolation="bilinear")
                ax.axis("off")
                st.pyplot(fig)
            else:
                st.error("Song not found.")
        except Exception as e:
            st.error(f"Error: {e}")
