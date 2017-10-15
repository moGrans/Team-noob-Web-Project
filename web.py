import bottle
from bottle import route, Bottle, template, request, run, get, post, static_file, app, redirect
from beaker.middleware import SessionMiddleware
from oauth2client import client
from oauth2client.client import OAuth2WebServerFlow
from oauth2client.client import flow_from_clientsecrets
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from beaker.middleware import SessionMiddleware
import httplib2

# import helper function in recording keyword history
import keyword_history
import os

CLIENT_ID = '511198361373-6lm1dk6kii30500e6hli6ktnas214etf.apps.googleusercontent.com'
CLIENT_SECRET = 'P_JlHj5B1t8Fgc9TdANWDThL'
SCOPE = 'https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email'
REDIRECT_URI = 'http://localhost:8080/redirect'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 86400,
    'session.data_dir': './data',
    'session.auto': True
}
wsgi_app = SessionMiddleware(app(), session_opts)

# homepage of the site which will request user input search content
@get('/')
def index():
    ss = request.environ.get('beaker.session')
    print(ss.get('user', None))
    keywords = request.query.get('keywords')
    if keywords == None or keywords == "":
        """Home Page"""
        return template("homepage.tpl")
    else:
        """Handle the form submission"""
        keywords = request.query.get('keywords')
        # handle search keyword input
        keyword_history.handle_input(keywords)
        # return result page
        return template("homepage_search_result.tpl", keywords = keywords, top_20_list = keyword_history.top_20_list, keyword_dict = keyword_history.keyword_dict, this_keyword_order = keyword_history.this_keyword_order, this_keyword_dict = keyword_history.this_keyword_dict)

# google login
@route('/login')
def google_login():
        ss = request.environ.get('beaker.session')
        print(ss.get('user', None))
        if ss.get('user', None) is None:
            flow = flow_from_clientsecrets(
                    'client_secrets.json',
                    scope='https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/userinfo.email',
                    redirect_uri='http://localhost:8080/redirect')
            uri = flow.step1_get_authorize_url()
            redirect(str(uri))
        else:
            redirect('/')

# redirect page
@route('/redirect')
def redirect_page():
    code = request.query.get("code", "")
    if code == "":
		redirect('/')
    flow = OAuth2WebServerFlow(client_id = CLIENT_ID,
        client_secret = CLIENT_SECRET,
        scope = SCOPE,
        redirect_uri = REDIRECT_URI)
    credentials = flow.step2_exchange(code)
    token = credentials.id_token['sub']
    http = httplib2.Http()
    http = credentials.authorize(http)
    # Get user email
    users_service = build('oauth2', 'v2', http = http)
    user_document = users_service.userinfo().get().execute()
    user_email = user_document['email']

    ss = request.environ.get('beaker.session')
    ss['user'] = user_email
    ss.save()
    redirect('/')

# log out
@route('/logout')
def log_out():
    ss = request.environ.get('beaker.session')
    ss.pop('user', None)
    ss.save()
    redirect('/')


# import static file for logo
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.getcwd())

# run the created web page
if __name__ == '__main__':
	run(app = wsgi_app, port = 8080, reloader = True)
