import grpc, time
from concurrent import futures
import store_pb2_grpc, store_pb2

from decentralized_nodes.destore_servicer import KeyValueStoreServicer

# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

myport = 32782
port1 = 32780


print('Starting server. Listening on port 32782.')
server.add_insecure_port(f'0.0.0.0:{myport}')
server.start()
# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(32782,32781,32780,1), server)

time.sleep(0.5)

friend_channel = grpc.insecure_channel(f'localhost:{port1}')
friend_stub = store_pb2_grpc.KeyValueStoreStub(friend_channel)


my_channel = grpc.insecure_channel(f'localhost:{myport}')
my_stub = store_pb2_grpc.KeyValueStoreStub(my_channel)


friends_ports = friend_stub.discover(store_pb2.DiscRequest(port=port1))

print("Friend Ports: " + friends_ports.ports)

my_stub.addPorts(store_pb2.portRequest(ports=friends_ports.ports))


# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)