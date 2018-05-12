import metapy
import json
import ssl
import csv

import urllib.request

from newsapi import NewsApiClient
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier
from textblob.sentiments import NaiveBayesAnalyzer

from nltk.tokenize import TweetTokenizer, sent_tokenize
from nltk.corpus import brown
from nltk import sent_tokenize, word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.tokenize import RegexpTokenizer

newsapi = NewsApiClient(api_key='7ee74deac24c411eb29bb20c37f05068')


# Returns a JSON data from a URL
def get_json_from_url(link):
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        return data


def hasNumbers(tokens):
    return any(token.isdigit() for token in tokens)

def getReviewLink(query, domain):
    query = query.lower()
    base_url = "https://www.googleapis.com/customsearch/v1?key=AIzaSyCWn3Bw5HOxsC6wyvUkg02v4ngDCDFP7ZU&cx=014029824769110719357:t_k1dyl2rku&q="
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(query)
    print(tokens)

    convertedQuery = ""
    for count, token in enumerate(tokens):
        if count == 0:
            convertedQuery = token
        else:
            convertedQuery = f'{convertedQuery}+{token}'

    full_url = f'{base_url}{convertedQuery}+review+site:{domain}'
    all_articles = get_json_from_url(full_url)
    # print(all_articles)

    totalResults = int(all_articles['searchInformation']['totalResults'])

    if totalResults == 0:
        return None

    # Loops from 1 to min(8, totalresults) until it finds a satisfying article
    for i in range(0, min(2, totalResults)):
        articleTitle = all_articles['items'][i]['title'].lower()
        titleTokens = tokenizer.tokenize(articleTitle)
        if ("review" not in articleTitle or
            "reviews" in articleTitle or
            "cases" in articleTitle or
            "case" in articleTitle or
            "camera" in articleTitle or
            hasNumbers(tokens) != hasNumbers(titleTokens) or
            not set(tokens).issubset(titleTokens)):
            continue
        else:
            return all_articles['items'][i]
    return None

def getReviewLinkOld(query, domain):
    print(query)
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(query)

    convertedQuery = ""
    for count, token in enumerate(tokens):
        if count == 0:
            convertedQuery = token
        else:
            convertedQuery = f'{convertedQuery}+{token}'

    all_articles = newsapi.get_everything(q=convertedQuery,
                                          domains=domain,
                                          language='en',
                                          sort_by='relevancy')

    if all_articles['status'] != "ok" or all_articles['totalResults'] == 0:
        return None

    # Loops from 1 to min(8, totalresults) until it finds a satisfying article
    for i in range(0, min(8, all_articles['totalResults'])):
        articleTitle = all_articles['articles'][i]['title'].lower()
        if "review" not in articleTitle or "reviews" in articleTitle or "cases" in articleTitle or "case" in articleTitle or "camera" in articleTitle:
            continue
        else:
            return all_articles['articles'][i]
    return None


def getBodyContent(url, domain):
    # Opening up connection, grabbing page
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # html scraping
    content = ""
    contentSoup = soup(page_html, "html5lib")
    if domain == "theverge.com":
        contentBody = None
        if contentSoup.find("div", {"class": "c-entry-content"}) != None:
            contentBody = contentSoup.find("div", {"class": "c-entry-content"})
        elif contentSoup.find("div", {"class": "entry-content"}) != None:
            contentBody = contentSoup.find("div", {"class": "entry-content"})
        else:
            return None
        paragraphs = contentBody.findAll("p", {}, text=True)
        for paragraph in paragraphs:
            content = f'{content}{paragraph.text}'

    elif domain == "phonearena.com":
        contentBody = contentSoup.find("div", {"id": "review-content"})
        if contentBody == None:
            return None
        unwanted = contentBody.findAll('script')
        for sub in unwanted:
            sub.extract()
        unwanted = contentBody.findAll('span')
        for sub in unwanted:
            sub.extract()
        unwanted = contentBody.findAll('h2')
        for sub in unwanted:
            sub.extract()
        myText = contentBody.findAll(text=True)

        breadcrum = [item.strip() for item in myText if str(item)]
        breadcrum = list(filter(None, breadcrum))

        return contentBody.get_text()

    elif domain == "slashgear.com":
        contentBody = contentSoup.find("div", {"class": "content"})
        if contentBody == None:
            return None
        paragraphs = contentBody.findAll("p", {}, text=True, recursive=False)
        for paragraph in paragraphs:
            content = f'{content}{paragraph.text}'

    elif domain == "techcrunch.com":
        contentBody = contentSoup.find("div", {"class": "article-content"})
        if contentBody == None:
            return None
        paragraphs = contentBody.findAll("p", {}, text=True, recursive=False)
        for paragraph in paragraphs:
            content = f'{content}{paragraph.text}'

    elif domain == "androidheadlines.com":
        contentBody = contentSoup.find("div", {"class": "entry-content"})
        if contentBody == None:
            return None
        paragraphs = contentBody.findAll("p", {}, text=True, recursive=False)
        for paragraph in paragraphs:
            content = f'{content}{paragraph.text}'
    else:
        return None

    # print(content)

    return content


