# Satis.AI_coding

## Repository & Project Organisation

This is a repo dedicated towards solving the coding challenege. A high level overview:

    ├── README.md          <- The top-level README for developers/data-scientists using this project.
    ├── base               <- Contains a wrapper for both model and trainer which should be inherted (see utils/trainer)
    ├── config.py          <- Contains all the variable data in our problem
    ├── optimise_cook.py   <- Code solving the problem
    ├── tests              <- Unit tests here
    ├── Pipfile            <- Pipenv requirements template.

## Running the Repo

# Prerequisites

Ensure you have pipenv installed.  If not, you can use the following command:

    pip install --user pipenv

## Installation and Running

Make sure you have the airbag images, if not please contact me and I will send them to you.

    pipenv shell
    pipenv install
    python3 optimise_cook.py
    
    

## A note on the the data

As it can be seen in the sample_input.csv, the order of the data is actually incorrect. Earlier order numbers, i.e. 05, have a later time stamp vs other orders i.e. 06. Due to this, we re-order the data for 
