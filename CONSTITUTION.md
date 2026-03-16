# ARACHNE CONSTITUTION

## Node Structure
Each node is represented by 7 bits:

- 1 bit polarity
- 6 bits connections

## Maximum Connections
Nodes may have at most 6 connections corresponding to spatial directions.

## Magnetic Polarity Rule
Nodes connect when polarities are opposite.

Formula:

connection = polarity_A XOR polarity_B

If the result equals 1 and the node has not exceeded the 6‑connection limit,
a connection may be established.