using CSV
using DataFrames
using Statistics

function load_stock_data(filename::String)
    println("Loading data from $filename...")
    return CSV.read(filename, DataFrame)
end

function compute_returns(df::DataFrame)
    grouped = groupby(df, :ticker)  # group by ticker
    result = DataFrame(:ticker => String[], :return => Float64[])
    
    for g in grouped
        sorted = sort(g, :timestamp)
        
        if nrow(sorted) >= 2
            first_close = parse(Float64, sorted[1, :close])  # first close price
            last_close = parse(Float64, sorted[end, :close])  # last close price
            ret = (last_close - first_close) / first_close
            push!(result, (sorted[1, :ticker], ret))
        end
    end
    return sort(result, :return, rev=true)  # sort by returns
end

function output_csv(data::DataFrame, filename::String)
    CSV.write(filename, data)
    println("Data written to $filename")
end

function main()
    filename = "stocks.csv"
    output_file = "top_stocks.csv"  # now outputs to CSV

    if !isfile(filename)
        println("File $filename not found.")
        return
    end
    
    df = load_stock_data(filename)
    returns_df = compute_returns(df)
    
    println("Top performing stocks:")
    show(first(returns_df, 5))  # display for debugging

    output_csv(returns_df, output_file)
end

main()
