import time
import torch
import sys

def matrix_multiplication(device):
    n = 4096*8
    a = torch.randn(n, n, device=device)
    b = torch.randn(n, n, device=device)
    c = torch.matmul(a, b)

def convolution(device):
    n = 128
    in_channels = 128
    out_channels = 256
    kernel_size = 3
    input_tensor = torch.randn(n, in_channels, n, n, device=device)
    conv_layer = torch.nn.Conv2d(in_channels, out_channels, kernel_size, padding=1).to(device)
    output_tensor = conv_layer(input_tensor)

def memory_transfer(device):
    n = 4096*5
    a = torch.randn(n, n)
    b = a.to(device)
    c = b.to('cpu')

def benchmark(device_name):
    # print(f"Running benchmark on {device_name}")
    device = torch.device(device_name)

    start_time = time.time()
    matrix_multiplication(device)
    elapsed_time = time.time() - start_time
    # print(f"Matrix multiplication time: {elapsed_time:.2f} seconds")

    start_time = time.time()
    convolution(device)
    elapsed_time = time.time() - start_time
    # print(f"Convolution time: {elapsed_time:.2f} seconds")

    start_time = time.time()
    memory_transfer(device)
    elapsed_time = time.time() - start_time
    # print(f"Memory transfer time: {elapsed_time:.2f} seconds")

if __name__ == "__main__":
    if not torch.cuda.is_available():
        # print("CUDA is not available on your system. Exiting.")
        sys.exit(1)

    # Run the benchmark on the GPU
    device_name = "cuda:0"
    benchmark(device_name)
    torch.cuda.empty_cache()

