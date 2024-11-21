import Discrete

stocks = int(input("Enter the number of stocks: "))
stock_prices = Discrete.DiscreteSignal(stocks)
for i in range(stocks) : 
    stock = float(input("Enter the stock price: "))
    stock_prices.set_value_at_time(i, stock)

window = int(input("Enter the window size: "))
unweighted_weights = Discrete.DiscreteSignal(stocks)
weighted_weights = Discrete.DiscreteSignal(stocks)
sum = window*(window+1)/2
for i in range(window) : 
    # weight = float(input("Enter the weight: "))
    unweighted_weight = 1/window
    weighted_weight = (window-i)/sum
    print(weighted_weight)
    unweighted_weights.set_value_at_time(i, unweighted_weight)
    weighted_weights.set_value_at_time(i, weighted_weight)

lti_system1 = Discrete.LTI_Discrete(stock_prices)
lti_system2 = Discrete.LTI_Discrete(stock_prices)

output1, constituent_impulses1, coefficients1 = lti_system1.output(unweighted_weights)
output2, constituent_impulses2, coefficients2 = lti_system2.output(weighted_weights)

print(f"Unweighted Average : {output1.values[stocks+window-1:2*stocks]}")
print(f"Weighted Average : {output2.values[stocks+window-1:2*stocks]}")
print(output2.values)
lti_system2.response_of_input_plot(stock_prices)
# lti_system2.impulse_multiplied_by_coefficients_plot(stock_prices)
print(output2.values)
# print(output.values)