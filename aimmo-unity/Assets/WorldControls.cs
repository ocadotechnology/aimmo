using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnitySocketIO;
using UnitySocketIO.Events;

public class WorldControls : MonoBehaviour 
{
	public SocketIOController io;

	// Use this for initialization
	void Start() 
	{
		io.On("connect", (SocketIOEvent e) => {
			Debug.Log("SocketIO Connected");
		});

		io.Connect();
	}
	
	// Update is called once per frame
	void Update() 
	{
		
	}
}
