import requests
import sqlite3
import schedule
import time
from threading import Thread
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Function to get a database connection
def get_db():
    db = sqlite3.connect('news.db')
    db.row_factory = sqlite3.Row  # This allows us to access columns by name
    return db

# Initialize the database
def init_db():
    db = get_db()
    db.execute('DROP TABLE IF EXISTS news')  # Drop the existing table if it exists
    db.execute('''
    CREATE TABLE news (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        url TEXT NOT NULL,
        source TEXT NOT NULL
    );
    ''')
    db.commit()

# Fetch news from multiple sources and store it in the database
def fetch_and_store_news():
    api_key = 'd83317d0b03040fc84d08443f5e77476'
    urls = [
        'https://www.iol.co.za/',
        'https://www.news24.com/',
        'https://www.timeslive.co.za/',
        'https://www.sabcnews.com/',
        'https://www.enca.com/',
        f'https://newsapi.org/v2/top-headlines?country=gb&category=business&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=gb&category=entertainment&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=gb&category=health&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=gb&category=science&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=gb&category=sports&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=us&category=entertainment&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=us&category=health&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=us&category=science&apiKey={api_key}',
        f'https://newsapi.org/v2/top-headlines?country=us&category=sports&apiKey={api_key}'
    ]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }
    db = get_db()
    db.execute('DELETE FROM news')  # Clear existing news articles

    for url in urls:
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for HTTP errors

            if 'newsapi.org' in url:
                news_data = response.json().get('articles', [])
                for article in news_data:
                    title = article['title']
                    description = article['description']
                    article_url = article['url']
                    source = article['source']['name']
                    
                    # Debugging: Print the extracted data
                    print(f"Title: {title}, Description: {description}, URL: {article_url}, Source: {source}")
                    
                    db.execute('INSERT INTO news (title, description, url, source) VALUES (?, ?, ?, ?)', 
                               (title, description, article_url, source))
            else:
                soup = BeautifulSoup(response.content, 'html.parser')
                articles = soup.find_all('article')  # Adjust this selector based on the actual HTML structure
                for article in articles:
                    title = article.find('h2').get_text() if article.find('h2') else 'No title'
                    description = article.find('p').get_text() if article.find('p') else 'No description'
                    article_url = article.find('a')['href'] if article.find('a') else 'No URL'
                    article_url = urljoin(url, article_url)  # Convert relative URL to absolute URL
                    source = url
                    
                    # Debugging: Print the extracted data
                    print(f"Title: {title}, Description: {description}, URL: {article_url}, Source: {source}")
                    
                    db.execute('INSERT INTO news (title, description, url, source) VALUES (?, ?, ?, ?)', 
                               (title, description, article_url, source))
        except Exception as e:
            print(f"Error fetching or storing news from {url}: {e}")

    db.commit()

# Schedule the news fetching function
def schedule_news_fetching():
    schedule.every(1).hour.do(fetch_and_store_news)
    
    def run_scheduler():
        while True:
            schedule.run_pending()
            time.sleep(1)
    
    scheduler_thread = Thread(target=run_scheduler)
    scheduler_thread.start()

# Initialize the