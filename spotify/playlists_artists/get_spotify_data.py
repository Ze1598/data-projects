from os import environ
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from typing import List, Dict
# https://github.com/plamere/spotipy/blob/master/examples/playlist_tracks.py


def authenticate(cliend_id: str, client_secret: str) -> spotipy.client.Spotify:
    """
    Authenticate to Spotify.
    """
    sp = spotipy.Spotify(
        client_credentials_manager=SpotifyClientCredentials(
            client_id=cliend_id,
            client_secret=client_secret
        )
    )

    return sp


def get_pl_length(sp: spotipy.client.Spotify, pl_uri: str) -> int:
    """
    Get the number of tracks available in the playlist (local files included).
    """
    return sp.playlist_tracks(
        pl_uri,
        offset=0,
        fields="total"
    )["total"]


def get_tracks_artist_info(sp: spotipy.client.Spotify, pl_uri: str) -> List[List[Dict]]:
    """
    Get all the artist info about each track of the playlist.

    From the retrieved data for each track, the portion about the artists
    is a list of dictionaries, one dictionary per track artist. 
    Thus, each element of the list returned by this function is itself a
    list of dictionatires.
    """
    # List for each track's artist info
    artists_info = list()
    # Start retrieving tracks from the beginning of the playlist
    offset = 0
    # Number of tracks in the playlist
    pl_length = get_pl_length(sp, pl_uri)

    # It's only possible to get a maximum of 100 tracks at once, so repeat the\
    # retrieval until we reach a request where we try to retrieve tracks after\
    # the last existing one
    while offset != pl_length:
        # Get the next batch of tracks
        pl_tracks = sp.playlist_tracks(
            pl_uri,
            offset=offset,
            fields="items.track"
        )

        # Get the list with the info about the artists of each track from the\
        # latest batch and append it to the running list
        [artists_info.append(pl_item["track"]["artists"])
            for pl_item in pl_tracks["items"]]

        # Update the offset according to the length of the latest batch
        offset += len(pl_tracks["items"])

    return artists_info


def get_artist_counts(artists_info: List[List[Dict]]) -> Dict[str, int]:
    """
    Find the frequency of each artist featured in the playlist and return
    a dictionary of the type Artist:Frequency.
    """
    # Frequency of each artist featured in the playlist
    artist_counts = dict()

    # Loop through the lists of artist information
    for track_artists in artists_info:
        # Loop through the artists associated with the current track
        for artist in track_artists:
            # Update the current artist's frequency count
            artist_name = artist["name"]
            if artist_name in artist_counts:
                artist_counts[artist_name] += 1
            else:
                artist_counts[artist_name] = 1

    return artist_counts


def save_artists_csv(artists_counts: Dict[str, int]) -> None:
    """
    Given a dictionary with the frequencies of each artist, create a
    DataFrame for that information and save it as a CSV file.
    """
    # Get a list of the artists featured in the playlist
    artists = list(artists_counts.keys())
    # Get a list of the frequencies of each artist
    frequencies = [freq for artist, freq in artists_counts.items()]
    # Create a dictionary for the dataframe
    data = {
        "Artist": artists,
        "Frequency": frequencies
    }
    # Create the dataframe and save it as CSV (without indices)
    new_df = pd.DataFrame(data=data)
    new_df.to_csv("artists_frequencies.csv", index=False)


if __name__ == "__main__":
    # Get the credentials from environment variables
    CLIENT_ID = environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = environ.get("SPOTIFY_CLIENT_SECRET")
    # Get a Spotify authenticated instance
    sp_instance = authenticate(CLIENT_ID, CLIENT_SECRET)

    # Playlist URI to look up
    # screams
    # pl_uri = "spotify:playlist:5Sh8nu5uSaHpkf2gwtcqFi"
    # good music
    pl_uri = "spotify:playlist:7bLzIyyGRUJw78eHtUZItf"

    # Get the artist information for all tracks of the playlist
    artists_info = get_tracks_artist_info(sp_instance, pl_uri)

    # Get the frequencies of each artist
    artists_counts = get_artist_counts(artists_info)

    # Save the artist frequencies in a CSV
    save_artists_csv(artists_counts)
