class Board:
    def __init__(self,size):
        self.size = size
        self.grid=[['.']*size for _ in range(size)]
        self.ship_count=0

    def add_ship(self,row,col):
        if self.grid[row][col]=="+":
            return False
        self.grid[row][col]="+"
        self.ship_count+=1
        return True

    def remove_oldest_ship(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j]=="+":
                    self.grid[i][j]="."
                    self.ship_count-=1
                    return

    def register_attack(self,row,col):
        if self.grid[row][col]=="+":
            self.grid[row][col]="X"
            return True
        elif self.grid[row][col]==".":
            self.grid[row][col]="O"
            return False

    def gets_hit_count(self):
        return sum(row.count("X") for row in self.grid)

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
            return 0<=col<6 and 0<=row<6
        except ValueError:
            return False



