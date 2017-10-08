from crawler import crawler

if __name__ == "__main__":
    ''' Testing functionality of crawler '''
    bot = crawler(None, 'urls.txt')
    bot.crawl(depth=2)

    i = bot.get_resolved_inverted_index()

    for word, links in i.items():
        print word
        for link in links:
            print '\t' + link