import tidalapi
import oauth_login
from colorama import Fore, Back, Style

session = oauth_login.get_tidalapi_session()
albums = tidalapi.Favorites(session, session.user.id).albums()


def find_album_from_title(title, artist):
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
        print(Fore.RED + "Could not find " + title + Style.RESET_ALL + "\n")
        return None
    
    # If artist is not specified
    if not artist:
        print(Fore.RED + "No artist provided. Returning first output." + Style.RESET_ALL + "\n")
        return search.albums[0]
    
    print(f"\nLooking for album {title} by {artist} ...")
    print(f"{'Album':30} Artist")

    for alb in search.albums:
        result = session.get_album(alb.id)
        print(f"{result.name:30} {result.artist.name}")

        if artist.lower() == result.artist.name.lower() and title.lower() == result.name.lower() :
            print(Fore.GREEN + "FOUND" + Style.RESET_ALL + "\n")
            return result
        
    print(Fore.RED + "Unable to find :(" + Style.RESET_ALL + "\n")
    return None


def cover_formula(album_object):
    """
    Creates the formula used in Excel for the album cover.

    Params:
        album_object [tidalapi.models.Album]
    
    Return:
        A string representing the Image formala of the album cover
    """
    if album_object:
        return f'=Image("{album_object.picture(1280,1280)}")\n'


def write_album_image(album_objects):
    '''
    Writes the formula for the album cover of each album class object to the file.

    Params:
        album_objects [list<tidalapi.models.Album>]: A list of the album objects.

    Return:
        Output is in the `../output/image_links.txt` file
    '''

    print("\nWritting image cover link in `../output/image_links.txt`...")
    
    with open("../output/image_links.txt", 'w') as f:
        
        data = ''
        for album in album_objects:
            try:
                data += cover_formula(album)

            except AssertionError:
                data += 'Image was not found!\n'

        print(data)
        f.write(data)


if __name__ == '__main__':
    while(True):
        list_art = input("Enter Artist:\n").lower()
        list_alb = input("Enter Album:\n").lower()

        #write_album_image(find_albums_from_title(list_alb, list_art))
        obj = find_album_from_title(list_alb, list_art)
        print(cover_formula(obj))