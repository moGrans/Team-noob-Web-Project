# create global variable
global keyword_dict 
global top_20_list
global keyword_order

# keyword_dict: record all keyword with count number
# top_20_list: record top 20 searched keyword since launched
# keyword_order: record all keywords in first appreance order,
# this_keyword_order: record keyword in first appreance order, reset everytime new phrase is searched
# this_keyword_dict: record this keywords with count number
keyword_dict = {}
top_20_list = []
keyword_order = []
this_keyword_order = []
this_keyword_dict = {}


def handle_input(search_string):
	# store search result into result history
    parse_search_input(search_string)
    # aquire top 20 count in searched order
    top_20_keyword()
    # sort top 20 in order of count
    insertion_sort()
    # reverse top 20 keyword
    top_20_list.reverse()



def parse_search_input(search_string):
	# reset for new input
	this_keyword_order[:] = []
	this_keyword_dict.clear()

	# convert input string into lowercase letter
	# break the string into list of word and record to total_keywords
	search_string = search_string.lower()
	search_keywords = search_string.split()

	# find number of times each keyword being searched
	for word in search_keywords:
		# this search's keyword
		if word not in this_keyword_dict:
			# add word and initial (1) count into dictonary of all searched keys since launched
			this_keyword_dict[word] = 1
			# add word into order list to record search order
			# total keyword
			if word not in this_keyword_order:
				this_keyword_order.append(word)
		else:
			# increment the count of the searched keyword
			this_keyword_dict[word] += 1
		
		# all
		if word not in keyword_dict:
			# add word and initial (1) count into dictonary of all searched keys since launched
			keyword_dict[word] = 1
			# add word into order list to record search order
			# total keyword
			if word not in keyword_order:
				keyword_order.append(word)
		else:
			# increment the count of the searched keyword
			keyword_dict[word] += 1


def insertion_sort():
	for i in range (1,len(top_20_list)):
		cur_word = top_20_list[i]
		pos = i
		while pos > 0 and keyword_dict[top_20_list[pos - 1]] > keyword_dict[top_20_list[i]]:
			top_20_list[pos] = top_20_list[pos - 1]
			pos = pos - 1
		top_20_list[pos] = cur_word


# compute top 20 count keywords
def top_20_keyword():
	# delete old result
	top_20_list[:] = []
	# loop through all keyword since launched
	for word in keyword_order:
		if len(top_20_list) < 20:
			# add keyword to top20list if the list is not full (contain 20 elements) despite the frequency count
			top_20_list.append(word)
		else:
			# find the minimum frequency count in the current top20list			
			min_top20 = top_20_list[0]
			for word_top20 in top_20_list:
				# if word_top20 count is lesser than the current min count then update min
				if keyword_dict[word_top20] < keyword_dict[min_top20]:
					min_top20 = word_top20
			# compare min count keyword in top 20 list and the current word in all search
			# remove min count keyword if current word is greater and replace with new keyword
			if keyword_dict[min_top20] < keyword_dict[word]:
				del top_20_list[min_top20]
				top_20_list.append(word)
