using CSV
using DataFrames
using Statistics
using JSON

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

function output_json(data::DataFrame, filename::String)
    # DF => Dict for JSON conversion
    json_data = Dict("stocks" => [])
    for row in eachrow(data)
        push!(json_data["stocks"], Dict("ticker" => row[:ticker], "return" => row[:return]))
    end

    # /W to json
    open(filename, "w") do f
        JSON.print(f, json_data)
    end
    println("Data written to $filename")
end

function main()
    filename = "stocks.csv"
    output_file = "top_stocks.json"  # name file

    if !isfile(filename)
        println("File $filename not found.")
        return
    end
    
    df = load_stock_data(filename)
    returns_df = compute_returns(df)
    
    println("Top performing stocks:")
    show(first(returns_df, 5))  # display for debugginig

    output_json(returns_df, output_file)
end

main()