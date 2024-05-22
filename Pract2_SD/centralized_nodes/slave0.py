import grpc, time,os,sys
from concurrent import futures
from proto import store_pb2_grpc
from store_servicer import KeyValueStoreServicer


# create a gRPC server
server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

# use the generated function `add_InsultingServiceServicer_to_server`
# to add the defined class to the server
store_pb2_grpc.add_KeyValueStoreServicer_to_server(KeyValueStoreServicer(32771,32770,32772,), server)



print('Starting server. Listening on port 32771.')
server.add_insecure_port('0.0.0.0:32771')
server.start()

# since server.start() will not block,
# a sleep-loop is added to keep alive
try:
    while True:
        time.sleep(86400)
except KeyboardInterrupt:
    server.stop(0)