using UnityEngine;
using System.Collections;

namespace UnitySocketIO.WebGL {
    [System.Serializable]
    public class EventJson {
        public string socketEvent;
        public string eventData;
    }
}