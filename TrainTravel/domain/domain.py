class Route:
    def __init__(self, number, departure_city, departure_time, arrival_city, arrival_time,  number_of_available_tickets):
        self.__number = number
        self.__departure_city = departure_city
        self.__departure_time = departure_time
        self.__arrival_time = arrival_time
        self.__arrival_city = arrival_city
        self.__number_of_available_tickets = number_of_available_tickets
        self.__number_of_tickets_sold = 0

    @property
    def number(self):
        return self.__number

    @property
    def departure_city(self):
        return self.__departure_city

    @property
    def departure_time(self):
        return self.__departure_time

    @property
    def arrival_time(self):
        return self.__arrival_time

    @property
    def arrival_city(self):
        return self.__arrival_city

    @property
    def number_of_available_tickets(self):
        return self.__number_of_available_tickets

    @property
    def number_of_tickets_sold(self):
        return self.__number_of_tickets_sold

    def setNumber(self, number):
        self.__number = number

    def setDepartureCity(self, departure_city):
        self.__departure_city = departure_city

    def setDepartureTime(self, departure_time):
        self.__departure_time = departure_time

    def setArrivalCity(self, arrival_city):
        self.__arrival_city = arrival_city

    def setArrivalTime(self, arrival_time):
        self.__arrival_time = arrival_time

    def setNumberOfAvailableTickets(self, number_of_available_tickets):
        self.__number_of_available_tickets = number_of_available_tickets

    def setNumberOfTicketsSold(self, number_of_tickets_sold):
        self.__number_of_tickets_sold = number_of_tickets_sold


    def __str__(self):
        return (str(self.number) + "," + self.departure_city + "," + self.__departure_time + "," +
                self.__arrival_city + "," + self.__arrival_time +"," + str(self.__number_of_available_tickets))

class RouteValidator:
    def validate(self, route):
        """

        :param route:
        :return:
        """
        if isinstance(route, Route) == False:
            raise RouteException("Route must be an instance of Route")
        try:
            route.setNumber(int(route.number))
        except ValueError:
            raise RouteException("Route number must be an integer")

        try:
            route.setNumberOfAvailableTickets(int(route.number_of_available_tickets))
            if route.number_of_available_tickets <0:
                raise RouteException("Number of available tickets must be positive")
        except ValueError:
            raise RouteException("Route number of available tickets must be an integer")

        if route.departure_city == route.arrival_city:
            raise RouteException("Route departure city must not be equal to arrival city")

        if route.departure_time >= route.arrival_time:
            raise RouteException("Route departure time must be less than arrival time")




class RouteException(Exception):
    pass