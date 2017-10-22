#
# Class Definition
#
class searchKW:
    """
	this class stores information of a single search
	kw_order: a list variable that store keyword by search order
			kw_dict: a dictionary variable that store keyword with cooresponding search count

		defined function:
		__init__: initialize by one single search string
		__add__: add self with another searchKW, use to add in NEW keyword (other) to HISTORY keyword (self)
		__exit__: empty/clear list and dict
	"""

    # constructor with searched string
    def __init__(self, search_string=""):
        # self.search_string = search_string.lower().split()
        #  store searched string using list by keyword in lower case
        search_string = search_string.lower().split()
        self.kw_order = []
        self.kw_dict = {}

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

    # add keywords from new search
    def __add__(self, other):
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
        return self

    # destructure to clear up variables
    def __exit__(self):
        # self.search_string[:] = []
        self.kw_order[:] = []
        self.kw_dict.clear()


#
# Variable Delcaration
#
user_kw_his = {}  # store searchKW by userid
top_20_list = []  # store top 20 keyword search of a specific userid


#
# Function Implementation
#

# handle raw search string from get method

def handle_input(search_string, ss_user):
    # store search result into result history
    this_search = searchKW(search_string)
    # user did not log in will not display and store keyword history
    if ss_user is None:
        return this_search
    # store by user id
    if ss_user not in user_kw_his:
        # new user id
        user_kw_his[ss_user] = this_search
    else:
        # user id already exist, add new search to previous search history
        user_kw_his[ss_user] = user_kw_his[ss_user] + this_search
    # find top 20 search count for ss_user
    top_20(ss_user)
    # sort top 20 in order of count
    insertion_sort(ss_user)
    # reverse to make desending order 
    top_20_list.reverse()
    # return the search parse for this specific search
    return this_search


# store search history by user name
def top_20(ss_user):
    # delete old result
    top_20_list[:] = []

    # user specific (syntatic)
    kdict = user_kw_his[ss_user].kw_dict
    klist = user_kw_his[ss_user].kw_order
    # loop through all keyword since launched
    min_20 = klist[0]  # initialize min count in top 20 keyword
    for word in klist:
        # include keyword if top 20 list is not full (20 elements)
        if len(top_20_list) < 20:
            top_20_list.append(word)
            # update min count in top 20 list
            min_20 = min_20 if kdict[min_20] < kdict[word] else word
        elif kdict[min_20] < kdict[word]:
            # replace min_20 if word has more count
            top_20_list.remove(min_20)
            top_20_list.append(word)
            # update new min
            min_20 = top_20_list[0]
            for word in top_20_list:
                min_20 = min_20 if kdict[min_20] < kdict[word] else word


# insertion_sort the top 20 keyword by count
def insertion_sort(ss_user):
    # user specific
    kdict = user_kw_his[ss_user].kw_dict
    # insertion_sort
    for i in range(1, len(top_20_list)):
        cur_word = top_20_list[i]
        pos = i
        while pos > 0 and kdict[top_20_list[pos - 1]] > kdict[top_20_list[i]]:
            top_20_list[pos] = top_20_list[pos - 1]
            pos = pos - 1
        top_20_list[pos] = cur_word
