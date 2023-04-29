from multiprocessing import Process
from sys import argv
import math


def task(iterations):
    x = 1
    for _ in range(iterations):
        x *= 1
    return x


if __name__ == '__main__':
    num_processes, total_iterations = int(argv[1]), int(argv[2])
    print(num_processes, total_iterations)
    remainder = total_iterations % num_processes
    process_list = []
    for i in range(num_processes):
        process_iterations = math.ceil(total_iterations / num_processes) if i < remainder else math.floor(total_iterations / num_processes)
        process_list.append(Process(target=task, args=(process_iterations,)))

    for i in process_list:
        i.start()
    for i in process_list:
        i.join()