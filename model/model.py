import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.idMapA = {}
        self._graph = nx.DiGraph()
        self._bestPath = []
        self._bestScore = 0

    def getAllGenre(self):
        return DAO.AllGenre()

    def allArtist(self):
        return DAO.allArtist()

    def buildGraph(self, genre):
        self._graph.clear()
        self.idMapA = {}

        for a in DAO.getAllNodes(genre):
            self.idMapA[a.ArtistId] = a

        self._graph.add_nodes_from(self.idMapA)

        allEdges = DAO.getAllEdge(genre, self.idMapA)

        for e in allEdges:
            self._graph.add_edge(e.a1.ArtistId, e.a2.ArtistId, weight=e.peso)

    def getGraphDetails(self):
        return len(self._graph.nodes), len(self._graph.edges)

    def getInfluenza(self):
        listNodes = []
        for n in self._graph.nodes:
            score = 0
            for e in self._graph.out_edges(n, data=True):
                score += e[2]["weight"]
            for i in self._graph.in_edges(n, data=True):
                score -= i[2]["weight"]
            listNodes.append([self.idMapA[n].Name, score])
        listNodes.sort(key=lambda x: x[1], reverse=True)
        return listNodes[0]

    def getTop5(self):
        top = []
        edges = list(self._graph.edges(data=True))
        for e in edges:
            top.append((self.idMapA[e[0]].Name, self.idMapA[e[1]].Name,e[2]["weight"]))
            top.sort(key=lambda x: x[2], reverse=True)
        return top[0:5]


    def getBestPath(self,artista):
        self._bestPath = []
        self._bestScore = 0
        artist_id = int(artista)
        parziale = [artist_id]
        self._ricorsione(parziale)
        return self._bestPath

    def _ricorsione(self, parziale):
        if len(parziale) > self._bestScore:
            self._bestScore = len(parziale)
            self._bestPath = copy.deepcopy(parziale)

        for v in self._graph.successors(parziale[-1]):
            peso1 = self._graph[parziale[-1]][v]["weight"]

            if len(parziale)<2:
                peso = 0

            else:
                peso = self._graph[parziale[-2]][parziale[-1]]["weight"]
            if peso1 > peso and v not in parziale:
                parziale.append(v)
                self._ricorsione(parziale)
                parziale.pop()
