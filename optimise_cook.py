import config
import os
from collections import Counter


class ProcessOrders:
    def __init__(self, cfg, in_csv: str) -> None:
        self.cfg = cfg
        self.in_csv = in_csv
        self.num_orders = 0

        # storing all our data inside a dictionary which is passed around
        self.rest_metadata = {k: None for k in self.cfg.dkeys}

        with open(in_csv, "r") as f:
            self.csv_r = [line.split(",") for line in f.readlines()]
            f.close()

        self.preprocess()

    def preprocess(self):
        # the first line contains the restraunt information
        self.rest_metadata["ID"] = self.csv_r[0][0]
        for i, k in enumerate(self.cfg.dkeys[1:]):
            # as we are using dictionary keys, we do not care about the string information in the cooking time asembly
            # i.e. 4C so we ignore it and convert it to an integer
            try:
                self.rest_metadata[k] = int(self.csv_r[0][i + 1])
            except ValueError:
                self.rest_metadata[k] = int(self.csv_r[0][i + 1][0])

        # there are two capacities possible in our cooking process: assembly and cooking
        # even if we could cook 4, we cannot assmeble 4 so we pick the smallest value
        self.rest_metadata["Small_Cap"] = min(
            self.rest_metadata["Cooking_Cap"], self.rest_metadata["Assemble_Cap"]
        )
        self.rest_metadata.pop("Cooking_Cap", None)
        self.rest_metadata.pop("Assemble_Cap", None)

        # deleting as we do not need anymore
        self.csv_r.pop(0)

    def process_csv(self):

        total_time = 0

        for n in self.csv_r:

            a_or_r = "ACCEPT"

            id = n[0]
            d_t = n[1]
            oid = n[2]
            orders = n[3:]
            self.num_orders = len(orders)

            time_order = self.time_cal
            total_time += time_order

            if self.num_orders > self.rest_metadata["Small_Cap"]:
                a_or_r = "REJECT"
            elif time_order > self.cfg.max_time:
                a_or_r = "REJECT"
            else:
                orders_j = "".join(orders) # combining all of our orders into one list so we can use a Counter
                num_ing_used = dict(Counter(orders_j))
                num_ing_used['P'] = 2 * self.num_orders

                # subtracting dictionaries generates a new dictionary
                new_ing = {key:self.rest_metadata[key]-num_ing_used[key] for key in num_ing_used}

                # using update to overwrite our keys
                self.rest_metadata.update(new_ing)

            print("{0}, {1}, {2}, {3}".format(id, oid, a_or_r, time_order))
        print("{0}, TOTAL, {1}".format(id, total_time))
        print("{0}, INVENTORY, {1}, {2}, {3}, {4}, {5}".format(id, self.rest_metadata['P'], self.rest_metadata['L'], self.rest_metadata['T'],
                                                               self.rest_metadata['V'], self.rest_metadata['B']))

    @property
    def time_cal(self) -> int:
        return (
            self.num_orders * self.rest_metadata["Cooking_Time"]
            + self.num_orders * self.rest_metadata["Assemble_Time"]
            + self.num_orders * self.rest_metadata["Package_Time"]
        )


if __name__ == "__main__":
    inp_csv = os.path.join(config.data_loc, "sample_input.csv")

    a = ProcessOrders(config, inp_csv)
    a.process_csv()
