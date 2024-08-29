# Telegraph
Scrivere un programma python che gestisca un sistema telegrafico.

I moduli e le classi vanno sviluppati nel package *telegraph*.
Non spostare o rinominare moduli e classi esistenti e non modificare le signature dei metodi.

In *main.py* viene fornito del semplice codice, da voi modificabile, che testa le funzionalità base.
Esso mostra esempi di uso dei metodi principali dei controlli richiesti.

Tutte le eccezioni, se non altrimenti specificato, sono di tipo *TelegraphException* definito nel modulo *exceptions*.

## R1: Stazioni e messaggi (5/19)
La classe ```TelegraphManager``` nel modulo *telegraph_manager* permette definire le stazioni telegrafiche e i messaggi scambiati.

Il metodo
```add_station(self, name: str) -> int```
permette di aggiungere una stazione indicandone il nome che la identifica univocamente.
Inserimenti duplicati devono essere ignorati.
Il metodo restituisce il numero di stazioni che sono state aggiunte fino a quel momento.

La property ```stations(self) -> Set[str]``` restituisce un set contenente i nomi delle stazioni aggiunte.

La classe ```Message```, definita nel modulo *elements*, ha le seguenti properties (in sola lettura):
- ```text(self) -> str``` (testo del messaggio)
- ```sender(self) -> srt``` (nome della stazione mittente)
- ```receiver(self) -> str``` (nome della stazione destinataria)

La dimensione degli oggetti ```Message``` (```__len__(self)```) deve essere pari alla lunghezza in caratteri del testo del messaggio.

Il metodo ```add_message(self, text: str, sender: str, receiver: str) -> Message``` permette di aggiungere un messaggio, specificandone il testo, la stazione mittente e la stazione destinataria.
Il metodo restituisce il messaggio aggiunto.
Un'eccezione deve essere lanciata nel caso in cui o la stazione mittente o la stazione destinataria (o entrambe) non siano definite.

## R2: Statistiche messaggi (5/19)
La classe ```TelegraphManager``` permette estrapolare informazioni sui messaggi inviati.

Il metodo ```get_destinations_by_frequency(self) -> Dict[int, List[str]]```
raggruppa le stazioni in base al numero di messaggi che vi sono destinati.
Esso restituisce un dizionario con il numero di messaggi destinati alla stazione come chiave, e una lista di stringhe ordinate alfabeticamente con i nomi delle stazioni che sono destinatarie di quel numero di messaggi come valore.

Il metodo ```get_most_frequent_exchange(self) -> Tuple[str, str]```
restituisce un tupla contenente la coppia di stazioni fra cui sono stati scambiati più messaggi (considerando ambo le direzioni).
L'ordine delle stazioni nella tupla restituita **NON** è importante.


## R3: Codifica (3/19)
La classe ```TelegraphManager``` permette di definire una codifica con cui inviare i messaggi tramite telegrafo.
I due simboli ammessi dalla codifica (punto e trattino) sono definiti nella classe ```Symbol``` nel modulo ```elements```.

Il metodo
```add_character_encoding(self, character: str, symbol: Symbol, previous: Optional[str] = None) -> str```
permette di definire la codifica di un carattere.
Il metodo accetta come parametri il carattere da codificare, un simbolo tra i due definiti in ```Symbol``` (punto o trattino), e un carattere precedentemente codificato.
La codifica del nuovo carattere è una stringa di simboli composta dalla codifica del carattere precedente più il nuovo simbolo.
Se il carattere precedente non è specificato la codifica del nuovo carattere è una stringa contenente il simbolo stesso.
Il metodo restituisce la codifica del carattere e lancia un'eccezione se il simbolo precedente non ha una codifica.

Il metodo
```encode_text(self, text: str) -> List[str]```
permette di codificare un testo passato come parametro.
Considerare un testo composto da parole separate da spazi, senza punteggiatura e con solamente lettere minuscole.
Il metodo restituisce una lista ordinata contenente la codifica delle parole nel testo.
La codifica di una parola una stringa composta dalle codifiche dei diversi caratteri separate da uno spazio.

## R4: Connessioni (3/19)
La classe ```TelegraphManager``` permette di definire delle connessioni **BIDIREZIONALI** tra le diverse stazioni.

Il metodo
```add_connection(self, station_1: str, station_2: str) -> None```
aggiunge una connessione **BIDIREZIONALE** tra le due stazioni i cui nomi sono forniti come parametri.

Il metodo
```are_connected(self, station_1: str, station_2: str) -> bool```
accetta come parametri i nomi di due stazioni, restituendo ```True``` se queste sono connesse e ```False``` se non lo sono.

Il metodo
```get_connected_stations(self, station: str) -> Set[str]```
accetta come parametro il nome di una stazione e restituisce un set contente i nomi delle stazioni a cui è connessa.


## R5 Percorso (3/19)
La classe ```TelegraphManager``` permette d'identificare il percorso più corto per recapitare i messaggi tra due stazioni.

Il metodo
```get_shortest_path(self, station_start: str, station_end: str) -> Optional[List[str]]```
accetta come parametri il nome della stazione mittente e il nome della stazione destinataria, e restituisce il percorso più corto che collega le due stazioni.
Il percorso è rappresentato da una lista contenente i nomi delle stazioni per cui il messaggio deve transitare, includendo la stazione di partenza e quella di arrivo.
Se non è presente un percorso restituire  ```None```. 
