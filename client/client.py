import asyncio
import datetime
import random
import time
import os
import logging
import sys
import json
from dotenv import load_dotenv

import grpc

load_dotenv(dotenv_path="../.env")
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.config import settings
from proto import data_pb2_grpc, data_pb2


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_config(file_path):
    with open(file_path, 'r') as config_file:
        config = json.load(config_file)
    return config


def generate_packet(packet_seq_num, records_in_packet):
    packet_timestamp = int(time.time())

    packet_data = []
    for i in range(records_in_packet):
        record = data_pb2.Data(
            Decimal1=random.uniform(0, 100),
            Decimal2=random.uniform(0, 100),
            Decimal3=random.uniform(0, 100),
            Decimal4=random.uniform(0, 100),
            Timestamp=int(time.time())
        )
        packet_data.append(record)

    packet = data_pb2.Packet(
        PacketTimestamp=packet_timestamp,
        PacketSeqNum=packet_seq_num,
        NRecords=records_in_packet,
        PacketData=packet_data
    )

    return packet


async def run_client(config_file):
    config = read_config(config_file)

    await asyncio.sleep(4) # подождать пока сервер инцилизируется

    total_packets = config['TotalPackets']
    records_in_packet = config['RecordsInPacket']
    time_interval = config['TimeInterval']
    grpc_server_addr = config['gRPCServerAddr']
    grpc_server_port = config['gRPCServerPort']

    channel = grpc.insecure_channel(f'{grpc_server_addr}:{grpc_server_port}')
    stub = data_pb2_grpc.DataServiceStub(channel)

    all_packet_sent = True

    for packet_seq_num in range(16, total_packets + 1):
        packet = generate_packet(packet_seq_num, records_in_packet)

        try:
            response = stub.SendPacket(packet)
            logger.info("Cервер принял данные. Сохранены в БД")
            logger.info(f"Номер пакета - {packet_seq_num}. Время - {datetime.datetime.now()}")
            for record in packet.PacketData:
                logger.info(f"Данные - Decimal1: {record.Decimal1}, Decimal2: {record.Decimal2}, Decimal3: {record.Decimal3}, Decimal4: {record.Decimal4}")
        except grpc.RpcError as e:
            if e.code() == grpc.StatusCode.ALREADY_EXISTS:
                logger.error(f"Error: {e.details()} - Данные в БД уже сущетсвуют.")
            elif e.code() == grpc.StatusCode.UNKNOWN:
                print()
                logger.error(f"Произошла неизвестная ошибка: {e.details()}")
            else:
                logger.error(f"gRPC ошибка: {e.code()}, {e.details()}")

            all_packet_sent = False


        if packet_seq_num < total_packets:
            time.sleep(time_interval)


    if all_packet_sent:
        logger.info("Все пакеты отправлены успешно. Клиент завершает работу.")
    else:
        logger.info("Некоторые пакеты не были отправлены. Клиент завершает работу.")

if __name__ == '__main__':
    asyncio.run(run_client(settings.json_path.client))
