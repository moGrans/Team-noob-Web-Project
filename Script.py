from crawler import crawler
from Database import database

if __name__ == "__main__":
    ''' Testing functionality of crawler '''
    print "Establish connection..."
    db = database()
    
    bot = crawler(db, 'urls.txt')
    bot.crawl(depth=2)

    print "Inserting into lexicon..."
    db.insertIntoLexicon(bot._lexicon)

    print "Inserting into document index"
    db.insertIntoDocIndex(bot._doc_index, bot._doc_title)

    print "Inserting into inverted index..."
    db.insertIntoInvertedIndex(bot._inverted_index)

    print "Inserting into resolved inverted index..."
    db.insertIntoReInvertedIndex(bot._resolved_inverted_index)
