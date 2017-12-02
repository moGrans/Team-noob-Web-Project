import datetime
import operator
import pymongo
import pprint

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

        self.lexiconDB = self.client.lexicon.Posts
        self.docIndexDB = self.client.document_index.Posts
        self.invertedIndexDB = self.client.inverted_index.Posts
        self.reInvertedIndexDB = self.client.resolved_inverted_index.Posts

        self.visitedUrlDB = self.client.visited_url.Posts

        self.pageRankDB = self.client.page_rank.Posts

    def insertIntoLexicon(self, _lexicon):
        """ Insert current crawled lexicon into mongoDB. """
        newPost = []

        if len(_lexicon) == 0:
            return 0

        for word_id, word in _lexicon.iteritems():
            newPost.append({'date':datetime.datetime.utcnow(),
                            "word":word,
                            "word_id":word_id})

        lexiconDB = self.client.lexicon.Posts
        result = lexiconDB.insert_many(newPost)

    def insertIntoDocIndex(self, _doc_index, _doc_title, page_ranks):
        """ Insert current crawled doc index into mongodDB. """
        newPost = []

        if len(_doc_index) == 0:
            return 0

        # A lambda fuction for use of assigning doc title
        hasKey = lambda key,col: col[key] if col.has_key(key) else ''
        for docID, url in dict(_doc_index).iteritems():
            if self.docIndexDB.find_one({'doc_id':docID}):
                continue
            newPost.append({'date':datetime.datetime.utcnow(),
                            'doc_id':docID,
                            'url':url,
                            'doc_title': hasKey(docID, _doc_title),
                            'doc_score': page_ranks[docID]})
        result = self.docIndexDB.insert_many(newPost)

    def insertIntoInvertedIndex(self, _inverted_index):
        """ Insert current crawled inverted index into monogoDB. """

        newPost = []
        if len(_inverted_index) == 0:
            return 0

        for wordID, docIDs in _inverted_index.iteritems():
            result = self.invertedIndexDB.find_one({'word_id':wordID})
            if not result:
                newPost.append({"word_id":wordID,
                                "doc_ids":list(docIDs)} )
            else:
                # Merging existing doc ids with newly crawled ids
                temp = result['doc_ids'].extend(list(docIDs))

                # Update cloud database
                self.invertedIndexDB.find_one_and_update({'word_id':wordID},
                                                         {'$set':{'doc_ids':temp}})

        result = self.invertedIndexDB.insert_many(newPost)

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

    # def insertIntoPageRank(self, word, sortedPages):
    #     """
    #     either insert or update ranked pages corresponding to
    #     a word on data base

    #     :word: str
    #     :sortedPages: list(int)
    #     """
    #     newPost = []
    #     if self.pageRankDB.find({'word':word}):
    #         self.pageRankDB.find_one_and_replace({'word':word},
    #                                             {'word':word,
    #                                             'sortedPages':sortedPages})
    #     else:
    #         self.pageRankDB.insert_one({'word':word,
    #                                     'sortedPages':sortedPages})

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