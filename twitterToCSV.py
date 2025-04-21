#!/usr/bin/env python3
"""
Twitter to CSV Exporter
This script collects tweets and exports them to CSV format for financial sentiment analysis.
"""

from twitterRequests import TwitterAPI
import csv
import os
from datetime import datetime
import re

class TwitterCSVExporter:
    def __init__(self, output_dir="twitter_data"):
        self.twitter = TwitterAPI()
        self.output_dir = output_dir
        
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def clean_text(self, text):
        """Clean tweet text by removing newlines and extra spaces"""
        text = text.replace('\n', ' ')
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_mentions(self, text):
        """Extract @mentions from tweet text"""
        return ','.join(re.findall(r'@(\w+)', text))
    
    def extract_cashtags(self, text):
        """Extract $cashtags from tweet text"""
        return ','.join(re.findall(r'\$(\w+)', text))
    
    def collect_and_export(self, accounts, count_per_account=20, filename=None):
        """
        Collect tweets from specified accounts and export to CSV
        
        Args:
            accounts (list): List of Twitter usernames to collect from
            count_per_account (int): Number of tweets to collect per account
            filename (str): Optional filename, defaults to a timestamped file
            
        Returns:
            str: Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tweets_{timestamp}.csv"
        
        filepath = os.path.join(self.output_dir, filename)
        
        # Define CSV headers
        headers = [
            'tweet_id',
            'username',
            'name',
            'verified',
            'date',
            'text',
            'likes',
            'retweets',
            'hashtags',
            'mentions',
            'cashtags',
            'urls',
            'is_retweet',
        ]
        
        # Open CSV file for writing
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
            
            # Collect and write tweets
            for username in accounts:
                print(f"Collecting tweets from @{username}...")
                tweets = self.twitter.get_tweets(username, count=count_per_account)
                
                for tweet in tweets:
                    clean_text = self.clean_text(tweet['text'])
                    
                    # Convert tweet data to CSV format
                    row = {
                        'tweet_id': tweet['id'],
                        'username': username,
                        'name': tweet['user']['name'],
                        'verified': 'Yes' if tweet['user']['verified'] else 'No',
                        'date': tweet['created_at'],
                        'text': clean_text,
                        'likes': tweet['favorite_count'],
                        'retweets': tweet['retweet_count'],
                        'hashtags': ','.join(tweet['hashtags']),
                        'mentions': self.extract_mentions(clean_text),
                        'cashtags': self.extract_cashtags(clean_text),
                        'urls': ','.join(tweet['urls']),
                        'is_retweet': 'Yes' if tweet['is_retweet'] else 'No',
                    }
                    
                    writer.writerow(row)
                
                print(f"Collected {len(tweets)} tweets from @{username}")
        
        print(f"Exported tweets to {filepath}")
        return filepath
    
    def export_search_results(self, username, keyword, count=20, filename=None):
        """
        Search tweets by keyword and export results to CSV
        
        Args:
            username (str): Twitter username to search within
            keyword (str): Keyword to search for
            count (int): Maximum number of tweets to return
            filename (str): Optional filename
            
        Returns:
            str: Path to the created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_{username}_{keyword}_{timestamp}.csv"

        matching_tweets = self.twitter.search_tweets_by_keyword(username, keyword, count)
        return self.collect_and_export([username], count, filename)


# Example usage
if __name__ == "__main__":
    exporter = TwitterCSVExporter()
    
    # Define list of relevant accounts to monitor
    financial_accounts = [
        "elonmusk",        # Elon Musk
        "SecYellen",       # Treasury Secretary Janet Yellen
        "federalreserve",  # Federal Reserve
        "JoeBiden",        # President Biden
        "WSJ",             # Wall Street Journal
    ]
    
    # Collect tweets and export to CSV
    csv_path = exporter.collect_and_export(
        accounts=financial_accounts,
        count_per_account=10,
        filename="financial_tweets.csv"
    )
    
    print(f"CSV file created at: {csv_path}")
    
    # Example of searching for specific keywords and exporting results
    keyword_csv = exporter.export_search_results(
        username="elonmusk",
        keyword="economy",
        count=5,
        filename="elon_economy_tweets.csv"
    )
    
    print(f"Keyword search CSV created at: {keyword_csv}")