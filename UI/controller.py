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
            self._view.txt_result.controls.clear()
            self._model.buildGraph(self._view._ddAnno1.value, self._view._ddAnno2.value)
            nNodi, nArchi, bestTre, nComp, maxComp = self._model.dettagliGrafo()
            self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
            self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}"))
            self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:"))
            for a in bestTre:
                self._view.txt_result.controls.append(ft.Text(f"{a[0]} --> {a[1]}: {a[2]["weight"]}"))
            self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse"))
            self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(maxComp)} nodi):"))
            for n in maxComp:
                self._view.txt_result.controls.append(ft.Text(f"{n}"))
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


