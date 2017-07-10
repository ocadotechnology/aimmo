using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;
using SimpleJSON;

public class WorkerManager : MonoBehaviour
{
	// Setup to ping the server every second.
	void Start()
	{
		Debug.Log("Starting the game...");

		BuildStaticScene();
		InvokeRepeating("UpdateMapState", 0.0f, 1.0f);
	}
		
	// Wrap request in a coroutine.
	void UpdateMapState()
	{
		Debug.Log("Updating map.");
		StartCoroutine(RequestMapState());
	}

	// Gets the updates of the map.
	IEnumerator RequestMapState()
	{
		UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:4000/update");
		yield return request.Send();

		var updates = JSON.Parse(request.downloadHandler.text);

		// Update the positions of the players.
		var playersList = updates["players"];

		for (int i = 0; i < playersList.Count; i++)
		{
			var player = playersList[i];

			string id = "player" + Convert.ToString(player["id"].AsInt);
			GameObject avatar = GameObject.Find(id);

			float x = (float) player["x"].AsInt;
			float y = (float) player["y"].AsInt;

			AvatarController controller = avatar.GetComponent<AvatarController>();
			Vector3 nextPosition = new Vector3(x, 0.5f, y);
			controller.SetNextPosition(nextPosition);

			Debug.Log("Moved " + id + " to position (" + x + ", " + y + ")");
		}

		// Generate new players if new players have been added.
		var newPlayers = updates["new_players"];

		for (int i = 0; i < newPlayers.Count; i++) 
		{
			var newPlayer = newPlayers[i];

			string id = "player" + Convert.ToString(newPlayer["id"].AsInt);
			float x = (float) newPlayer["x"].AsInt;
			float y = (float) newPlayer["y"].AsInt;

			CreatePlayer (id, x, y);
		}

		// Delete players.
		var deletedPlayers = updates["deleted_players"];

		for (int i = 0; i < deletedPlayers.Count; i++)
		{
			string id = "players" + Convert.ToString(deletedPlayers[i].AsInt);

			GameObject avatarToDelete = GameObject.Find(id);
			Destroy(avatarToDelete);
		}
	}

	// Wrap initialisation request in coroutine.
	public void BuildStaticScene()
	{
		Debug.Log("Initialising map...");
		StartCoroutine(GetFixedObjects());
	}

	// Request map dimensions and static objects, i.e. walls.
	IEnumerator GetFixedObjects()
	{
		UnityWebRequest request = UnityWebRequest.Get("http://127.0.0.1:4000/start");
		yield return request.Send();

		var map = JSON.Parse(request.downloadHandler.text);
		Debug.Log(map);

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

	// Create new player.
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
