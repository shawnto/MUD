#!/usr/bin/env python

# Shuffles data in a matrix for testing digestion middleware

import asyncio
import json
import websockets
import random



class MatrixShuffler:
    def __init__(self):
        self.has_joined = False
        self.node_id = None


m_shuffle = MatrixShuffler()


async def join_socket():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        if m_shuffle.has_joined == False:
            await websocket.send(json.dumps({'type': 'JOIN'}))
            print(f"> Sent join request")
            assigned_id = await websocket.recv()
            m_shuffle.node_id = json.loads(assigned_id)['id']
            m_shuffle.has_joined = True
            print(f"< Received id: {assigned_id}")
        while True:
            await asyncio.sleep(.25)
            print('listening...')
            try:
                message = await websocket.recv()
                data = json.loads(message)
            except websockets.exceptions.ConnectionClosed:
                print('Closed connection')
                break
            # this would be better done by tracking ids across nodes
            print(f'Checking message {data}')
            if (data['type'] == 'DATA' and data['DIGEST'] == 'MATRIX'):
                shuffled = random.shuffle(data['payload'])
                print('sending message', data)
                await websocket.send(json.dumps({'type': 'DATA', 'payload': shuffled, 'id': m_shuffle.node_id}))




def main():
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(join_socket())]
    loop.run_until_complete(asyncio.wait(tasks))



if __name__ == '__main__':
    main()



