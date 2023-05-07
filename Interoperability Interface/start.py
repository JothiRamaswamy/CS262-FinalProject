
import os
import sys
import grpc

from client import Client

import tasks_pb2_grpc

from server import TasksService
from concurrent import futures

def start_client(this_client, stubs):
  """
    Start a client to get user input for AWS and GCP script paths, read the files, 
    and then run the `run_task` function on the input scripts.
    
    Parameters:
    this_client (class): An instance of the TasksClient class.
    stubs (dict): A dictionary containing stubs for connecting to the grpc server.

    Returns:
    None
    """
  while(True):
    try:
      aws_script = input("AWS text script path for us to run on the cloud: ")
      try:
        with open(aws_script) as f:
          aws_script_text = f.read()
      except:
        print("File invalid")
        continue
      gcp_script = input("GCP text script path for us to run on the cloud: ")
      try:
        with open(gcp_script) as f:
          gcp_script_text = f.read()
      except:
        print("File invalid")
        continue

      # Call the run_task function to execute the user's input scripts
      this_client.run_task(aws_script=aws_script_text, gcp_script=gcp_script_text, stubs=stubs)
      
    except KeyboardInterrupt:
      print("\nExiting...")
      break


if __name__ == "__main__":

  SERVER_HOST = "localhost:3001"
  SERVER_HOST_BACKUP_1 = "localhost:3002"
  SERVER_HOST_BACKUP_2 = "localhost:3003"

  if len(sys.argv) < 2:
    print("please specify running client or server")

# if the client is specified as what the user wants to start, connect grpc to server host, create
# client, start background listener thread, and direct to start menu 
  elif sys.argv[1] == "client":
    os.system('clear') # clear terminal on start for client
    with grpc.insecure_channel(SERVER_HOST) as channel:
      with grpc.insecure_channel(SERVER_HOST_BACKUP_1) as channel1:
        with grpc.insecure_channel(SERVER_HOST_BACKUP_2) as channel2: # channel to connect grpc, make calls
          stub = tasks_pb2_grpc.TaskServiceStub(channel)
          stub1 = tasks_pb2_grpc.TaskServiceStub(channel1)
          stub2 = tasks_pb2_grpc.TaskServiceStub(channel2)
          client = Client()

          start_client(client, [stub, stub1, stub2])


# if the server is specified as what the user wants to start, connect grpc server, create server
# object, and start it
  elif sys.argv[1] == "server":
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), options=(('grpc.so_reuseport', 0),))
    HOST = SERVER_HOST
    try:
      server.add_insecure_port(SERVER_HOST)
    except RuntimeError:
      try:
        HOST = SERVER_HOST_BACKUP_1
        server.add_insecure_port(SERVER_HOST_BACKUP_1)
      except RuntimeError:
        HOST = SERVER_HOST_BACKUP_2
        server.add_insecure_port(SERVER_HOST_BACKUP_2)
    service = TasksService()
    tasks_pb2_grpc.add_TaskServiceServicer_to_server(service, server)
    os.system('clear')
    print("[STARTING] Server is starting at IPv4 Address " + HOST + " ...")
    server.start()
    try:
      server.wait_for_termination()
    except KeyboardInterrupt:
      print("\nExiting...")
      pass

  else:
    print("please specify running client or server")