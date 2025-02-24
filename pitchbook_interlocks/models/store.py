from typing import TypeVar, Generic

T = TypeVar("T")


class Store(Generic[T]):
    def __init__(self):
        self._store: dict[str, T] = {}

    def insert(self, key: str, item: T) -> None:
        self._store[key] = item

    def get(self, key: str) -> T:
        return self._store[key]

    def exists(self, key: str) -> bool:
        return key in self._store

    def values(self) -> list[T]:
        return list(self._store.values())

    def remove(self, key: str) -> None:
        if key in self._store:
            del self._store[key]

    def keys(self) -> list[str]:
        return list(self._store.keys())

    def items(self) -> list[tuple[str, T]]:
        return list(self._store.items())
