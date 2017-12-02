import bottle
from bottle import route, Bottle, template, request, run, get, post, static_file, app, redirect, error
from beaker.middleware import SessionMiddleware
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from module.Database import database
from autocorrect import spell
import httplib2
import requests
import os

# import helper function in recording keyword history
from module import kw_his

# Google client information
CLIENT_ID = '511198361373-6lm1dk6kii30500e6hli6ktnas214etf.apps.googleusercontent.com'
CLIENT_SECRET = 'P_JlHj5B1t8Fgc9TdANWDThL'
SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
TEST_HOST = 'localhost'
TEST_PORT = '8080'
LANUCH_HOST = '0.0.0.0'
LANUCH_PORT = '80'
# Redirect url to be changed if instance is to be relauched
REDIRECT_URI = '0.0.0.0:80/redirect'
REVOKE_URL = 'https://accounts.google.com/o/oauth2/revoke'

token = None

# Set the database to be global variable for ease of use
db = None

# configure beaker session
session_opts = {
    'session.type': 'file',
    'session.cookie_expires': False,
    'session.data_dir': './data',
    'session.auto': True
}

wsgi_app = SessionMiddleware(app(), session_opts)


def takeForth(elem):
    return elem[3]

# homepage of the site which will request user input search content
@get('/')
def index():
    # make a lazy session instance available every request request.environ.get
    ss = request.environ.get('beaker.session')
    ss_user = ss.get('user', None)

    # Use get method to obtain user searched keywords
    keywords = request.query.get('keywords')
    page = request.query.get('page')

    if page is None and (keywords is None or keywords is ""):
        ss.pop('query_string',None)
        ss.pop('keywords',None)
        # Home Page
        return template("view/homepage.html", ss_user=ss_user, ss=ss)
    else:
        # Handle the form submission
        keywords = request.query.get('keywords')
        splwords = keywords.split(' ')

        correction = False
        correctedwords = []
        for word in splwords:
            corrected = spell(word)
            if corrected != word:
                print corrected
                correction = True
            correctedwords.append(corrected)

        print correctedwords
        correctedKeywords = ' '.join(correctedwords)
        print correctedKeywords
        # acquire keyword history
        user_cookie = ss[ss_user] if ss_user in ss else kw_his.searchKW()

        # Handle search keyword input
        results = kw_his.handle_input(keywords,ss_user,user_cookie)
        this_search,user_kw,top_20_list = results[0], results[1], results[2]

        # Store new user-based keyword dictionary
        ss[ss_user] = user_kw
        ss.save()

        # Returns a list of tuple sorted by page ranks
        # tuple = ( url, title )
        urls = db.findRelatedPageRank(splwords[0])

        # if not urls:
        #     redirect("error_page.tpl")

        if page is None or page is "":
            page = 1
            query_string = "?keywords=" + keywords.replace(" ","+")
            ss['query_string'] = query_string

        corrected_string = "?keywords=" + correctedKeywords.replace(" ","+")
        ss['corrected_string'] = corrected_string
        page = int(page)

        if urls is not None:
            total_page = (len(urls) + 9)//10
        else:
            total_page = 0
              
        # Return result page
        return template("view/query_result.html", keywords=keywords,
                        this_search=this_search,
                        ss=ss,
                        ss_user=ss_user,
                        top_20_list=top_20_list,
                        user_kw=user_kw,
                        url = urls,
                        page = page,
                        correction = correction,
                        correctedKeywords = correctedKeywords,
                        total_page = total_page)




# google login
@route('/login')
def google_login():

    ss = request.environ.get('beaker.session')

    if ss.get('user', None) is None:
        # create flow from json and stores client id, client secret and other parameter
        flow = flow_from_clientsecrets(
                'client_secrets.json',
                scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                redirect_uri= REDIRECT_URI)
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

    # Get user email
    users_service = build('oauth2', 'v2', http=http)
    user_document = users_service.userinfo().get().execute()

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
        raise HttpError

    # redirect back to homepage
    redirect('/')

# import static file for logos/images
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

# # test error return page
# @route('/404')
# def error404():
#     return template("error_page.tpl")


# error page
@error(404)
def error404(error):
    return template("view/error_page.html")


# run the created web page
if __name__ == '__main__':
    print 'Initializing database'
    db = database()
    print 'Booting up web service'
    run(app=wsgi_app, host=LANUCH_HOST,port=LANUCH_PORT, reloader=True)
