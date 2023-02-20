mkdir ansys\modelcenter\workflow\grpc_modelcenter\proto
python -m grpc_tools.protoc -I./protos --python_out=./ansys/modelcenter/workflow/grpc_modelcenter/proto --grpc_python_out=./ansys/modelcenter/workflow/grpc_modelcenter/proto ./protos/modelcenter.proto

