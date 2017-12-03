import datetime
import operator
import pymongo
import re
from SpellingCheck import autocorrect
from trie import Trie

# CONNECTION_STR = \
#     "mongodb://Gransy:dfvGhUj068c9YqiA\
# @cluster0-shard-00-00-chyjq.mongodb.net:27017,\
# cluster0-shard-00-01-chyjq.mongodb.net:27017,\
# cluster0-shard-00-02-chyjq.mongodb.net:27017/\
# test?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin"

CONNECTION_STR = "mongodb://localhost"

class database():

    def __init__(self):
        """ Establish connection to mongoDB """
        try:
            # Connecting to mongoDB
            self.client  = pymongo.MongoClient(CONNECTION_STR)
        except Exception as error:
            assert False, error

        self.lexiconDB = self.client.project.lexicon
        self.docIndexDB = self.client.project.document_index
        self.invertedIndexDB = self.client.project.inverted_index
        self.reInvertedIndexDB = self.client.project.resolved_inverted_index

        self.visitedUrlDB = self.client.project.visited_url

        self.pageRankDB = self.client.project.page_rank

        self.wordAppearanceDB = self.client.project.word_appearance

        self.trie = Trie()

        self.spellingChecker = None

        WORD_SEPARATORS = re.compile(r'\s|\n|\r|\t|[^a-zA-Z0-9\-_]')

    def insertIntoLexicon(self, _lexicon):
        """ Insert current crawled lexicon into mongoDB. """
        newPost = []

        if len(_lexicon) == 0:
            return 0

        for word_id, word in _lexicon.iteritems():
            newPost.append({'date':datetime.datetime.utcnow(),
                            "word":word,
                            "word_id":word_id})

        result = self.lexiconDB.insert_many(newPost)

    def insertIntoDocIndex(self, _doc_index, _doc_title, page_ranks, _doc_content, seen):
        """ Insert current crawled doc index into mongodDB. """
        newPost = []

        if len(_doc_index) == 0:
            return 0

        # A lambda fuction for use of assigning doc title
        hasKey = lambda key,col: col[key] if col.has_key(key) else ''
        for docID, url in dict(_doc_index).iteritems():
            if docID not in seen:
                continue
            newPost.append({'date':datetime.datetime.utcnow(),
                            'doc_id':docID,
                            'url':url,
                            'doc_title': hasKey(docID, _doc_title),
                            'doc_score': page_ranks[docID],
                            'doc_content': _doc_content[docID]})

        result = self.docIndexDB.insert_many(newPost)

    def insertIntoWordAppearance(self, _lexicon, _word_appearance):

        newPost = []

        if len(_word_appearance) == 0:
            return

        for word_id, word in _lexicon.iteritems():
            result = self.wordAppearanceDB.find_one({'word_id':word_id})

            doc_id_collect = []
            pos_collect = []

            for doc_id, pos in (_word_appearance[word_id]).iteritems():
                doc_id_collect.append(doc_id)
                pos_collect.append(_word_appearance[word_id][doc_id])

            if not result:
                newPost.append({"word_id":word_id,
                                "doc_id_collect":doc_id_collect,
                                "pos_collect":pos_collect})
            else:
                doc_id_collect = result["doc_id_collect"].extend(doc_id_collect)
                pos_collect = result["pos_collect"].extend(pos_collect)

                self.wordAppearanceDB.find_one_and_update({'word_id':word_id},
                                                          {'$set':{'doc_id_collect':doc_id_collect}},
                                                          {'$set':{'pos_collect':pos_collect}})

        self.wordAppearanceDB.insert_many(newPost)

    def insertIntoInvertedIndex(self, _inverted_index):
        """ Insert current crawled inverted index into monogoDB. """

        newPost = []
        if len(_inverted_index) == 0:
            return 0

        for wordID, docIDs in _inverted_index.iteritems():
            result = self.invertedIndexDB.find_one({'word_id':wordID})
            if not result:
                newPost.append({"word_id":wordID,
                                "doc_ids":list(docIDs)})
            else:
                # Merging existing doc ids with newly crawled ids
                temp = result['doc_ids'].extend(list(docIDs))

                # Update cloud database
                self.invertedIndexDB.find_one_and_update({'word_id':wordID},
                                                         {'$set':{'doc_ids':temp}})

        self.invertedIndexDB.insert_many(newPost)

    def insertIntoReInvertedIndex(self, _resolved_inverted_index):
        """ Insert resolved inverted index into monogoDB. """

        newPost = []
        if len(_resolved_inverted_index) == 0:
            return 0

        for word, urls in _resolved_inverted_index.iteritems():
            result = self.reInvertedIndexDB.find_one({'word':word})
            if not result:
                newPost.append({"word":word,
                                "urls":list(urls)})
            else:
                # Merging exising url set with newly creawled urls
                temp = result['urls'].extend(list(urls))

                # Update cloud database
                self.reInvertedIndexDB.find_one_and_update({'word':word},
                                                           {'$set':{'urls':temp}})

        result = self.reInvertedIndexDB.insert_many(newPost)

    def checkURL(self, url):
        """
        Check whether or not the input url has been visited.

        :url: str
        :return: bool
        """
        if self.visitedUrlDB.find_one({'url':url}):
            return False
        else:
            self.visitedUrlDB.insert_one({'url':url})
            return True

    def findWord(self, arg):
        """
        Depending on type of arg, function will return a word id
        or a word
        If word id is given, the word is returned
        If word is given, the word id is returned
        -> findWord(word_id) => word
        -> fidnWord(word)    => word_id
        Note in both case if nothing is found, None is returned

        :arg: int or str
        :return: str or int
                 None   # if not found
        """
        if type(arg) == int:
            result = self.lexiconDB.find_one({'word_id':arg})
            if not result:
                return None
            else:
                return result['word']
        elif type(arg) == str:
            result = self.lexiconDB.find_one({'word':arg})
            if not result:
                return None
            else:
                return result['word_id']
        else:
            raise TypeError

    def findDoc(self, arg):
        """
        Depending on type of arg, function will return a tuple
        If url id is given, the doc id is returned
        If doc id is given, the url is returned
        -> findDoc(doc_id) => (url, doc_id, title, score)
        -> findDoc(url)    => (url, doc_id, title, score)
        Note in both case if nothing is found, None is returned

        :arg: int or str
        :return: str or int
                 None   # if not found
        """
        if type(arg) == int:
            result = self.docIndexDB.find_one({'doc_id':arg})
            if not result:
                return None
            else:
                return (result['url'], arg, result['doc_title'], result['doc_score'])

        elif type(arg) == str:
            result = self.docIndexDB.find_one({'url':arg})
            if not result:
                return None
            else:
                return (arg, result['doc_id'], result['doc_title'], result['doc_score'])
        else:
            raise TypeError

    def findRelatedDocIDs(self, word_ID):
        """
        Find document ids corresponding to a word id, a list of ids
        returned
        if there is no such existing, None otherwise

        :word_ID: int
        :return: list(int)
                 None   # if not found
        """
        result = self.invertedIndexDB.find_one({'word_id':word_ID})
        if not result:
            return None
        else:
            return result['doc_ids']


    def findRelatedDocUrls(self, word):
        """
        Find document urls corresponding to the word, a list of urls
        returned
        if there is no such existing, None otherwise

        :word_ID: int
        :return: list(str)
                 None       # if not found
        """
        result = self.reInvertedIndexDB.find_one({'word':word})
        if not result:
            return None
        else:
            return result['urls']

    def findRelatedPageRank(self, word):
        """
        Find the ranked list of urls related to a word
        If such word not found, None returned
        :word: str
        :return: list(str)
                 None       # if not found
        """
        wordRelated = self.lexiconDB.find_one({'word': word})


        if not wordRelated:
            return None

        word_ID = wordRelated['word_id']

        relatedDocIDs = self.findRelatedDocIDs(word_ID)

        if not relatedDocIDs:
            return None

        result = {}
        for eachID in relatedDocIDs:
            found = self.docIndexDB.find_one({'doc_id':eachID})
            result[ (found['url'], found['doc_title']) ] = found['doc_score']

        sortedURL = sorted(result.items(), key=operator.itemgetter(1))
        sortedURL = [ele[0] for ele in sortedURL]
        sortedURL.reverse()

        return sortedURL

    def initializeTrieTree(self):

        words = []

        for eachLexicon in self.lexiconDB.find({}):
            self.trie.insert(eachLexicon['word'])
            words.append(eachLexicon['word'])

        self.spellingChecker = autocorrect(words)

    def searchSuggestion(self, userInput):
        """
        Give back search suggestion depending on current input
        :param userInput: str
        :return: str
                 None if no result can be found
        """
        words = self.WORD_SEPARATORS.split(userInput.lower())
        suggestions = []

        if len(words) == 1:
            # User is inputting the first word
            suggestions = self.trie.get_start(words[0])

            corrected = None

            if len(suggestions) == 0:
                # if don't get nothing, try auto correct
                corrected = self.spellingChecker.correction(words[0])

            # Try another time after finished correction
            suggestions = self.trie.get_start(corrected)
            if len(suggestions) == 0:
                return None


        elif len(words) > 1:

            temp_pos_clt = []
            docCandidate = []

            for wordIndex in range(words):
                result = self.wordAppearanceDB.find_one({'word':words[wordIndex]})
                temp_pos_clt.append(result['pos_collect'])
                docCandidate.append(result['doc_id_collect'])



    def getDescription(self, word_ids, doc_id, nWords):
        """
        Depending on the given word id and doc id, return a string has
        a length specified by nWords
        :param word_ids: int
        :param doc_id: int
        :param nWords: int
        :param nWords: int
        :return: str
        """

        # result = self.wordAppearanceDB.find_one({'word_id':word_id})
        pass


    def multi_word_search(self, list_of_words):
        pass

