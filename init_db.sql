CREATE TABLE IF NOT EXISTS grpc_data (
    packet_seq_num INTEGER,
    record_seq_num INTEGER,
    packet_time_stamp INTEGER,
    decimal1 FLOAT,
    decimal2 FLOAT,
    decimal3 FLOAT,
    decimal4 FLOAT,
    record_time_stamp INTEGER,
    PRIMARY KEY (packet_seq_num, record_seq_num)
);