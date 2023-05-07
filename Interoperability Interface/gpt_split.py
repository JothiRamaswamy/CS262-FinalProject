import os
import openai

def read_script(file_path):
    """
    Reads the contents of a given file and returns it as a string.
    
    Args:
        file_path (str): The path to the file to be read.
        
    Returns:
        str: The contents of the file as a string.
    """
    with open(file_path, "r") as f:
        return f.read()


def split_tasks(script):
    """
    Separates a given Python script into two scripts: one containing CPU-heavy computation tasks
    and the other containing GPU-heavy computation tasks, using OpenAI's GPT-3 model.
    
    Args:
        script (str): The Python script to be split.
        
    Returns:
        Tuple[list, list]: A tuple containing two lists of strings. The first list contains
        the lines of the CPU-heavy tasks script, and the second list contains the lines of
        the GPU-heavy tasks script.
    """
    openai.api_key = os.environ["OPEN_AI_KEY"]

    prompt = (
        f"Given the following Python script, separate it into two separate scripts: "
        f"one containing CPU-heavy computation tasks and the other containing GPU-heavy computation tasks.\n\n"
        f"---\n"
        f"{script}\n"
        f"---\n\n"
        f"CPU-heavy tasks script:\n"
        f"---\n"
        f"{{cpu_script}}\n"
        f"---\n\n"
        f"GPU-heavy tasks script:\n"
        f"---\n"
        f"{{gpu_script}}"
    )

    try:
        response = openai.Completion.create(
            engine="text-davinci-codex-003",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        output = response.choices[0].text.strip().split("---\n")

        cpu_script = output[1].strip()
        gpu_script = output[3].strip()
    except Exception as e:
        cpu_script = script
        gpu_script = script

    return cpu_script.split("\n"), gpu_script.split("\n")


def create_script_split(filename="aws_script.py", cloud="AWS"):
    """
    Reads a Python script from a file, splits it into CPU-heavy and GPU-heavy tasks scripts,
    and saves each of them to a separate file.
    
    Args:
        filename (str, optional): The name of the file containing the Python script to be split.
            Defaults to "aws_script.py".
        cloud (str, optional): The cloud provider to use for the scripts. Defaults to "AWS".
        
    Returns:
        Tuple[str, str]: A tuple containing the names of the files that contain the CPU-heavy and
        GPU-heavy tasks scripts, respectively.
    """
    script_path = filename
    script = read_script(script_path)
    cpu_tasks, gpu_tasks = split_tasks(script)

    cpu_filename = f"cpu_{cloud}_script.py"
    gpu_filename = f"gpu_{cloud}_script.py"
    with open(cpu_filename, "w") as f:
        f.write("\n".join(cpu_tasks))

    with open(gpu_filename, "w") as f:
        f.write("\n".join(gpu_tasks))

    return (cpu_filename, gpu_filename)

if __name__ == "__main__":
    create_script_split()
