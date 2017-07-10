#region License
/*
 * NativeSocketIO.cs
 *
 * The MIT License
 *
 * Copyright (c) 2014 Fabio Panettieri
 * Copyright (c) 2016 Peter Braith
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in
 * all copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
 * THE SOFTWARE.
 */
#endregion

using UnityEngine;
using System;
using System.Threading;
using System.Collections;
using System.Collections.Generic;
using WebSocketSharp;
using UnitySocketIO.IO;
using UnitySocketIO.Packet;
using UnitySocketIO.Events;
using UnitySocketIO.Data;

namespace UnitySocketIO.SocketIO {
    public class NativeSocketIO : BaseSocketIO {

        public WebSocket Socket { get { return socket; } }
        public bool IsConnected {
            get {
                if(socket == null)
                    return false;

                return socket.IsConnected;
            }
        }

        WebSocket socket = null;
        bool connected;

        Thread socketThread;
        Thread pingThread;

        Encoder encoder;
        Decoder decoder;
        Parser parser;

        int packetID;

        Dictionary<string, List<Action<SocketIOEvent>>> eventHandlers;

        object eventQueueLock;
        Queue<SocketIOEvent> eventQueue;

        object ackQueueLock;
        Queue<SocketPacket> ackQueue;
        List<Ack> ackList;

        bool isConnected;

        bool pinging;
        bool pong;


        public override void Init(SocketIOSettings settings) {
            base.Init(settings);

            encoder = new Encoder();
            decoder = new Decoder();
            parser = new Parser();

            packetID = 0;

            eventHandlers = new Dictionary<string, List<Action<SocketIOEvent>>>();

            eventQueueLock = new object();
            eventQueue = new Queue<SocketIOEvent>();

            ackQueueLock = new object();
            ackQueue = new Queue<SocketPacket>();
            ackList = new List<Ack>();

            socket = new WebSocket("ws://" + settings.url + (settings.port != 0 ? ":" + settings.port.ToString() : "") + "/socket.io/?EIO=3&transport=websocket");
            socket.OnOpen += OnSocketOpen;
            socket.OnMessage += OnSocketMessage;
            socket.OnError += OnSocketError;
            socket.OnClose += OnSocketClose;
        }

        void Update() {
            if(socket == null)
                return;

            lock(eventQueueLock) {
                while(eventQueue.Count > 0) {
                    EmitEvent(eventQueue.Dequeue());
                }
            }

            lock(ackQueueLock) {
                while(ackQueue.Count > 0) {
                    InvokeAck(ackQueue.Dequeue());
                }
            }

            if(isConnected != socket.IsConnected) {
                isConnected = socket.IsConnected;
                if(isConnected) {
                    EmitEvent("connect");
                } else {
                    EmitEvent("disconnect");
                }
            }

            if(ackList.Count == 0)
                return;

            if(DateTime.Now.Subtract(ackList[0].time).TotalSeconds < settings.timeToDropAck)
                return;

            ackList.RemoveAt(0);
        }

        public override void Connect() {
            connected = true;

            socketThread = new Thread(SocketThread);
            socketThread.Start(socket);

            pingThread = new Thread(PingThread);
            pingThread.Start(socket);
        }

        public override void Close() {
            EmitClose();
            connected = false;
        }



        public override void Emit(string e) {
            EmitMessage(-1, string.Format("[\"{0}\"]", e));
        }

        public override void Emit(string e, Action<string> action) {
            EmitMessage(++packetID, string.Format("[\"{0}\"]", e));
            ackList.Add(new Ack(packetID, action));
        }

        public override void Emit(string e, string data) {
            EmitMessage(-1, string.Format("[\"{0}\",{1}]", e, data));
        }

        public override void Emit(string e, string data, Action<string> action) {
            EmitMessage(++packetID, string.Format("[\"{0}\",{1}]", e, data));
            ackList.Add(new Ack(packetID, action));
        }

        public override void On(string e, Action<SocketIOEvent> callback) {
            if(!eventHandlers.ContainsKey(e)) {
                eventHandlers[e] = new List<Action<SocketIOEvent>>();
            }

            eventHandlers[e].Add(callback);
        }

        public override void Off(string e, Action<SocketIOEvent> callback) {
            if(!eventHandlers.ContainsKey(e))
                return;

            List<Action<SocketIOEvent>> _eventHandlers = eventHandlers[e];

            if(!_eventHandlers.Contains(callback))
                return;

            _eventHandlers.Remove(callback);

            if(_eventHandlers.Count == 0)
                eventHandlers.Remove(e);
        }
        
