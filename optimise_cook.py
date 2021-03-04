import config
import os
import datetime
from collections import Counter


class ProcessOrders:
    def __init__(self, cfg, in_csv: str) -> None:
        self.cfg = cfg
        self.in_csv = in_csv
        self.num_orders = 0

        # storing all our data inside a dictionary which is passed around
        self.rest_metadata = {k: None for k in self.cfg.dkeys}

        with open(in_csv, "r") as f:
            self.csv_r = [line.split(",") for line in f.read().splitlines()]
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

        # deleting as we do not need anymore
        self.csv_r.pop(0)

    def process_csv(self):

        total_time = 0
        time_left = 20  # total time we have, if we have

        for n in self.csv_r:

            a_or_r = "ACCEPT"

            id = n[0]
            d_t = datetime.datetime.strptime(
                n[1], "%Y-%m-%d %H:%M:%S"
            )  # “YYYY-MM-DD hh:mm:ss” format
            oid = n[2]
            orders = n[3:]
            self.num_orders = len(orders)

            time_order = self.time_cal  # how long it takes to process the current order
            order_finished = d_t + datetime.timedelta(0, time_order * 60)

            if time_order > self.cfg.max_time:
                # if the order takes more than 20 minutes
                a_or_r = "REJECT"
            elif time_order > time_left:
                # this occurs when we may already have an order in flight and thus cannot have two orders simulatenously
                # occuring due to capacity issues
                a_or_r = "REJECT"
            elif (
                min(
                    self.rest_metadata["P"],
                    self.rest_metadata["L"],
                    self.rest_metadata["T"],
                    self.rest_metadata["V"],
                    self.rest_metadata["B"],
                )
                <= 0
            ):
                a_or_r = "REJECT"
            else:
                total_time += time_order
                time_left -= time_order
                orders_j = "".join(
                    orders
                )  # combining all of our orders into one list so we can use a Counter
                num_ing_used = dict(Counter(orders_j))
                num_ing_used["P"] = 2 * self.num_orders

                # subtracting dictionaries generates a new dictionary
                new_ing = {
                    key: self.rest_metadata[key] - num_ing_used[key]
                    for key in num_ing_used
                }

                # using update to overwrite our keys
                self.rest_metadata.update(new_ing)

            print("{0}, {1}, {2}, {3}".format(id, oid, a_or_r, time_order))
            time_left = 20
        print("{0}, TOTAL, {1}".format(id, total_time))
        print(
            "{0}, INVENTORY, {1}, {2}, {3}, {4}, {5}".format(
                id,
                self.rest_metadata["P"],
                self.rest_metadata["L"],
                self.rest_metadata["T"],
                self.rest_metadata["V"],
                self.rest_metadata["B"],
            )
        )

    @property
    def time_cal(self) -> int:
        # these ratios handle how many burgers can be assembled at once, as an example if we have 5 burgers with a
        # capacity of 4, 3, 2 our ratio is 5/4, 5/3, 5/2 for our total time!

        burger_ratio = self.num_orders / self.rest_metadata["Cooking_Time"]
        assemble_ratio = self.num_orders / self.rest_metadata["Assemble_Time"]
        package_ratio = self.num_orders / self.rest_metadata["Package_Time"]

        return (
            burger_ratio * self.rest_metadata["Cooking_Time"]
            + assemble_ratio * self.rest_metadata["Assemble_Time"]
            + package_ratio * self.rest_metadata["Package_Time"]
        )


if __name__ == "__main__":

    # read each csv per line
    # push each csv per line

    inp_csv = os.path.join(config.data_loc, "sample_input.csv")

    a = ProcessOrders(config, inp_csv)
    a.process_csv()
