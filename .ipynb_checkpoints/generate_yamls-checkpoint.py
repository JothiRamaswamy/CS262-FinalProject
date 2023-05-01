import yaml
with open('example.yaml', 'r') as file:
    cpu_yaml_template = yaml.safe_load(file)
    
cpus = [2,4,8]
steps = [1e9, 5e9, 1e10, 5e10, 1e11]

for cpu in cpus:
    for step in steps:
        cpu_yaml_template['resources']['cpus'] = cpu
        cpu_yaml_template['run'] = f"python cpu_task.py {int(cpu)} {int(step)}"
        
        with open(f'./cpu_yamls/{cpu}cpus_{int(step)}steps.yaml', 'w') as file:
            yaml.dump(cpu_yaml_template, file, sort_keys=False)

with open('gpu_example.yaml', 'r') as file:
    gpu_yaml_template = yaml.safe_load(file)

steps = [1e6, 5e6, 1e7, 5e7, 1e8]
for step in steps:
    gpu_yaml_template['run'] = f"python gpu_task.py {int(step)}"
    with open(f'./gpu_yamls/{int(step)}steps.yaml', 'w') as file:
            yaml.dump(gpu_yaml_template, file, sort_keys=False)