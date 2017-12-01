import operator

#
# Class Definition
#
class searchKW:
	""" this class stores information of a single search 
			kw_order: a list variable that store keyword by search order
			kw_dict: a dictionary variable that store keyword with cooresponding search count

		defined function:
		__init__: initialize by one single search string
		__add__: add self with another searchKW, use to add in NEW keyword (other) to HISTORY keyword (self)
		__exit__: empty/clear list and dict
	"""

	# constructor with searched string
	def __init__(self, search_string = ""):
		#self.search_string = search_string.lower().split()		# store searched string using list by keyword in lower case
		search_string = search_string.lower().split()
		self.kw_order = []
		self.kw_dict = {}
		self.login = False	
		self.recent = []								
		# search keyword count dictionary initialization
		for word in search_string:
			if word not in self.kw_dict:
				# add new keyword into dictionary with count of 1
				self.kw_dict[word] = 1
				# add new keyword into list
				self.kw_order.append(word)
			else:
				# increment search count in dictionary
				self.kw_dict[word] += 1
		search_string.reverse()
		self.recent = search_string[:10]
		print "recent edit in __init__: self.recent = ",self.recent
			

	# add keywords from new search
	def __add__(self,other):		
		for word in other.kw_order:
			# new keyword
			if word not in self.kw_order:
				# add to dictionary with search count in other
				self.kw_dict[word] = other.kw_dict[word]
				# add to list
				self.kw_order.append(word)
			# key already exists in previous search
			else:
				# update count
				self.kw_dict[word] = self.kw_dict[word] + other.kw_dict[word]
		# update recent word list
		recent = other.recent + self.recent
		self.recent = recent[:10]
		print "recent edit in __add__: self.recent = ",self.recent
		return self

	# destructure to clear up variables
	def __exit__(self):
		#self.search_string[:] = []
		self.kw_order[:] = []
		self.kw_dict.clear()
		self.recent[:] = []

#
# Function Implementation
#

# handle raw search string from get method
def handle_input(search_string,ss_user,user_cookie):
	# store search result into result history
    this_search = searchKW(search_string)
    # user did not log in will not display and store keyword history
    if ss_user is None:
    	return [this_search,searchKW(),[]]
    # user id already exist, add new search to previous search history
    user_kw = user_cookie + this_search
    # sort top 20 in order of count
    top_20_list = sort_rankings(user_kw)

    # return the search parse for this specific search
    return [this_search,user_kw,top_20_list]


# insertion_sort the top 20 keyword by count
def sort_rankings(user_kw):
	# user specific
	kdict = user_kw.kw_dict

	result = sorted(kdict, key=kdict.__getitem__)
	result.reverse()
	return result[:20]





