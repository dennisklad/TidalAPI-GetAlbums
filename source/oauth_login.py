import tidalapi
import csv

def get_tidalapi_session():
    
    session = tidalapi.Session()

    with open('oauth_logins.csv', mode='r+') as f:
        
        reader = csv.reader(f)
        logins = [row[0] for row in reader]
        
        session_id    = str(logins[0])
        access_token  = str(logins[1])
        refresh_token = str(logins[2])
        token_type    = str(logins[3])
        
    try:
        session.load_oauth_session(session_id, token_type, access_token, refresh_token)
        
        #print("Testing oauth logins...")
        tidalapi.Favorites(session, session.user.id).albums()[0].name
        #print("All good!\n")
        
    except Exception:
        # Will run until you visit the printed url and link your account
        session.login_oauth_simple()

        print('Here are the OAuth logins:\n')
        print('\nSession_id:   \n' + session.session_id)
        print('\nAccess_token: \n' + session.access_token)
        print('\nRefresh token:\n' + session.refresh_token)
        print('\nToken_type:   \n' + session.token_type)
        
        print('Saving the OAUTH logins in `oauth_logins.csv`. Keep this file secure!')

        with open('oauth_logins.csv', mode='w') as f:
            writer = csv.writer(f)
            writer.writerows([[session.session_id], [session.access_token], [session.refresh_token], [session.token_type]])
                
    return session