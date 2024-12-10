from concurrent import futures
import grpc
import os
import json
from proto import dron_pb2_grpc, dron_pb2
from validators import validate_dron_data
from queue_publisher import publish_to_queue
import logging

logging.basicConfig(level=logging.INFO)
VALIDATIONSERVICE_PORT = os.getenv("VALIDATIONSERVICE_PORT", "50051")


class DronService(dron_pb2_grpc.DronValidationServicer):
    def ValidateData(self, request, context):
        message = {
            "dron_id": request.dron_id,
            "timestamp": request.timestamp,
            "temperature": request.temperature,
            "humidity": request.humidity,
            "latitude": request.latitude,
            "longitude": request.longitude,
            "token": request.token,
        }
        try:
            validate_dron_data(message)
            publish_to_queue(json.dumps(message))
            return dron_pb2.ValidationResponse(is_valid=True)
        except ValueError as e:
            context.set_details(str(e))
            context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
            return dron_pb2.ValidationResponse(is_valid=False)


def serve():
    logging.info("Start grpc")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    dron_pb2_grpc.add_DronValidationServicer_to_server(DronService(), server)
    server.add_insecure_port("[::]:50051")
    logging.info("GRPC server started on port 50051")
    server.start()
    server.wait_for_termination()
