### System Requirements
1. brew
1. python 3.7
1. pipenv

### Setup

    make init

### Run

    python main.py
Note that I have provided some data files in `./data`. Check these out to change the order data thrown thru the system.

### Test

    make test


## Discussion

### Tests
Some important stuff that is not tested includes the Shelf class and orchestration behaviour of Kitchen class.

Also singleton pattern for Kitchen -- I thought it would be a good idea but I'm having second thoughts.

I'm happy the the test coverage for Order -- wrote these first ;-)

### Overflow
The way I implemented the overflow shelf and was to split out the concept of a order's value into initial_value - total_decay:

    infant_value: this is basically shelf_life in this example but could be different.
    regular_decay: order decay due to sitting on a regular shelf
    overflow_decay: order decay due to sitting on overflow shelf
