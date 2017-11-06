from crawler import crawler
from Database import database
import operator

if __name__ == "__main__":
    ''' Testing functionality of crawler '''
    print "Establish connection to cloud..."

    print "\nStart crawling"
    db = database()

    bot = crawler(db, 'urls.txt')
    bot.crawl(depth=1)

    print "Inserting into lexicon..."
    db.insertIntoLexicon(bot._lexicon)

    print "Inserting into document index"
    db.insertIntoDocIndex(bot._doc_index, bot._doc_title, bot._page_ranks)

    print "Inserting into inverted index..."
    db.insertIntoInvertedIndex(bot._inverted_index)

    print "Inserting into resolved inverted index..."
    db.insertIntoReInvertedIndex(bot._resolved_inverted_index)

    print "Crawling fininshed printing out page ranks"
    
    # Sorting cache of page rank
    sortedPages = sorted(bot._page_ranks.items(), key=operator.itemgetter(1))
    sortedPages.reverse()

    print "Maximize the window to have better display"
    # Formatting print out
    tplt = '{0:<100}{1:>5}'

    print tplt.format("URL", "Score")

    for eachPair in sortedPages:
        print tplt.format(eachPair[0], [1])
