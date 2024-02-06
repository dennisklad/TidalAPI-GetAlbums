import tidalapi
import xlsxwriter
import datetime
import pandas as pd
import oauth_login
import os

from get_album_cover import find_album_from_title, write_album_image
from requests.sessions import session
from colorama import Fore, Back, Style

PATH_ALBUMS = "../albums/"
session = oauth_login.get_tidalapi_session()
albums = tidalapi.Favorites(session, session.user.id).albums()


def write_tidal_albums():
    #Open File to write
    out_workbook = xlsxwriter.Workbook(PATH_ALBUMS+'albums'+str(datetime.datetime.now())[:10]+'.xlsx')
    out_sheet = out_workbook.add_worksheet('albums')
    
    #Create headers
    [out_sheet.write(0, idx, data) for idx, data in enumerate(["Artist","Title","Release","Tracks","Duration"])]
    
    #Write data to file
    for row_num in range(len(albums)):
        out_sheet.write(row_num+1, 0, ' & '.join([str(artist.name) for artist in albums[row_num].artists]))
        out_sheet.write(row_num+1, 1, albums[row_num].name)
        out_sheet.write(row_num+1, 2, albums[row_num].release_date.year)
        out_sheet.write(row_num+1, 3, albums[row_num].num_tracks)
        out_sheet.write(row_num+1, 4, int(albums[row_num].duration/60))
        
    out_workbook.close()


def compare_new_albums():
    
    #Compare new rows that were added in the latest iteration
    files = os.listdir(PATH_ALBUMS)
    dfnew, dfold = pd.read_excel(PATH_ALBUMS + files[len(files)-1]), pd.read_excel(PATH_ALBUMS + files[len(files)-2])
    merged = dfnew.append(dfold)
    merged = merged.drop_duplicates(keep=False).sort_index()
    merged_add = pd.DataFrame({'Artist':[],'Title':[],'Release':[],'Tracks':[],'Duration':[]})
    merged_rem = pd.DataFrame({'Artist':[],'Title':[],'Release':[],'Tracks':[],'Duration':[]})
    
    album_titles  = []
    album_artists = []
    
    for idx in range(len(merged)):
        it_album_title = merged.iloc[idx,1]
        it_album_art   = merged.iloc[idx,0]
        is_in_old = len(dfold.loc[dfold['Title']==it_album_title]) > 0
        is_in_new = len(dfnew.loc[dfnew['Title']==it_album_title]) > 0
        
        #If the album is included in both then it was a mistake.
        if is_in_new and is_in_old:
            #print(idx, it_album_title,'was removed and added again.')
            continue
        
        #If the album is included only in the new excel then it was added.
        elif is_in_new:
            album_titles.append(it_album_title)
            album_artists.append(it_album_art)
            print(Fore.GREEN + it_album_title,'was added.' + Style.RESET_ALL)
            merged_add.loc[len(merged_add.index)] = merged.iloc[idx]       
        
        #If the album is included only in the old excel then it was removed.
        elif is_in_old:
            print(Fore.RED + it_album_title,'was removed.' + Style.RESET_ALL)
            merged_rem.loc[len(merged_rem.index)] = merged.iloc[idx]

    out = []
    for title, artist in zip(album_titles, album_artists):    
        out.append(find_album_from_title(title, artist))
    
    write_album_image(out)

    merged_add.to_excel("../output/unique_added.xlsx")
    merged_rem.to_excel("../output/unique_removed.xlsx")

    #Print values to console
    print(f"\nNew file {files[len(files)-1]} has {len(dfnew)} rows.   \
        \nOld file {files[len(files)-2]} has {len(dfold)} rows.       \
        \nYou added {len(merged_add)} albums since the last update.   \
        \nYou removed {len(merged_rem)} albums since the last update.\n")


if __name__ == '__main__':
    # Call functions
    write_tidal_albums()
    compare_new_albums()