# Restaurant_Challenge

## Repository & Project Organisation

This is a repo dedicated towards solving the restaurant order challenge. A high level overview:

    ├── README.md          <- The top-level README for this project.
    ├── config.py          <- Contains all the variable data in our problem
    ├── data/              <- Contains the data for our challenge
    ├── order.py           <- Code containing order classes
    ├── restaurant.py      <- Code containing restaurant class
    ├── solution.py        <- Code containing the running of the problem
    ├── tests              <- Unit tests here
    ├── Pipfile            <- Pipenv requirements template.

# Prerequisites

Ensure you have pipenv installed.  If not, you can use the following command:

    pip install --user pipenv

## Installation and Running

    pipenv shell
    pipenv install
    python3 solution.py


## A note on the the data

As it can be seen in the sample_input.csv, the order of the data is actually incorrect. Earlier order numbers, i.e. 05, have a later time stamp vs other orders i.e. 06. This is left as is and is assumed that there may have been an outage. Otherwise, one could try and sort the data in an ordered fashion.


## Formatting

Please note that black was used to format the code to adhere to pep8 rules.
