using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class AvatarController : MonoBehaviour 
{
	private const float speed = 1.0f;

	private float startTime;
	private Vector3 currPosition;
	private Vector3 nextPosition;

	void Start()
	{
		startTime = Time.time;
		currPosition = transform.position;
		nextPosition = transform.position;
	}

	// Move the player to next position.
	void Update() 
	{
		if (nextPosition != currPosition) 
		{
			float step = (Time.time - startTime) * speed;
			transform.position = Vector3.Lerp(currPosition, nextPosition, step);
		}	
	}

	// Set next destination.
	public void SetNextPosition(Vector3 position)
	{
		currPosition = transform.position;
		nextPosition = position;
		startTime = Time.time;
	}
}
