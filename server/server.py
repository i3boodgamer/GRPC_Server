import asyncio
import logging
import json
import sys
import os
from dotenv import load_dotenv

import grpc
from google.protobuf import empty_pb2

load_dotenv(dotenv_path="../.env")

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.models import db_helper, GRPCData
from core.config import settings
from proto import data_pb2_grpc


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


with open(settings.json_path.server) as config_file:
    config = json.load(config_file)


class DataServiceServicer(data_pb2_grpc.DataServiceServicer):
    async def SendPacket(self, request, context):
        async with db_helper.session_factory() as session:
            for index, record in enumerate(request.PacketData):
                data_record = GRPCData(
                    packet_seq_num=request.PacketSeqNum,
                    record_seq_num=index,
                    packet_time_stamp=request.PacketTimestamp,
                    decimal1=record.Decimal1,
                    decimal2=record.Decimal2,
                    decimal3=record.Decimal3,
                    decimal4=record.Decimal4,
                    record_time_stamp=record.Timestamp
                )
                session.add(data_record)
            await session.commit()

        return empty_pb2.Empty()


async def server():
    ser = grpc.aio.server()
    data_pb2_grpc.add_DataServiceServicer_to_server(DataServiceServicer(), ser)
    server_address = f'[::]:{config["gRPCServerPort"]}'
    ser.add_insecure_port(server_address)
    await ser.start()
    logger.info(f'gRPC сервер запущен на {server_address}')
    await ser.wait_for_termination()

if __name__ == '__main__':
    asyncio.run(server())
