# ARACHNE CORE v12

Author: Gerdson Lopez

ARACHNE is a compact knowledge architecture based on:

- hexagonal node topology
- maximum 6 connections
- serpens spiral growth
- magnetic polarity rule (XOR)
- 7-bit node representation

Version: v12 (stable)

The system is designed to allow extremely compact knowledge networks suitable for local AI systems.

## Node structure

1 bit → polarity  
6 bits → connections  

Total: **7 bits per node**

## Connection rule

connection = polarity_A XOR polarity_B

Nodes connect when polarities are opposite and connection limit is not exceeded.

## Goals

- compact knowledge storage
- distributed intelligence
- low energy systems
- scalable architecture