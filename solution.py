import os

import config
from order import CSVOrderParser
from restaurant import Restaurant

if __name__ == "__main__":
    inp_csv = os.path.join(config.data_loc, "sample_input.csv")

    with open(inp_csv, "r") as f:
        meta_res = f.readline().split(",")
        orders = [CSVOrderParser().parse_order(line) for line in f.read().splitlines()]
        f.close()

    res = Restaurant(config, meta_res)

    for val in orders:
        res.accept(val)
    res.final_report()
