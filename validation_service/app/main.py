from multiprocessing import Process
from grpc_server import serve
from queue_consumer import consume_messages

if __name__ == "__main__":
    p1 = Process(target=serve)
    p2 = Process(target=consume_messages)
    print("Hello")
    p1.start()
    p2.start()

    p1.join()
    p2.join()
