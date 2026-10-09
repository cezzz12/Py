class Flight:
    def __init__(self,id,departure_city,departure_time,arrival_city,arrival_time):
        self.__id = id
        self.__departure_city = departure_city
        self.__departure_time = departure_time
        self.__arrival_city = arrival_city
        self.__arrival_time = arrival_time

    @property
    def id(self):
        return self.__id
    @property
    def departure_city(self):
        return self.__departure_city
    @property
    def departure_time(self):
        return self.__departure_time
    @property
    def arrival_city(self):
        return self.__arrival_city
    @property
    def arrival_time(self):
        return self.__arrival_time

    def set_id(self,id):
        self.__id = id
    def set_departure_city(self,departure_city):
        self.__departure_city = departure_city
    def set_departure_time(self,departure_time):
        self.__departure_time = departure_time
    def set_arrival_city(self,arrival_city):
        self.__arrival_city = arrival_city
    def set_arrival_time(self,arrival_time):
        self.__arrival_time = arrival_time

    def __str__(self):
        return (str(self.id)+ "," + self.__departure_city + "," + self.__departure_time +
                "," + self.__arrival_city + "," + self.__arrival_time)


class FlightValidator:
    def validate(self,flight):
        if not isinstance(flight,Flight):
            raise TypeError("Flight must be an instance of Flight class")
        try:
            flight.set_id(int(flight.id))
        except ValueError:
            raise FlightException("Flight id must be an integer")

        if flight.departure_city == flight.arrival_city:
            raise FlightException("Flight not valid")
        if flight.departure_time>=flight.arrival_time:
            raise FlightException("Flight not valid")

        departure_minutes=self.calculateTimeinMinutes(flight.departure_time)
        arrival_minutes=self.calculateTimeinMinutes(flight.arrival_time)
        duration=arrival_minutes-departure_minutes
        if duration<15 or duration>90:
            raise FlightException("Flight not valid")

    def calculateTimeinMinutes(self, time):
        time_tokens = time.split(':')
        hour, minute = time_tokens[0], time_tokens[1]
        return int(hour) * 60 + int(minute)


class FlightException(Exception):
    pass