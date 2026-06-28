import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDGenre(self):
        allGenre = self._model.getAllGenre()
        generi = list(
            map(lambda x: ft.dropdown.Option(data=x, key= x.GenreId ,text=x.Name, on_click=self._choiceGenre), allGenre))

        self._view._ddGenre.options = generi

        self._view.update_page()

    def _choiceGenre(self,e):
        self._genre = e.control.data


    def fillDDArtist(self):
        allArtist = self._model.idMapA.values()
        artist = list(
            map(lambda x:ft.dropdown.Option(data=x, key=str(x.ArtistId), text=x.Name, on_click=self._choiceArtist), allArtist))
        self._view._ddArtist.options = artist
        self._view.update_page()

    def _choiceArtist(self,e):
        self._artist = e.control.data


    def handleCreaGrafo(self, e):
        genre = self._view._ddGenre.value

        self._view.txt_result.controls.clear()

        if genre is None:
            self._view.txt_result.controls.append(ft.Text("Inserire il genere dall'elenco",color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(genre)
        n,e = self._model.getGraphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi : {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi : {e} "))
        self.fillDDArtist()

        a,s = self._model.getInfluenza()
        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {a}, con influenza {s}"))

        lista = self._model.getTop5()
        self._view.txt_result.controls.append(ft.Text(f"Di seguito la top 5"))

        for a in lista:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} --> {a[1]} : {a[2]}"))

        self._view.update_page()



    def handleCammino(self,e):
        a1 = self._view._ddArtist.value

        self._view.txt_result.controls.clear()

        if a1 is None:
            self._view.txt_result.controls.append(ft.Text("Inserire l'artista dall'elenco", color="red"))
            self._view.update_page()
            return

        st = self._model.getBestPath(a1)

        self._view.txt_result.controls.append(ft.Text(f"Trovato il cammino max", color="green"))
        for c in st:
            self._view.txt_result.controls.append(ft.Text(f"{self._model.idMapA[c].Name}"))

        self._view.update_page()