import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def fillDDNazione(self):
        nations = self._model.getNation()
        naz = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x, on_click=self._choiceNation), nations)
        )

        self._view._ddNazione.options = naz
        self._view.update_page()

    def _choiceNation(self,e):
        self._naz = e.control.data



    def handleCreaGrafo(self,e):
        naz = self._view._ddNazione.value

        self._view.txt_result.controls.clear()

        if naz is None:
            self._view.txt_result.controls.append(ft.Text("Inserire il genere dall'elenco", color="red"))
            self._view.update_page()
            return

        self._model.buildGraph(naz)
        n, e = self._model.graphDetails()
        self._view.txt_result.controls.clear()
        self._view.txt_result.controls.append(ft.Text(f"Grafo creato correttamente", color="green"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi : {n}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi : {e} "))
        self.fillCliente()
        c, s = self._model.clienteAffine()

        self._view.txt_result.controls.append(ft.Text(f"Artista più influente: {c}, con influenza {s}"))
        lista = self._model.top_5_minus()
        self._view.txt_result.controls.append(ft.Text(f"Di seguito la top 5"))

        for a in lista:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} --> {a[1]} : {a[2]}"))

        self._view.update_page()


    def fillCliente(self):
        cliente = list(self._model._idMapC.values())
        cl = list(
            map(lambda x: ft.dropdown.Option(data=x, key=x.CustomerId, text= x, on_click=self._choiceCliente), cliente)
        )

        self._view._ddCliente.options = cl
        self._view.update_page()

    def _choiceCliente(self, e):
        self._cl = e.control.data


    def handleCammino(self,e):
        c1 = self._view._ddCliente.value

        self._view.txt_result.controls.clear()

        if c1 is None:
            self._view.txt_result.controls.append(ft.Text("Inserire il cliente dall'elenco", color="red"))
            self._view.update_page()
            return

        st = self._model.getBestPath(c1)
        if len(st) == 0:
            self._view.txt_result.controls.append(
                ft.Text(f"Il cliente selezionato non fa parte del genere scelto in partenza", color="orange"))
            self._view.update_page()
            return

        self._view.txt_result.controls.append(ft.Text(f"Trovato il cammino max", color="green"))
        for cl in st:
            self._view.txt_result.controls.append(ft.Text(f"{cl}"))

        self._view.update_page()

