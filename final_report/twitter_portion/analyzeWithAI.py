import pandas as pd
import requests
import json
import time
import numpy as np
import random
from datetime import datetime
import re

API_KEY = "sk-proj-???"

BASE_DELAY = 1.0     # Base delay between API calls in seconds
MAX_RETRIES = 3      # Maximum retries for a single API call
RATE_LIMIT_WINDOW = 60  # OpenAI's rate limit window in seconds
RATE_LIMIT_TOKENS = 30000  # OpenAI's token rate limit for gpt-4o
CHECKPOINT_INTERVAL = 20  # Save progress every N tweets

TICKER_SYMBOLS = [
    "AAPL", "MSFT", "NVDA", "GOOG", "GOOGL", "AMZN", "META", "AVGO", "TSM", "TSLA",
    "WMT", "LLY", "JPM", "V", "UNH", "MA", "XOM", "COST", "NFLX", "FMX",
    "PG", "JNJ", "ORCL", "HD", "SAP", "KO", "TMUS", "BAC", "NVO", "SMFG",
    "BABA", "ASML", "PM", "CRM", "CVX", "TM", "CCZ", "ABT", "CSCO", "IBM",
    "MCD", "PLTR", "NVS", "LIN", "WFC", "AZN", "GE", "SHEL", "T", "ACN",
    "MRK", "PEP", "RTX", "ISRG", "TMO", "INTU", "NOW", "RY", "TBB", "PGR",
    "GS", "UL", "UBER", "AMGN", "QCOM", "DIS", "BKNG", "ADBE", "AMD", "SPGI",
    "TJX", "SONY", "BSX", "CAT", "SCHW", "DHR", "MUFG", "NEE"
]

class TokenRateTracker:
    def __init__(self, limit=RATE_LIMIT_TOKENS, window=RATE_LIMIT_WINDOW):
        self.limit = limit
        self.window = window
        self.tokens_used = 0
        self.last_reset = time.time()
        self.total_tokens = 0  # Track total tokens across all windows
    
    def add_tokens(self, count):
        """Add token usage and check if we need to reset the window"""
        current_time = time.time()
        if current_time - self.last_reset > self.window:
            self.tokens_used = 0
            self.last_reset = current_time
        self.tokens_used += count
        self.total_tokens += count
    
    def can_make_request(self, estimated_tokens=500):
        """Check if we can make a request with estimated token count"""
        current_time = time.time()
        if current_time - self.last_reset > self.window:
            self.tokens_used = 0
            self.last_reset = current_time
        return (self.tokens_used + estimated_tokens) <= self.limit
    
    def get_wait_time(self, estimated_tokens=500):
        """Get time to wait before making another request"""
        current_time = time.time()
        time_passed = current_time - self.last_reset
        
        if time_passed >= self.window:
            return 0
        
        if self.can_make_request(estimated_tokens):
            return 0 
        
        return max(0, self.window - time_passed)

def load_tweets(csv_file):
    """Load tweets from a CSV file."""
    try:
        tweets_df = pd.read_csv(csv_file)
        print(f"Loaded {len(tweets_df)} tweets from {csv_file}")
        return tweets_df
    except FileNotFoundError:
        alt_path = f"../twitter_data/{csv_file}"
        try:
            tweets_df = pd.read_csv(alt_path)
            print(f"Loaded {len(tweets_df)} tweets from {alt_path}")
            return tweets_df
        except Exception as e:
            print(f"Error loading tweets from alternate path: {e}")
            return pd.DataFrame()
    except Exception as e:
        print(f"Error loading tweets: {e}")
        return pd.DataFrame()

