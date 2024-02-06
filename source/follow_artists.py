import tidalapi
import oauth_login

session = oauth_login.get_tidalapi_session()

fav = tidalapi.Favorites(session, session.user.id)

# Artists already saved in favorites
fav_artists = [artist.name for artist in fav.artists()]

# Artists from favorite albums
artists_from_fav_albums = []
for album in fav.albums():
    for artist in album.artists:
        artists_from_fav_albums.append(artist)

# Favorite artists from albums that are not in favorites
for artist in artists_from_fav_albums:
    # Checking if you follow artist
    if not artist.name in fav_artists:
        print("You are now following", artist.name)
        fav.add_artist(artist.id)