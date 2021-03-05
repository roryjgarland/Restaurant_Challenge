from abc import abstractmethod
import datetime


class OrderParser:
    """
    Abstract class which is used to parse the various order types
    """

    def __init__(self):
        pass

    @abstractmethod
    def parse_order(self, *args, **kwargs):
        pass


class CSVOrderParser(OrderParser):
    """
    Separation of concerns - just in case there are different methods
    """

    def __init__(self):
        super(CSVOrderParser, self).__init__()

    def parse_order(self, order: list):
        """
        Function which converts our specific input, list[str], into an order class
        :param order:
        :return:
        """
        # parse order R1,2020-12-08 19:15:31,O1,BLT,LT,VLT
        return Order(order[2], order[1], order[0], order[3:])


class Order:
    def __init__(self, o_id: str, time: str, r_id: str, orders: list):
        """

        :param o_id: this is the id of the order
        :param time: time of the order
        :param r_id: type(str) restaurant
        :param orders: type(list) all of the orders taken
        """

        self.o_id = o_id
        self.time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        self.r_id = r_id
        self.orders = orders

        # keeping track of our times to complete each aspect and if they have been completed
        self.c_time = 0
        self.c_done = False
        self.a_time = 0
        self.a_done = False
        self.p_time = 0
        self.p_done = False

        # this occurs when our cooking breaks our capacity i.e. if we have 5 burgers but only 4 capacity at cooking
        self.over_time = 0
        self.over_done = False
