# Map Generators

---

The generators are map creation services. The Django application is exposed 
to different map creation service classes. There is a map generation service
as part of the Django application which uses the default map generator: the
class Main in the map_generator file.

A map generator is a class that inherits from BaseGenerator and has to 
implement the `get_map` method. 

#### The Main Map Generator

The main map is supposed to be used for the generation of big worlds. This
should be the only generator used at this time. The `Level1` generator and
`BaseLevelGenerator` are legacy classes which eventually will be removed.
The whole map is randomly generated, but the generation is regulated by the 
[World Map](world-map.md) settings.

Obstacles are filled according to the obstacle ratio. Once an obstacle is 
added we ensure that each habitable cell can reach each other, thus the 
map will be connected and each generated avatar can reach others. 

#### Implementation details

The `get_map` method builds the map gradually adding random obstacles 
until the obstacle ratio is reached.(see [World Map](world-map.md) settings) 

To ensure that the map is connected, we check that all the adjacent 
habitable cells can reach all the other cells. To check that neighbours 
reach each other efficiently we use A* for path 
finding. 

#### Serialisation to JSON
We store our game information in `JSON` for the backend to be able to 
deserialize it. The below is a _**proposed**_ format which we are working
towards.

```Javascript
{
  "id": 1,
  // each level is set in one era only
  "era": "future"
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

