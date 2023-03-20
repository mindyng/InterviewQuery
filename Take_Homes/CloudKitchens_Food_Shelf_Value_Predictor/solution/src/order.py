from enum import Enum
from time import time


class OrderStatus(Enum):
    waiting = 1
    delivered = 2
    discarded = 3


class Order:
    """ Represents each order and in charge of computing current value.

    Attributes:
        name:
        temp:
        decay_rate:
        shelf_life:
        created_at:
        status:
        overflow_in:
        overflow_out:
        _discarded_at:
        _delivered_at:
        ### ~ @property[ies] ~ ###
        terminated_at:
        delivered_at:
        discarded_at:
        status:
        total_decay:
        order_age:
        value:
        infant_value:
        regular_decay:
        overflow_decay:

    Public methods:
        has_value: Checks to see whether :attr: value is > 0

    """

    def __init__(self, data: dict, overflow: bool = False):
        try:
            self.name = data["name"]
            self.temp = data["temp"]
            self.decay_rate = float(data["decayRate"])
            self.shelf_life = int(data["shelfLife"])
        except KeyError as e:
            # TODO meh bug report https://bugs.python.org/issue2651
            raise KeyError(
                "Inadequate data to create Order.\n"
                f"Missing key: {e}\n"
                f"data: {data}\n"
            )

        self.created_at = time()
        self.status = OrderStatus.waiting
        self.overflow_in = time() if overflow else None
        self.overflow_out = None
        self._discarded_at = None
        self._delivered_at = None

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return (
            f"~~ {self.name} ~~\n"
            # f"status: {self.status.name}\n"
            # f"temp: {self.temp}\n"
            # f"shelf_life: {self.shelf_life}\n"
            f"value: {self.value}\n"
            # f"\tinfant_value: {self.infant_value}\n"
            # f"total_decay: {self.total_decay}\n"
            # f"\ttemp: {self.regular_decay}\n"
            # f"\toverflow_decay: {self.overflow_decay}\n"
            # f"\tdecay_rate: {self.decay_rate}\n"
            # f"created_at: {self.created_at}\n"
            # f"\toverflow_in: {self.overflow_in}\n"
            # f"\toverflow_out: {self.overflow_out}\n"
        )

    @property
    def terminated_at(self) -> float:
        """Basically serves to freeze the aging process of an order if terminated. """
        return self.delivered_at or self.discarded_at

    @property
    def delivered_at(self) -> float:
        return self._delivered_at

    @property
    def discarded_at(self) -> float:
        return self._discarded_at

    @property
    def status(self) -> float:
        return self._status

    @property
    def total_decay(self) -> float:
        return self.regular_decay + self.overflow_decay

    @property
    def order_age(self) -> float:
        return self._compute_order_age()

    @property
    def value(self) -> float:
        return self._get_value()

    @property
    def infant_value(self) -> float:
        return self.shelf_life

    @property
    def regular_decay(self) -> float:
        return self._compute_regular_decay()

    @property
    def overflow_decay(self) -> float:
        return self._compute_overflow_decay()

    @delivered_at.setter
    def delivered_at(self, delivered_at: float) -> None:
        self._delivered_at = delivered_at
        self.status = OrderStatus.delivered

    @discarded_at.setter
    def discarded_at(self, discarded_at: float) -> None:
        self._discarded_at = discarded_at
        self.status = OrderStatus.discarded

    @status.setter
    def status(self, status: OrderStatus) -> None:
        if type(status) != OrderStatus:
            raise ValueError("status must be of type OrderStatus")
        self._status = status

    ###########################
    ### ~ Public methods ~ ###
    ###########################
    def has_value(self) -> bool:
        return self.value > 0

    ###########################
    ### ~ Private methods ~ ###
    ###########################
    def _compute_overflow_decay(self) -> float:
        """ Computes decay attributed to being on overflow shelf. """
        return 2 * self.decay_rate * self._compute_overflow_shelf_age()

    def _compute_regular_decay(self) -> float:
        """ Computes decay attributed to being on a regular shelf. """
        return self.decay_rate * self._compute_regular_shelf_age()

    def _compute_order_age(self) -> float:
        start = self.created_at
        end = self.terminated_at if self._is_terminated() else time()
        return end - start

    def _compute_overflow_shelf_age(self) -> float:
        if not self._has_overflow():
            return 0.0
        overflow_out = time() if self.overflow_out is None else self.overflow_out

        return overflow_out - self.overflow_in

    def _compute_regular_shelf_age(self) -> float:
        return self.order_age - self._compute_overflow_shelf_age()

    def _currently_on_overflow_shelf(self) -> bool:
        return self._has_overflow() and self.overflow_out is None

    def _get_value(self) -> bool:
        """ Compute value based on following formula:
        value = ([shelf life] - [order age]) - ([overflow shelf decay]) - ([regular shelf decay])
        """
        return self.infant_value - self.order_age - self.total_decay

    def _has_overflow(self) -> bool:
        return self.overflow_in is not None

    def _is_terminated(self) -> bool:
        return self.terminated_at is not None
