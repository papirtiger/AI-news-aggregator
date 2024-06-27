import logging
import feedparser
import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_rss(url):
    logging.info(f"Fetching RSS from {url}")
    try:
        feed = feedparser.parse(url)
        results = []
        for entry in feed.entries[:10]:  # Limit to 10 most recent entries
            title = entry.title
            description = entry.summary[:200] + '...' if len(entry.summary) > 200 else entry.summary
            link = entry.link
            results.append(f"Headline: {title}\nDescription: {description}\nLink: {link}\n")
        return "\n".join(results)
    except Exception as e:
        logging.error(f"Error fetching RSS from {url}: {str(e)}")
        return ""

def scrape_website(url, article_selector, title_selector, description_selector, link_selector):
    logging.info(f"Scraping website {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select(article_selector)[:10]  # Limit to 10 most recent articles
        
        results = []
        for article in articles:
            title = article.select_one(title_selector).text.strip()
            description = article.select_one(description_selector).text.strip()[:200] + '...'
            link = article.select_one(link_selector)['href']
            if not link.startswith('http'):
                link = url + link
            results.append(f"Headline: {title}\nDescription: {description}\nLink: {link}\n")
        return "\n".join(results)
    except Exception as e:
        logging.error(f"Error scraping website {url}: {str(e)}")
        return ""

def is_relevant(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

def main():
    logging.info("Starting AI news aggregation")

    # List of news sources
    sources = [
        {"type": "rss", "url": "https://techcrunch.com/category/artificial-intelligence/feed/"},
        {"type": "rss", "url": "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml"},
        {"type": "scrape", "url": "https://www.wired.com/category/artificial-intelligence/", 
         "selectors": {"article": "div.summary-item", "title": "h3", "description": "div.summary-item__dek", "link": "a"}},
        {"type": "rss", "url": "https://blogs.nvidia.com/feed/"},
        {"type": "rss", "url": "https://openai.com/blog/rss.xml"},
    ]

    keywords = ["artificial intelligence", "AI", "machine learning", "deep learning", "neural network", 
                "AI ethics", "AI legislation", "AI regulation", "AI risk", "AI safety"]

    output = f"AI News Updates - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"

    for source in sources:
        logging.info(f"Processing source: {source['url']}")
        output += f"From source: {source['url']}\n"
        if source['type'] == 'rss':
            content = fetch_rss(source['url'])
        else:
            content = scrape_website(source['url'], **source['selectors'])
        
        # Filter content for relevance
        relevant_content = "\n".join([item for item in content.split('\n\n') if is_relevant(item, keywords)])
        output += relevant_content + "\n---\n\n"

    with open('ai_news_updates.txt', 'w', encoding='utf-8') as f:
        f.write(output)

    logging.info("AI news updates have been written to ai_news_updates.txt")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise
