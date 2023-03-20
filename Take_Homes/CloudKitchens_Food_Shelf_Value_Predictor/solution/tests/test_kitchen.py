import unittest
import random
import src
from src import Kitchen


class KitchenTestCase(unittest.TestCase):
    """" Kitchen test cases."""

    def setUp(self):
        """ Create simple order """
        global kitchen

        self.order_names = [
            "A Calamari Nugget",
            "Banana Split",
            "McFlurry",
            "Acai Bowl",
            "Yoghurt",
        ]
        self.order_temps = ["Hot", "Frozen", "Frozen", "Cold", "Cold"]
        self.order_decay_rates = [0.5, 0.63, 0.4, 0.3, 0.37]
        self.order_shelf_lifes = [360, 20, 375, 249, 263]
        self.shelf_data = {"Hot": 15, "Cold": 15, "Frozen": 15, "Overflow": 20}

        kitchen = Kitchen(self.shelf_data)

        # Used to artifically induce age to test value computations
        self.backdate_by = 10

    def tearDown(self):
        kitchen.empty_kitchen()

    def test_place_single_order_count(self):
        order_data = self.generate_order_data()
        kitchen.attempt_placement(order_data)

        self.assertEqual(kitchen._count_waiting_orders(), 1)

    def test_place_single_order_shelf(self):
        order_data = self.generate_order_data()
        placed = kitchen.attempt_placement(order_data)
        shelf = kitchen._get_shelf(order_data["temp"])
        overflow_shelf = kitchen.overflow_shelf

        self.assertEqual(placed, True)
        self.assertEqual(len(overflow_shelf), 0)
        self.assertEqual(len(shelf), 1)

    def test_place_multiple_orders_shelf(self):
        temp = "Hot"
        times = self.shelf_data[temp]
        for _ in range(times):
            kitchen.attempt_placement(self.generate_order_data(temp=temp))

        shelf = kitchen._get_shelf(temp)
        self.assertEqual(len(shelf), times)

    def test_overflow_after_shelf_full(self):
        temp = "Hot"
        times = self.shelf_data[temp]
        for _ in range(times):
            kitchen.attempt_placement(self.generate_order_data(temp=temp))

        kitchen.attempt_placement(self.generate_order_data(temp=temp))

        self.assertEqual(len(kitchen.overflow_shelf), 1)

    def test_auto_discard_if_overflow_full(self):
        temp = "Hot"
        times = self.shelf_data[temp] + self.shelf_data["Overflow"]
        for _ in range(times):
            kitchen.attempt_placement(self.generate_order_data(temp=temp))
        kitchen.attempt_placement(self.generate_order_data(temp=temp))

        self.assertEqual(kitchen._count_recently_discarded(), 1)

    def test_auto_discard_zero_value_orders(self):
        temps = ["Hot", "Cold", "Frozen"]
        for temp in temps:
            order_data = self.generate_order_data(temp=temp, shelfLife=0)
            kitchen.attempt_placement(order_data)

        overflow_order_data = self.generate_order_data(temp="overflow", shelfLife=0)
        kitchen.attempt_placement(overflow_order_data)

        self.assertEqual(kitchen._count_waiting_orders(), 0)
        self.assertEqual(kitchen._count_recently_discarded(), 4)

    def test_discard_zero_value_orders(self):
        pass

    def generate_order_data(self, **kwargs):
        return {
            "name": self.generate_order_name(**kwargs),
            "temp": self.generate_order_temp(**kwargs),
            "decayRate": self.generate_order_decay_rate(**kwargs),
            "shelfLife": self.generate_order_shelf_life(**kwargs),
        }

    def generate_order_name(self, **kwargs):
        return kwargs["name"] if "name" in kwargs else random.choice(self.order_names)

    def generate_order_temp(self, **kwargs):
        return kwargs["temp"] if "temp" in kwargs else random.choice(self.order_temps)

    def generate_order_decay_rate(self, **kwargs):
        return (
            kwargs["decayRate"]
            if "decayRate" in kwargs
            else random.choice(self.order_decay_rates)
        )

    def generate_order_shelf_life(self, **kwargs):
        return (
            kwargs["shelfLife"]
            if "shelfLife" in kwargs
            else random.choice(self.order_shelf_lifes)
        )