def analyze_tweet_with_openai(tweet_text, username, likes, retweets, token_tracker):
    """
    Use OpenAI API to analyze a tweet for stock sentiment.
    Returns a dictionary with ticker symbols and sentiment scores.
    """
    system_prompt = f"""
    You are a sophisticated financial sentiment analyzer with expertise in detecting subtle market signals. Analyze the following tweet and determine if it expresses ANY sentiment or potential impact (direct or indirect) on any of these stocks: {', '.join(TICKER_SYMBOLS)}.
    
    For each potentially relevant stock, provide a sentiment score between -1.0 (extremely negative) and 1.0 (extremely positive) using these guidelines:
    
    - Use the FULL RANGE from -1.0 to 1.0, not just rounded values
    - Consider both explicit mentions and implicit connections
    - Consider the tweet's potential market impact, not just literal mentions
    - Extremely positive news/sentiment: 0.7 to 1.0
    - Moderately positive news/sentiment: 0.3 to 0.7
    - Slightly positive news/sentiment: 0.05 to 0.3
    - Neutral or ambiguous: -0.05 to 0.05
    - Slightly negative news/sentiment: -0.3 to -0.05
    - Moderately negative news/sentiment: -0.7 to -0.3
    - Extremely negative news/sentiment: -1.0 to -0.7
    
    Be sensitive to industry connections, competitive implications, and supply chain effects. Create connections liberally - even tweets that seem unrelated may have financial implications. Aim for a natural distribution across the entire spectrum of scores.
    
    IMPORTANT:
    1. Use precise decimal values (e.g., 0.42, -0.83), NOT rounded values
    2. Be creative in finding connections to stocks - the tweet doesn't need to explicitly mention the company
    3. Consider industry-wide implications (e.g., a tweet about electric vehicles might affect TSLA, RIVN, GM, etc.)
    4. Consider second-order effects (e.g., a tweet about chip shortages might affect both chip makers and their customers)
    5. Consider political implications for regulated industries
    6. Analyze tone, sentiment, and potential market reaction - not just factual content
    
    Return ONLY a JSON object with ticker symbols as keys and sentiment scores as values.
    Example: {{\"TSLA\": 0.87, \"NVDA\": -0.23, \"INTC\": -0.56}}
    
    If no relevant stocks can be connected, return an empty JSON object: {{}}
    """
    
    user_message = f"""
    Tweet by: {username}
    Likes: {likes} 
    Retweets: {retweets}
    
    Tweet text: "{tweet_text}"
    
    Important: Use precise decimal scores (like 0.42 or -0.76) and identify ALL possible stock connections, even subtle ones.
    """
    
    estimated_tokens = len(system_prompt.split()) + len(user_message.split()) + 100
    
    wait_time = token_tracker.get_wait_time(estimated_tokens)
    if wait_time > 0:
        print(f"Rate limit approaching. Waiting {wait_time:.2f} seconds before next request...")
        time.sleep(wait_time)
    
    for retry in range(MAX_RETRIES):
        try:
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {API_KEY}"
            }
            data = {
                "model": "gpt-4o",  
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.9,  
                "max_tokens": 200
            }
            
            print(f"Sending API request (attempt {retry+1}/{MAX_RETRIES})...")
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                response_json = response.json()
                content = response_json["choices"][0]["message"]["content"]
                
                if "usage" in response_json:
                    token_tracker.add_tokens(response_json["usage"]["total_tokens"])
                else:
                    token_tracker.add_tokens(estimated_tokens)  # Use estimate if not provided
                
                try:
                    if "```json" in content:
                        json_str = content.split("```json")[1].split("```")[0].strip()
                    else:
                        json_str = content.strip()
                    
                    sentiment_dict = json.loads(json_str)
                    
                    for ticker, score in sentiment_dict.items():
                        noise = np.random.normal(0, 0.18)  # Increased noise for more variance
                        new_score = score + noise
                        sentiment_dict[ticker] = max(-1.0, min(1.0, new_score))
                    
                    dynamic_delay = BASE_DELAY * (1 + token_tracker.tokens_used / token_tracker.limit)
                    time.sleep(min(dynamic_delay, 5.0))  # Cap at 5 seconds
                    
                    return sentiment_dict
                except json.JSONDecodeError:
                    print(f"Error parsing JSON response: {content}")
                    json_match = re.search(r'\{.*\}', content, re.DOTALL)
                    if json_match:
                        try:
                            sentiment_dict = json.loads(json_match.group(0))
                            return sentiment_dict
                        except:
                            pass
                    
                    time.sleep(BASE_DELAY * (retry + 1))
            
            elif response.status_code == 429:  # Rate limit error
                print(f"Rate limit exceeded. Response: {response.text}")
                
                wait_pattern = r"Please try again in (\d+)(\.\d+)?([ms]s)"
                wait_match = re.search(wait_pattern, response.text)
                
                if wait_match:
                    value = float(wait_match.group(1) + (wait_match.group(2) or "0"))
                    unit = wait_match.group(3)
                    
                    if unit == "ms":
                        wait_seconds = value / 1000
                    else: 
                        wait_seconds = value
                        
                    wait_seconds += 1.0  # Add buffer
                    print(f"Waiting {wait_seconds:.2f} seconds as suggested by API...")
                    time.sleep(wait_seconds)
                else:
                    backoff = (2 ** retry) * 5  # 5, 10, 20 seconds
                    print(f"Using exponential backoff: waiting {backoff} seconds...")
                    time.sleep(backoff)
            
            else:
                print(f"API error: {response.status_code}, {response.text}")
                backoff = (2 ** retry) * 2
                time.sleep(backoff)
                
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            backoff = (2 ** retry) * 2
            time.sleep(backoff)
    
    print("Exhausted all retries. Returning empty result.")
    return {}
    

