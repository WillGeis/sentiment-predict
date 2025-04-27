using CSV
using DataFrames
using Statistics

df = CSV.read("top_stocks_data.csv", DataFrame)
grouped = groupby(df, :ticker)

results = DataFrame(
    ticker = String[],
    open_variance = Float64[],
    high_variance = Float64[],
    low_variance = Float64[], # IHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIA
    close_variance = Float64[],
    volume_variance = Float64[],
)

for g in grouped
    push!(results, (
        ticker = first(g.ticker),
        open_variance = var(g.open),
        high_variance = var(g.high),
        low_variance = var(g.low),# IHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIA
        close_variance = var(g.close),
        volume_variance = var(g.volume),
    ))
end

# Write the results to a CSV file ----> for the future change this otherwise you WILL get an error (I think)
CSV.write("stock_variance.csv", results)

println("Variance data was written to stock_variance.csv.")
