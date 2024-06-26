# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import storage_pb2 as storage__pb2


class StorageServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SaveValue = channel.unary_unary(
                '/storage.StorageService/SaveValue',
                request_serializer=storage__pb2.Value.SerializeToString,
                response_deserializer=storage__pb2.Empty.FromString,
                )
        self.GetValue = channel.unary_unary(
                '/storage.StorageService/GetValue',
                request_serializer=storage__pb2.Key.SerializeToString,
                response_deserializer=storage__pb2.Value.FromString,
                )
        self.GetAllValues = channel.unary_unary(
                '/storage.StorageService/GetAllValues',
                request_serializer=storage__pb2.Empty.SerializeToString,
                response_deserializer=storage__pb2.ValueList.FromString,
                )


class StorageServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SaveValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetValue(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetAllValues(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_StorageServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SaveValue': grpc.unary_unary_rpc_method_handler(
                    servicer.SaveValue,
                    request_deserializer=storage__pb2.Value.FromString,
                    response_serializer=storage__pb2.Empty.SerializeToString,
            ),
            'GetValue': grpc.unary_unary_rpc_method_handler(
                    servicer.GetValue,
                    request_deserializer=storage__pb2.Key.FromString,
                    response_serializer=storage__pb2.Value.SerializeToString,
            ),
            'GetAllValues': grpc.unary_unary_rpc_method_handler(
                    servicer.GetAllValues,
                    request_deserializer=storage__pb2.Empty.FromString,
                    response_serializer=storage__pb2.ValueList.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'storage.StorageService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class StorageService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SaveValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.StorageService/SaveValue',
            storage__pb2.Value.SerializeToString,
            storage__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetValue(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.StorageService/GetValue',
            storage__pb2.Key.SerializeToString,
            storage__pb2.Value.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetAllValues(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/storage.StorageService/GetAllValues',
            storage__pb2.Empty.SerializeToString,
            storage__pb2.ValueList.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
