import tidalapi
import oauth_login

from colorama import Fore, Back, Style

session = oauth_login.get_tidalapi_session()

albums = tidalapi.Favorites(session, session.user.id).albums()

def find_album_from_title(title, artist=[]):
    '''
    Find the Tidal Album Object from a list of album titles.

    Params:
        titles [list]: A list of strings representing the titles of the albums.
        artists [list]: An optional list of string representing the artist of the album.

    Return:
        A list of album class objects.
    '''
    
    search = session.search('album', title, 100)
    
    # If no result is returned
    if len(search.albums) == 0 :
        print(Fore.RED + "Could not find " + title + Style.RESET_ALL)
        print()
        return
    
    # If artist is specified look for the value in the search
    if len(artist) != 0 :
        
        print(f"\nLooking for album {title} by {artist} ...")
        print(f"Album{'':30} Artist")

        for alb in search.albums:
            result = session.get_album(alb.id)
            print(f"{result.name:30} {result.artist.name}")

            if artist == result.artist.name.lower() and title == result.name.lower() :
                print(Fore.GREEN + "FOUND" + Style.RESET_ALL)
                print('"=""Image("' + result.picture(1280,1280) + '")\n')
                return
        
        print("---------------------------------\n")
        # print(search.albums)

    # If no artist is specified then take the first result
    else:
        print("Try again...")
        
    


def get_album_image(fav_albums=albums):
    '''
    Writes the link for the album cover of each album class object to the file.

    Params:
        fav_albums [list]: A list of album class objects. Default is the favorite album library.

    Return:
        Output is in the `image_links.txt` file
    '''

    print("Writting image cover link in `image_links.txt`...")
    
    with open("./image_links.txt",'w') as f:
        
        data = ''
        for a in fav_albums:
            data += '"=""Image("' + a.picture(1280,1280) + '")\n'
        f.write(data)


# list_art = """Psychedelic Porn Crumpets""".split('\n')
# list_alb = """And Now for the Whatchamacallit""".split('\n')

while(True):
    list_art = input("Enter Artist:\n").lower()
    list_alb = input("Enter Album:\n").lower()

    #get_album_image(find_albums_from_title(list_alb, list_art))
    find_album_from_title(list_alb, list_art)