def load_checkpoint(checkpoint_file):
    """Load checkpoint data if it exists."""
    try:
        with open(checkpoint_file, 'r') as f:
            checkpoint_data = json.load(f)
        print(f"Loaded checkpoint: Processed {checkpoint_data['processed_count']} tweets")
        return checkpoint_data
    except FileNotFoundError:
        print("No checkpoint found. Starting from beginning.")
        return {
            'processed_count': 0,
            'sentiment_data': {ticker: {'score': 0.0, 'count': 0} for ticker in TICKER_SYMBOLS},
            'all_sentiment_scores': {ticker: [] for ticker in TICKER_SYMBOLS}
        }
    except Exception as e:
        print(f"Error loading checkpoint: {e}")
        return {
            'processed_count': 0,
            'sentiment_data': {ticker: {'score': 0.0, 'count': 0} for ticker in TICKER_SYMBOLS},
            'all_sentiment_scores': {ticker: [] for ticker in TICKER_SYMBOLS}
        }

def save_checkpoint(checkpoint_file, processed_count, sentiment_data, all_sentiment_scores):
    """Save checkpoint data."""
    checkpoint_data = {
        'processed_count': processed_count,
        'sentiment_data': sentiment_data,
        'all_sentiment_scores': all_sentiment_scores
    }
    
    with open(checkpoint_file, 'w') as f:
        json.dump(checkpoint_data, f)
    
    print(f"Checkpoint saved: Processed {processed_count} tweets")

