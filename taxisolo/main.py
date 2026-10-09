# main.py

from repository.repository import DriverRepository, OrderRepository
from service.service import TaxiService
from ui.ui import TaxiUI
import os

def create_files():
    if not os.path.exists("drivers.txt"):
        drivers_data = """\
1,Alex
2000,Ion
"""
        with open("drivers.txt", "w") as file:
            file.write(drivers_data)

    if not os.path.exists("orders.txt"):
        orders_data = """\
1,10
2000,8
1,5
1,6
2000,4
"""
        with open("orders.txt", "w") as file:
            file.write(orders_data)

def main():
    create_files()

    driver_repo = DriverRepository()
    order_repo = OrderRepository()

    driver_repo.load_from_file("drivers.txt")
    order_repo.load_from_file("orders.txt")

    service = TaxiService(driver_repo, order_repo)
    ui = TaxiUI(service)

    ui.run()

if __name__ == "__main__":
    main()
