using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnitySocketIO;
using UnitySocketIO.Events;
using SimpleJSON;

public class WorldControls : MonoBehaviour 
{
	public SocketIOController io;

	// Use this for initialization
	void Start() 
	{
		io.On("connect", (SocketIOEvent e) => {
			Debug.Log("SocketIO Connected.");
		});
			
		io.Connect();

		io.On("world-init", (SocketIOEvent e) => {
			Debug.Log("Initalising world...");
			WorldInit(e.data);
		});

		io.On("world-update", (SocketIOEvent e) => {
			Debug.Log("Update!");
			WorldUpdate(e.data);
		});

	}

	void WorldInit(string rawMap)
	{
		var map = JSON.Parse(rawMap);

		// Create plane (floor).
		float minX = (float) map["minX"].AsInt;
		float minY = (float) map["minY"].AsInt;
		float maxX = (float) map["maxX"].AsInt;
		float maxY = (float) map["maxY"].AsInt;

		GameObject floor = GameObject.CreatePrimitive(PrimitiveType.Plane);
		floor.transform.position = new Vector3(minX + maxX, 0.0f, minY + maxY);
		floor.transform.localScale = new Vector3((maxX - minX) / 10.0f, 1.0f, (maxY - minY) / 10.0f);
		floor.GetComponent<Renderer>().material.color = Color.gray;

		// Create cubes (walls).
		var objectList = map["objects"];

		for (int i = 0; i < objectList.Count; i++)
		{
			var obj = objectList[i];

			string id = "object" + Convert.ToString(obj["id"].AsInt);

			float x = (float) obj["x"].AsInt;
			float y = (float) obj["y"].AsInt;

			// Create new game object.
			GameObject wall = GameObject.CreatePrimitive(PrimitiveType.Cube);
			wall.transform.position = new Vector3(x, 0.5f, y);
			wall.name = id;
			wall.GetComponent<Renderer>().material.color = Color.black;

			Debug.Log(id + " is at position (" + x + ", " + y + ")");
		}

		// Create spheres (avatars)
		var playersList = map["players"];

		for (int i = 0; i < playersList.Count; i++) 
		{
			var player = playersList[i];

			string id = "player" + Convert.ToString(player["id"].AsInt);

			float x = (float) player["x"].AsInt;
			float y = (float) player["y"].AsInt;

			// Create new game object.
			CreatePlayer(id, x, y);
		}
	}

	void WorldUpdate(string rawPlayersList) 
	{
		Debug.Log("Raw players list: " + rawPlayersList);

		var playersList = JSON.Parse(rawPlayersList)["players"];

		for (int i = 0; i < playersList.Count; i++)
		{
			var player = playersList[Convert.ToString(i + 1)];

			string id = "player" + Convert.ToString(player["id"].AsInt);
			GameObject avatar = GameObject.Find(id);

			float x = (float) player["x"].AsInt;
			float y = (float) player["y"].AsInt;

			// TEMPORARY!
			if (avatar == null) 
			{
				CreatePlayer(id, x, y);
			}
			avatar = GameObject.Find(id);
				
			AvatarController controller = avatar.GetComponent<AvatarController>();
			Vector3 nextPosition = new Vector3(x, 0.5f, y);
			controller.SetNextPosition(nextPosition);
		
			Debug.Log("Moved " + id + " to position (" + x + ", " + y + ")");
		}
	}

	// Helper method
	void CreatePlayer(string id, float x, float y)
	{
		// Generate 3D shape.
		GameObject avatar = GameObject.CreatePrimitive(PrimitiveType.Sphere);

		avatar.transform.position = new Vector3(x, 0.5f, y);
		avatar.name = id;
		avatar.AddComponent<AvatarController>();

		// Assign random colour.
		avatar.GetComponent<Renderer>().material.color = UnityEngine.Random.ColorHSV();

		Debug.Log("Created " + id + " at position (" + x + ", " + y + ")");
	}
}
