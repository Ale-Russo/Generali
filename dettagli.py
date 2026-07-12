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

"""