from datetime import datetime
import math
from multiprocessing import Process


def task(iterations):
    x = 0
    for _ in range(iterations):
        x += 1
    return x


if __name__ == '__main__':
    start_time = datetime.now()
    try:
        num_processes = int(input("How many processes would you like to run?"))
        total_iterations = int(input("How many iterations would you like to run?"))
    except:
        num_processes = 2
        total_iterations = 100000
    print(num_processes, total_iterations)
    remainder = total_iterations % num_processes
    process_list = []
    for i in range(num_processes):
        process_iterations = math.ceil(total_iterations / num_processes) if i < remainder else math.floor(total_iterations / num_processes)
        process_list.append(Process(target=task, args=(process_iterations,)))
    try:
        # start the processes
        for i in process_list:
            i.start()
        # wait for the processes to finish
        for i in process_list:
            i.join()
    except KeyboardInterrupt:
        pass
    end_time = datetime.now()
    print(end_time - start_time)
