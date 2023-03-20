from time import time
from collections import namedtuple
from src import Order, OrderStatus
from queue import deque
from typing import List, Tuple, Optional


class Shelf:
    """ Manages investory on shelf.

    This class belongs to a Kitchen and has many Orders. It stores orders in
    a FIFO basis as laid out in requirements.

    Attributes:
        queue: the meat of the class reprenting the FIFO structure.
        capacity: max number of orders that can be in shelf at any one time.
        ### ~ @property[ies] ~ ###
        next_created_at: returns the created_at of order at top of queue.

    Public methods:
        attempt_placement: places order in queue shelf has necessary space.
        attempt_delivery: deliver next-in-line order if present.
        discard_zero_value_orders: discards orders with zero value from queue.
        has_space:
    """

    def __init__(self, temp, capacity: int = 15) -> None:
        self.capacity = capacity
        self.queue = deque(maxlen=self.capacity)
        self.type = temp

    def __str__(self) -> str:
        shelf_header = f"###### {self.type} ######\n"
        if not self._has_next():
            return shelf_header + f"{self.type} shelf is empty!\n\n"

        order_strs = [
            str(order) + f"value_norm: {self._normalize_value(order)}\n\n"
            for order in self.queue
        ]

        return "".join([shelf_header] + order_strs)

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self.queue)

    def _normalize_value(self, order: Order) -> float:
        min_, max_ = self._get_minmax_values()
        range_ = max_ - min_
        return (order.value - min_) / range_ if range_ else 1

    @property
    def next_created_at(self) -> Optional[float]:
        """ Property for top order created_at timestamp.
        Returns:
            A timestamp seconds since epoch for the order at the top of the queue
        """
        if self._has_next():
            return self._get_next_created_at()

    ##########################
    ### ~ Public methods ~ ###
    ##########################

    def attempt_placement(self, order: Order) -> bool:
        """ Places order in queue shelf has necessary space.

        Args:
            order: order to be appended to queue

        Returns:
            True if placement successful, False otherwise
        """
        if not self.has_space():
            return False
        self._place_order(order)
        return True

    def attempt_delivery(self) -> Optional[Order]:
        """ Deliver next-in-line order if present. """
        if self._has_next():
            return self._deliver_order()

    def discard_zero_value_orders(self) -> List[Order]:
        """ Discards orders with value <= 0.
        Mutates orders whose value has dropped below 0 by setting the order
        discarded_at timestamp
        Mutates queue by filtering the orders that have discarded_at timestamp set

        Returns:
            A list of orders that have been mutated and removed from the queue
        """
        discarded = []
        for i, order in enumerate(self.queue):
            if not order.has_value():
                order.discarded_at = time()
                discarded.append(order)
                self.deque.remove(order)
        return discarded

    def has_space(self) -> bool:
        """ Checks whether the shelf has reached capacity or not. """
        return len(self.queue) < self.capacity

    def is_empty(self) -> bool:
        return not self._has_next()

    def empty_shelf(self) -> None:
        self.queue = deque(maxlen=self.capacity)

    def count_waiting_orders(self) -> int:
        return sum([order.status == OrderStatus.waiting for order in self.queue])

    ###########################
    ### ~ Private methods ~ ###
    ###########################

    def _place_order(self, order: Order) -> None:
        self.queue.append(order)

    def _deliver_order(self) -> Order:
        order = self._pop_next()
        order.delivered_at = time()
        return order

    def _pop_next(self) -> Order:
        """ Gets the order from the top of the queue.
        Mutates the queue by popping the "next" order from the top of the queue
        """
        if self.is_empty():
            raise IndexError("Shelf is empty!")
        return self.queue.popleft()

    def _peek_next(self) -> Optional[Order]:
        """ See :meth: _pop_next """
        if not self.is_empty():
            return self.queue[0]

    def _get_minmax_values(self) -> Tuple[float]:
        """ Gets the min and max values of orders on shelf.
        Used for calculating the normalized value of each order when displaying.

        Returns:
            Tuple of floats representing min and max values of orders on shelf.
        """
        values = self._get_values()
        return min(values), max(values)

    def _get_values(self) -> List[float]:
        """ Gets list of values of all orders currently on shelf. """
        return list(map(lambda order: order.value, self.queue))

    def _get_next_created_at(self) -> float:
        """ Gets the created_at timestamp for order at top of queue. """
        return self._peek_next().created_at

    def _has_next(self) -> bool:
        """ Checks whether shelf has at least 1 order. """
        return len(self.queue) >= 1


class Borg:
    """ Alex Martelli's 'Borg' singleton class."""

    _shared_state = {}

    def __init__(self):
        self.__dict__ = self._shared_state


