from domain.domain import RouteValidator, RouteException
from repository.repository  import RouteRepository


class RouteService:
    HOURLY_RATE = 50

    def __init__(self, filename):
        self.repository = RouteRepository(filename)
        self.filename = filename
        self.RouteValidator = RouteValidator()
        self.ServiceValidator = ServiceValidator()
        self.__income = 0

    def addRoute(self, new_route):
        try:
            self.RouteValidator.validate(new_route)
            self.ServiceValidator.validate(new_route, self.filename)
            self.repository.add(new_route)
        except RouteException as error:
            print(error)
        except ServiceException as error:
            print(error)

    def calculateTimeInMinutes(self, time):
        time_tokens = time.split(':')
        hours, minutes = time_tokens[0], time_tokens[1]
        return int(hours)*60 + int(minutes)


    def calculatePriceOfTicket(self, number):
        route = self.repository.findRouteByNumber(number)
        departure_time = self.calculateTimeInMinutes(route.departure_time)
        arrival_time = self.calculateTimeInMinutes(route.arrival_time)
        route_time = arrival_time - departure_time
        return route_time / 60 * self.HOURLY_RATE

    def ticketAccepted(self, number):
        price = self.calculatePriceOfTicket(number)
        self.__income += price
        route = self.repository.findRouteByNumber(number)
        route.setNumberOfAvailableTickets(route.number_of_available_tickets-1)
        route.setNumberOfTicketsSold(route.number_of_tickets_sold+1)
        self.repository.writeFile()

    @property
    def income(self):
        return self.__income

    def sortRoutes(self):
        routes = self.repository.getRoutes().copy()
        for i in range(len(self.repository.routes)):
            for j in range(i, len(self.repository.routes)):
                if routes[i].number_of_tickets_sold < routes[j].number_of_tickets_sold:
                    routes[i], routes[j] = routes[j], routes[i]
        return routes

class ServiceException(Exception):
    pass

class ServiceValidator:
    def validate(self, new_route, filename):
        for route in RouteService(filename).repository.getRoutes():
            if new_route.number == route.number:
                raise ServiceException('Route is duplicated')
