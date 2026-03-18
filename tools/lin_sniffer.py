import serial
import argparse
import time
import os


class LinParser:

    def __init__(self):
        self.buffer = bytearray()

    def decode_pid(self, pid):
        return pid & 0x3F

    def checksum(self, pid, data, enhanced=True):

        if enhanced:
            values = [pid] + list(data)
        else:
            values = list(data)

        s = sum(values)

        while s > 0xFF:
            s = (s & 0xFF) + (s >> 8)

        return (~s) & 0xFF

    def parse_stream(self, data):

        frames = []

        self.buffer.extend(data)

        while len(self.buffer) >= 4:

            if self.buffer[0] != 0x00 or self.buffer[1] != 0x55:
                self.buffer.pop(0)
                continue

            pid = self.buffer[2]

            found = False

            for length in range(1, 9):

                frame_len = 2 + 1 + length + 1

                if len(self.buffer) < frame_len:
                    break

                payload = self.buffer[3:3 + length]
                cs = self.buffer[3 + length]

                if cs in (
                        self.checksum(pid, payload, True),
                        self.checksum(pid, payload, False)
                ):

                    frames.append((pid, payload, cs))

                    del self.buffer[:frame_len]

                    found = True
                    break

            if not found:
                self.buffer.pop(0)

        return frames


class LinSniffer:

    def __init__(self, port, baud):

        self.ser = serial.Serial(port, baud, timeout=0)

        self.parser = LinParser()

        self.pid_table = {}

    def process(self):

        data = self.ser.read(self.ser.in_waiting or 1)

        frames = self.parser.parse_stream(data)

        now = time.time()

        updated = False

        for pid, payload, cs in frames:

            frame_id = pid & 0x3F

            entry = self.pid_table.get(frame_id)

            if entry is None:

                self.pid_table[frame_id] = {
                    "data": payload,
                    "cs": cs,
                    "count": 1,
                    "last": now,
                    "period": None
                }

            else:

                period = (now - entry["last"]) * 1000

                entry["last"] = now
                entry["data"] = payload
                entry["cs"] = cs
                entry["count"] += 1
                entry["period"] = period

            updated = True

        return updated

    def print_table(self):

        os.system("cls" if os.name == "nt" else "clear")

        print("LIN Reverse Engineering Sniffer\n")

        print("PID    COUNT   PERIOD(ms)   CS   DATA")
        print("--------------------------------------------------------")

        for pid in sorted(self.pid_table):

            e = self.pid_table[pid]

            if e["period"] is None:
                period = "-"
            else:
                period = f"{e['period']:.1f}"

            data_str = " ".join(f"{b:02X}" for b in e["data"])

            print(
                f"{pid:02X}    "
                f"{e['count']:6d}    "
                f"{period:>8}    "
                f"{e['cs']:02X}   "
                f"{data_str}"
            )


def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--port", default="COM7")
    parser.add_argument("--baud", type=int, default=19200)

    args = parser.parse_args()

    sniffer = LinSniffer(args.port, args.baud)

    print("Starting LIN sniffer...")
    print(f"Port: {args.port}  Baud: {args.baud}\n")

    try:

        while True:

            updated = sniffer.process()

            if updated:
                sniffer.print_table()

            time.sleep(0.01)

    except KeyboardInterrupt:

        print("\nStopping sniffer...")

    finally:

        sniffer.ser.close()
        print("Serial closed.")


if __name__ == "__main__":
    main()