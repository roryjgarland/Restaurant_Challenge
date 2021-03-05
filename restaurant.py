import datetime
from collections import Counter
from typing import List, Tuple, Union

import config
from order import Order


class Restaurant:
    """
    Our restaurant class which takes in a config file and initial parameters to construct it. i.e.

    res = Restaurant(cfg, init_p)

    These will contain all the information on the restaurant, from ingredients used to the capacity of the store.
    Restaurant also keeps tracking the number of orders in flight, the current time (updated by a new order), and the
    total time taken.

    To pass an order to the Restaurant, we can do the following

    res.accept(order)

    This does two things, first it calls self.__check_capacity(order) which monitors which orders are currently in
    flight and decides if another order can be undertaken or not. Depending on the various outcomes, an accept or reject
    is returned. If enough time has passed, __check_capacity(order), will update the current capacity as previous orders
    will have completed part of their operation. If enough time has passed, the order will be removed. The second thing
    it does is returns a string output of the state of the order.

    Following each of the orders, we produce our final statistics via

    res.final_report()

    """

    def __init__(self, cfg: config, init_p: List[str]) -> None:
        """
        :param cfg: Config with meta parameters i.e ing, data loc, etc
        :param init_p: init parameters for restaurant
        """
        self.cfg = cfg
        self.init_p = init_p
        self.num_orders = 0
        self.total_time = datetime.timedelta(0, 0)

        self.current_time = datetime.timedelta(0, 0)  # the time at the restaurant
        self.orders_in_flight = []  # list of all the orders being done
        self.current_capacity = self.cfg.max_time

        self.rest_metadata = {k: None for k in self.cfg.dkeys}

        self.rest_metadata["ID"] = self.init_p[0]

        for i, k in enumerate(self.cfg.dkeys[1:]):
            # as we are using dictionary keys, we do not care about the string information in the cooking time assembly
            # i.e. 4C so we ignore it and convert it to an integer

            try:
                self.rest_metadata[k] = int(self.init_p[i + 1])
            except ValueError:
                self.rest_metadata[k] = int(self.init_p[i + 1][0])

    def accept(self, order: Order) -> None:
        """
        :param order: Order object containing relevant parameters
        :return:
        """
        a_or_r, time_order = self.__check_capacity(order)
        print("{0}, {1}, {2}, {3}".format(order.r_id, order.o_id, a_or_r, time_order))

    def __check_capacity(
        self, order
    ) -> Union[Tuple[str, str], Tuple[str, datetime.timedelta]]:
        """
        Function which checks capacity every time an order is called
        order
        :return:
        """

        self.current_time = order.time

        # first we need to check if our current orders being processed has been updated
        for ord_in_f in self.orders_in_flight:
            # going through to see if any of the parts of our order have finished
            if (
                not ord_in_f.c_done
                and self.current_time > ord_in_f.c_time + ord_in_f.time
            ):  # are the burgers cooked
                self.current_capacity += ord_in_f.c_time
                ord_in_f.c_done = True

            if (
                not ord_in_f.a_done
                and self.current_time
                > ord_in_f.a_time + ord_in_f.c_time + ord_in_f.time
            ):  # have the burgers been assembled
                self.current_capacity += ord_in_f.a_time
                ord_in_f.a_done = True

            if (
                not ord_in_f.p_done
                and self.current_time
                > ord_in_f.p_time + ord_in_f.a_time + ord_in_f.c_time + ord_in_f.time
            ):  # havea the burgers been packed
                self.current_capacity += ord_in_f.p_time
                ord_in_f.p_done = True

            if (
                not ord_in_f.p_done
                and self.current_time
                > ord_in_f.p_time
                + ord_in_f.a_time
                + ord_in_f.c_time
                + ord_in_f.time
                + ord_in_f.over_time
            ):  # have we also done the penalty time too
                self.current_capacity += ord_in_f.over_time
                ord_in_f.over_time = True
                self.orders_in_flight.pop(ord_in_f)

        self.num_orders = len(order.orders)
        time_order = self.time_cal(
            order
        )  # how long it takes to process the current order

        if time_order > self.cfg.max_time:
            return "REJECT", ""
        elif time_order > self.current_capacity:
            return "REJECT", ""
        # checking to see if we have run out of ingredients
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
            return "REJECT", ""
        else:
            # updating our current capacity and time_order
            self.current_capacity -= time_order
            self.total_time += time_order
            self.orders_in_flight.append(order)

            # combining all of our c_orders into one list so we can use a Counter
            orders_j = "".join(order.orders)
            num_ing_used = dict(Counter(orders_j))
            num_ing_used["P"] = 2 * self.num_orders  # number of patties left

            # subtracting dictionaries generates a new dictionary
            new_ing = {
                key: self.rest_metadata[key] - num_ing_used[key] for key in num_ing_used
            }

            # using update to overwrite our keys
            self.rest_metadata.update(new_ing)

            del new_ing

            return "ACCEPT", time_order

    def time_cal(self, order) -> datetime.timedelta:
        """
        Calculating the time it takes to produce the order. We use a penalty time if the restaurant goes over its
        capacity
        :return: time take for order in seconds
        """

        order.c_time = datetime.timedelta(
            0,
            min(self.num_orders, self.rest_metadata["Cooking_Cap"])
            * self.rest_metadata["Cooking_Time"]
            * 60,
        )
        order.a_time = datetime.timedelta(
            0,
            min(self.num_orders, self.rest_metadata["Assemble_Cap"])
            * self.rest_metadata["Assemble_Time"]
            * 60,
        )
        order.p_time = datetime.timedelta(
            0,
            min(self.num_orders, self.rest_metadata["Package_Cap"])
            * self.rest_metadata["Package_Time"]
            * 60,
        )

        order.over_time = datetime.timedelta(
            0,
            (self.num_orders - self.rest_metadata["Cooking_Cap"])
            * self.rest_metadata["Cooking_Time"]
            + (self.num_orders - self.rest_metadata["Assemble_Cap"])
            * self.rest_metadata["Assemble_Time"]
            + (self.num_orders - self.rest_metadata["Package_Cap"])
            * self.rest_metadata["Package_Time"]
            * 60,
        )

        return order.c_time + order.a_time + order.p_time + order.over_time

    def final_report(self) -> None:
        """
        Function which produces the report of the restaurant
        :return:
        """
        print("{0}, TOTAL, {1}".format(self.rest_metadata["ID"], self.total_time))
        print(
            "{0}, INVENTORY, {1}, {2}, {3}, {4}, {5}".format(
                self.rest_metadata["ID"],
                self.rest_metadata["P"],
                self.rest_metadata["L"],
                self.rest_metadata["T"],
                self.rest_metadata["V"],
                self.rest_metadata["B"],
            )
        )
