from collections.abc import Collection
from typing import Dict, List, Tuple, Set, Optional
from telegraph.elements import Message, Station, Symbol
from telegraph.exceptions import TelegraphException

class TelegraphManager:

    def __init__(self) -> None:
        self._stations = {}
        self._messages = []
        self._encoding = {}
    
    # R1
    def add_station(self, name: str) -> int:
        self._stations[name] = Station(name)
        return len(self._stations)

    @property
    def stations(self) -> Set[str]:
        return set(self._stations.keys())

    def add_message(self, text: str, sender: str, receiver: str) -> Message:
        if sender not in self._stations:
            raise TelegraphException("Sender not defined")
        if receiver not in self._stations:
            raise TelegraphException("Receiver not defined")
        msg = Message(text, sender, receiver)
        self._messages.append(msg)
        return msg

    # R2
    def get_destinations_by_frequency(self) -> Dict[int, List[str]]:
        stations_to_freq = {s: 0 for s in self._stations.keys()}
        for msg in self._messages:
            stations_to_freq[msg.receiver] += 1
        freq_to_station = {f: [] for f in stations_to_freq.values()}
        for s, f in stations_to_freq.items():
            freq_to_station[f].append(s)
        return {f: sorted(s) for f, s in freq_to_station.items()}

    def get_most_frequent_exchange(self) -> Tuple[str, str]:
        station_pairs = {}
        for msg in self._messages:
            pair = (msg.sender, msg.receiver) if msg.sender < msg.receiver else (msg.receiver, msg.sender)
            if pair not in station_pairs:
                station_pairs[pair] = 0
            station_pairs[pair] += 1
        return max(list(station_pairs.items()), key = lambda t: t[1])[0]

    # R3
    def add_character_encoding(self, character: str, symbol: Symbol, previous: Optional[str] = None) -> str:
        if previous is not None and previous not in self._encoding:
            raise TelegraphException("Encoding for previous character not defined")
        previous = self._encoding[previous] if previous is not None else ""
        encoding = previous + symbol
        self._encoding[character] = encoding
        return encoding

    def encode_text(self, text: str) -> List[str]:
        return [" ".join([self._encoding[c] for c in word]) for word in text.split(" ")]
    
    # R4
    def add_connection(self, station_1: str, station_2: str) -> None:
        station_1 = self._stations[station_1]
        station_2 = self._stations[station_2]
        station_1.add_link(station_2)
        station_2.add_link(station_1)

    def are_connected(self, station_1: str, station_2: str) -> bool:
        return station_2 in self._stations[station_1].links

    def get_connected_stations(self, station: str) -> Set[str]:
        return set(self._stations[station].links.keys())
    
    # R5
    def get_shortest_path(self, station_start: str, station_end: str) -> Optional[List[str]]:
        explored = set()        
        to_explore = [[self._stations[station_start]]]
        while to_explore:
            path = to_explore.pop(0)
            current_station = path[-1]
            if current_station.name == station_end:
                return [s.name for s in path]
            for name, station in current_station.links.items():
                if name not in explored:
                    to_explore.append(path + [station])
                    explored.add(name)               
        return None
