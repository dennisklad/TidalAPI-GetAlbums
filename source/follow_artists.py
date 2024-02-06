import tidalapi
import oauth_login

session = oauth_login.get_tidalapi_session()

fav         = tidalapi.Favorites(session, session.user.id)
fav_albums  = fav.albums()
fav_artists = fav.artists()

artists_from_fav_albums = []
artist_names = []

for album in fav_albums:
    [artists_from_fav_albums.append(artist) for artist in album.artists]

for artist in fav_artists:
    artist_names.append(artist.name)

for artist in artists_from_fav_albums:
    # print("Checking if you follow", artist.name)
    
    if not artist.name in artist_names:
        print("You are now following", artist.name)
        fav.add_artist(artist.id)
        
# print(f"{album:80} by {artist}")