        void OnDestroy() {
            if(socketThread != null)
                socketThread.Abort();
        }

        void OnApplicationQuit() {
            if(socket == null)
                return;

            if(!socket.IsConnected)
                return;

            Close();
        }


        void OnSocketOpen(object sender, EventArgs e) {
            EmitEvent("open");
        }

        void OnSocketMessage(object sender, MessageEventArgs e) {
            SocketPacket packet = decoder.Decode(e);

            switch(packet.enginePacketType) {
                case EnginePacketType.OPEN:
                    HandleOpen(packet);
                    break;

                case EnginePacketType.CLOSE:
                    EmitEvent("close");
                    break;

                case EnginePacketType.MESSAGE:
                    HandleMessage(packet);
                    break;

                case EnginePacketType.PING:
                    HandlePing();
                    break;

                case EnginePacketType.PONG:
                    HandlePong();
                    break;

            }
        }

        void OnSocketError(object sender, ErrorEventArgs e) {
            Debug.Log(e.Message);
        }

        void OnSocketClose(object sender, CloseEventArgs e) {
            EmitEvent("close");
        }


        void SocketThread(object _obj) {
            WebSocket _socket = (WebSocket)_obj;

            while(connected) {
                if(_socket.IsConnected) {
                    Thread.Sleep(settings.reconnectTime);
                } else {
                    _socket.Connect();
                }
            }

            _socket.Close();
        }

        void PingThread(object _obj) { 
            WebSocket _socket = (WebSocket)_obj;

            DateTime pingStart;

            while(connected) {
                if(!_socket.IsConnected) {
                    Thread.Sleep(settings.reconnectTime);
                } else {
                    pinging = true;
                    pong = false;

                    EmitPacket(new SocketPacket(EnginePacketType.PING));
                    pingStart = DateTime.Now;

                    while(_socket.IsConnected && pinging && (DateTime.Now.Subtract(pingStart).TotalSeconds < settings.pingTimeout)) {
                        Thread.Sleep(100); // wait for ping timeout
                    }

                    if(!pong) {
                        _socket.Close();
                    }

                    Thread.Sleep(settings.pingInterval);
                }
            }
        }


        void HandleOpen(SocketPacket packet) {
            SocketID = JsonUtility.FromJson<SocketOpenData>(packet.json).sid;

            EmitEvent("open");
        }

        void HandleMessage(SocketPacket packet) {
            if(packet.json == "")
                return;

            if(packet.socketPacketType == SocketPacketType.ACK) {
                for(int i = 0; i < ackList.Count; i++) {
                    if(ackList[i].packetID != packet.id)
                        continue;

                    lock(ackQueueLock) {
                        ackQueue.Enqueue(packet);
                    }

                    return;
                }
            }

            if(packet.socketPacketType == SocketPacketType.EVENT) {
                SocketIOEvent e = parser.Parse(packet.json);

                lock(eventQueueLock) {
                    eventQueue.Enqueue(e);
                }
            }
        }

        void HandlePing() {
            EmitPacket(new SocketPacket(EnginePacketType.PONG));
        }

        void HandlePong() {
            pong = true;
            pinging = false;
        }

        void EmitEvent(string type) {
            EmitEvent(new SocketIOEvent(type));
        }

        void EmitEvent(SocketIOEvent e) {
            if(!eventHandlers.ContainsKey(e.name)) {
                return;
            }
            
            foreach(Action<SocketIOEvent> eventHandler in eventHandlers[e.name]) {
                eventHandler(e);
            }
        }

        void EmitMessage(int id, string json) {
            EmitPacket(new SocketPacket(EnginePacketType.MESSAGE, SocketPacketType.EVENT, 0, "/", id, json));
        }

        void EmitClose() {
            EmitPacket(new SocketPacket(EnginePacketType.MESSAGE, SocketPacketType.DISCONNECT, 0, "/", -1, JsonUtility.ToJson("")));
            EmitPacket(new SocketPacket(EnginePacketType.CLOSE));
        }

        void EmitPacket(SocketPacket packet) {
            socket.Send(encoder.Encode(packet));
        }

        void InvokeAck(SocketPacket packet) {
            Ack ack;

            for(int i = 0; i < ackList.Count; i++) {
                if(ackList[i].packetID != packet.id)
                    continue;

                ack = ackList[i];
                ackList.RemoveAt(i);
                ack.Invoke(parser.ParseData(packet.json));

                return;
            }
        }

    }
}