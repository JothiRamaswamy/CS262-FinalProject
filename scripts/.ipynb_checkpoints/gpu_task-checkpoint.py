import torch
from sys import argv
import math


def task(iterations):
    device = torch.device("cuda")
    # Create 512x512 identity matrices on the GPU
    matrix_A = torch.eye(512, dtype=torch.float32, device=device)
    matrix_B = torch.eye(512, dtype=torch.float32, device=device)


    # Perform the matrix multiplications
    for _ in range(iterations):
        result = torch.matmul(matrix_A, matrix_B)


if __name__ == '__main__':
    total_iterations = int(argv[1])
    task(total_iterations)