class Kitchen(Borg):
    """ Orchestrates order placements and deliveries.
    The meat of the project is defined here.

    To ensure safety of our data we make Kitchen a singleton class with
    Alex Martelli's 'Borg' singleton class.

    Attribtutes:
        shelf_dict: a mapping between shelf_name: [shelf instance] e.g. "Hot": <Shelf>
        recently_discarded: a queue holding a sliding window of recently discarded orders
        recently_delivered: see :attr: recently_discarded
        ### ~ @property[ies] ~ ###
        overflow_shelf: gets the overflow shelf from shelf_dict with "overflow" key
        shelves: casts dict_values of :attr: shelf_dict to list

    Public methods:
        attempt_placement:
        attempt_delivery:
        discard_zero_value_orders:
    """

    def __init__(self, metadata, max_retention: int = 50) -> None:
        Borg.__init__(self)
        if not hasattr(self, "set"):  # Ensures single state for data
            self.shelf_dict = {
                temp.lower(): Shelf(temp, capacity)
                for temp, capacity in metadata.items()
            }
            self.max_retention = max_retention
            self.recently_discarded = deque(maxlen=max_retention)
            self.recently_delivered = deque(maxlen=max_retention)
            self.placements_complete = False
            self.set = True

    def __str__(self) -> str:
        shelf_strs = [str(self.shelf_dict[temp]) for temp in self.shelf_dict]
        return "".join(shelf_strs)

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def overflow_shelf(self) -> Shelf:
        return self._get_shelf("overflow")

    @property
    def shelves(self) -> List[Shelf]:
        return [shelf for shelf in self.shelf_dict.values()]

    ##########################
    ### ~ Public methods ~ ###
    ##########################
    def attempt_placement(self, data: dict) -> bool:
        """ Creates order and places it on shelf or discards it.
        Attributes:
            data: a dictionary representing the order data

        Returns:
            True if order was successfully placed, False otherwise
        """
        order = self._create_order(data)

        if self._has_shelf_space(order.temp) and order.has_value():
            self.discard_zero_value_orders()
            return self._place_order(order)

        # Nowhere to put order, discard immediately
        self._discard_order(order)
        return False

    def attempt_delivery(self) -> Optional[Order]:
        """ Delivers the next order if available.
        This will deliver the oldest found on any shelf, if one exists. The order
        is taken from the current shelf and added to :attr: recently_delivered queue.
        """
        shelf = self._get_next_shelf()
        if shelf is not None:
            order = self._deliver_next_from(shelf)
            self.discard_zero_value_orders()
            return order

    def discard_zero_value_orders(self) -> None:
        """ See :cls: Shelf :meth: discard_zero_value_orders.
        Discards zero value orders from all non-empty shelves. Adds discarded
        orders to :attr: recently_discarded.
        """
        for shelf in self._get_non_empty_shelves():
            self.recently_discarded.extend(shelf.discard_zero_value_orders())

    def empty_kitchen(self) -> None:
        for shelf in self.shelves:
            shelf.empty_shelf()

        self.recently_discarded = deque(maxlen=self.max_retention)
        self.recently_delivered = deque(maxlen=self.max_retention)

    ###########################
    ### ~ Private methods ~ ###
    ###########################
    def _create_order(self, data: dict) -> Order:
        return Order(data)

    def _count_waiting_orders(self) -> int:
        """ Counts all orders on all shelves. """
        return sum([shelf.count_waiting_orders() for shelf in self.shelf_dict.values()])

    def _count_recently_discarded(self) -> int:
        return len(self.recently_discarded)

    def _count_recently_delivered(self) -> int:
        return len(self.recently_delivered)

    def _discard_order(self, order: Order) -> None:
        """ Called directly from Kitchen when order never placed on shelf. """
        order.discarded_at = time()
        self.recently_discarded.append(order)

    def _deliver_next_from(self, shelf: Shelf) -> Optional[Order]:
        order = shelf.attempt_delivery()
        if order is not None:
            self.recently_delivered.append(order)
            return order

    def _get_non_empty_shelves(self) -> List[Order]:
        """ Gets non-empty shelves, empty list if no non-empty shelves. """
        return [shelf for shelf in self.shelves if not shelf.is_empty()]

    def _get_next_shelf(self) -> Optional[Shelf]:
        shelves = self._get_non_empty_shelves()
        if len(shelves) > 0:
            return min(shelves, key=lambda shelf: shelf.next_created_at)

    def _get_shelf(self, temp: str) -> Shelf:
        temp = temp.lower()
        if temp not in self.shelf_dict:
            raise ValueError(f"No {temp} shelf in shelf_dict:\n {self.shelf_dict}")
        return self.shelf_dict[temp]

    def _get_available_shelf(self, temp: str) -> Shelf:
        shelf = self._get_shelf(temp)
        return shelf if shelf.has_space() else self.overflow_shelf

    def _has_next(self) -> bool:
        return any([shelf.has_space() for shelf in self.shelves])

    def _has_shelf_space(self, temp: str) -> bool:
        shelf = self._get_shelf(temp)
        return shelf.has_space() or self.overflow_shelf.has_space()

    def _place_order(self, order: Order) -> bool:
        shelf = self._get_available_shelf(order.temp)
        return shelf.attempt_placement(order)
