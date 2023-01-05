# l = [18, 15, 14, 12, 9, 10, 8, 7, 6, 2, 1]
# previous = 10000

# for num in range(len(l)):
#     if l[num] > previous:
#         l[num - 1] = l[num]
#         l[num] = previous
#     previous = l[num]
# print(l)



# d = {
#     "A": [3, 1, 10, 21],
#     "B": [15, 20, 16, 6, 3],
#     "C": [4, 5, 6, 7, 9, 10]
# }

# nums = []

# for key, value in d.items():
#     for num in d[key]:
#         if num % 5 == 0:
#             nums.append(num)

# set_nums = set(nums)

# print(set_nums)



# prices = {"banana": 5}

# def is_available(prices, key):
#     if key in prices:
#         return True
#     else:
#         return False

# print(is_available(prices, "kiwi"))



# prices = {"banana": 5, "kiwi": 6}

# def print_prices(prices):
#     for key, value in prices.items():
#         print(f"{key} ${value}")

# print_prices(prices)



# prices = {"banana": "5$", "kiwi": "6$"}

# def calculate_total_price(prices, basket):
#     price = 0

#     for key, value in basket.items():
#         price_string = prices[key]
#         price_string = price_string[:-1]
#         price += int(price_string) * value
#     return price

# basket1 = {"banana": 1, "kiwi": 3}
# print(calculate_total_price(prices, basket1))



# print("{1}{1}{0}".format("UC", "SC"))