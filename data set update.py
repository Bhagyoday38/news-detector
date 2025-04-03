import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# List of top news websites you want to scrape, including Indian sources
urls = [
    'https://www.bbc.com/news',
    'https://edition.cnn.com/',
    'https://www.nytimes.com/section/world',
    'https://www.theguardian.com/world',
    'https://www.reuters.com/news/world',
    'https://www.aljazeera.com/news/',
    'https://www.huffpost.com/news/world',
    'https://www.usatoday.com/news/world/',
    'https://www.nbcnews.com/world',
    'https://www.foxnews.com/world',
    'https://www.abcnews.go.com/International',
    # Indian news websites
    'https://timesofindia.indiatimes.com/',
    'https://www.thehindu.com/',
    'https://www.ndtv.com/',
    'https://www.indiatoday.in/',
    'https://www.hindustantimes.com/',
    'https://www.firstpost.com/',
    'https://www.moneycontrol.com/news/',
    'https://www.cnbctv18.com/news/',
    'https://www.mintlive.com/',
    'https://www.sportmonks.com/',
    'https://www.espn.in/',
    'https://sports.ndtv.com/',
    'https://sportstar.thehindu.com/',
    'https://kheloindia.gov.in/',
    'https://www.cricbuzz.com/',
    'https://www.business-standard.com/'
]

# Function to scrape news articles
def scrape_news(url):
    articles = []
    
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Modify this based on the structure of the website (classes, tags, etc.)
        for article in soup.find_all('h3'):
            title = article.get_text(strip=True)
            anchor = article.find('a')
            if anchor and 'href' in anchor.attrs:  # Check if anchor exists and has an href
                link = anchor['href']
                if not link.startswith('http'):
                    link = requests.compat.urljoin(url, link)
                articles.append({
                    'title': title,
                    'link': link,
                    'text': '',  # Placeholder for the article text
                    'label': 'REAL'
                })
                
    except Exception as e:
        print(f'Error scraping {url}: {e}')
    
    return articles

# Scrape each website
all_articles = []
for url in urls:
    articles = scrape_news(url)
    all_articles.extend(articles)
    print(f'Successfully scraped {len(articles)} articles from {url}.')
    time.sleep(2)  # To avoid overwhelming the server

# Convert to DataFrame and save
df = pd.DataFrame(all_articles)
df.to_csv('news_data.csv', index=False)

print(f'Total articles scraped: {len(all_articles)}')
