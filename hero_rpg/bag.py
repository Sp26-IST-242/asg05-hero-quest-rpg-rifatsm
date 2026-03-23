"""
bag.py
======
Generic Bag[T] container for the Hero Quest RPG.

Key concept:
  TypeVar T is a placeholder resolved at instantiation time.
  Bag[Item] and Bag[Weapon] are the same class, but the type checker
  ensures you never accidentally mix the two.
"""

from typing import TypeVar, Generic

# T can stand for any type; resolved when Bag[T] is used
T = TypeVar("T")


class Bag(Generic[T]):
    """
    A capacity-limited generic container that holds items of any type T.

    Attributes:
        capacity : Maximum number of items allowed.
        _items   : Internal (private) list (ordered, indexed) storing items of type T.
    """

    def __init__(self, capacity: int) -> None:
        self.capacity: int = capacity
        self._items: list[T] = []

    def add(self, item: T) -> bool:
        """
        Add an item to the bag.

        Returns:
            True  — item added successfully.
            False — bag is at capacity; item rejected.
        """
        if len(self._items) >= self.capacity:
            return False
        self._items.append(item)
        return True

    def remove(self, item: T) -> bool:
        """
        Remove the first occurrence of `item`.

        Returns:
            True  — item found and removed.
            False — item not present in the bag.
        """
        if item in self._items:
            self._items.remove(item)
            return True
        return False

    def all(self) -> list[T]:
        """Return a shallow copy so the internal list stays protected."""
        return list(self._items)

    def is_full(self) -> bool:
        """Return True when no more items can be added."""
        return len(self._items) >= self.capacity 

    def __len__(self) -> int:
        """Support len(bag)."""
        return len(self._items)
        
