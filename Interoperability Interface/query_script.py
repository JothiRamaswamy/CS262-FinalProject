import subprocess

def query_info(data):
    """
    A helper function that parses the data string and extracts relevant information.
    :param data: a string containing the data to be parsed
    :return: a dictionary containing the relevant information
    """
    info = {}
    # split data into lines
    lines = data.split("\n")
    # extract lines that start with "sky-bench"
    relevant_lines = [line for line in lines if line.startswith("sky-bench")]
    for line in relevant_lines:
        print(line)
        # split each line into fields
        fields = line.split()
        # extract resources, status, duration, and spent fields
        resources = fields[2][:3]
        status = fields[3]
        duration = fields[4]
        spent = fields[5]
        # add the information to the info dictionary
        info[resources] = [status, duration, spent]
    return info

def run_cpu_query(test=False):
    """
    A function that runs CPU queries and extracts relevant information.
    :param test: a boolean indicating whether to run the function in test mode
    :return: a string containing the relevant information
    """
    if test:
        # if in test mode, return sample data
        return "\n".join(["\t".join(["AWS", "8cpus1000000000steps", "123", "0.0123"]), "\t".join(["AWS", "8cpus5000000000steps", "456", "0.0456"])])
        
    # define the CPUs, steps, and names to query
    cpus = [8]
    steps = [1e9, 5e9, 1e10, 5e10, 1e11]
    names = []
    for cpu in cpus:
        for step in steps:
            name = f"{cpu}cpus{int(step)}steps"
            names.append(name)

    # run the queries and extract the information
    infos = []
    completed = []
    while len(completed) < len(names):
        for name in names:
            if name in completed:
                continue
            print()
            print(name, len(completed))
            # run the query
            query = f"sky bench show {name}"
            data = subprocess.getoutput(query)
            # extract relevant information from the data
            info = query_info(data)
            # check if the query has completed and add the information to the list of infos
            if 'AWS' in info and info["AWS"][0] == 'FINISHED':
                infos.append("\t".join(['AWS', name] + info['AWS']))
            if 'GCP' in info and info["GCP"][0] == 'FINISHED':
                infos.append("\t".join(['GCP', name] + info['GCP']))
            if 'AWS' in info and 'GCP' in info and info["AWS"][0] == 'FINISHED' and info["GCP"][0] == 'FINISHED':
                completed.append(name)
                if len(completed) == len(infos):
                    break

    return "\n".join(infos)

def run_gpu_query(test: bool = False) -> str:
    """
    Returns the query results of running a benchmark test on different GPUs.
    
    Args:
        test (bool): A flag indicating whether or not to run a test query.
    
    Returns:
        str: A formatted string with the benchmark test results.
    """
    # If test flag is set to True, return a test query result
    if test:
        return "\n".join(["\t".join(["AWS", "1000000steps", "123", "0.0123"]), "\t".join(["AWS", "5000000steps", "456", "0.0456"])])
    
    # Define GPUs and number of steps
    gpus = ["K80"]
    steps = [1e6, 5e6, 1e7]
    names = []
    
    # Generate query names based on GPU and number of steps
    for gpu in gpus:
        for step in steps:
            name = f"{int(step)}steps"
            names.append(name)
            name = f"{gpu}{int(step)}steps"
            names.append(name)

    infos = []
    completed = []
    
    # Continue querying until all names have been completed
    while len(completed) < len(names):
        for name in names:
            if name in completed:
                continue
            
            print(name, len(completed))
            
            # Run a benchmark test query
            query = f"sky bench show {name}"
            data = subprocess.getoutput(query)
            
            # Parse query results and append to `infos` list
            info = query_info(data)
            if 'AWS' in info and info["AWS"][0] == 'FINISHED':
                infos.append("\t".join(['AWS', name] + info['AWS']))
            if 'GCP' in info and info["GCP"][0] == 'FINISHED':
                infos.append("\t".join(['GCP', name] + info['GCP']))
            
            # Add name to `completed` list if all providers have finished and all names have been queried
            if 'AWS' in info and 'GCP' in info and info["AWS"][0] == 'FINISHED' and info["GCP"][0] == 'FINISHED':
                completed.append(name)
                if len(completed) == len(infos):
                    break

    # Return benchmark test results as a formatted string
    return "\n".join(infos)