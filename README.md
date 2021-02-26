# Multi-Input Uniform Datastreams (MUD)


## Overview

Mud is a network of nodes connected via websockets to consume, digest and record datastreams.

A Collator node... collates the data streams over a time interval (default 1 second), and logs it to a file (this largely for testing purposes).
The collator node uses the TimeKeeper module to maintain time intervals, deltas, and "frames". Where a frame is the captured datastream over a defined interval.
Nodes may be rewritten and added to MUD simply by connection to the web-socket and follow the (currently very loosely) defined schema for messaging.

## Collator

Starts a server and takes input from nodes or digests.

## Node, digestors or producers

Implements web sockets, and sends data over the collator's addressed socket. Digestors watch messages for their defined DIGEST_TYPE, and transform
data as defined by arbitrary code in the digest node.


## Logging

Currently, MUD simply logs to a csv every 20 frames to track data ingestion. 