def getSentences(doc):

    tok = metapy.analyzers.ICUTokenizer(suppress_tags=True)
    tok.set_content(doc.content())
    tokens = []
    for token in tok:
        tokens.append(token)
    return tokens


battery_words = {
    'longer': 2.0,
    'long': 3.0,
    'longest': 3.5,
    'short': -2.0,
    'shorter': -2.5,
    'entire': 0.4
}

display_words = {
    'bright': 3.0,
    'colorful': 2.0,
    'contrasty': 2.0,
    'dim': -1.0,
    '1440p': 3.4,
    '1080p': -1.4,
    '720p': -3.5,
    'AMOLED': 5.2,
    'OLED': 3.5,
    'Quad': 2.0,
    'LCD': -0.5,
    'tint': -0.5,
    'accurate': 1.0
}

performance_words = {
    'snappy': 2.0,
    '6GB': 3.0,
    'responsive': 2.0,
    'smooth': 2.0,
    'fluid': 2.0,
    'fast': 1.5,
    'octa': 1.5,
    'mediatek': -1.2,
    'laggy': -2.0,
    'hiccup': -1.0
}

overall_words = {
    'solid': 3.0,
    'best': 3.0,
    'excellent': 3.0,
}

camera_words = {
    'clear': 3.0,
    'crisp': 2.0,
    'crispy': 2.0,
    'rich': 2.0,
    'HDR+': 3.0,
    'machine': 1.5,
    'dual': 2.0,
    'single': -0.2,
    'wide': 1.2,
    'laggy': -0.8,
    'grainy': -1.5,
    'reducing': 1.5,
    'noisy': -1.5,
    'overexposure': -1.5,
    'overexposed': -1.5,
    'overexpose': -1.5,
    'underexposure': -1.5,
    'underexposed': -1.5,
    'underexpose': -1.5,
    '960': 3.0,
    '4K': 2.0,
    'portrait': 1.0,
    'dull': 1.0,
    'tinted': -1.5,
    'dark': -0.3,
    'soft': -1.5,
    'zoom': 1.5,
    'saturated': 0.5,
    'improved': 2.5,
    'improvements': 1.5,
    'light': 1.0,
    'f/1.5': 3.0,
    'f/1.6': 1.5,
    'bokeh': 2.5,
    'two': 2.5,
    'low-light': 0.5,
    'DxOMark’s': 1.5,
    'DxOMark': 1.5
}


def getSentiment(sentences, category):
    if not sentences:
        return None

    score = 0.0
    count = 0

    SIA = SentimentIntensityAnalyzer()

    if category == "battery":
        SIA.lexicon.update(battery_words)
    elif category == "display":
        SIA.lexicon.update(display_words)
    elif category == "performance":
        SIA.lexicon.update(performance_words)
    elif category == "camera":
        SIA.lexicon.update(camera_words)
    elif category == "overall":
        SIA.lexicon.update(battery_words)
        SIA.lexicon.update(display_words)
        SIA.lexicon.update(camera_words)
        SIA.lexicon.update(performance_words)

    for sentence in sentences:
        # analysis = TextBlob(sentence)
        sentimentScore = SIA.polarity_scores(sentence)["compound"]
        if round(sentimentScore, 2) != 0:
            score += sentimentScore
            count += 1
    if count == 0:
        return None

    finalScore = score/count
    if category == "overall":
        finalScore = ((finalScore*100) + 0.9*(100))/(100+0.9*(100))
    elif category == "camera":
        finalScore = ((finalScore*100) + 0.8*(100))/(100+0.8*(100))
    elif category == "performance":
        finalScore = ((finalScore*100) + 0.5*(100))/(100+0.5*(100))
    return round(finalScore, 5)


def openFile(filename):
    with open('battery-training.csv', 'r') as fp:
        cl = NaiveBayesClassifier(fp)


