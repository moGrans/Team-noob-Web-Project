from bottle import route, template, request, run

# global variable
keyword_dict = {}
top_20_dict = {}
# homepage of the site which will request user input search content
@route('/')
def index():
    """Home Page"""
    return template("homepage.tpl") 

# response of the user input
@route('/', method="POST")
def search_handler():
    """Handle the form submission"""
    search_string = request.forms.get('search_string')
    parse_search_input(search_string)
    top_20_keyword()
    return template("homepage_search_result.tpl", search_string = search_string, top_20_dict = top_20_dict)


def parse_search_input(search_string):
	#break the string into list of word and record to total_keywords
	search_keywords = search_string.split()

	#find number of times each keyword being searched
	for word in search_keywords:
		if word not in keyword_dict:
			keyword_dict[word] = 1
		else:
			keyword_dict[word] += 1


def top_20_keyword():
	# delete old result
	top_20_dict.clear()
	# loop through all keyword since launched
	for word,count in keyword_dict.items():
		if len(top_20_dict) < 20:
			# display all searched keyword if keyword does not exceed 20
			top_20_dict[word] = count
		else:
			# find minimum key value in top 20 list
			# compare with the current count value
			# delete and replace with new frequent value
			min_index = min(top_20_dict, key=top_20_dict.get)
			if top_20_dict[min_index] < count:
				del top_20_dict[min_index]
				top_20_dict[word] = count

# run the created web page
if __name__ == '__main__':
	run(reloader = True)