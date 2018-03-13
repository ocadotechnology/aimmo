# Map Generators

---

The generators are map creation services. The Django application is exposed to different map creation service classes. There is a map generation service as part of the Django application which uses the default map generator: the class Main in the map_generator file.

A map generator is a class that inherits from BaseGenerator and has to implement the `get_map` method. 

#### The Main Map Generator

The main map is supposed to be used for the generation of big worlds. The whole map is randomly generated, but the generation is regulated by the [World Map](world-map) settings.

Obstacles are filled according to the obstacle ratio. Once an obstacle is added we ensure that each habitable cell can reach each other, thus the map will be connected and each generated avatar can reach others. 

#### Implementation details

The `get_map` method builds the map gradually adding random obstacles until the obstacle ratio is reached.(see [World Map](world-map) settings) 

To ensure that the map is connected, we check that all the adjacent habitable cells can reach all the other cells. This strategy is guaranteed to work. We know that all the habitable cells are connected. Adding an obstacle can either disconnect the component in two or keep a connected component. If the component is disconnected by the new added cell, then we have the guarantee that the neighbours of the new added cell will not reach each other. Thus, we have only to check if neighbors can reach each other.

To check that neighbors reach each other efficiently we use A* for path finding. The chosen [admissible heuristic](https://en.wikipedia.org/wiki/Admissible_heuristic) function is the Manhattan distance function. A detailed presentation of the algorithm and choosing heuristics can be found [here](http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html).

#### Levels JSON
We store our levels in `JSON` for the backend and `*.unity` scene files for the frontend. The below is a _**proposed**_ format that we think will cover all the situations we need for the level 1 milestone.

```Javascript
{
  "id": 1,
  // each level is set in one era only
  "era": "less_flat"
  "terrain": {
    "width": 10,
    "height": 10,
  }
  // we can figure out minX, minY, maxX, maxY and origin from these two corners.
  "south_west_corner": {
    "x": -2,
    "y": -2,
  },
  "north_east_corner": {
    "x": 2,
    "y": 2,
  },
  // the spawn location of the player
  "spawn_location": {
    "x": 0,
    "y": 1,
  },
  "obstacles": [
    {
      // the location here is the bottom left cell of the obstacle
      "location": {
        "x": 0,
        "y": 1,
      },
      "width": 2,
      "height": 1,
      "type": "van",
      "orientation": "east",
    }
  ],
  "pickups": [
    {
      "type": "damage",
      "value": 5,
      "location": {
        "x": 0,
        "y": 1,
      }
    }
  ]
}
```

