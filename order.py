import datetime
from abc import abstractmethod


class OrderParser:
    """
    Abstract class which is used to generate a child class for a given need i.e. reading in csv
    """

    def __init__(self):
        pass

    @abstractmethod
    def parse_order(self, *args, **kwargs):
        pass


class CSVOrderParser(OrderParser):
    """
    Child class of OrderParser which looks to deal with csv only
    """

    def __init__(self):
        super(CSVOrderParser, self).__init__()

    def parse_order(self, order_str: str):
        """
        Function which converts our specific input, list[str], into an order class
        :param order_str:
        :return:
        """
        # parse order R1,2020-12-08 19:15:31,O1,BLT,LT,VLT
        order = order_str.split(",")

        try:
            time = datetime.datetime.strptime(order[1], "%Y-%m-%d %H:%M:%S")
        except:
            return None

        return Order(order[2], time, order[0], order[3:])


class Order:
    """
    Our order class which produces an order object containing the necessary information for an order
    """

    def __init__(
        self, o_id: str, time: datetime.datetime, r_id: str, orders: list
    ) -> None:
        """

        :param o_id: type(str) this is the id of the order
        :param time: type(str) time of the order
        :param r_id: type(str) restaurant
        :param orders: type(list) all of the orders taken
        """

        self.o_id = o_id
        self.time = time
        self.r_id = r_id
        self.orders = orders
        self.num_orders = len(orders)


class MonitorOrder:
    """
    MonitorOrder is used by the restaurant to keep track of all the various times:

    c/a/p_time -> how much time to cook/assemble/package the food
    c/a/p_complete -> time this task will be done
    c/a/p_done -> bool value which registers if it is done

    over_time -> if the burgers are over capacity, this will add extra time onto the order

    """

    def __init__(self, order, meta_dic):
        self.time = order.time

        # keeping track of our times to complete each aspect and if they have been completed

        # Cooking Time

        self.c_time = datetime.timedelta(
            0,
            min(order.num_orders, meta_dic["Cooking_Cap"])
            * meta_dic["Cooking_Time"]
            * 60,
        )

        self.c_complete = self.time + self.c_time
        self.c_done = False

        self.a_time = datetime.timedelta(
            0,
            min(order.num_orders, meta_dic["Assemble_Cap"])
            * meta_dic["Assemble_Time"]
            * 60,
        )

        self.a_complete = self.a_time + self.c_complete

        self.a_done = False

        self.p_time = datetime.timedelta(
            0,
            min(order.num_orders, meta_dic["Package_Cap"])
            * meta_dic["Package_Time"]
            * 60,
        )
        self.p_complete = self.p_time + self.a_complete

        self.p_done = False

        # this occurs when our cooking breaks our capacity i.e. if we have 5 burgers but only 4 capacity at cooking
        self.over_time = datetime.timedelta(
            0,
            (order.num_orders - meta_dic["Cooking_Cap"]) * meta_dic["Cooking_Time"]
            + (order.num_orders - meta_dic["Assemble_Cap"]) * meta_dic["Assemble_Time"]
            + (order.num_orders - meta_dic["Package_Cap"])
            * meta_dic["Package_Time"]
            * 60,
        )
        self.over_done = False

        self.total_time = self.c_time + self.a_time + self.p_time + self.over_time

        self.complete_time = self.total_time + self.time
