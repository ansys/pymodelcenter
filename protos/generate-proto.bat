set out_dir=./ansys/modelcenter/workflow/grpc_modelcenter/proto
python -m grpc_tools.protoc -I./grpc-modelcenter --python_out=%out_dir% --grpc_python_out=%out_dir% --pyi_out=%out_dir% ./grpc-modelcenter/*.proto

