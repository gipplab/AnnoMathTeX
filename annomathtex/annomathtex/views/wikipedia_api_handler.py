import requests
from bs4 import BeautifulSoup
import wikipedia


class WikipediaAPIHandler():




    def get_suggestions(self, search_string, limit=5):
        return wikipedia.search(search_string, results=5)


    def get_wikipedia_article(self, article_name):
        article_name = article_name.replace(' ', '_')
        url = "https://en.wikipedia.org/w/index.php?title={}&action=edit".format(article_name)
        r = requests.get(url)
        content = r.content.decode('utf-8')
        soup = BeautifulSoup(content)
        wikipedia_article = soup.find("textarea").contents[0]
        return wikipedia_article





if __name__ == '__main__':
    w = WikipediaAPIHandler()

    s = w.get_suggestions("quantum")[0]
    w.get_wikipedia_article(s)

