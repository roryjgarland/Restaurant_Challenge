# Restaurant_Challenge

In this challenge we want to solve the restaurant capacity challenge given some input data. To solve this problem, we use the idea of discrete time steps where the restaurant has its time defined by the order and then is updated once a new order comes in.


## Repository & Project Organisation

This is a repo dedicated towards solving the restaurant order challenge. A high level overview:

    ├── README.md          <- The top-level README for this project.
    ├── config.py          <- Contains all the variable data in our problem
    ├── data/              <- Contains the data for our challenge
    ├── order.py           <- Code containing order classes
    ├── restaurant.py      <- Code containing restaurant class
    ├── solution.py        <- Code containing the running of the problem
    ├── tests/             <- Folder for unit tests
    ├── Pipfile            <- Pipenv requirements template.

# Prerequisites

Ensure you have pipenv installed.  If not, you can use the following command:

    pip install --user pipenv

## Installation and Running

    pipenv shell
    pipenv install
    python3 solution.py


## Formatting

Please note that black was used to format the code to adhere to pep8 rules.


## Todo:

This is sequential in orders and could be improved. i.e. if we have an order of 5 burgers, we currently just add on a 
penalty and then process the next order. However, if we were to have an order of 3 burgers to come in afterwards we 
could possibly cook these at the same time thus speeding up time!


Have a dictionary which tracks all orders and times to do orders. This allows us to see a history of the orders and what the most popular order type/amount was, thus allowing us to better prepare.
