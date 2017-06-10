# FROM: https://stackoverflow.com/questions/20548628/how-to-do-parallel-programming-in-python
from multiprocessing import Pool


def solve(num, letter):
    for i in range(num):
        print(letter + ": " + str(i))

pool = Pool()
result1 = pool.apply_async(solve, [5000000, 'A'])    # evaluate "solve1(A)" asynchronously
result2 = pool.apply_async(solve, [5000000, 'B'])    # evaluate "solve2(B)" asynchronously
answer1 = result1.get(timeout=10)
answer2 = result2.get(timeout=10)