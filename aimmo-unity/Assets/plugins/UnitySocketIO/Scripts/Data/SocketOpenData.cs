using UnityEngine;
using System.Collections;

namespace UnitySocketIO.Data {
    [System.Serializable]
    public class SocketOpenData {

        public string sid;
        public string[] upgrades;
        public int pingInterval;
        public int pingTimeout;

    }
}