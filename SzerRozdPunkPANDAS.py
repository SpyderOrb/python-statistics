import numpy as np
import pandas as pd

n = 4
#Xi = list(map(int, input('Xi: ').strip().split()))[:n]

#Fi = list(map(int, input('Fi: ').strip().split()))[:n]
# Fi = np.array(Fi, dtype=np.float64)

Xi = [1, 2, 3, 4]
Xi = np.array(Xi)

print(Xi)
print(Xi.shape)
print(Xi.ndim)
print(Xi.size)
print(Xi.dtype)
print(Xi.mean(axis=0))
rand_arr = np.random.random((5,))
print(rand_arr)

Fi = [-1, -5, -7, -9]
Fi = np.array(Fi)

Xi = np.concatenate((Fi, Xi))
print(Xi)
# Xi = np.array_split(Xi, 4)
# print(Xi)
print(Xi[Xi < 2])

matrix = np.array([(1, 2, 3), (4, 5, 6)])
print(matrix)
print(matrix.shape)
matrix_rand = np.random.randint(2, 5, (2, 2))
print(matrix_rand)
new_matrix = np.arange(12).reshape(3, 4)
print(new_matrix)
print('\n')
n_matrix = np.arange(6)
n_matrix = n_matrix[np.newaxis, :]
print(n_matrix)
