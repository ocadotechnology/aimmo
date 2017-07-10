using UnityEngine;
using System.Collections;
using UnitySocketIO.Events;

namespace UnitySocketIO.IO {
    public class Parser {
        
        public SocketIOEvent Parse(string json) {
            string[] data = json.Split(new char[] { ',' }, 2);
            string e = data[0].Substring(2, data[0].Length - 3);

            if(data.Length == 1) {
                return new SocketIOEvent(e);
            }

            return new SocketIOEvent(e, data[1].TrimEnd(']'));
        }

        public string ParseData(string json) {
            return json.Substring(1, json.Length - 2);
        }

    }
}