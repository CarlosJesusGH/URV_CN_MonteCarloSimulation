import monte_carlo_cpp
import numpy as np

A = np.array([[1,2,1],
              [2,1,0],
              [-1,1,2]])


#print("add="); print(monte_carlo_cpp.add(5,3))
#print("random_number="); print(monte_carlo_cpp.random_number())
print("monte carlo=", monte_carlo_cpp.simulate(A))
print('example.det(A) = \n', monte_carlo_cpp.det(A))