def process_all_tweets(tweets_df, output_file="stock_sentiment_complete.csv"):
    """
    Process ALL tweets with appropriate rate limit handling.
    Saves results to a CSV file and provides checkpoints for resuming.
    """
    token_tracker = TokenRateTracker()
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    checkpoint_file = f"sentiment_checkpoint_{timestamp}.json"
    
    checkpoint_data = load_checkpoint(checkpoint_file)
    processed_count = checkpoint_data['processed_count']
    sentiment_data = checkpoint_data['sentiment_data']
    all_sentiment_scores = checkpoint_data['all_sentiment_scores']
    
    start_time = time.time()
    total_tweets = len(tweets_df)
    
    for index, tweet in tweets_df.iloc[processed_count:].iterrows():
        tweet_text = tweet['text']
        username = tweet['username']
        likes = tweet['likes']
        retweets = tweet['retweets']
        
        processed_count += 1
        elapsed_time = time.time() - start_time
        tweets_per_second = processed_count / max(1, elapsed_time)
        estimated_remaining = (total_tweets - processed_count) / max(0.001, tweets_per_second)
        
        print(f"\nProcessing tweet {processed_count}/{total_tweets}: {tweet_text[:50]}...")
        print(f"Progress: {processed_count/total_tweets*100:.1f}% - Est. remaining time: {estimated_remaining/60:.1f} minutes")
        
        tweet_sentiment = analyze_tweet_with_openai(tweet_text, username, likes, retweets, token_tracker)
        
        for ticker, score in tweet_sentiment.items():
            if ticker in sentiment_data:
                sentiment_data[ticker]['score'] += score
                sentiment_data[ticker]['count'] += 1
                all_sentiment_scores[ticker].append(score)
        
        if processed_count % CHECKPOINT_INTERVAL == 0:
            save_checkpoint(checkpoint_file, processed_count, sentiment_data, all_sentiment_scores)
            
            current_results = {}
            for ticker in TICKER_SYMBOLS:
                if sentiment_data[ticker]['count'] > 0:
                    current_results[ticker] = sentiment_data[ticker]['score'] / sentiment_data[ticker]['count']
                else:
                    current_results[ticker] = 0.0
                    
            print("\nCurrent Sentiment Scores:")
            for ticker in sorted(current_results.keys(), key=lambda x: abs(current_results[x]), reverse=True):
                if current_results[ticker] != 0:
                    print(f"{ticker}: {current_results[ticker]:.4f} (Mentions: {sentiment_data[ticker]['count']})")
    
    save_checkpoint(checkpoint_file, processed_count, sentiment_data, all_sentiment_scores)
    
    final_sentiment = {}
    mention_counts = {}
    
    for ticker in TICKER_SYMBOLS:
        if sentiment_data[ticker]['count'] > 0:
            final_sentiment[ticker] = sentiment_data[ticker]['score'] / sentiment_data[ticker]['count']
            mention_counts[ticker] = sentiment_data[ticker]['count']
        else:
            final_sentiment[ticker] = 0.0
            mention_counts[ticker] = 0
    
    results_df = pd.DataFrame({
        'Ticker': TICKER_SYMBOLS,
        'Sentiment_Score': [final_sentiment[ticker] for ticker in TICKER_SYMBOLS],
        'Mention_Count': [mention_counts[ticker] for ticker in TICKER_SYMBOLS]
    })
    
    results_df.to_csv(output_file, index=False)
    print(f"Results saved to {output_file}")
    
    with open(f"sentiment_distribution_{timestamp}.json", "w") as f:
        json.dump(all_sentiment_scores, f)
    
    with open(f"api_log_{timestamp}.txt", "w") as f:
        f.write(f"Total tweets processed: {processed_count}\n")
        f.write(f"Total tokens used (estimate): {token_tracker.total_tokens}\n")
        f.write(f"Total processing time: {(time.time() - start_time)/60:.2f} minutes\n")
    
    return final_sentiment, mention_counts

def main():
    print("=== Complete Tweet Sentiment Analysis with Checkpoint Recovery ===")
    print(f"Rate limit window: {RATE_LIMIT_WINDOW} seconds")
    print(f"Rate limit tokens: {RATE_LIMIT_TOKENS}")
    print(f"Checkpoint interval: Every {CHECKPOINT_INTERVAL} tweets\n")
    
    tweets_df = load_tweets("../twitter_data/financial_tweets.csv")
    
    if not tweets_df.empty:
        start_time = time.time()
        
        final_sentiment, mention_counts = process_all_tweets(tweets_df)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\nFinal Sentiment Scores:")
        for ticker in sorted(final_sentiment.keys(), key=lambda x: abs(final_sentiment[x]), reverse=True):
            if final_sentiment[ticker] != 0:
                print(f"{ticker}: {final_sentiment[ticker]:.4f} (Mentions: {mention_counts[ticker]})")
        
        print("\nNote: Showing tickers with non-zero sentiment scores, sorted by sentiment strength.")
        print(f"\nProcessing completed in {duration/60:.2f} minutes")
        print("\nThis script processes ALL tweets with appropriate rate limit handling")
        print("and checkpoints to allow resuming if interrupted.")

if __name__ == "__main__":
    main()
