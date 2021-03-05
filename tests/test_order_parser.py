import datetime
import unittest

from order import CSVOrderParser, Order


class OrderParser(unittest.TestCase):

    def test_csv_to_CSVOrderParser(self) -> None:
        input_str = "R1,2020-12-08 19:15:31,O1,BLT,LT,VLT"
        actual = CSVOrderParser().parse_order(input_str)
        expected = Order("O1", datetime.datetime.strptime("2020-12-08 19:15:31", "%Y-%m-%d %H:%M:%S"), "R1",
                         ["BLT", "LT", "VLT"])

        self.assertEqual(actual.r_id, expected.r_id)
        self.assertEqual(actual.o_id, expected.o_id)
        self.assertEqual(actual.time, expected.time)
        self.assertEqual(actual.orders, expected.orders)
