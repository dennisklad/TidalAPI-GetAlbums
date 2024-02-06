import tidalapi
import oauth_login
from colorama import Fore, Back, Style
import csv

session = oauth_login.get_tidalapi_session()

links = []
titles = []
artists = []
out = []

# Reading the input file
with open('Images.tsv', 'r') as fin:
    next(fin) # Skip first line
    for row in fin:
        links.append(row.split('\t')[1])
        artists.append(row.split('\t')[2])
        titles.append(row.split('\t')[3][:-1])

start = 0
end = 100

for link, title, artist in zip(links[start:end], titles[start:end], artists[start:end]):
    
    if link != "#N/A":
        print(Fore.RED + "Album already has a link." + Style.RESET_ALL + '\n')
        out.append(link + '\n')
        continue

    # If artist is specified look for the value in the search
    if len(artist) == 0 :
        print(Fore.RED + "No artist was specified." + Style.RESET_ALL + '\n')
        continue

    search = session.search('album', title, 50)

    # If no result is returned
    if len(search.albums) == 0 :
        print(Fore.RED + "Could not find " + title + Style.RESET_ALL + '\n')
        continue

    print(f"\nLooking for album {title} by {artist} ...")
    #print(f"Album{'':30} Artist")

    found = False

    for alb in search.albums:
        result = session.get_album(alb.id)
        #print(f"{result.name:30} {result.artist.name}")
        #print(f"{artist.lower()}, {result.artist.name.lower()} | {title.lower()}, {result.name.lower()}")

        if artist.lower() in result.artist.name.lower() and title.lower() in result.name.lower():
            print(Fore.GREEN + "FOUND" + Style.RESET_ALL)
            out.append('="Image("' + result.picture(1280,1280) + '")\n')
            found = True
            continue
    
    if not found:
        out.append('NOT FOUND!')

    print("---------------------------------\n")
    # print(search.albums)

# Write output csv file
with open('Images_out.txt', 'w') as fout:
    fout.write(''.join(i for i in out))