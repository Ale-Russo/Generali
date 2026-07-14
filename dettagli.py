"""
CHECK SU DATE DI NASCITA

(SQL)
AND n.date_of_birth IS NOT NULL
AND YEAR(n.date_of_birth) <= 2026

(PY)
for row in cursor:
    data_nascita_str = str(row["date_of_birth"])
    anno_nascita = int(data_nascita_str.split("-")[0])
        if anno_nascita <= 2026:
             eta = 2026 - anno_nascita
             nodo = Attore(row["id"], row["name"], eta)
             nodi_validi.append(nodo)

VERIFICARE SE NULL:
-date
tabella movies:
-country
-income (anche valori strani)
-languages
-production_company
tabella names:
-height
-known_for_movies (sono codici dei film separati da virgola)


tip

La tabella `genre` è separata da `movie`. Questo vuol dire che un film come "Inception"
avrà una riga in `movie`, ma potrebbe avere tre righe in `genre` (Action, Sci-Fi, Thriller).
Se fai una JOIN secca tra `movie` e `genre` senza i dovuti accorgimenti (come un `GROUP BY` o un `DISTINCT`),
il film ti uscirà triplicato nei risultati e le tue medie sui voti o sui guadagni sballeranno in un secondo.


PRIMA (attori, se hanno recitato insieme in qualche film)
Permettere all'utente di selezionare da un apposito menu a tendina un Genere cinematografico (es. Action, Sci-Fi, Drama). L'elenco deve essere popolato all'avvio dell'applicazione, in ordine alfabetico.
b. Alla pressione del bottone "Crea Grafo", creare un grafo semplice, non orientato e pesato, in cui:
I vertici sono tutti gli attori/attrici (tabella names filtrando opportunamente role_mapping per category uguale a 'actor' o 'actress') che hanno recitato in almeno un film appartenente al genere selezionato.
Esiste un arco tra due vertici se e solo se i due attori hanno recitato insieme in almeno un film (di qualsiasi genere, non per forza quello selezionato).
Il peso dell'arco è pari al numero totale di film in cui i due attori hanno collaborato.

SECONDA (registi, media dei voti di uno maggiore dell'altro)
Permettere all'utente di inserire in un campo di testo un Anno (es. 2010).
b. Alla pressione del bottone "Crea Grafo", creare un grafo semplice, orientato e pesato, in cui:
I vertici sono tutti i Registi (tabella names via director_mapping) che hanno diretto almeno due film nell'anno inserito.
Per ogni coppia di registi R1 e R2, esiste un arco da R1 a R2 se e solo se la media dei voti (campo avg_rating in ratings) dei film diretti da R1 in quell'anno è strettamente maggiore della media dei voti dei film diretti da R2 nello stesso anno.
Il peso dell'arco è pari al valore assoluto della differenza tra la media dei voti di R1 e la media dei voti di R2.

TERZA (attori, recitato in un film con regista in comune)
a.All'avvio dell'applicazione, popolare un menu a tendina con tutti i Registi (tabella names unita a director_mapping) in ordine alfabetico.
b. Alla pressione di "Crea Grafo", creare un grafo semplice, non orientato e pesato, in cui:
I vertici sono tutti gli attori e le attrici (category = 'actor' o 'actress') che hanno recitato in almeno un film diretto dal regista selezionato.
(Nota: è necessario memorizzare il ruolo esatto, actor o actress, all'interno dell'oggetto nodo).
Esiste un arco tra due vertici se e solo se i due attori hanno recitato insieme in almeno un film diretto da quel medesimo regista.
Il peso dell'arco è pari alla somma dei voti totali (campo total_votes in ratings) di tutti i film che i due attori hanno in comune sotto la direzione di quel regista.
(Se un film non ha voti, contribuisce con 0).

QUARTA (film, se condividono almeno un attore)
a. Permettere all'utente di inserire in un campo di testo una Durata Minima in minuti (es. 120).
b. Alla pressione di "Crea Grafo", creare un grafo semplice, non orientato e pesato, in cui:
I vertici non sono persone, ma Film (tabella movie) la cui durata (duration) è strettamente maggiore della durata inserita dall'utente.
Esiste un arco tra due film se e solo se condividono almeno un attore/attrice nel cast (escludere esplicitamente i registi o altre categorie).
Il peso dell'arco è pari al numero esatto di attori/attrici che i due film condividono.





"""