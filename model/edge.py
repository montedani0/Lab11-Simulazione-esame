from dataclasses import dataclass

from model.artista import Artista


@dataclass

class Edge:
    a1 : Artista
    a2 : Artista
    peso : int
