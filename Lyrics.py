import requests
import urllib.parse

# Enter your Musixmatch API key here
api_key = "YOUR API_KEY"

def identify_song(lyrics):
    # Clean and preprocess the lyrics
    lyrics = lyrics.lower()
    lyrics = "".join(c for c in lyrics if c.isalnum() or c.isspace())
    lyrics = urllib.parse.quote(lyrics)

    # Query the Musixmatch API to search for a track with the given lyrics
    url = f"https://api.musixmatch.com/ws/1.1/track.search?q_lyrics={lyrics}&f_artist_name=&f_album_name=&page_size=1&page=1&s_track_rating=desc&apikey={api_key}"
    response = requests.get(url).json()

    # Check if the API returned any search results
    if response['message']['header']['status_code'] != 200 or response['message']['body']['track_list'] == []:
        return "Sorry, we could not find a match for those lyrics."

    # Extract the first search result (most likely match) and return its details
    track = response['message']['body']['track_list'][0]['track']
    track_name = track['track_name']
    artist_name = track['artist_name']
    album_name = track['album_name']

    # Retrieve additional information about the identified song
    track_id = track['track_id']
    url = f"https://api.musixmatch.com/ws/1.1/track.get?track_id={track_id}&apikey={api_key}"
    response = requests.get(url).json()
    if response['message']['header']['status_code'] == 200:
        track_info = response['message']['body']['track']
        genre_name = track_info['primary_genres']['music_genre_list'][0]['music_genre']['music_genre_name']
        popularity = track_info['track_rating']
        release_date = track_info.get('first_release_date', 'unknown')

        return f"We found a match! The song is '{track_name}' by {artist_name}, from the album '{album_name}'.\nIt's a {genre_name} song released on {release_date} and has a popularity rating of {popularity}."
    else:
        return f"We found a match! The song is '{track_name}' by {artist_name}, from the album '{album_name}'."
# Example usage
lyrics = "We're up all night to get lucky"
print(identify_song(lyrics))
