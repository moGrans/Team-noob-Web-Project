import Database

if __name__ == "__main__":
    db = Database.database()

    db.initializeTrieTree()

    s_w, s_d = db.multi_word_search(['uoft', 'ece'])
    print s_w
    print s_d

    for each in db.getDescription(s_w, s_d):
        print each

    print db.getDescriptionForOneWord('uoft','http://www.eecg.toronto.edu/~enright')