from dataclasses import dataclass
from random import randint

from simulation.cell import Cell
from simulation.worksheet import WORKSHEET, WorksheetData


@dataclass
class Obstacle:
    """A dataclass representing an obstacle in the simulation."""

    texture_choice: int
    orientation = "north"
    width: int = 1
    height: int = 1

    def serialize(self, cell: Cell):
        return {"location": cell.location.serialize(), "texture": self.texture_choice}

    def make_obstacle(worksheet: WorksheetData = WORKSHEET) -> "Obstacle":
        """
        Returns an obstacle with a randomly generated texture choice based on number of different
        obstacle textures indicated in the worksheet.

        Args:
            worksheet (WorksheetData, optional): The worksheet to use to generate the obstacle. Defaults to WORKSHEET.
        """
        texture_choice = randint(1, worksheet.number_of_obstacle_textures)
        return Obstacle(texture_choice)
