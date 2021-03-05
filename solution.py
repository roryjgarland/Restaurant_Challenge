import os

import config
from order import CSVOrderParser
from restaurant import Restaurant

if __name__ == "__main__":
    inp_csv = os.path.join(config.data_loc, "sample_input.csv")

    with open(inp_csv, "r") as f:
        meta_csv = [line.split(",") for line in f.read().splitlines()]
        f.close()

    res = Restaurant(config, meta_csv[0])

    for val in meta_csv[1:]:
        val_o = CSVOrderParser().parse_order(val)
        res.accept(val_o)
    res.final_report()
