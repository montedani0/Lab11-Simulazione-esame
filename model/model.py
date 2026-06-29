import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self._graph = nx.Graph()
        self._idMapC = {}
        self._bestPath = []





    def getNation(self):
        naz = DAO.getNaz()
        naz.sort()
        return naz


    def buildGraph(self,nazione):
        self._idMapC = {}
        self._graph.clear()
        customer = DAO.getCustomer(nazione)

        for c in customer:
            self._idMapC[c.CustomerId] = c

        self._graph.add_nodes_from(self._idMapC.values())

        allEdges = DAO.getEdge(nazione,self._idMapC)

        for e in allEdges:
            self._graph.add_edge(e.c1, e.c2, weight=e.peso)


    def clienteAffine(self):
        lista_gradi = list(self._graph.degree(weight='weight'))
        lista_gradi.sort(key=lambda x: x[1], reverse=True)
        return lista_gradi[0][0], lista_gradi[0][1]

    def top_5_minus(self):
        lista = []
        listEdges = list(self._graph.edges(data=True))
        for e in listEdges:
            if e[2]['weight'] > 0:
                lista.append((e[0], e[1], e[2]['weight']))

        lista.sort(key=lambda x: x[2])
        return lista[0:5]



    def graphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)


    def getBestPath(self,cliente_selezionato):
        self._bestPath = []
        cl = self._idMapC[int(cliente_selezionato)]
        parziale = [cl]
        self._ricorsione(parziale)
        return self._bestPath

    def _ricorsione(self,parziale):
        if len(parziale) > len(self._bestPath):
            self._bestPath = copy.deepcopy(parziale)
        for v in self._graph.neighbors(parziale[-1]):
            peso1 = self._graph[parziale[-1]][v]['weight']
            if len(parziale)<2:
                peso = 1000
            else:
                peso = self._graph[parziale[-2]][parziale[-1]]['weight']
            if peso1 < peso and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()



