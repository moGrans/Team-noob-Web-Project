# import bottle
from bottle import route, template, request, run, get, post, static_file
# import helper function in recording keyword history
import keyword_history
import os

# homepage of the site which will request user input search content
@get('/')
def index():
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

# import static file for logo
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.getcwd())

# run the created web page
if __name__ == '__main__':
	run(reloader = True)
