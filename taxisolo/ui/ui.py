# ui/ui.py

class TaxiUI:
    def __init__(self, service):
        self.service = service

    def add_order(self):
        try:
            driver_id = int(input("Enter driver ID: "))
            distance = float(input("Enter distance (km): "))
            self.service.add_order(driver_id, distance, "orders.txt")
            print("Order added successfully.")
        except ValueError as e:
            print(f"Error: {e}")

    def display_all(self):
        print(self.service.display_all())

    def compute_income(self):
        try:
            driver_id = int(input("Enter driver ID: "))
            print(self.service.compute_income(driver_id))
        except ValueError as e:
            print(f"Error: {e}")

    def run(self):
        while True:
            print("\n1. Add Order")
            print("2. Display All")
            print("3. Compute Income")
            print("4. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.add_order()
            elif choice == "2":
                self.display_all()
            elif choice == "3":
                self.compute_income()
            elif choice == "4":
                break
            else:
                print("Invalid choice. Please try again.")
