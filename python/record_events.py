import asyncio


async def listen(rm_host):

    device = "/dev/input/event1"

    # The async subprocess library only accepts a string command, not a list.
    command = f"ssh -o ConnectTimeout=2 {rm_host} cat {device}"

    proc = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )

    try:

        x = 0
        y = 0
        pressure = 0
        distance = 0
        tilt_x = 0
        tilt_y = 0

        print("time,x,y,pressure,distance,tilt_x,tilt_y")

        # Keep looping as long as the process is alive.
        # Terminated websocket connection is handled with a throw.
        while proc.returncode is None:

            buf = await proc.stdout.read(16)
            assert len(buf) == 16

            a = buf[0:8]  # for timestamp
            b = buf[8:12]  # for type and code
            c = buf[12:16]  # for value

            # bytes 0:4 are seconds, bytes 5:8 nanoseconds
            timestamp = a[0] + a[1] * 0x100 + a[2] * 0x10000 + a[3] * 0x1000000
            timestamp *= 1_000_000
            timestamp += a[4] + a[5] * 0x100 + a[6] * 0x10000 + a[7] * 0x1000000

            typ = b[0]
            code = b[2] + b[3] * 0x100
            val = c[0] + c[1] * 0x100 + c[2] * 0x10000 + c[3] * 0x1000000

            # end of frame?
            if typ == 0 and code == 0:
                print(f"{timestamp},{x},{y},{pressure},{distance},{tilt_x},{tilt_y}")

            # type == 3 && code == 0 -> value == x
            # type == 3 && code == 1 -> value == y
            # type == 3 && code == 24 -> value == pressure
            # type == 3 && code == 25 -> value == distance
            # type == 3 && code == 26 -> value == tilt x
            # type == 3 && code == 27 -> value == tilt y

            if typ == 3:
                if code == 0:
                    x = val
                elif code == 1:
                    y = val
                elif code == 24:
                    pressure = val
                elif code == 25:
                    distance = val
                elif code == 26:
                    tilt_x = val
                elif code == 27:
                    tilt_y = val

    except KeyboardInterrupt:
        pass
    finally:
        proc.kill()


def run(rm_host="remarkable", host="localhost"):

    asyncio.get_event_loop().run_until_complete(listen(rm_host))


if __name__ == "__main__":
    run()
