# Mobile Metrics
An application that dynamically scrapes smartphone text reviews from popular news websites and performs a sentiment analysis on them. Then it uses the result to tell the user how good the smartphone is. 

## Requirements
- Flask
- Node.js and npm
- Python3
- TextBlob
- NLTK
- BeautifulSoup

## Usage
1. Clone the repository
2. Install the necessary requirements.
3. Run `python manage.py runserver` within the backend folder
4. Run `npm start` within the frontend folder 
5. Go to `localhost:5000` on your browser.

## Functions
* getReviewLink(query, domain) - Returns a json data of the review article. `query` is the name of the smartphone. `domain` is the review site to grab from.
* getBodyContent(url, domain) - Returns a string of the review text. `url` is the specific website to retrieve text from. `domain` is the domain of the `url`.
* getBodyContent(url, domain) - Returns a string of the review text. `url` is the specific website to retrieve text from. `domain` is the domain of the `url`.
* getSentiment(sentences, category) - Returns a float representin the sentiment score ranging from -1 to 1. `sentences` is the list of strings to assign sentiment. `category` is what kind of category the `sentences` are in.
* getNaiveSentiment(filename, sentence) - Returns a probability distribution object of sentiment. `filename` is the file for training data. `sentence` is the text to perform sentiment analysis on.
* class Article - A simple article class that holds the variables: title, url, body, domain, battery, display, performance, camera, overall
* analyze(query) - Returns a list containing the average sentiment of each category, and a list of article objects. `query` is the search term (smartphone name).

## Implementation
The application is built on Flask and ReactJS. It uses Flask to handle the back end and ReactJS for the front end. The file `project.py` is where all the text retrieving and processing happens. When Flask is running and connected with ReactJS through an endpoint, it will listen for a search term. Once the user performs a search on the browser, the data will be sent to Flask. Flask will input this search term into `analyze`, which will spit out an average sentiment score. Flask sends this score to ReactJS to display.

## The process:
###Getting the reviews
1) User types in a smartphone name (eg. Pixel 2 XL, Galaxy S9)
2) Performs a query search through Google’s Search API to get appropriate URL and title. (The article’s text content itself is not provided, thus we must use web scraping tools.)
3) Provides the URL to Beautiful Soup to scrape the text content from the appropriate websites 
### Processing the text
1) Tokenizes the texts into sentences using  NLTK (Natural Language ToolKit). Creates n different tokens based on n different categories (battery, performance etc.). Each category only has a relevant sentence.
2) Performs sentiment analysis on each category using VADER (Valence Aware Dictionary and sEntiment Reasoner) and TextBlob. Both of them use lexicon dictionaries that are known to be reliable in most use cases. 
3) Improve sentiment analysis using weighting and Naive Bayes Analyzer
### Integration
1) VM (Virtual Environment) is created using pipenv.
2) Flask runs on the VM to handle all the back end tasks such as the text retrieval, and processing. 
3) ReactJS is used to display the elements and receive the query. 


## Changing API key
You may change Google's Search API key. To do so, open `project.py` and change the variable `GOOGLE_API_KEY`.

## License
Copyright (c) Bryan Ulziisaikhan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.