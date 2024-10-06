from sqlalchemy import Integer, Float, TIMESTAMP, INTEGER
from sqlalchemy.orm import mapped_column

from .base import Base


class GRPCData(Base):
    packet_seq_num = mapped_column(Integer, primary_key=True)
    record_seq_num = mapped_column(Integer, primary_key=True)
    packet_time_stamp = mapped_column(INTEGER)
    decimal1 = mapped_column(Float)
    decimal2 = mapped_column(Float)
    decimal3 = mapped_column(Float)
    decimal4 = mapped_column(Float)
    record_time_stamp = mapped_column(INTEGER)
