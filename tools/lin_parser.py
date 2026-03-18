import serial


def decode_pid(pid):
    frame_id = pid & 0x3F

    id0 = (frame_id >> 0) & 1
    id1 = (frame_id >> 1) & 1
    id2 = (frame_id >> 2) & 1
    id3 = (frame_id >> 3) & 1
    id4 = (frame_id >> 4) & 1
    id5 = (frame_id >> 5) & 1

    p0_calc = id0 ^ id1 ^ id2 ^ id4
    p1_calc = ~(id1 ^ id3 ^ id4 ^ id5) & 1

    p0 = (pid >> 6) & 1
    p1 = (pid >> 7) & 1

    parity_ok = (p0 == p0_calc) and (p1 == p1_calc)

    return frame_id, parity_ok


def checksum(pid, data, enhanced=True):

    if enhanced:
        values = [pid] + list(data)
    else:
        values = list(data)

    s = sum(values)

    while s > 0xFF:
        s = (s & 0xFF) + (s >> 8)

    return (~s) & 0xFF


def main():

    ser = serial.Serial("COM7", 19200, timeout=1)

    buffer = bytearray()

    while True:

        data = ser.read(64)

        if not data:
            continue

        buffer.extend(data)

        while len(buffer) >= 4:

            # break + sync
            if buffer[0] != 0x00 or buffer[1] != 0x55:
                buffer.pop(0)
                continue

            pid = buffer[2]

            found = False

            for length in range(1, 9):

                frame_len = 2 + 1 + length + 1

                if len(buffer) < frame_len:
                    break

                data_bytes = buffer[3:3+length]
                cs = buffer[3+length]

                cs_enh = checksum(pid, data_bytes, True)
                cs_cls = checksum(pid, data_bytes, False)

                if cs in (cs_enh, cs_cls):

                    frame_id, parity_ok = decode_pid(pid)

                    print(
                        f"ID:{frame_id:02X} "
                        f"DATA:{' '.join(f'{b:02X}' for b in data_bytes)} "
                        f"CS:{cs:02X} "
                        f"LEN:{length}"
                    )

                    del buffer[:frame_len]
                    found = True
                    break

            if not found:
                buffer.pop(0)


if __name__ == "__main__":
    main()
