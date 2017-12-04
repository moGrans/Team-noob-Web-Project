import Database

if __name__ == "__main__":
    db = Database.database()

    db.initializeTrieTree()
    s_w, s_d = db.multi_word_search(['computer', 'university'])
    print s_w
    print s_d

    print db.getDescription(s_w, s_d)
