import re


class TransformClass():

    def __init__(self, location, rooms, price, area):
        self.location = location
        self.rooms = rooms
        self.price = price
        self.area = area

    result_loc = []
    result_room = []
    result_pric = []
    result_area = []

    def transformLocations(self):
        for values in self.location:
            for value in values:
                cutted_value = re.search(': (.*),', value).group(1)
                self.result_loc.append(cutted_value)
        # return result_loc
        # print(result_loc)

    def transformRooms(self):
    # Calculations for rooms
    #     result_room = []
        for values in self.rooms:
            for value in values:
                res = value[0]
                self.result_room.append(int(res))
        # return result_room
        # print(result_room)

    # Calculation for price
    def transformPrices(self):
        # result_pric = []
        for values in self.price:
            for value in values:
                splited = value.split('z')[0]
                self.result_pric.append(int(splited))
        # return result_pric
        # print(result_pric)

    def transformArea(self):
        # Calculation for area
        # result_area = []
        for values in self.area:
            for value in values:
                splited_ar = value.split(' ')[0]
                splited_re = splited_ar.replace(',', '.')
                self.result_area.append(float(splited_re))
        # return result_area
        # print(result_area)

    def run(self):
        self.transformLocations()
        self.transformRooms()
        self.transformPrices()
        self.transformArea()

if __name__ == '__main__':
    transf = Transform()
    transf.run()
