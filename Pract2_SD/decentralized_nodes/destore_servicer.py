# Description: This file contains the implementation of the KeyValueStoreServicer class, which is responsible for 
#handling the gRPC requests made by the client. The KeyValueStoreServicer class implements the KeyValueStoreServicer
#interface defined in the store_pb2_grpc module. 
from proto import store_pb2, store_pb2_grpc, storage_pb2, storage_pb2_grpc
from decentralized_nodes.destore_service import store_service
import time,grpc

class KeyValueStoreServicer(store_pb2_grpc.KeyValueStoreServicer):
    def __init__(self, myport, port1, port2,weight):
        self.time = 0
        #Als ports coneguts, iniciem coneixent el d'un amic i el nostre
        self.ports = [port1,myport]
        self.weight = weight
        self.READ_QUORUM = 2
        self.WRITE_QUORUM = 3
        #ports = [myport,port1,port2]
        
        #Iniciem canal amb la base de dades
        self.db_channel = grpc.insecure_channel(f'localhost:50052')
        self.db_stub = storage_pb2_grpc.StorageServiceStub(self.db_channel)

        values = self.db_stub.GetAllValues(storage_pb2.Empty())
        for value in values.values:
            print(f"Received value from server: {value.key} - {value.data}")
            store_service.doCommit(value.key, value.data)
        
        print("elport:"+str(myport)+" port1:"+str(port1))
        

    def put(self, putRequest, context):
        quorum = self.weight
        time.sleep(self.time)
        #Ask for vote
        for port in self.ports:
            channel = grpc.insecure_channel(f'localhost:{port}') 
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            response_quorum = stub.askVote(store_pb2.AskRequest(key=putRequest.key))
            quorum = quorum + response_quorum.weight
            #print("\033[91mQuorum: "+str(quorum)+ " Weight: "+str(response_quorum.weight)+"\033[0m")
            if quorum >= self.WRITE_QUORUM:

                success = True
            else:
                success = False
        if success:
            put_response = store_service.put(putRequest.key, putRequest.value)  
            if put_response:
                for port in self.ports:
                    #print("Sending doCommit request to port: "+str(port))
                    channel = grpc.insecure_channel(f'localhost:{port}') 
                    stub = store_pb2_grpc.KeyValueStoreStub(channel)
                    #print("Sending doCommit request with key: "+putRequest.key+" value: "+putRequest.value)
                    response_docommit = stub.doCommit(store_pb2.DoCommitRequest(key=putRequest.key, value=putRequest.value))
                    #print("Put request response received with key: ")

        value = storage_pb2.Value(key=putRequest.key, data=putRequest.value)
        self.db_stub.SaveValue(value)
        response_put = store_pb2.PutResponse(success=success)
        #print("\033[91mresponse = : "+str(success)+"response put:"+ str(response_put) +"\033[0m")
        return response_put
         #comprovar si som master
        #si som master, agafar lock i two phase commit (nse ordre)

    def get(self, getRequest, context):
        #mirar si el lock esta agafat
        #si esta agafat, esperar poc temps
        #retornar valor
        value,found = store_service.get(getRequest.key)
        response = store_pb2.GetResponse()
        response.value = value
        response.found = found
        #print("Get request response received with key: " + str(response.found) +response.value)
        quorum = 0
        for port in self.ports:
            #print ("Asking for vote:"+str(port))
            channel = grpc.insecure_channel(f'localhost:{port}') 
            stub = store_pb2_grpc.KeyValueStoreStub(channel)
            response_quorum = stub.askVote(store_pb2.AskRequest(key=getRequest.key))
            #print ("Response quorum:"+str(response_quorum.weight)+str(response_quorum.value))
            if response_quorum.value == value:
                quorum = quorum + response_quorum.weight
            if quorum >= self.READ_QUORUM:
                response.found = True
            else:
                response.found = False

        time.sleep(self.time)
        return response

    def slowDown(self, slowDownRequest, context):
        try:
            self.time = slowDownRequest.seconds
            #print("SlowDown request received with seconds: " + str(self.time))
        except (AttributeError, TypeError) as e:
            # Handle specific exceptions
            self.time = 0
            return store_pb2.SlowDownResponse(success=False, error_message=str(e))
        #time.sleep(self.time)
        return store_pb2.SlowDownResponse(success=True)

    def restore(self, empty, context):
        self.time = 0
        return store_pb2.RestoreResponse(success=True)

    def askVote(self, askRequest, context):
        value = store_service.askVote(askRequest.key)
        response = store_pb2.AskResponse(weight=self.weight, value=value)
        #print("Ask sent with key: " + str(response.value))
        return response
    
    def doCommit(self, doCommitRequest, context):
        store_service.doCommit(doCommitRequest.key, doCommitRequest.value)
        response = store_pb2.google_dot_protobuf_dot_empty__pb2.Empty()
        return response
    
    def discover(self, discRequest, context):
        disc_answer = ""
        if self.ports:
            for port in self.ports:
                disc_answer = disc_answer + str(port) + ","
        response = store_pb2.DiscResponse(ports = disc_answer)
        return response

    def addPorts(self, portRequest, context):  
        fr_ports = portRequest.ports.split(",")
        for item in fr_ports:
            if item != "":
                try:
                    port = int(item)  # Convert item to integer
                    if port not in self.ports:
                        self.ports.append(port)
                except ValueError:
                    print(f"Skipping invalid port value: {item}")

        return store_pb2.google_dot_protobuf_dot_empty__pb2.Empty()

    