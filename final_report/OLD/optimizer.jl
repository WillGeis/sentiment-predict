using CSV
using DataFrames
using Statistics
using JuMP
using Ipopt

# Load stock data
stock_data = CSV.read("master_stocks.csv", DataFrame)

function compute_returns(df)
    df = sort(df, :ticker)
    returns = [missing; diff(df.close) ./ df.close[1:end-1]]
    df[!, :return] = returns
    return df
end

returns_data = combine(groupby(stock_data, :ticker), compute_returns) # Compute returns
returns_wide = unstack(returns_data, :ticker, :return; combine=mean)
returns_wide_clean = dropmissing(returns_wide) # Drop rows with missing returns

clean_stocks = names(returns_wide_clean) # Stocks that have all data
valid_stock_data = filter(row -> row[:ticker] in clean_stocks, stock_data)
returns_matrix = Matrix{Float64}(returns_wide_clean[:, clean_stocks])

sigma = cov(returns_matrix) # Compute the covariance matrix for the returns (sigma)

mu = Float64[]

for stock in clean_stocks
    timepoints = subset(valid_stock_data, :ticker => ByRow(==(stock)))
    expected_return = 0.0
    for time in eachrow(timepoints)
        ret = (time[:open] - time[:close]) / time[:open]
        expected_return += ret
    end
    expected_return /= 100

    if ismissing(expected_return) || isnan(expected_return) || isinf(expected_return) # Bad stock catch
        println("stock dropped: $stock")
        continue
    end

    push!(mu, expected_return)
end

extra_elements_needed = size(sigma, 1) - length(mu)
if extra_elements_needed > 0 # If extra elements are needed, add duplicate entries to mu, manually fix data later
    println("Adding $extra_elements_needed duplicate entries to mu.")
    push!(mu, repeat([mu[end]], extra_elements_needed)...)
end

lambda = 0.5
model = Model(Ipopt.Optimizer)
n_stocks = length(mu)

@variable(model, x[1:n_stocks] >= 0)
@constraint(model, sum(x) == 1)
@objective(model, Min, -mu' * x + lambda * (x' * sigma * x))

optimize!(model)

println("Optimal allocation: ", value.(x))
println("Max_val: ", maximum(value.(x)))
println("Optimal Objective: ", objective_value(model))

stocks_info = [(clean_stocks[i], value(x[i]), mu[i]) for i in 1:n_stocks]

# Sort stocks by optimal allocation (descending) for risk categorization
sorted_stocks = sort(stocks_info, by = x -> x[2], rev=true)

# Write to CSV
csv_filename = "topstocks.csv"
CSV.write(csv_filename, DataFrame(Stock = [stock[1] for stock in sorted_stocks],
                                 Allocation = [stock[2] for stock in sorted_stocks],
                                 ExpectedReturn = [stock[3] for stock in sorted_stocks]))

println("Results saved to $csv_filename.")

# Write to TXT
txt_filename = "topstocks.txt"
open(txt_filename, "w") do f
    println(f, "Top Stocks")
    for i in (length(sorted_stocks))
        stock = sorted_stocks[i]
        println(f, "$i. $(stock[1]) - Estimated Return: $(stock[3])")
    end
end

println("Results saved to $txt_filename.")
