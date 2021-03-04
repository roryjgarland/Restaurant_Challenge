from abc import abstractmethod


class OrderParser:
    def __init__(self):
        pass

    @abstractmethod
    def parse_order(self, *args, **kwargs):
        pass


class CSVOrderParser(OrderParser):
    """
    Seperation of concerns - just in case there are differnt methods
    """

    def __init__(self):
        super(CSVOrderParser, self).__init__()

    def parse_order(self, order_str: str):
        # parse order R1,2020-12-08 19:15:31,O1,BLT,LT,VLT
        ord = order_str.split(",")
        return Order(ord[2], ord[1], ord[0], ord[3:])


class Order:
    def __init__(self, id, time, r_id, line_items):
        """

        :param id: this is
        :param time:
        :param r_id:
        :param orders:
        """
        # by convetion id is discriminator, and time is very important

        self.id = id
        self.time = time
        self.r_id = r_id
        self.line_items = line_items
