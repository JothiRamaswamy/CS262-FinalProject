from typing import List
from tasks_pb2 import ServerMessage

from tasks_pb2_grpc import TaskServiceStub

import tasks_pb2

class Client:

    def run_task(self, aws_script, gcp_script, stubs: List[TaskServiceStub]):
        fail_count = 0
        try:
            received_info = stubs[0].RunTask(tasks_pb2.ClientMessage(aws_script=aws_script, gcp_script=gcp_script))
        except:
            fail_count += 1
            try:
                received_info = stubs[1].RunTask(tasks_pb2.ClientMessage(aws_script=aws_script, gcp_script=gcp_script))
            except Exception as e:
                print(e)
                fail_count += 1
                try:
                    received_info = stubs[2].RunTask(tasks_pb2.ClientMessage(aws_script=aws_script, gcp_script=gcp_script))
                except:
                    fail_count += 1
        if fail_count == 3:
            print("No servers active or server error in running scripts")
            return 1
        print(received_info.cpu_results)
        print(received_info.gpu_results)
        return received_info