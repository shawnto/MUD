#!/usr/bin/env python

# Shuffles data in a matrix for testing digestion middleware

import asyncio
import json
import websockets


# Sensor sim for a depth camera with a trivial 3x3 matric of vision


class DepthCam:
    def __init__(self):
        self.has_joined = False
        self.node_id = None


d_cam = DepthCam()

TEST_MATRIX = [[111, 222, 333], [444, 555, 666], [777, 888, 999]]

async def join_socket():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        if d_cam.has_joined == False:
            await websocket.send(json.dumps({'type': 'JOIN'}))
            print(f"> Sent join request")
            assigned_id = await websocket.recv()
            d_cam.node_id = json.loads(assigned_id)['id']
            d_cam.has_joined = True
            print(f"< Received id: {assigned_id}")
        while True:
            await asyncio.sleep(0.25)
            data = json.dumps({'payload': TEST_MATRIX, 'id': d_cam.node_id, 'type': 'DATA', 'DIGEST': 'MATRIX'})
            # this would be better done by tracking ids across nodes
            await websocket.send(data)



def main():
    asyncio.get_event_loop().run_until_complete(join_socket())
    asyncio.get_event_loop().run_forever()



if __name__ == '__main__':
    main()



