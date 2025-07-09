# 📈 Sentiment Adjusted Trading Optimization

**Notice:** this README.md is AI generated based on the final report .ipynb which is human written, see that for a full report

This project explores the intersection of quantitative finance and real-time sentiment analysis by optimizing a stock portfolio based on traditional financial metrics **and** sentiment extracted from social media activity by high-profile figures. It demonstrates how recent tweets can be quantified to adjust expected stock returns dynamically.

---

## 🚀 Project Overview

We designed two portfolio optimization models:

- **Non-Sentiment Model**: Allocates assets using historical and real-time market data.
- **Sentiment-Adjusted Model**: Incorporates sentiment scores derived from influential tweets to adjust return forecasts.

Both models follow a **mean-variance optimization** strategy with constraints to encourage diversification.

---

## 📊 Data Sources

### 📁 Stock Data
- **Historical Data**: Pulled from Kaggle datasets
- **Real-Time Data**: Collected using Alpha Vantage API

### 🐦 Twitter Data
- Scraped tweets from public profiles of key financial and political figures
- Extracted mentions of companies, hashtags, cashtags, and timestamps

### 🧠 Sentiment Analysis
- Applied GPT-4o to score tweets per stock between -1.0 (strong negative) and 1.0 (strong positive)
- Scores dynamically weighted based on recency and speaker influence

---

## 🧮 Optimization Models

Each model solves a portfolio allocation problem where the goal is to maximize expected returns while minimizing risk (measured via portfolio variance).

### 🔹 Non-Sentiment Model


\[ \text{Objective: } \max ( \mu^{NS} \cdot x - \lambda x^T \Sigma x ) \]



### 🔹 Sentiment-Adjusted Model


\[ \text{Objective: } \max ( (\mu^{NS} + \text{Sentiment Adjustment}) \cdot x - \lambda x^T \Sigma x ) \]



Constraints:
- \(\sum x_i = 1\)
- \(x_i \geq 0\)
- \(x_i \leq \eta\) (diversification limit)

---

## 🛠️ Tech Stack

- **Languages**: Julia, Python
- **APIs**: Alpha Vantage, custom Twitter scraper
- **Optimization**: JuMP + Ipopt
- **Sentiment Analysis**: OpenAI GPT-4o
- **Visualization**: Plots.jl


---

## 🧪 Sample Results

| Metric | Without Sentiment | With Sentiment |
|--------|-------------------|----------------|
| Top Sector | Industrials | Technology |
| Top Stock  | HON (Honeywell) | SPOT (Spotify) |
| Sentiment Weight | 0 | 10 |

---

## 🔮 Future Work

- Turn this into a live service with streaming APIs
- Improve tweet filtering using entity recognition and sarcasm detection
- Expand sentiment source pool beyond just prominent figures
- Backtest performance vs market benchmarks

---

## 👨‍💻 Authors & Contributions

| Role | Will | Timothy | Shing |
|------|------|---------|-------|
| Modeling | 20% | 20% | 60% |
| Analysis | 20% | 50% | 30% |
| Data Gathering | 50% | 50% | 0% |
| Implementation | 40% | 40% | 20% |
| Report Writing | 50% | 30% | 20% |

---

## 📎 Disclaimer

This repository is an academic project and **not intended as investment advice**. Proceed cautiously when adapting these ideas to real markets.

---
