Cleanspark llc : Electricity Pricing Model Takehome

Machine Learning
Python
Pandas
Regression
Time Series
Finish Time :
6 Hrs
Clean Spark


CleanSpark Python Exercise: June 2019

This repository is where we (CleanSpark) host the take-home Python exercise for the Junior Data Scientist/Analyst position. Please carefully read this entire document before continuing. There is a fair amount of scaffolding in this repo to ensure everyone starts on an even playing field. This scaffolding includes packages that you may not be familiar with; however, we outline their primary usage below. Learning to work with new open-source packages is a core skill required for any successful Python developer.


Getting started

Note from IQ Staff: There were steps here for installing and using
pip and pipenv, these have been removed since the required packages
are already in Google Colab

Running tests

It is commonly accepted that code without tests is bad code. For that reason, all production code is thoroughly tested at CleanSpark. Python code is verified using the pytest package. The good news is, we had already installed pytest and written tests for you.

We need to make sure you know how to run the tests we have written. Run the following command inside of your virtual environment:

!python -m pytest
You should see that all the tests are failing. It is your job to get these tests to pass by writing code. Keep reading for a description of the code you will need to write. The code of billing_unit_test.py is included below

```
"""Unit test suite for clsk.billing."""

from math import isclose

import pytest

import billing


def test_energy_charge(): # noqa: D103
# Arrange ----------------------------------------------------------------
data = billing._get_data()
# Act --------------------------------------------------------------------
result = billing.energy_charge(data)
# Assert -----------------------------------------------------------------
assert isclose(result, 7429.879999999999, rel_tol=1e-4)


def test_demand_charge(): # noqa: D103
# Arrange ----------------------------------------------------------------
data = billing._get_data()
# Act --------------------------------------------------------------------
result = billing.demand_charge(data)
# Assert -----------------------------------------------------------------
assert isclose(result, 2240.0, rel_tol=1e-4)
```

NOTE: You should not alter billing_unit_test.py. These tests were written for you to pass and to expose you to how to write tests in Python.


Problem Description


Energy and Power

At CleanSpark we analyze electricity bills every day. In general, an electricity bill is composed of two primary parts: energy charges and maximum-power (demand) charges. In order to understand these two portions of the bill, we must first understand the difference between energy and power.

One helpful analogy is between electricity consumption and driving your car. In order to understand this better, let’s use a concrete example. Imagine you want to drive from San Diego to San Francisco this weekend. After checking Google Maps, you know that you need to travel roughly 500 miles.

Now, let’s assume someone asked you how long it will take you to get to San Francisco. What would you say? … Hopefully, you thought to yourself, I don’t have enough information. I need to know how fast I am driving in order to know how long it will take.”

This is because time and distance require a speed (or rate) to convert between the two. You may recall the familiar definition of a rate:


speed = distance/time
 

Now, assume I also told you that you will be traveling at an average speed of 60 mph over your 500 mile journey to San Francisco and then asked you how long it would take. Using our definition of speed (rate) we can easily calculate the time required to get to San Francisco:

time = distance/speed = 500 mi/60 mph = 8.3 h

Extending the example above to electricity we can say that energy is to distance what power is to speed. However the units can be a bit tricky. Energy is measured in kWh and power is measured in kW. In order to provide some more context, let\’s assume a building consumed 50 kWh over a 30 minute period and I asked you what the averave power was. Well extending our formula from above:

power = energy/time = 50kWh/0.5h = 100kW

Now that you understand energy and power we can discuss how energy bills are typically calculated.


Electricity bills

As mentioned before, energy bills have two primary components: energy and max-power (demand). These two portions are calculated in completely different ways. We will first discuss energy and then max-power (demand).

Energy rates have units of $/kWh and are calculated at every 15 minute interval. For example, if the energy rate is 
$0.01/kWh and the building consumed 100 kWh of energy over that 15 minute interval, they are charged $1.00. This occurs at every 15 minute interval in the month and all of the charges get summed up. This sum of energy charges is the energy portion of your bill. *Note: This operation is very similar to a dot product.* Max-power (demand) rates have units of 
$/kW and are calculated only once per month. For example, for an entire month of data let\'s assume the maximum average power (demand) in a single interval was 100 kW and the demand rate is 
$
$20/kW. The customer would be they are charged \$2000 once for that month.


Problem

You are given a month electricity consumption data (kWh) in 15 minute intervals for a commercial facility located in San Diego, CA. This data can be read into a pandas DataFrame using the pre-coded _get_data function in the cell below. Each interval is labeled with the time it began and all intervals are 15 minutes long. Your task is to add logic to the two stubbed functions in the cell below module. The first method is called energy_charge and the second is called demand_charge.

An example pricing scheme (electricity tariff) is outlined below. Your functions will need to use the electricity consumption data and the pricing scheme to calculate the energy and demand charges. Please feel free to import any other third party packages you think you will need. In additions, feel free to write as many extra helper functions as you need and include them in the cell below file as well.


Energy rates

Period	Rate
Weekends	\$0.05/kWh|1 |Weekdays (12:00 am - 4:00 pm)| \$0.20/kWh
Weekdays (4:00 pm - 9:00 pm)	\$0.30/kWh| |Weekdays (9:00 pm - 12:00 am)| \$0.10/kWh
Demand rates

Monthly max: \$20/kW


Correct Solution

You will know if you have implemented the logic correctly when you run your tests and both of them pass.

Good luck and happy coding!
