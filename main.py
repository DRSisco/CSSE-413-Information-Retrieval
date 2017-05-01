from BeautifulSoup import BeautifulSoup
from os import listdir
from os.path import isfile, join
import re
import math;

FILES = "./Presidents"

files = [f for f in listdir(FILES) if isfile(join(FILES, f))]

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True

def isRelevant(input, title_tags, anchor_tags, text, file):
    search_terms = input.split(' ')
    for term in search_terms:
        print 'file ' + file
        print number_of_results
        number_of_results = len(re.findall(term, text, re.IGNORECASE))

    return False

def idf(total_docs, n, f):
    temp = (total_docs - n + 0.5) / (n + 0.5)
    return math.log(temp)

def main():
    while True:
        query = raw_input("? ")
        if query == "quit" or query == 'exit':
            break
        print search(str(query))

def search(input):
    relevantFiles = list()
    for file in files:
        f = open(FILES + "/" + file, 'r')
        soup = BeautifulSoup(f)
        title_tags = soup.findAll("title")
        anchor_tags = soup.findAll('a')
        text = soup.getText()
        if isRelevant(input, title_tags, anchor_tags, text, file):
            relevantFiles.append(file)
    return relevantFiles

if __name__ == '__main__':
    main()
