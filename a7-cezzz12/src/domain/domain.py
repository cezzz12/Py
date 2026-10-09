class Student:
    def __init__(self, id, name, group):
        self.id = id
        self.name = name
        self.group = group

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getGroup(self):
        return self.group

    def __str__(self):
        return str(self.id) + " " + self.name + " " + str(self.group)


if __name__ == '__main__':
    student = Student('1', '<NAME>', 1)
    print(student.__str__())
