class Symbol:
    DOT = "."
    DASH = "-"

class Message:
    def __init__(self, text: str, sender: str, receiver: str):
        self._text = text
        self._sender = sender
        self._receiver = receiver

    @property
    def text(self) -> str:
        return self._text

    @property
    def sender(self) -> str:
        return self._sender

    @property
    def receiver(self) -> str:
        return self._receiver

    def __len__(self) -> int:
        return len(self.text)


class Station:
    def __init__(self, name):
        self._name = name
        self._links = {}

    @property
    def name(self):
        return self._name

    @property
    def links(self):
        return self._links

    def add_link(self, station):
        self._links[station.name] = station

    



