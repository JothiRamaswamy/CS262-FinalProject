import yaml

def generate_yamls():
    """
    Generates YAML files with varying resource configurations for CPU and GPU tasks.
    Necessary for us to run tasks using Skypilot and measure the cost/speed of tasks.

    Returns:
        None
    """
    # Load the CPU YAML template from a file
    with open('example.yaml', 'r') as file:
        cpu_yaml_template = yaml.safe_load(file)
        
    # Define a range of CPU resources to test
    cpus = [2,4,8]

    # Define a range of computation steps to test
    steps = [1e9, 5e9, 1e10, 5e10, 1e11]

    # Generate YAML files with different CPU resources and computation steps
    for cpu in cpus:
        for step in steps:
            cpu_yaml_template['resources']['cpus'] = cpu
            cpu_yaml_template['run'] = f"python cpu_AWS_script.py {int(cpu)} {int(step)}"
            
            with open(f'./cpu_yamls/{cpu}cpus_{int(step)}steps.yaml', 'w') as file:
                yaml.dump(cpu_yaml_template, file, sort_keys=False)

    # Load the GPU YAML template from a file
    with open('gpu_example.yaml', 'r') as file:
        gpu_yaml_template = yaml.safe_load(file)

    # Define a range of computation steps to test with GPUs
    steps = [1e6, 5e6, 1e7, 5e7, 1e8]
    
    # Define a range of GPUs to test
    gpus = ['V100', "K80", "T4"]

    # Generate YAML files with different computation steps and GPUs for AWS
    for step in steps:
        gpu_yaml_template['run'] = f"python gpu_AWS_script.py {int(step)}"
        with open(f'./gpu_yamls/aws_gpu_yamls/{int(step)}steps.yaml', 'w') as file:
                yaml.dump(gpu_yaml_template, file, sort_keys=False)

    # Load the GPU YAML template from a file for GCP
    with open('gcp_example.yaml', 'r') as file:
        gpu_yaml_template = yaml.safe_load(file)

    # Define a range of computation steps to test with GPUs for GCP
    steps = [1e6, 5e6, 1e7, 5e7, 1e8]
    
    # Define a range of GPUs to test with GCP
    gpus = ['V100', "K80", "T4"]

    # Generate YAML files with different computation steps and GPUs for GCP
    for step in steps:
        for gpu in gpus:
            gpu_yaml_template['run'] = f"python gpu_GCP_script.py {int(step)}"
            gpu_yaml_template['resources']['candidates'][0]['accelerators'] = gpu
            with open(f'./gpu_yamls/gcp_gpu_yamls/{gpu}{int(step)}steps.yaml', 'w') as file:
                    yaml.dump(gpu_yaml_template, file, sort_keys=False)