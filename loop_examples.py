## Ultra basic loop
# 6.58 seconds
import time

start = time.time()
total_sum = 0
for i in range(100000000):
    total_sum += i
print(f'Sum: {total_sum}')
print(f'For loop: {time.time() - start} seconds')

## Built-in functions loop
# 0.84 seconds
import time

start = time.time()
total_sum = sum(range(100000000))
print(f'Sum: {total_sum}')
print(f'Sum/range: {time.time() - start} seconds')

## Numpy vectorized loop
# 0.22 seconds
import time
import numpy as np

start = time.time()
total_sum = np.sum(np.arange(100000000))
print(f'Sum: {total_sum}')
print(f'Duration: {time.time() - start} seconds')

## Ultra basic loop with conditions and manual computations
# 15.7 seconds
import time
import numpy as np

random_scores = np.random.randint(1, 100, size=100000010)
start = time.time()
count_failed = 0
sum_failed = 0
for score in random_scores:
    if score < 70:
        sum_failed += score
        count_failed += 1
print(sum_failed/count_failed)
print(f'For Loop: {time.time() - start} seconds')

## Numpy conditional loop with built-in computations
# 0.78 seconds
import time
import numpy as np

random_scores = np.random.randint(1, 100, size=100000010)
start = time.time()
mean_failed = (random_scores[random_scores < 70]).mean()
print(mean_failed)
print(f'Numpy: {time.time() - start} seconds')
