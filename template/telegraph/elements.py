class Symbol:
    DOT = "."
    DASH = "-"

class Message:

    @property
    def text(self) -> str:
        pass

    @property
    def sender(self) -> str:
        pass

    @property
    def receiver(self) -> str:
        pass

    def __len__(self) -> int:
        pass
