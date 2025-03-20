from django.test import TestCase


class Robot:
    def __init__(self, name, velocity):
        self.name = name
        self.velocity = velocity
    
    def robot_data(self):
        data_list = [self.name, self.velocity]
        
        return data_list 

    def run(self, time):
        distance = self.velocity / time
        
        return distance


robot_1 = Robot('Alfa Centauri', 60)
print(robot_1.robot_data()) 

distance_1 = robot_1
