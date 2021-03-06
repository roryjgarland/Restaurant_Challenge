import datetime
from collections import Counter
from typing import List, Tuple, Union

import config
from order import Order, MonitorOrder


class Restaurant:
    """
    We approach this problem by using discrete time step i.e. when an order comes in, it sets our time in the restaurant
    to that and we calculate our capacity using this information. When the next order comes in, we move forward in time
    that much and calculate where our orders are.

    The restaurant class which takes in a config file and initial parameters to construct it. i.e.

    res = Restaurant(cfg, init_p)

    These will contain all the information on the restaurant, from ingredients used to the capacity of the store.
    Restaurant also keeps tracking the number of orders in flight, the current time (updated by a new order), and the
    total time taken.

    To pass an order to the Restaurant, we can do the following

    res.accept(order)

    accept then calls self.__check_capacity(order) which works as follows:

    1) Check that our order time is ahead of restaurant time, otherwise we reject the order
    2) Update our current capacity by seeing how much we have moved in time via self.__update_capacity()
    3) Using the updated times and capacity, check if we can handle the order
    4) If we can, update the ingredients, capacity etc

    Following the orders, we produce our final statistics via

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

        self.current_time = datetime.datetime.utcfromtimestamp(
            0
        )  # the time at the restaurant
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

        # first we check if our restaurant time is ahead of our order time, if so we cannot process orders in the past
        if self.current_time > order.time:
            return self.__reject_order()

        # if the order time is in the future, we update
        self.current_time = order.time

        # now that time has advanced, we update our work flow in the restaurant
        self.__update_capacity()

        # calculating the time for an order
        monitor_order = self.time_cal(order)

        # can we handle this order?
        # max current_capacity can be is 20
        if monitor_order.total_time > self.current_capacity:
            return self.__reject_order()
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
            return self.__reject_order()
        else:
            # updating our current capacity and time_order
            self.current_capacity -= monitor_order.total_time
            self.total_time += monitor_order.total_time
            self.orders_in_flight.append(monitor_order)

            # combining all of our c_orders into one list so we can use a Counter
            orders_j = "".join(order.orders)
            num_ing_used = dict(Counter(orders_j))
            num_ing_used["P"] = 2 * order.num_orders  # number of patties left

            # subtracting dictionaries generates a new dictionary
            new_ing = {
                key: self.rest_metadata[key] - num_ing_used[key] for key in num_ing_used
            }

            # using update to overwrite our keys
            self.rest_metadata.update(new_ing)

            del new_ing

            return "ACCEPT", monitor_order.total_time

    def __update_capacity(self) -> None:
        # first we need to check if our current orders being processed has been updated
        for ord_in_f in self.orders_in_flight:
            # going through to see if any of the parts of our order have finished
            if (
                not ord_in_f.c_done and self.current_time > ord_in_f.c_complete
            ):  # are the burgers cooked
                self.current_capacity += ord_in_f.c_time
                ord_in_f.c_done = True

            if (
                not ord_in_f.a_done and self.current_time > ord_in_f.a_complete
            ):  # have the burgers been assembled
                self.current_capacity += ord_in_f.a_time
                ord_in_f.a_done = True

            if (
                not ord_in_f.p_done and self.current_time > ord_in_f.p_complete
            ):  # have the burgers been packed
                self.current_capacity += ord_in_f.p_time
                ord_in_f.p_done = True

            if (
                not ord_in_f.p_done and self.current_time > ord_in_f.complete_time
            ):  # have we also done the penalty time too
                self.current_capacity += ord_in_f.over_time
                ord_in_f.over_time = True
                self.orders_in_flight.pop(ord_in_f)

    @staticmethod
    def __reject_order() -> Tuple[str, str]:
        return "REJECT", ""

    def time_cal(self, order) -> MonitorOrder:
        """
        Calculating the time it takes to produce the order. We use a penalty time if the restaurant goes over its
        capacity
        :return: time take for order in seconds
        """
        return MonitorOrder(order, self.rest_metadata)

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
