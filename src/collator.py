#!/usr/bin/env python

# Collator server. Initializes and opens a websocket to receive streams from other nodes.

import asyncio
import websockets
import csv
from uuid import uuid4
from timekeeper import TimeKeeper
from json import dumps, loads
from copy import deepcopy


class Collator:
    def __init__(self):
        self.timekeep = TimeKeeper()
        self.inputs = {}
        self.data_timeline = {}
        self.interval_buffer = {}
        self.data_storage = 'temp.csv'
    
    def add_node(self, node):
        uid = str(uuid4())
        self.inputs[uid] = node
        return uid

    def write_timeline(self):
        with open(self.data_storage, 'w', newline='\n') as csvfile:
            writer = csv.writer(csvfile, dialect='unix')
            print(self.data_timeline)
            for incre_key, value in self.data_timeline.items():
                writer.writerow([incre_key,  *[(k, v) for k, v in value.items()]])

    def end_interval(self):
        print(f'Interval ended with {collator.interval_buffer}')
        self.data_timeline[self.timekeep.step_counter] = deepcopy(self.interval_buffer)
        self.interval_buffer = {}
        self.timekeep.begin_new_interval()

collator = Collator()




async def poll_socket(websocket, path):
    async for message in websocket:
        if collator.timekeep.has_interval_passed():
            collator.end_interval()
    #async for message in websocket:
        in_stream = loads(message)
        print(in_stream)
        if in_stream['type'] == 'JOIN':
            print('join request received')
            assigned_id = collator.add_node(websocket)
            print(f'{assigned_id} created')
            await websocket.send(dumps({'id': assigned_id}))
        elif in_stream['type'] == 'DATA' and in_stream.get('DIGEST') != 'MATRIX':
            print(f'Recieved Data: {in_stream["payload"]}')
            if not collator.interval_buffer.get(in_stream['id']):
                collator.interval_buffer[in_stream['id']] = [in_stream['payload']]
            else:
                collator.interval_buffer[in_stream['id']].append(in_stream['payload'])
        elif in_stream.get('DIGEST') == 'MATRIX':
            await websocket.send(message)
        if collator.timekeep.step_counter % 10 == 0:
            collator.write_timeline()

        
    


def main():
    '''
    Spin up the server and start polling for requests
    '''
    collator = Collator()
    start_server = websockets.serve(poll_socket, "localhost", 8765)
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    main()

