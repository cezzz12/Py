from domain.domain import Driver,Order

class DriverRepository:
    def __init__(self):
        self.drivers = []

    def load_from_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(",")  # Corrected this line
                driver = Driver(int(parts[0]), parts[1])
                self.drivers.append(driver)

    def find_driver(self, driver_id):
        for driver in self.drivers:
            if driver.id == driver_id:  # Fixed attribute access (should be 'id', not 'driver_id')
                return driver
        return None

    def get_all_drivers(self):
        return self.drivers

class OrderRepository:
    def __init__(self):
        self.orders = []

    def load_from_file(self, file_path):
        with open(file_path, "r") as file:
            for line in file:
                parts = line.strip().split(",")
                order = Order(int(parts[0]), float(parts[1]))
                self.orders.append(order)

    def save_to_file(self,file_path):
        with open(file_path,"w") as file:
            for order in self.orders:
                file.write(f"{order.order_id},{order.price}\n")

    def add_order(self,order):
        self.orders.append(order)

    def get_all_orders(self):
        return self.orders

