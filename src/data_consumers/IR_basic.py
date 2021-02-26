#!/usr/bin/env python

# sensor simulation for IR 0-255 data stream

import asyncio
import json
import websockets
import random


def sensor_stream():
    values = list(range(250))
    while True:
        yield random.choice(values)


class IRBasic:
    def __init__(self):
        self.has_joined = False
        self.node_id = None


ir_basic = IRBasic()

async def join_socket():
    ir_basic = IRBasic()
    uri = "ws://localhost:8765"
    stream = sensor_stream()
    async with websockets.connect(uri) as websocket:
        if ir_basic.has_joined == False:
            await websocket.send(json.dumps({'type': 'JOIN'}))
            print(f"> Sent join request")
            assigned_id = await websocket.recv()
            ir_basic.node_id = json.loads(assigned_id)['id']
            ir_basic.has_joined = True
            print(f"< Received id: {assigned_id}")
        while True:
            await asyncio.sleep(0.5)
            print('Sending Sensor Data')
            await websocket.send(json.dumps({'type': 'DATA', 'payload': next(stream), 'id': ir_basic.node_id}))



def main():
    asyncio.get_event_loop().run_until_complete(join_socket())
    asyncio.get_event_loop().run_forever()



if __name__ == '__main__':
    main()



