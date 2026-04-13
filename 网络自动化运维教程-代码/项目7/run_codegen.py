"""Generates protocol messages and gRPC stubs."""

from grpc_tools import protoc
# 编译huawei-grpc-dialout.proto文件
protoc.main(
    (
        '',
        '-I./proto',
        '--python_out=.',
        '--grpc_python_out=.',
        './proto/huawei-grpc-dialout.proto', #文件路径
    )
)
# 编译huawei-telemetry.proto文件
protoc.main(
    (
        '',
        '-I./proto',
        '--python_out=.',
        '--grpc_python_out=.',
        './proto/huawei-telemetry.proto',
    )
)
# 编译huawei-devm.proto文件
protoc.main(
    (
        '',
        '-I./proto',
        '--python_out=.',
        '--grpc_python_out=.',
        './proto/huawei-devm.proto',
    )
)
