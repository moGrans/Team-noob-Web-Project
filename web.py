# import bottle
from bottle import route, template, request, run, get, post, static_file
# import helper function in recording keyword history
import keyword_history

# homepage of the site which will request user input search content
@get('/')
def index():
    """Home Page"""
    return template("homepage.tpl") 

# response of the user input
@post('/')
def search_handler():
    """Handle the form submission"""
    search_string = request.forms.get('search_string')
    # store search result into result history
    keyword_history.parse_search_input(search_string)
    # aquire top 20 count in searched order
    keyword_history.top_20_keyword()
    # return result page
    return template("homepage_search_result.tpl", search_string = search_string, top_20_list = keyword_history.top_20_list, keyword_dict = keyword_history.keyword_dict)

# import static file for logo
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='/Users/melissapan/Documents/CSC326/Lab1')

# @route('/images/<filename:re:.*\.png>')
# def send_image(filename):
#     return static_file(filename, root='/path/to/image/files', mimetype='image/png')
    
# run the created web page
if __name__ == '__main__':
	run(reloader = True)
