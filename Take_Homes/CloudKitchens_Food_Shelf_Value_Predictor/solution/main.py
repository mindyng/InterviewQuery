from random import expovariate, uniform
from time import sleep, time
from optparse import OptionParser
from json import loads as json_loads
from src import Kitchen
import threading
import logging


def placements(kitchen: Kitchen, order_data_path: str, lambd_: float = 3.25):
    """ Reads file at data_path into memory and simulates order placements.
    We are loading entire file into memory so probably not best if we have a large
    file. We can read chunk by chunk with something like pandas but for now... meh.
    """
    with open(order_data_path) as f:
        orders = json_loads(f.read())
        for order in orders:
            print(f"Placing order for * {order['name']} *\n")
            kitchen.attempt_placement(order)
            print(kitchen, end=" ")
            print(f"---################# {time()} ####################---")
            poisson_wait = expovariate(1 / lambd_)
            sleep(poisson_wait)
    kitchen.placements_complete = True


def deliveries(kitchen: Kitchen, lo: int = 2, hi: int = 10):
    while True:
        uniform_wait = uniform(lo, hi)
        sleep(uniform_wait)
        print("Attempting a delivery...", end=" ")
        order = kitchen.attempt_delivery()

        if order is None and kitchen.placements_complete:  # No more placements, break
            print(
                "nothing delivered.\nKitchen closing down for the night. Thanks for playing!"
            )
            break
        elif order is None:  # Exponential delay between retries
            lo *= 2
            hi *= 2

        print(f"{order.name if order is not None else 'nothing'} delivered.")
        print(kitchen, end=" ")
        print(f"---################# {time()} ####################---")


def main(order_data_path: str, metadata_path: str) -> None:
    """
    In the Placements thread do the following:
        Open up a stream to the file with data
        Until stream is not at EOF
            Read in one packet at a time
            Feed that packet to kitchen.new_order(packet)
            Implement __repr__ for Kitchen class to print out state of kitchen
            Wait some time given by poisson(3.25)
        Close stream

    In the Deliveries thread do the following:
        Until kitchen's shelves have no more orders
            Deliver an order with kitchen.deliver_order()
            Wait some time given by uniform(2,10)
    """
    with open(metadata_path) as f:
        kitchen_metadata = json_loads(f.read())

    kitchen = Kitchen(kitchen_metadata)

    placements_thread = threading.Thread(
        name="placements", target=placements, args=([kitchen, order_data_path])
    )
    deliveries_thread = threading.Thread(
        name="deliveries", target=deliveries, args=([kitchen])
    )

    placements_thread.start()
    deliveries_thread.start()

    placements_thread.join()
    deliveries_thread.join()


if __name__ == "__main__":
    """ Usage: python main.py -d [file path to data] """
    parser = OptionParser()
    parser.add_option(
        "-d",
        "--data",
        dest="order_data_path",
        help="File path to read order data from",
        default="./data/orders.json",
    )

    parser.add_option(
        "-m",
        "--metadata",
        dest="metadata_path",
        help="File path to shelf metadata",
        default="./data/metadata.json",
    )

    options, _ = parser.parse_args()
    main(options.order_data_path, options.metadata_path)
