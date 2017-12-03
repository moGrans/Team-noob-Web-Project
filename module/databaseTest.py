import Database

if __name__ == "__main__":
    db = Database.database()

    db.initializeTrieTree()

    print db.trie.get_start('studen')
    print db.trie.get_start('uni')