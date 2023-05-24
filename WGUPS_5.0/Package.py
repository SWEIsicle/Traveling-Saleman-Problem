# Create class for packages
# Gives packages attributes
# Has an update function to set the status of a package
# O(1)
class Package:
    def __init__(self, id, address, city, state, zipcode, deadline, weight, delivery_status):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.deadline = deadline
        self.weight = weight
        self.delivery_status = delivery_status
        self.departure_time = None
        self.delivery_time = None

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.id, self.address, self.city, self.state, self.zipcode,
                                                       self.deadline, self.weight, self.delivery_time,
                                                       self.delivery_status)

    # O(1)
    def update_status(self, convert_timedelta):
        if self.delivery_time < convert_timedelta:
            self.delivery_status = "Delivered"
        elif self.departure_time < convert_timedelta:
            self.delivery_status = "En route"
        else:
            self.delivery_status = "At Hub"
