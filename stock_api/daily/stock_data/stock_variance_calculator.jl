using CSV
using DataFrames
using Statistics

df = CSV.read("master_stocks.csv", DataFrame)
grouped = groupby(df, :ticker)

results = DataFrame(
    ticker = String[],
    open_variance = Union{Missing, Float64}[],
    high_variance = Union{Missing, Float64}[],
    low_variance = Union{Missing, Float64}[],# IHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIA
    close_variance = Union{Missing, Float64}[],
    volume_variance = Union{Missing, Float64}[],
)

for g in grouped
    push!(results, (
        ticker = first(g.ticker), # IHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIA
        open_variance = var(g.open),
        high_variance = var(g.high),
        low_variance = var(g.low),
        close_variance = var(g.close),# IHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIAIHATEJULIA
        volume_variance = var(g.volume),
    ))
end

CSV.write("master_stock_variance.csv", results)
# Write the results to a CSV file ----> for the future change this otherwise you WILL get an error (I think)
println("Variance data was written to master_stock_variance.csv.")


