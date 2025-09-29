#!/usr/bin/python3

import math

class Graph:
    def __init__(self):
        self.edges = []
        self.V = set()

    def add_edge(self, u, v, conversion_rate):
        self.edges.append((u, v, conversion_rate, -math.log(conversion_rate)))
        self.V.add(u)
        self.V.add(v)


def BellmanFord(g, source):
    if source not in g.V:
        raise Exception("Wrong source vertex!")

    distance = {v: float('inf') for v in g.V}
    distance[source] = 0

    predecessor = {v: None for v in g.V}

    for _ in range(len(g.V) - 1):
        for u, v, _, w in g.edges:
            if distance[v] > distance[u] + w:
                distance[v] = distance[u] + w
                predecessor[v] = u

    for u, v, _, w in g.edges:
        if distance[v] > distance[u] + w:
            distance[v] = distance[u] + w
            predecessor[v] = u

            walk = v
            path = [v]
            while predecessor[walk] != v:
                walk = predecessor[walk]
                path.append(walk)
            path.append(v)
            path.reverse()

            return (False, path)

        return (True, None)


"""
g = Graph()
g.add_edge('EUR', 'USD',  1.02)
g.add_edge('USD', 'EUR',  0.98)
g.add_edge('USD', 'UAH',    40)
g.add_edge('UAH', 'USD', 0.025)
g.add_edge('EUR', 'UAH',    40)
g.add_edge('UAH', 'EUR', 0.025)
result, path = BellmanFord(g, 'USD')
"""

"""
g = Graph()
g.add_edge('GBP', 'JPY', 200)
g.add_edge('JPY', 'CHF', 0.0055)
g.add_edge('CHF', 'GBP', 0.92)
result, path = BellmanFord(g, 'GBP')
"""

g = Graph()
g.add_edge('CAD', 'AUD', 0.93)
g.add_edge('AUD', 'NZD', 1.09)
g.add_edge('NZD', 'USD', 0.62)
g.add_edge('USD', 'CAD', 1.60)
result, path = BellmanFord(g, 'CAD')


w_total = 0
for i in range(len(path) - 1):
    for u, v, _, w in g.edges:
        if u == path[i] and v == path[i + 1]:
            w_total += w


print(result)
print(path)
print(round((1 - math.e ** w_total) * 100, 2), "%")
