import bottle
from bottle import route, Bottle, template, request, run, get, post, static_file, app, redirect
from beaker.middleware import SessionMiddleware
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
import httplib2
import requests
import os

# import helper function in recording keyword history
import kw_his

# Google client information
CLIENT_ID = '511198361373-6lm1dk6kii30500e6hli6ktnas214etf.apps.googleusercontent.com'
CLIENT_SECRET = 'P_JlHj5B1t8Fgc9TdANWDThL'
SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
REDIRECT_URI = 'http://localhost:8080/redirect'
REVOKE_URL = 'https://accounts.google.com/o/oauth2/revoke'

token = None

# configure beaker session
session_opts = {
    'session.type': 'cookie',
    'session.cookie_expires': False,
    'session.data_dir': './data',
    'session.auto': True
}

wsgi_app = SessionMiddleware(app(), session_opts)


# homepage of the site which will request user input search content
@get('/')
def index():
    # make a lazy session instance available every request request.environ.get
    ss = request.environ.get('beaker.session')
    ss_user = ss.get('user', None)
    print(ss.get('user', None))
    # Use get method to obtain user searched keywords
    keywords = request.query.get('keywords')
    if keywords is None or keywords is "":
        # Home Page
        return template("homepage.tpl", ss_user=ss_user, ss=ss)
    else:
        # Handle the form submission
        keywords = request.query.get('keywords')
        # Handle search keyword input
        results = kw_his.handle_input(keywords,ss_user,user_cookie)
        this_search,user_kw,top_20_list = results[0], results[1], results[2]
        # Store new user-based keyword dictionary
        ss[ss_user] = user_kw
        ss.save()
        # Return result page
        return template("homepage_search_result.tpl", keywords=keywords,
                        this_search=this_search,
                        ss=ss,
                        ss_user=ss_user,
                        top_20_list=kw_history.top_20_list,
                        user_kw_his=kw_history.user_kw_his)


# google login
@route('/login')
def google_login():
    ss = request.environ.get('beaker.session')

    print(ss.get('user', None))

    if ss.get('user', None) is None:
        # create flow from json and stores client id, client secret and other parameter
        flow = flow_from_clientsecrets(
            'client_secrets.json',
            scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
            redirect_uri='http://localhost:8080/redirect')
        # generate authorization server URI
        uri = flow.step1_get_authorize_url()
        # redirect to google sign in prompt
        redirect(str(uri))
    else:
        # already sign in
        redirect('/')


# redirect page
@route('/redirect')
def redirect_page():
    # retrieve one time code attached to query string after browser is redirected
    code = request.query.get("code", "")
    if code is "":
        redirect('/')
    # exchange one time code for access token by submitting http request
    flow = OAuth2WebServerFlow(client_id=CLIENT_ID,
                               scope=SCOPE,
                               client_secret=CLIENT_SECRET,
                               redirect_uri=REDIRECT_URI)
    # exchanges an authorization code for a Credentials
    credentials = flow.step2_exchange(code)

    # apply necessary credential headers to all requests made by an httplib2.Http instance
    http = httplib2.Http()
    http = credentials.authorize(http)

    global token
    # Set token as global for further use
    token = credentials.get_access_token(http).access_token

    print "The access token: ", token

    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()
    print (user_document)
    user_email = user_document['email']
    # store log in information in a beaker session
    ss = request.environ.get('beaker.session')
    ss['user'] = user_email
    ss['picture'] = user_document['picture']
    ss.save()
    # redirect back to home page
    redirect('/')


# log out
@route('/logout')
def log_out():
    ss = request.environ.get('beaker.session')
    # remove user sign in session from beaker
    ss.pop('user', None)
    ss.pop('picture', None)
    ss.save()
    try:
        response = requests.post(REVOKE_URL,
                                 params={'token': token},
                                 headers={'content-type': 'application/x-www-form-urlencoded'})
    except:
        print "Went wrong when getting response from REVOKE url"
    # redirect back to homepage
    redirect('/')

# import static file for logos/images
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.getcwd())


# run the created web page
if __name__ == '__main__':
    run(app=wsgi_app, port=8080, reloader=True)
