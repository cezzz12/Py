class Driver:
    def __init__(self, id, name):
        self.name = name
        self.id = id

    def __str__(self):
        return f"{self.id},{self.name}"

class Order:
    def __init__(self,driver_id,distance):
        self.distance = distance
        self.driver_id = driver_id

    def __str__(self):
        return f"{self.driver_id},{self.distance}"
