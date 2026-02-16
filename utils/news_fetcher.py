"""
News fetching module
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

class NewsFetcher:
    """Class to handle news fetching from various sources"""
    
    SOURCES = {
        "india": {
            "name": "India News",
            "url": f"https://newsapi.org/v2/top-headlines?country=in&apiKey={NEWS_API_KEY}"
        },
        "technology": {
            "name": "Technology",
            "url": f"https://newsapi.org/v2/top-headlines?category=technology&country=in&apiKey={NEWS_API_KEY}"
        }
    }
    
    DEMO_NEWS = {
        "india": [
            {"title": "Demo news 1", "source": "Demo Source"}
        ]
    }
    
    @staticmethod
    def fetch_news(category):
        """Fetch news for given category"""
        # Implementation here
        pass