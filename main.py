from BeautifulSoup import BeautifulSoup
from os import listdir
from os.path import isfile, join
import re
import math;
from skipgrams import skipbigrams

FILES = "./Presidents"

files = [f for f in listdir(FILES) if isfile(join(FILES, f))]
k = 1.25

def visible(element):
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
    elif re.match('<!--.*-->', str(element.encode('utf-8'))):
        return False
    return True


def getTermFrequency(input, title_tags, anchor_tags, text, fileScore):
    number_of_results = len(re.findall(input, text, re.IGNORECASE))
    number_of_results += len(re.findall(input, anchor_tags, re.IGNORECASE))
    number_of_results += 10 * len(re.findall(input, title_tags, re.IGNORECASE))
    return number_of_results


def numRelevantFiles(counts):
    totalFiles = list()
    i = 0
    while i < len(counts[0]):
        total = 0
        for count in counts:
            if count[i] > 0:
                total += 1
        totalFiles.append(total)
        i += 1
    return totalFiles


def idf(total_docs, n):
    temp = (total_docs - n + 0.5) / (n + 0.5)
    return math.log(temp)

def calcBM25(idfs, freq, length, alength):
    total = 0
    i = 0
    for idfval in idfs:
        b = .75 * idfval
        total += (freq[i] * (k + 1))/ (freq[i] + (k * (1 - b + (b * (length/alength)))))
    return total

def main():
    while True:
        query = raw_input("? ")
        if query == "quit" or query == 'exit':
            break
        print search(str(query))


def search(input):
    relevantFiles = list()
    search_terms = input.split(' ')
    docLength = list()
    frequency = list()
    for file in files:
        fileCounts = list()
        f = open(FILES + "/" + file, 'r')
        soup = BeautifulSoup(f)
        title_tags = ' '.join([t.getText() for t in soup.findAll("title")])
        anchor_tags = ' '.join([t.getText() for t in soup.findAll("a")])
        text = soup.getText()
        docLength.append(len(text.split(" ")))
        for term in search_terms:
            fileCounts.append(getTermFrequency(term, title_tags, anchor_tags, text,fileCounts))
        frequency.append(fileCounts)
    numFiles = numRelevantFiles(frequency)
    averageDocLength = sum(docLength)/len(docLength)
    idfs = list()
    i = 0
    while i < len(search_terms):
        idfs.append(idf(len(files), numFiles[i]))
        i += 1
    BM25s = list()
    i = 0
    while i < len(files):
        BM25s.append(calcBM25(idfs, frequency[i], docLength[i], averageDocLength))
        i += 1

    maxBM25 = max(BM25s)
    print maxBM25
    return files[BM25s.index(maxBM25)].title()

if __name__ == '__main__':
    main()
