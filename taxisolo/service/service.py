from domain.domain import Order,Driver
class TaxiService:
    def __init__(self,driver_repo,order_repo):
        self.driver_repo = driver_repo
        self.order_repo = order_repo

    def add_order(self,driver_id,distance,orders_file):
        driver=self.driver_repo.find_driver(driver_id)
        if not driver:
            raise ValueError(f"Driver with ID {driver_id} does not exist.")
        if distance < 1:
            raise ValueError("Distance must be at least 1 km.")

        order = Order(driver_id, distance)
        self.order_repo.add_order(order)
        self.order_repo.save_to_file(orders_file)

    def display_all(self):
        drivers = self.driver_repo.get_all_drivers()
        orders = self.order_repo.get_all_orders()

        driver_info = "\n".join(str(driver) for driver in drivers)
        order_info = "\n".join(str(order) for order in orders)

        return f"Drivers:\n{driver_info}\n\nOrders:\n{order_info}"

    def compute_income(self, driver_id):
        driver = self.driver_repo.find_driver(driver_id)
        if not driver:
            raise ValueError(f"Driver with ID {driver_id} does not exist.")

        orders = self.order_repo.get_all_orders()
        total_income = sum(order.distance * 2.5 for order in orders if order.driver_id == driver_id)

        return f"Driver {driver.name} (ID: {driver.id}) has an income of {total_income:.2f} RON."