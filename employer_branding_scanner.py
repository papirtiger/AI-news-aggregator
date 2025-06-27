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

def scrape_website(url, article=None, title=None, description=None, link=None):
    logging.info(f"Scraping website {url}")
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if article:
            articles = soup.select(article)[:10]  # Limit to 10 most recent articles
        else:
            articles = [soup]  # If no article selector, treat the whole page as one article
        
        results = []
        for article_elem in articles:
            title_text = article_elem.select_one(title).text.strip() if title else ""
            description_text = article_elem.select_one(description).text.strip()[:200] + '...' if description else ""
            link_elem = article_elem.select_one(link) if link else None
            link_url = link_elem['href'] if link_elem else url
            if not link_url.startswith('http'):
                link_url = url + link_url
            results.append(f"Headline: {title_text}\nDescription: {description_text}\nLink: {link_url}\n")
        return "\n".join(results)
    except Exception as e:
        logging.error(f"Error scraping website {url}: {str(e)}")
        return ""

def is_relevant(text, keywords):
    return any(keyword.lower() in text.lower() for keyword in keywords)

def main():
    logging.info("Starting employer branding news aggregation")
    # List of employer branding and HR-related news sources
    sources = [
        {"type": "rss", "url": "https://hrdailyadvisor.blr.com/feed/"},
        {"type": "rss", "url": "https://www.hrzone.com/rss.xml"},
        {"type": "rss", "url": "https://recruitingdaily.com/feed/"},
        {"type": "rss", "url": "https://employerbranding.co/feed/"},
        {"type": "rss", "url": "https://www.indeed.com/employers/blog/feed"},
        {"type": "rss", "url": "https://www.glassdoor.com/employers/blog/feed/"},
        {"type": "rss", "url": "https://resources.workable.com/blog/feed"},
        {"type": "rss", "url": "https://www.hrgrapevine.com/content/rss"},
        {"type": "rss", "url": "https://www.peoplematters.in/rss"},
        {"type": "rss", "url": "https://www.shrm.org/hr-today/news/hr-news/_layouts/15/feed.aspx"},
    ]

    keywords = [
        "employer branding",
        "rekruttering",
        "recruitment",
        "medarbejdertilfredshed",
        "employee satisfaction",
        "employer value proposition",
        "EVP",
        "HR marketing",
        "recruitment marketing",
        "arbejdsglaede",
        "employer brand",
    ]

    output = f"Employer Branding News Updates - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    for source in sources:
        logging.info(f"Processing source: {source['url']}")
        output += f"From source: {source['url']}\n"
        if source['type'] == 'rss':
            content = fetch_rss(source['url'])
        else:
            content = scrape_website(source['url'], **source.get('selectors', {}))
        
        # Filter content for relevance
        relevant_content = "\n".join([item for item in content.split('\n\n') if is_relevant(item, keywords)])
        output += relevant_content + "\n---\n\n"
    
    with open('eb_news_updates.txt', 'w', encoding='utf-8') as f:
        f.write(output)
    logging.info("Employer branding news updates have been written to eb_news_updates.txt")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")
        raise
