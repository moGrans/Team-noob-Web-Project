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
        # store search result into result history
        keyword_history.parse_search_input(keywords)
        # aquire top 20 count in searched order
        keyword_history.top_20_keyword()
        # sort top 20 in order of count
        keyword_history.insertion_sort()
        # return result page
        return template("homepage_search_result.tpl", keywords = keywords, top_20_list = keyword_history.top_20_list, keyword_dict = keyword_history.keyword_dict, this_keyword_order = keyword_history.this_keyword_order)


# # response of the user input
# @post('/')
# def search_handler():
#     """Handle the form submission"""
#     search_string = request.forms.get('search_string')
#     # store search result into result history
#     keyword_history.parse_search_input(search_string)
#     # aquire top 20 count in searched order
#     keyword_history.top_20_keyword()
#     # return result page
#     return template("homepage_search_result.tpl", search_string = search_string, top_20_list = keyword_history.top_20_list, keyword_dict = keyword_history.keyword_dict)

# import static file for logo
@route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root=os.getcwd())

# @route('/images/<filename:re:.*\.png>')
# def send_image(filename):
#     return static_file(filename, root='/path/to/image/files', mimetype='image/png')

# run the created web page
if __name__ == '__main__':
	run(reloader = True)
