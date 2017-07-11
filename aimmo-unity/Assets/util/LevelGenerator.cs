using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LevelGenerator : MonoBehaviour 
{
	private const float tileSize = 1.0f;

	//Vector2 Snap(Vector3 position){}

	List<Vector2> ObstaclesMap()
	{
		List<Vector2> obstaclesMap = new List<Vector2>();

		// TODO: Get all the 3D geometry in the scene and build a 2D map. 

		Debug.Log(obstaclesMap);
		return obstaclesMap;
	}
}
