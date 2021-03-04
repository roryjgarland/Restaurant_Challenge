import config
from order import Order


class Restaurant:
    def __init__(self, cfg, id) -> None:
        self.cfg = cfg
        self.id = id

        self.rest_metadata = {k: None for k in self.cfg.dkeys}

    def handle_order(self, ord: Order):
        """
        :param ord: Always an Order object to allow encapsulation
        :return:
        """

        pass


if __name__ == "__main__":
    # create dictionary which maps restraunt to instance
    hello_dic = {"R1": Restaurant, "R2": Restaurant}
