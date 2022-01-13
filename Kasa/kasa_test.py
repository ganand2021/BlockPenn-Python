#!/usr/bin/python
import asyncio
from kasa import Discover, SmartPlug

devices = asyncio.run(Discover.discover())
for addr, dev in devices.items():
    asyncio.run(dev.update())
    print(f"{addr} >> {dev}")

async def main():
    p = SmartPlug("192.168.0.216")

    await p.update()
    print(p.alias)
    print(p.hw_info['mac'])
    if p.is_on:
        print("Turning off")
        await p.turn_off()
    else:
        print("Turning on")
        await p.turn_on()


if __name__ == "__main__":
    asyncio.run(main())

