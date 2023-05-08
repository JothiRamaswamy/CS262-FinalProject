from query_script import run_cpu_query, run_gpu_query
from gpt_split import create_script_split
from generate_yamls import generate_yamls
import tasks_pb2
import tasks_pb2_grpc


class TasksService(tasks_pb2_grpc.TaskServiceServicer):
    
    def generate_python_scripts(self, aws_script, gcp_script):
        """Generates python scripts for AWS and GCP based on user input.

        Args:
            aws_script (str): The script for AWS.
            gcp_script (str): The script for GCP.
        """
        # Writes the AWS script to a file.
        try:
            with open("aws_script.py", "w") as f:
                f.write(aws_script)
            # Writes the GCP script to a file.
            with open("gcp_script.py", "w") as f:
                f.write(gcp_script)
            return 0
        except:
            return 1
        

    def RunTask(self, request, context):
        """Runs a task requested by the client.

        Args:
            request: A request message containing the user input.
            context: The context of the gRPC call.

        Returns:
            A response message containing the results of the task.
        """
        generate_yamls()  # Generates YAML files based on the user input.
        self.generate_python_scripts(request.aws_script, request.gcp_script)  # Generates Python scripts based on the user input.
        aws_cpu_script, aws_gpu_script = create_script_split()  # Splits the AWS Python scripts into CPU and GPU parts.
        gcp_cpu_script, gcp_gpu_script = create_script_split(filename="gcp_script.py", cloud="GCP")  # Splits the GCP Python scripts into CPU and GPU parts.
        cpu_results = run_cpu_query(test=True)  # Runs a test of the CPU queries on AWS and GCP.
        print(f"finished running {aws_cpu_script}, {gcp_cpu_script}")  # Prints a message indicating that the CPU queries have finished running.
        gpu_results = run_gpu_query(test=True)  # Runs a test of the GPU queries on AWS and GCP.
        print(f"finished running {aws_gpu_script}, {gcp_gpu_script}")  # Prints a message indicating that the GPU queries have finished running.
        # Returns the results of the queries.
        return tasks_pb2.ServerMessage(cpu_results=cpu_results, gpu_results=gpu_results)
