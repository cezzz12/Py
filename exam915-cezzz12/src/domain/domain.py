class Board:
    def __init__(self, size):
        self.size = size
        self.grid = [['.'] * size for _ in range(size)]
        self.AlienShip_count = 0
        self.Asteroid_count = 0


    def add_AlienShip(self,row,col):
        if self.grid[row][col]=="X" or self.grid[row][col]=="E":
            return False
        self.grid[row][col]="X"
        self.AlienShip_count=self.AlienShip_count+1
        return True

    def add_Asteroid(self,row,col):
        if self.grid[row][col]=="*" or self.grid[row][col]=="E" or self.grid[row][col]=="X":
            return False
        self.grid[row][col]="*"
        self.Asteroid_count+=1
        return True

    def add_Earth(self,row,col):
        self.grid[row][col]="E"

    def register_attack(self,row,col):
        if self.grid[row][col]=="X":
            self.grid[row][col]="-"
            return True
        elif self.grid[row][col]=="." or self.grid[row][col]=="*":
            self.grid[row][col]="-"
            return False


class Position:
    def __init__(self,col_letter,row_number):
        self.col= ord(col_letter.upper())-ord('A')
        self.row=int(row_number)

    @staticmethod
    def is_valid(position_str):
        if len(position_str)!=2:
            return False
        try:
            col=ord(position_str[0].upper())-ord('A')
            row=int(position_str[1])
            return 0<=col<=7 and 0<=row<=7
        except ValueError:
            return False





