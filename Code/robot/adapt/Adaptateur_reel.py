from .adapt import Adaptateur
from utils import getAngleFromVect, getDistanceFromPts

class AdaptateurReel(Adaptateur):
    """Adaptateur pour le robot réel, interagissant avec le hardware."""
    def __init__(self, robot):
        self.robot = robot
        self.last_position = (robot.x, robot.y)
        self.last_direction = robot.direction

    def initialise(self):
        self.last_position = (self.robot.x, self.robot.y)
        self.last_direction = self.robot.direction
