import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handleCreaGrafo(self, e):
        try:
            self._view._txt_result.controls.clear()
            self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
            nNodi, nArchi, bestTre, nComp, maxComp = self._model.dettagliGrafo()
            self._view._txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
            self._view._txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
            self._view._txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}"))
            self._view._txt_result.controls.append(ft.Text(f"Archi di peso maggiore:"))
            for a in bestTre:
                self._view._txt_result.controls.append(ft.Text(f"{a[0]} --> {a[1]}: {a[2]["weight"]}"))
            self._view._txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse"))
            self._view._txt_result.controls.append(ft.Text(f"Componente più grande ({len(maxComp)} nodi):"))
            for n in maxComp:
                self._view._txt_result.controls.append(ft.Text(f"{n}"))
        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione grafo: {ex}")
        self._view.update_page()



    def handle_path(self, e):
        pass

    def fillDDAnni(self):
        years = self._model.getAllYears()
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddAnno1.options = yearsDD
        self._view._ddAnno2.options = yearsDD
        self._view.update_page()

    def fillDDCustomers(self):
        customers = self._model.getNodes()
        customersDD = list(map(lambda x: ft.dropdown.Option(key=str(x.CustomerId), text=x.FirstName+ " "+ x.LastName), customers))
        self._view._ddClienti.options = customersDD
        self._view.update_page()

    def fillDDShapes(self, e):  #QUANDO NECESSARIO UN ALTRO VALORE DELLA VIEW
        v = self._view
        y = v.ddyear.value
        if y is None:
            return
        shapes = self._model.getAllShapes(y)
        shapesDD = list(map(lambda x: ft.dropdown.Option(x), shapes))
        self._view.ddshape.options = shapesDD
        self._view.update_page()

    def handleCreaGrafoECCEZIONI(self, e):
        self._view._txt_result.controls.clear()

        try:
            self._model.buildGraph()

            self._view._txt_result.controls.append(
                ft.Text("Grafo correttamente creato.")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero nodi: {self._model.getNumNodi()}")
            )
            self._view._txt_result.controls.append(
                ft.Text(f"Numero archi: {self._model.getNumEdges()}")
            )
            self.fillDDArtisti()

            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella creazione del grafo: {ex}")

    def controlloNumerico(self):
        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._view.create_alert("Inserisci un valore numerico valido per N.")
            return

        if N <= 0:
            self._view.create_alert("N deve essere un intero positivo.")
            return

    def handleSelezione(self, e):
        self._view._txt_result.controls.clear()

        if self._model.getNumNodi() == 0:
            self._view.create_alert("Creare prima il grafo.")
            return

        if self._artistaValue is None:
            self._view.create_alert("Selezionare un artista dal menu a tendina.")
            return

        try:
            N = int(self._view._txtInN.value)
        except (ValueError, TypeError):
            self._view.create_alert("Inserisci un valore numerico valido per N.")
            return

        if N <= 0:
            self._view.create_alert("N deve essere un intero positivo.")
            return

        try:
            best_group, total_tracks = self._model.getBestGroup(self._artistaValue, N)

            if not best_group:
                self._view._txt_result.controls.append(ft.Text("Nessun gruppo trovato."))
                self._view.update_page()
                return

            sorted_group = sorted(best_group, key=lambda a: a.Name)

            self._view._txt_result.controls.append(ft.Text("Lista degli artisti selezionati:"))
            self._view._txt_result.controls.append(ft.Text(""))
            for artist in sorted_group:
                num_albums = self._model.getNumAlbumsForArtist(artist.ArtistId)
                num_tracks = len(artist.Tracks)
                num_playlists = len(artist.Playlists)
            self._view._txt_result.controls.append(ft.Text(f"  - {artist}: album: {num_albums}, "f"brani: {num_tracks}, playlist: {num_playlists}"))
            self._view._txt_result.controls.append(ft.Text(""))
            self._view._txt_result.controls.append(ft.Text(f"Numero totale di artisti selezionati: {len(best_group)}"))
            self._view._txt_result.controls.append(ft.Text(f"Numero complessivo di brani: {total_tracks}"))
            self._view.update_page()

        except Exception as ex:
            self._view.create_alert(f"Errore nella ricerca del gruppo: {ex}")


