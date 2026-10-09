from domain.domain import Route
from service.service import RouteService


class UserInterface:
    ADD_OPTION = 1
    SELL_OPTION = 2
    SHOW_INCOME_OPTION = 3
    REPORT_OPTION = 4


    def __init__(self, filename):
        self.filename = filename
        self.service = RouteService(filename)

    def __printMenu(self):
        print("0. Exit")
        print("1. Add a train route")
        print("2. Sell a ticket")
        print("3. Show the total income")
        print("4. Show report")

    
    def runUi(self):
        while True:
            self.__printMenu()
            option = int(input("Enter your choice: "))
            if option == 0:
                break
            if option == self.ADD_OPTION:
                number = input("Enter your number: ")
                departure_city = input("Enter your departure city: ")
                departure_time = input("Enter your departure time: ")
                arrival_city = input("Enter your arrival city: ")
                arrival_time = input("Enter your arrival time: ")
                number_of_available_tickets = input("Enter your number of available tickets: ")
                new_route = Route(number, departure_city, departure_time, arrival_city, arrival_time, number_of_available_tickets)
                self.service.addRoute(new_route)

            elif option == self.SELL_OPTION:
                number = int(input("Enter your number: "))
                print(self.service.calculatePriceOfTicket(number))
                accept_option = input("Do you want to accept the ticket? (yes/no): ")
                if accept_option == "yes":
                    self.service.ticketAccepted(number)

            elif option == self.SHOW_INCOME_OPTION:
                print(self.service.income)

            elif option == self.REPORT_OPTION:
                sorted_routes = self.service.sortRoutes()
                for route in sorted_routes:
                    print(route, "Tickets Sold: ", route.number_of_tickets_sold)