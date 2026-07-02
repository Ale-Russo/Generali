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
        self._view.txt_result.controls.clear()
        self._model.creaGrafo(self._view._ddAnno1.value, self._view._ddAnno2.value)
        nNodi, nArchi, bestTre, nComp, maxComp = self._model.dettagliGrafo()
        self._view.txt_result.controls.append(ft.Text(f"Grafo correttamente creato", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di nodi: {nNodi}"))
        self._view.txt_result.controls.append(ft.Text(f"Numero di archi: {nArchi}"))
        self._view.txt_result.controls.append(ft.Text(f"Archi di peso maggiore:", color="red"))
        for a in bestTre:
            self._view.txt_result.controls.append(ft.Text(f"{a[0]} --> {a[1]}: {a[2]["weight"]}"))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo ha {nComp} componenti connesse", color="red"))
        self._view.txt_result.controls.append(ft.Text(f"Componente più grande ({len(maxComp)} nodi):", color="red"))
        for n in maxComp:
            self._view.txt_result.controls.append(ft.Text(f"{n}"))
        self._view.update_page()

    def handle_path(self, e):
        pass

    def fillDDAnni(self):
        years = self._model.getAllYears()
        yearsDD = list(map(lambda x: ft.dropdown.Option(x), years))
        self._view._ddAnno1.options = yearsDD
        self._view._ddAnno2.options = yearsDD
        self._view.update_page()


