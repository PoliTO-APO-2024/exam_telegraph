from collections.abc import Collection
from typing import Dict, List, Tuple, Set, Optional
from telegraph.elements import Message, Symbol
from telegraph.exceptions import TelegraphException

class TelegraphManager:

    def __init__(self) -> None:
        pass
    
    # R1
    def add_station(self, name: str) -> int:
        pass

    @property
    def stations(self) -> Set[str]:
        pass

    def add_message(self, text: str, sender: str, receiver: str) -> Message:
        pass

    # R2
    def get_destinations_by_frequency(self) -> Dict[int, List[str]]:
        pass

    def get_most_frequent_exchange(self) -> Tuple[str, str]:
        pass

    # R3
    def add_character_encoding(self, character: str, symbol: Symbol, previous: Optional[str] = None) -> str:
        pass

    def encode_text(self, text: str) -> List[str]:
        pass
    
    # R4
    def add_connection(self, station_1: str, station_2: str) -> None:
        pass

    def are_connected(self, station_1: str, station_2: str) -> bool:
        pass

    def get_connected_stations(self, station: str) -> Set[str]:
        pass
    
    # R5
    def get_shortest_path(self, station_start: str, station_end: str) -> Optional[List[str]]:
        pass
