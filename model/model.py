import copy

from database.DAO import DAO
import networkx as nx

class Model:
    def __init__(self):
        pass

    def getAnni(self):
        return DAO.getAnni()

    def buildGraphPESATO_NON_ORIENTATO(self, anno1, anno2):     #PESATO NON ORIENTATO
        grafo = self._grafo
        grafo.clear()
        circuiti = DAO.getAllCircuits()
        for c in circuiti:
            c.risultati = {}
            ris = DAO.getRisultatiAnni(c.circuitId, anno1, anno2)
            for r in ris:
                if r["year"] not in c.risultati:
                    c.risultati[r["year"]] = []

                c.risultati[r["year"]].append((r["driverId"], r["position"]))
        grafo.add_nodes_from(circuiti)

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
                        grafo.add_edge(c1,c2, weight=peso)

    def buildGraphPESATO_ORIENTATO(self, cat, date1, date2):
        self._graph.clear()
        self._products = DAO.getProductsByCategory(cat)
        for p in self._products:
            self._idMapP[p.product_id] = p

        self._graph.add_nodes_from(self._products)

        allEdges = DAO.getAllEdges(cat, date1, date2, self._idMapP)
        for e in allEdges:
            self._graph.add_edge(e.p1, e.p2, weight= e.peso)

    def basiGrafo(self):
        grafo = self._grafo
        nNodi = len(grafo.nodes())
        nArchi = len(grafo.edges())
        return nNodi, nArchi

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
        gradi = list(grafo.degree()) #NODO CON GRADO MAGGIORE
        nodo_max_grado, max_grado = max(gradi, key=lambda x: x[1])

        pesi_incidenti = list(self._graph.degree(weight='weight')) #NODO CON PESO MAGGIORE
        nodo_max_peso, max_peso = max(pesi_incidenti, key=lambda x: x[1])

        #nodi della maxComp ordinati in senso decrescente di peso minimo degli archi incidenti  (SEI COOKED)
        risultato = []
        for nodo in maxComp:
            pesi_archi = [dati['weight'] for _, _, dati in self._grafo.edges(nodo, data=True)]
            if pesi_archi:
                peso_minimo = min(pesi_archi)
                risultato.append((nodo, peso_minimo))

        maxCompOrdinata = sorted(risultato, key=lambda x: x[1], reverse=True)

        #PESO ARCHI USCENTI - PESO ARCHI ENTRANTI
        infMax = -1
        bestNode = None
        for n in grafo.nodes:
            inf = grafo.out_degree(n, weight="weight") - grafo.in_degree(n, weight="weight")
            if inf > infMax:
                bestNode = self._idMap[n.CustomerId]
                infMax = inf

        #NODI CON NUMERO DI ARCHI USCENTI MAGGIORE E PESO TOTALE (SOMMA) DI QUESTI ULTIMI
        statistiche_nodi = []
        for nodo in self._grafo.nodes:
            archi_uscenti = self._grafo.out_edges(nodo, data=True)
            num_uscenti = len(archi_uscenti)
            peso_totale = 0
            for u, v, dati in archi_uscenti:
                peso_totale += dati["weight"]
            statistiche_nodi.append((nodo, num_uscenti, peso_totale))
        ordinati = sorted(statistiche_nodi, key=lambda x: x[1], reverse=True)
        bestFive = ordinati[:5]

        #LISTA ARCHI USCENTI DAL NODO
        grafo.out_edges(n)
        #NUMERO ARCHI USCENTI DAL NODO
        grafo.out_degree(n)





        return nNodi, nArchi, bestTre, nComp, maxComp, nodo_max_grado, max_grado, nodo_max_peso, max_peso, maxCompOrdinata, bestNode


    #-------------------------------------------------------------------------
    #RICORSIONE
    #-------------------------------------------------------------------------
    #SI CONDIZIONE DI TERMINAZIONE

    #CON OGGETTO DI PARTENZA
    def getBestGroup(self, starting_artist, N):
        self._bestGroup = []
        self._maxTracks = 0
        parziale = [starting_artist]
        self._ricorsione(parziale, N)
        return self._bestGroup, self._maxTracks


    def _ricorsione(self, parziale, N):
        if len(parziale) == N:
            total = self._getTotalTracks(parziale)
            if total > self._maxTracks:
                self._maxTracks = total
                self._bestGroup = copy.deepcopy(parziale)
            return

        for candidate in self._graph.nodes:
            if candidate in parziale:
                #skip questo candidato se già inserito in parziale
                continue

            # verifico se il candidato è adiacente ad almeno un elemento di parziale,
            # altrimenti skip il resto del codice perchè non è un candidato valido
            adjacent = any(self._graph.has_edge(candidate, existing) for existing in parziale)
            if not adjacent:
                continue

            # verifico che questo candidato non sia connesso a nessun elemento di parziale con un
            # arco di peso 1
            blocked = any(self._graph.has_edge(candidate, existing) and self._graph[candidate][existing]['weight'] == 1 for existing in parziale)
            if blocked:
                continue

            parziale.append(candidate)
            self._ricorsione(parziale, N)
            parziale.pop()

    #SENZA OGGETTO DI PARTENZA
    import copy

    def getBestGroup(self, K, M, y1, y2):
        self._bestGroup = []
        self._maxImp = 0

        # 1. FILTRO PREVENTIVO
        # Isoliamo solo i team che hanno partecipato ad almeno M campionati.
        candidati_validi = []
        for c in self._compConn:
            if len(c.Risultati) >= M:
                candidati_validi.append(c)

        # 2. LA CACHE (Il salvavita dell'esame)
        # Calcoliamo l'indice I una sola volta per ogni team valido e ce lo salviamo in RAM.
        self._cache_imp = {}
        for c in candidati_validi:
            # Usiamo la tua funzione che richiama il DAO!
            self._cache_imp[c.constructorId] = self.getImpTeam(c, y1, y2)

        # 3. INNESCO RICORSIONE PURE (Combinazioni)
        # Partiamo con lista vuota e start_index = 0
        self._ricorsione([], candidati_validi, 0, K)

        return self._bestGroup, self._maxImp

    def _ricorsione(self, parziale, candidati, start_index, K):
        # CASO BASE: abbiamo i K team
        if len(parziale) == K:
            # Calcoliamo la somma pescando istantaneamente dalla RAM (niente DB!)
            totale = sum(self._cache_imp[c.constructorId] for c in parziale)

            if totale > self._maxImp:
                self._maxImp = totale
                self._bestGroup = copy.deepcopy(parziale)
            return

        # CICLO OTTIMIZZATO (Combinazioni pure)
        for i in range(start_index, len(candidati)):
            candidate = candidati[i]

            parziale.append(candidate)
            self._ricorsione(parziale, candidati, i + 1, K)
            parziale.pop()

    # La tua funzione getImpTeam va benissimo, lasciala!
    # Puoi invece CANCELLARE la funzione totI, non serve più.
    #-----------------------------------------------------
    #NO CONDIZIONE DI TERMINAZIONE
    def getBestCammino(self, primo):
        self._bestCammino = []
        parziale = [self._idMap[int(primo)]]
        self._ricorsione(parziale)
        return self._bestCammino

    def getBestCammino2(self):  #SE NON C'E' UN ELEMENTO DI PARTENZA NELLA LISTA
        self._bestCammino = []
        for nodo in self._grafo.nodes:
            if nodo.Essential != "?":
                self._ricorsione([nodo])
        return self._bestCammino

    def _ricorsione(self, parziale):
        if len(parziale) > len(self._bestCammino):
            self._bestCammino = copy.deepcopy(parziale)

        #condizioni inserimento
        ultimo = parziale[-1]
        for candidate in self._grafo.neighbors(ultimo):
            if candidate in parziale:
                continue

            if candidate.Fatturato > ultimo.Fatturato:
                continue


            parziale.append(candidate)
            self._ricorsione(parziale)
            parziale.pop()


    def getBestCammino3(self):  #GRAFO ORIENTATO E DIZIONARIO PER TOTALITA' DATI
        self._bestCammino = []
        self._bestScore = 0

        for nodo in self._grafo.nodes:
            mese_partenza = nodo.datetime.month
            mesi_count = {mese_partenza: 1}
            self._ricorsione([nodo], mesi_count)

        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale, mesi_count):
        score_attuale = self._getPunteggio(parziale)
        if score_attuale > self._bestScore:
            self._bestScore = score_attuale
            self._bestCammino = copy.deepcopy(parziale)

        ultimo = parziale[-1]

        for candidate in self._grafo.successors(ultimo):
            if candidate.duration <= ultimo.duration:
                continue

            mese_cand = candidate.datetime.month
            if mesi_count.get(mese_cand, 0) >= 3:
                continue

            parziale.append(candidate)
            mesi_count[mese_cand] = mesi_count.get(mese_cand, 0) + 1

            self._ricorsione(parziale, mesi_count)

            parziale.pop()
            mesi_count[mese_cand] -= 1

    #ROBE DI ARCHI
    def getBestCammino4(self, primo):
        self._bestCammino = []
        parziale = [self._idMap[int(primo)]]
        self._ricorsione(parziale)
        return self._bestCammino

    def _ricorsione(self, parziale):
        if len(parziale) > len(self._bestCammino):
            self._bestCammino = copy.deepcopy(parziale)
        #condizioni inserimento
        ultimo = parziale[-1]
        for candidate in self._grafo.neighbors(ultimo):
            if candidate in parziale:
                continue

            if len(parziale) > 1:
                penultimo = parziale[-2]
                peso_ultimo = self._grafo[penultimo][ultimo]["weight"]
                peso_candidato = self._grafo[ultimo][candidate]["weight"]
                if peso_candidato < peso_ultimo:
                    continue


            parziale.append(candidate)
            self._ricorsione(parziale)
            parziale.pop()

    def getPesoArchiCammino(self, parziale):
        peso = 0
        if len(parziale) > 1:
            for i in range(len(parziale)-1):
                corrente = parziale[i]
                prossimo = parziale[i+1]
                peso+=  self._grafo[corrente][prossimo]["weight"]
        return peso

