using CSV
using DataFrames
using Statistics

# Load CSV files
tickers_sectors = CSV.read("tickers_with_sectors.csv", DataFrame)
sentiment_data = CSV.read("stock_sentiment_complete.csv", DataFrame)
unique_sectors = CSV.read("unique_sectors.csv", DataFrame)

rename!(tickers_sectors, [:Ticker, :Sector])
rename!(unique_sectors, [:Sector])

merged = innerjoin(sentiment_data, tickers_sectors, on=:Ticker)
filtered = semijoin(merged, unique_sectors, on=:Sector)

# average group sentiment
grouped = combine(groupby(filtered, :Sector), 
    :Sentiment_Score => mean => :Average_Sentiment_Score,
    :Mention_Count => sum => :Total_Mentions)

# Save the result
CSV.write("sector_sentiment.csv", grouped)
