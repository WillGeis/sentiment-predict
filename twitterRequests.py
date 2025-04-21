import requests
import json
import re
from datetime import datetime
from typing import List, Dict, Any, Optional, Union

class TwitterAPI:
    def __init__(self):
        self.base_url = "https://syndication.twitter.com/srv/timeline-profile/screen-name"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
    def get_tweets(self, username: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Get tweets for a specific Twitter user
        
        Args:
            username (str): Twitter username without '@'
            count (int): Number of tweets to retrieve (default: 10)
            
        Returns:
            List[Dict]: List of tweet objects with processed data
        """
        url = f"{self.base_url}/{username}"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            html = response.text
            
            # Extract JSON data from the HTML
            start_str = '<script id="__NEXT_DATA__" type="application/json">'
            end_str = '</script></body></html>'
            
            start_index = html.index(start_str) + len(start_str)
            end_index = html.index(end_str, start_index)
            
            json_str = html[start_index:end_index]
            data = json.loads(json_str)
            
            # Extract tweets from the JSON data
            raw_tweets = data["props"]["pageProps"]["timeline"]["entries"]
            
            # Process the raw tweets
            processed_tweets = []
            for entry in raw_tweets:
                if "content" in entry and "tweet" in entry["content"]:
                    tweet = entry["content"]["tweet"]
                    
                    # Extract tweet data
                    tweet_data = {
                        "id": tweet.get("id_str", ""),
                        "text": tweet.get("full_text", ""),
                        "created_at": self._parse_date(tweet.get("created_at", "")),
                        "retweet_count": tweet.get("retweet_count", 0),
                        "favorite_count": tweet.get("favorite_count", 0),
                        "user": {
                            "username": username,
                            "name": tweet.get("user", {}).get("name", ""),
                            "verified": tweet.get("user", {}).get("verified", False),
                        },
                        "hashtags": self._extract_hashtags(tweet.get("full_text", "")),
                        "urls": self._extract_urls(tweet.get("full_text", "")),
                        "is_retweet": "retweeted_status" in tweet,
                    }
                    
                    processed_tweets.append(tweet_data)
                    
                    if len(processed_tweets) >= count:
                        break
            
            return processed_tweets
            
        except Exception as e:
            print(f"Error fetching tweets for {username}: {str(e)}")
            return []
    
    def search_tweets_by_keyword(self, username: str, keyword: str, count: int = 10) -> List[Dict[str, Any]]:
        """
        Search tweets from a user containing specific keywords
        
        Args:
            username (str): Twitter username to search within
            keyword (str): Keyword to search for
            count (int): Maximum number of tweets to return
            
        Returns:
            List[Dict]: List of matching tweet objects
        """
        # First get all available tweets
        all_tweets = self.get_tweets(username, count=100)  # Get more tweets to search through
        
        # Filter tweets by keyword (case insensitive)
        matching_tweets = [
            tweet for tweet in all_tweets
            if keyword.lower() in tweet["text"].lower()
        ]
        
        # Return the specified count
        return matching_tweets[:count]
    
    def get_top_tweets(self, username: str, count: int = 10, metric: str = "favorite_count") -> List[Dict[str, Any]]:
        """
        Get top tweets from a user based on engagement metrics
        
        Args:
            username (str): Twitter username
            count (int): Number of tweets to retrieve
            metric (str): Metric to sort by - "favorite_count" (likes) or "retweet_count"
            
        Returns:
            List[Dict]: List of top tweet objects
        """
        # Get all available tweets
        all_tweets = self.get_tweets(username, count=100)  # Get more tweets to rank
        
        # Sort by the specified metric
        if metric not in ["favorite_count", "retweet_count"]:
            metric = "favorite_count"  # Default to likes
            
        sorted_tweets = sorted(all_tweets, key=lambda x: x[metric], reverse=True)
        
        # Return the top N
        return sorted_tweets[:count]
    
    def _parse_date(self, date_str: str) -> str:
        """Parse Twitter date format to ISO format"""
        try:
            dt = datetime.strptime(date_str, "%a %b %d %H:%M:%S %z %Y")
            return dt.isoformat()
        except:
            return date_str
    
    def _extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from tweet text"""
        return re.findall(r"#(\w+)", text)
    
    def _extract_urls(self, text: str) -> List[str]:
        """Extract URLs from tweet text"""
        url_pattern = r'https?://[^\s]+'
        return re.findall(url_pattern, text)


def print_tweet(tweet, index=None):
    """Pretty print a tweet object"""
    prefix = f"[{index}] " if index is not None else ""
    
    print(f"{prefix}Tweet by @{tweet['user']['username']} ({tweet['created_at']})")
    print(f"{'✓ ' if tweet['user']['verified'] else ''}@{tweet['user']['username']}: {tweet['text']}")
    print(f"❤️ {tweet['favorite_count']} | 🔄 {tweet['retweet_count']}")
    
    if tweet['hashtags']:
        print(f"Hashtags: {', '.join(['#' + tag for tag in tweet['hashtags']])}")
    
    if tweet['is_retweet']:
        print("(Retweet)")
    
    print("-" * 50)
