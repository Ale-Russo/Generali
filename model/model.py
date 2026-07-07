from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        pass

    def getAnni(self):
        return DAO.getAnni()

    def buildGraphPESATO_NON_ORIENTATO(self, anno1, anno2):     #PESATO NON ORIENTATO
        graph = self._graph
        graph.clear()
        circuiti = DAO.getAllCircuits()
        for c in circuiti:
            c.risultati = {}
            ris = DAO.getRisultatiAnni(c.circuitId, anno1, anno2)
            for r in ris:
                if r["year"] not in c.risultati:
                    c.risultati[r["year"]] = []

                c.risultati[r["year"]].append((r["driverId"], r["position"]))
        graph.add_nodes_from(circuiti)

        for c in DAO.getAllPesi(anno1, anno2):
            self._arrivi[c["circuitId"]] = c["arrivi"]

        for i in range(len(circuiti)):
            c1 = circuiti[i]
            anni_c1 = set(c1.risultati.keys())
            for j in range(i+1, len(circuiti)):
                c2 = circuiti[j]
                anni_c2 = set(c2.risultati.keys())

                if len(anni_c1) > 0 and len(anni_c2) > 0 :
                    peso = self._arrivi.get(c1.circuitId,0)+self._arrivi.get(c2.circuitId,0)
                    if peso > 0:
                        graph.add_edge(c1,c2, weight=peso)

    def buildGraphPESATO_ORIENTATO(self, cat, date1, date2):
        self._graph.clear()
        self._products = DAO.getProductsByCategory(cat)
        for p in self._products:
            self._idMapP[p.product_id] = p

        self._graph.add_nodes_from(self._products)

        allEdges = DAO.getAllEdges(cat, date1, date2, self._idMapP)
        for e in allEdges:
            self._graph.add_edge(e.p1, e.p2, weight= e.peso)

    def dettagliGrafo(self):
        grafo = self._grafo
        nNodi = len(grafo.nodes())
        nArchi = len(grafo.edges())
        archi = grafo.edges(data=True)
        archiOrdinati = sorted(archi, key=lambda x: x[2]['weight'], reverse=True)
        bestTre = archiOrdinati[:3]
        compConn = list(nx.connected_components(grafo))
        nComp = len(compConn)
        maxComp = max(compConn, key=len)
        #
        gradi = list(grafo.degree())
        nodo_max_grado, max_grado = max(gradi, key=lambda x: x[1])
        pesi_incidenti = list(self._graph.degree(weight='weight'))
        nodo_max_peso, max_peso = max(pesi_incidenti, key=lambda x: x[1])




        return nNodi, nArchi, bestTre, nComp, maxComp, nodo_max_grado, max_grado, nodo_max_peso, max_peso