import random
import math
import json
from collections import deque

MAX_CONNECTIONS = 6
CELL_SIZE = 7
RING_MIN_SIZE = 6

class Node:
    def __init__(self, nid):
        self.id = nid
        self.polarity = random.randint(0,1)
        self.connections = set()

class Cell:
    def __init__(self, cid, center):
        self.id = cid
        self.center = center
        self.nodes = [center]
        self.neighbors = set()
        self.layer = 0
        self.angle = 0
        self.x = 0
        self.y = 0
        self.z = 0

class Arachne:

    def __init__(self):
        self.nodes = {}
        self.cells = []
        self.current_ring = []
        self.rings = []

    def add_node(self, nid):
        if nid not in self.nodes:
            self.nodes[nid] = Node(nid)

    def connect(self, a, b):
        na = self.nodes[a]
        nb = self.nodes[b]
        if len(na.connections) >= MAX_CONNECTIONS: return False
        if len(nb.connections) >= MAX_CONNECTIONS: return False
        if not (na.polarity ^ nb.polarity): return False
        na.connections.add(b)
        nb.connections.add(a)
        return True

    def create_cell(self, center_id):
        self.add_node(center_id)
        cid = f"C{len(self.cells)}"
        cell = Cell(cid, center_id)

        for i in range(6):
            nid = f"{center_id}_{i}"
            self.add_node(nid)
            if self.connect(center_id, nid):
                cell.nodes.append(nid)

        if len(cell.nodes) != CELL_SIZE:
            return None

        cell.angle = len(self.current_ring)
        self.cells.append(cell)
        self.current_ring.append(cell)
        return cell

    def attach(self, A, B):
        links = 0
        for na in A.nodes:
            for nb in B.nodes:
                if links >= 3: return
                if self.connect(na, nb):
                    links += 1
        if links > 0:
            A.neighbors.add(B.id)
            B.neighbors.add(A.id)

    def check_cycle(self):
        return len(self.current_ring) >= RING_MIN_SIZE

    def elevate(self):
        self.rings.append(self.current_ring)
        new_layer = len(self.rings)
        next_ring = []
        for i, old in enumerate(self.current_ring):
            nid = f"N_L{new_layer}_{i}"
            new_cell = self.create_cell(nid)
            if new_cell:
                new_cell.layer = new_layer
                new_cell.angle = i + new_layer
                next_ring.append(new_cell)
        self.current_ring = next_ring

    def expand(self):
        nid = f"N{len(self.cells)}"
        cell = self.create_cell(nid)
        if not cell: return
        if len(self.current_ring) > 1:
            prev = self.current_ring[-2]
            self.attach(cell, prev)
        if self.check_cycle():
            self.attach(self.current_ring[0], self.current_ring[-1])
            self.elevate()

    def compute_coords(self):
        for cell in self.cells:
            r = 1 + cell.layer * 2
            angle = cell.angle * 0.5
            cell.x = r * math.cos(angle)
            cell.y = r * math.sin(angle)
            cell.z = cell.layer * 1.5

    def export_json(self, filename="output/arachne.json"):
        data = []
        for c in self.cells:
            data.append({
                "id": c.id,
                "x": c.x,
                "y": c.y,
                "z": c.z,
                "layer": c.layer
            })
        with open(filename, "w") as f:
            json.dump(data, f, indent=2)

    def run(self, steps=50):
        for _ in range(steps):
            self.expand()
        self.compute_coords()

if __name__ == "__main__":
    a = Arachne()
    a.run(80)
    a.export_json()