def getNaiveSentiment():
    cl = openFile('battery-training.csv')
    prob_dist = cl.prob_classify("I wish the phone was lasting longer.")
    testProb1 = round(prob_dist.prob("pos"), 2)
    testProb2 = round(prob_dist.prob("neg"), 2)
    print("Pos: {}".format(testProb1))
    print("Neg: {}".format(testProb2))

    return None


class Article:
    def __init__(self, _url, _body):
        self.title = None
        self.url = _url
        self.body = _body
        self.battery = None
        self.display = None
        self.performance = None
        self.camera = None
        self.overall = None


domains = ["theverge.com", "phonearena.com", "slashgear.com",
           "techcrunch.com", "androidheadlines.com"]


def analyze(query):
    articles = dict.fromkeys(domains, None)
    for domain in domains:
        article = getReviewLink(query, domain)
        articleURL = None
        title = None
        body = None

        if article != None:
            articleURL = article['link']
            title = article['title']
            body = getBodyContent(articleURL, domain)

        newArticle = Article(articleURL, body)
        newArticle.title = title
        print(title)
        articles[domain] = newArticle

        # Tokenize body to sentences
        if body == None:
            continue
        SentenceTokens = sent_tokenize(articles[domain].body)

        # Filters out irrelevant sentences
        performanceTokens = [i for i in SentenceTokens if (u"performance") in word_tokenize(
            i.lower()) or (u"software") in word_tokenize(i.lower())]
        batteryTokens = [i for i in SentenceTokens if (
            u"battery") in word_tokenize(i.lower())]
        displayTokens = [i for i in SentenceTokens if ((u"display") in word_tokenize(
            i.lower()) or (u"screen")) in word_tokenize(i.lower())]
        cameraTokens = [i for i in SentenceTokens if (u"camera") in word_tokenize(
            i.lower()) or (u"photos") in word_tokenize(i.lower())]
        overallTokens = SentenceTokens

        # Get sentimental values and assign them
        articles[domain].performance = getSentiment(
            performanceTokens, "performance")
        articles[domain].battery = getSentiment(batteryTokens, "battery")
        articles[domain].display = getSentiment(displayTokens, "display")
        articles[domain].camera = getSentiment(cameraTokens, "camera")
        articles[domain].overall = getSentiment(overallTokens, "overall")

        # print(f'Performance: {articles[domain].performance}')
        # print(f'battery: {articles[domain].battery}')
        # print(f'display: {articles[domain].display}')
        # print(f'camera: {articles[domain].camera}')
        # print(f'overall: {articles[domain].overall}')

    averagePerformance = None
    averageBattery = None
    averageDisplay = None
    averageCamera = None
    averageOverall = None

    totalPerformance = 0.0
    totalBattery = 0.0
    totalDisplay = 0.0
    totalCamera = 0.0
    totalOverall = 0.0

    countPerformance = 0
    countBattery = 0
    countDisplay = 0
    countCamera = 0
    countOverall = 0

    isPerformance = False
    isBattery = False
    isDisplay = False
    isCamera = False
    isOverall = False

    for domain in domains:
        if articles[domain].performance != None:
            totalPerformance += articles[domain].performance
            countPerformance += 1
            isPerformance = True

        if articles[domain].battery != None:
            totalBattery += articles[domain].battery
            countBattery += 1
            isBattery = True

        if articles[domain].display != None:
            totalDisplay += articles[domain].display
            countDisplay += 1
            isDisplay = True

        if articles[domain].camera != None:
            totalCamera += articles[domain].camera
            countCamera += 1
            isCamera = True

        if articles[domain].overall != None:
            totalOverall += articles[domain].overall
            countOverall += 1
            isOverall = True

    if isPerformance is False:
        totalPerformance = None
    elif isBattery is False:
        totalBattery = None
    elif isDisplay is False:
        totalDisplay = None
    elif isCamera is False:
        totalCamera = None
    elif isOverall is False:
        totalOverall = None

    if totalPerformance != None and countPerformance != 0:
        averagePerformance = totalPerformance / countPerformance
    if totalBattery != None and countBattery != 0:
        averageBattery = totalBattery / countBattery
    if totalDisplay != None and countDisplay != 0:
        averageDisplay = totalDisplay / countDisplay
    if totalCamera != None and countCamera != 0:
        averageCamera = totalCamera / countCamera
    if totalOverall != None and countOverall != 0:
        averageOverall = totalOverall / countOverall

    return [averagePerformance, averageBattery, averageDisplay, averageCamera, averageOverall]


if __name__ == '__main__':
    # print(sampleText)
   # print(batterySIA.polarity_scores("All my research suggests that this phone has poor battery life."))
    print(analyze("LG G6"))
