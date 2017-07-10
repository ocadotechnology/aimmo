using UnityEngine;
using System.Collections;

namespace UnitySocketIO.WebGL {
    [System.Serializable]
    public class AckJson {
        public int packetID;
        public string data;
    }
}