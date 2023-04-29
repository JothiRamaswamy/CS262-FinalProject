import os
import subprocess
from joblib import Parallel, delayed
import openai


def read_script(file_path):
    with open(file_path, "r") as f:
        return f.read()


def split_tasks(script):
    openai.api_key = os.environ["OPENAI_API_KEY"]

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

    response = openai.Completion.create(
        engine="text-davinci-codex-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    output = response.choices[0].text.strip().split("---\n")

    cpu_script = output[1].strip()
    gpu_script = output[3].strip()

    return cpu_script.split("\n"), gpu_script.split("\n")


def run_task(task, task_type):
    with open(f"{task_type}_temp_script.py", "w") as f:
        f.write("\n".join(task))

    subprocess.run(["skypilot", f"{task_type}_temp_script.py"])


def main():
    script_path = "input_script.py"
    script = read_script(script_path)
    cpu_tasks, gpu_tasks = split_tasks(script)

    # Run CPU tasks sequentially
    for task in cpu_tasks:
        run_task(task, "cpu")

    # Run GPU tasks sequentially, after CPU tasks are completed
    for task in gpu_tasks:
        run_task(task, "gpu")


if __name__ == "__main__":
    main()
