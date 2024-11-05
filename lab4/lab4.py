"""
Vezbe, dvocas 4
"""


#%%
# Zadatak 1
def compute_product(*numbers, squared=False):
    # Option 1
    # p = 1
    # for number in numbers:
    #     p *= number**2 if squared else number
    # return p
    # Option 2
    from functools import reduce
    return reduce(lambda a,b: a * b, [n**2 if squared else n for n in numbers])


#%%
# print(compute_product(1,-4,13,2))
# print(compute_product(1, -4, 13, 2, squared=True))
# print()
# # Calling the compute_product function with a list
num_list = [2, 7, -11, 9, 24, -3]
# # This is NOT a way to make the call:
# print("Calling the function by passing a list as the argument")
# print(compute_product(num_list))
# print()
# # instead, this is how it should be done (the * operator is 'unpacking' the list):
print("Calling the function by passing an UNPACKED list as the argument")
print(compute_product(*num_list))

#%%
# Zadatak 2

def select_strings(*strings, threshold=3):
    # Option 1
    # selection = []
    # for string in strings:
    #     if string.lower()[0] == string.lower()[-1] and len(set(string)) > threshold:
    #         selection.append(string)
    # return selection
    # Option 2
    # return [s for s in strings if s.lower()[0] == s.lower()[-1] and len(set(s)) > threshold]
    # Option 3
    return list(filter(lambda s: s.lower()[0] == s.lower()[-1] and len(set(s)) > threshold, strings))


#%%
str_list = ['yellowy', 'Bob', 'lovely', 'Yesterday', 'too']
print(select_strings(*str_list))

#%%
# Zadatak 3

# (order_id, product_name, quantity, price_per_item)
# <order_id: total_price>
def process_product_orders(orders, discount=None, shipping_cost=10):
    # Option 1
    # d = dict()
    # for order_id, product_name, quantity, price_per_item in orders:
    #     tot_price = quantity * price_per_item
    #     if discount:
    # #        tot_price = tot_price * (1 - discount/100)
    #         tot_price *= (1 - discount/100)
    #     if tot_price < 100:
    #         tot_price += shipping_cost
    #     d[order_id] = tot_price
    # return d
    # Option 2
    def compute_tot_price(order):
        _, _, quantity, price_per_item = order
        tot_price = quantity * price_per_item
        if discount:
            tot_price *= (1 - discount/100)
        return tot_price if tot_price > 100 else tot_price + shipping_cost

    # return {order[0]: compute_tot_price(order) for order in orders}
    # Option 3
    return dict(map(lambda order: (order[0], compute_tot_price(order)), orders))


#%%
orders = [("34587", "Learning Python, Mark Lutz", 4, 40.95),
          ("98762", "Programming Python, Mark Lutz", 5, 56.80),
          ("77226", "Head First Python, Paul Barry", 3, 32.95),
          ("88112", "Einführung in Python3, Bernd Klein", 3, 24.99)]

print(process_product_orders(orders))
print()
print("The same orders with discount of 10%")
print(process_product_orders(orders, discount=10))

#%%
# Zadatak 4
import functools
def timer(func):
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):

        # Nešto uradite pre
        from time import perf_counter
        start_time = perf_counter()

        value = func(*args, **kwargs)

        # Nešto uradite posle
        working_time = perf_counter() - start_time
        print(f"Function {func.__name__} completed its task in {working_time:.4f} seconds")

        return value
    return wrapper_timer


#%%
# Zadatak 4.1
@timer
def compute_sum_loop(n):
    sum_of_sums = 0
    for x in range(n+1):
        # S(x) = 1 + 2 + ... + x-1 + x
        for i in range(x + 1):
            sum_of_sums += i
    return sum_of_sums

@timer
def compute_sum_lc(n):
    return sum([sum(range(x+1)) for x in range(n+1)])

@timer
def compute_sum_mr(n):
    from functools import reduce
    mapping = map(lambda x: sum(range(x+1)), range(n+1))
    return reduce(lambda a,b: a + b, mapping)


#%%
print(compute_sum_loop(10000))
print()
print(compute_sum_lc(10000))
print()
print(compute_sum_mr(10000))

#%%
# Zadatak 4.2

@timer
def mean_median_diff(n, k, iterations=10):
    from random import randint, seed
    from statistics import mean, median

    seed(1)
    diffs = []
    for _ in range(iterations):
        random_numbers = []
        for _ in range(n):
            random_numbers.append(randint(1, k))
        diffs.append(mean(random_numbers) - median(random_numbers))

    for i, diff in enumerate(diffs):
        print(f"Iteration {i+1}: {diff:.4f}")

    print()
    print(f"Average difference across all iterations: {mean(diffs):.4f}")


#%%
mean_median_diff(100, 250, iterations=20)


#%%
#Zadatak 5

def standardiser(func):
    @functools.wraps(func)
    def wrapper_standardiser(*args, **kwargs):

        # Nešto uradite pre
        if all([isinstance(arg, (int, float)) for arg in args]):
            from statistics import mean, stdev
            m = mean(args)
            sd = stdev(args)
            args = [(arg - m)/sd for arg in args]
        else:
            print("Not all positional arguments are numbers. Keeping the arguments as given")

        func_str = f"Calling function {func.__name__} with positional arguments: "
        func_str += ", ".join([f'{arg:.4f}' for arg in args])
        if kwargs:
            func_str += "\nand keyword arguments: " + ", ".join(f"{key}={val}" for key, val in kwargs.items())
        print(func_str)

        value = func(*args, **kwargs)

        # Nešto uradite posle
        value = round(value, 4)

        return value
    return wrapper_standardiser



#%%
# Zadatak 5.1

@standardiser
def sum_of_sums(*numbers, n=10):
    return sum([sum([x**i for i in range(n+1)]) for x in numbers])


#%%
print(sum_of_sums(1,3,5,7,9,11,13, n=7))

