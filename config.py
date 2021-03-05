import datetime

"""
Simple config file which can be updated as necessary - keeps all hard coded values outside of our class and allows
for easy to edit
"""

data_loc = "/home/roryjgarland/Documents/Projects/Satis.AI_coding/data/"

ing = {
    "B": "Bacon",
    "L": "Lettuce",
    "T": "Tomatoes",
    "V": "Veggie Burger",
}

max_time = datetime.timedelta(0, 20 * 60)

dkeys = [
    "ID",
    "Cooking_Cap",
    "Cooking_Time",
    "Assemble_Cap",
    "Assemble_Time",
    "Package",
    "Package_Time",
    "P",
    "L",
    "T",
    "V",
    "B",
]
