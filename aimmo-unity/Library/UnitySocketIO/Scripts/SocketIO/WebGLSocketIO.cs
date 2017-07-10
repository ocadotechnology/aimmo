using UnityEngine;
using System.Collections;
using System.Collections.Generic;
using System;
using UnitySocketIO.IO;
using UnitySocketIO.Events;
using UnitySocketIO.Packet;
using UnitySocketIO.WebGL;

namespace UnitySocketIO.SocketIO {
    public class WebGLSocketIO : BaseSocketIO {

        int packetID;

        //Parser parser;

        Dictionary<string, List<Action<SocketIOEvent>>> eventHandlers;

        object ackQueueLock;
        Queue<SocketPacket> ackQueue;
        List<Ack> ackList;

        bool isReady;

        public override void Init(SocketIOSettings settings) {
            base.Init(settings);

            //parser = new Parser();

            eventHandlers = new Dictionary<string, List<Action<SocketIOEvent>>>();

            ackList = new List<Ack>();

            AddSocketIO();
            AddEventListeners();
        }

        public void SetSocketID(string socketID) {
            SocketID = socketID;
        }

        void AddSocketIO() {
            Application.ExternalEval(@"
                var socketIOScript = document.createElement('script');
                socketIOScript.setAttribute('src', 'http" + (settings.sslEnabled ? "s" : "") + @"://" + settings.url + (!settings.sslEnabled && settings.port != 0 ? ":" + settings.port.ToString() : "") +  @"/socket.io/socket.io.js');
                document.head.appendChild(socketIOScript);
            ");
        }

        void AddEventListeners() {
            Application.ExternalEval(@"
                window.socketEvents = {};

                window.socketEventListener = function(event, data){
                    var socketData = {
                        socketEvent: event,
                        eventData: typeof data === 'undefined' ? '' : JSON.stringify(data)
                    };

                    SendMessage('" + gameObject.name + @"', 'InvokeEventCallback', JSON.stringify(socketData));
                };
            ");
        }

        public override void Connect() {
            Application.ExternalEval(@"
                window.socketIO = io.connect('http" + (settings.sslEnabled ? "s" : "") + @"://" + settings.url + (!settings.sslEnabled && settings.port != 0 ? ":" + settings.port.ToString() : "") + @"/');
                
                window.socketIO.on('connect', function(){
                    SendMessage('" + gameObject.name + @"', 'SetSocketID', window.socketIO.io.engine.id);
                });

                for(var socketEvent in window.socketEvents){
                    window.socketIO.on(socketEvent, window.socketEvents[socketEvent]);
                }
            ");
        }

        public override void Close() {
            Application.ExternalEval(@"
                if(typeof window.socketIO !== 'undefined')
                    window.socketIO.disconnect();
            ");
        }


        public override void Emit(string e) {
            Application.ExternalEval(@"
                if(typeof window.socketIO !== 'undefined')
                    window.socketIO.emit('" + e + @"');
            ");
        }

        public override void Emit(string e, string data) {
            Application.ExternalEval(@"
                if(typeof window.socketIO !== 'undefined')
                    window.socketIO.emit('" + e + @"', " + data + @");
            ");
        }

        public override void Emit(string e, Action<string> action) {
            packetID++;

            Application.ExternalEval(@"
                if(typeof window.socketIO !== 'undefined'){
                    window.socketIO.emit('" + e + @"', function(data){
                        var ackData = {
                            packetID: " + packetID.ToString() + @",
                            data: typeof data === 'undefined' ? '' : JSON.stringify(data)
                        };

                        SendMessage('" + gameObject.name + @"', 'InvokeAck', JSON.stringify(ackData));
                    });
                }
            ");

            ackList.Add(new Ack(packetID, action));
        }

        public override void Emit(string e, string data, Action<string> action) {
            packetID++;

            Application.ExternalEval(@"
                if(typeof window.socketIO !== 'undefined'){
                    window.socketIO.emit('" + e + @"', " + data + @", function(data){
                        var ackData = {
                            packetID: " + packetID.ToString() + @",
                            data: typeof data === 'undefined' ? '' : JSON.stringify(data)
                        };

                        SendMessage('" + gameObject.name + @"', 'InvokeAck', JSON.stringify(ackData));
                    });
                }
            ");

            ackList.Add(new Ack(packetID, action));
        }





        public override void On(string e, Action<SocketIOEvent> callback) {
            if(!eventHandlers.ContainsKey(e)) {
                eventHandlers[e] = new List<Action<SocketIOEvent>>();
            }

            eventHandlers[e].Add(callback);

            Application.ExternalEval(@"
                if(typeof window.socketEvents['" + e + @"'] === 'undefined'){
                    window.socketEvents['" + e + @"'] = function(data){
                        window.socketEventListener('" + e + @"', data);
                    };

                    if(typeof window.socketIO !== 'undefined'){
                        window.socketIO.on('" + e + @"', function(data){
                            window.socketEventListener('" + e + @"', data);
                        });
                    }
                }
            ");    
        }

        public override void Off(string e, Action<SocketIOEvent> callback) {
            if(!eventHandlers.ContainsKey(e))
                return;

            List<Action<SocketIOEvent>> _eventHandlers = eventHandlers[e];

            if(!_eventHandlers.Contains(callback))
                return;

            _eventHandlers.Remove(callback);

            if(_eventHandlers.Count == 0) {
                eventHandlers.Remove(e);
            }
        }



        public void InvokeAck(string ackJson) {
            Ack ack;
            AckJson ackData = JsonUtility.FromJson<AckJson>(ackJson);
            
            for(int i = 0; i < ackList.Count; i++) {
                if(ackList[i].packetID == ackData.packetID) {
                    ack = ackList[i];
                    ackList.RemoveAt(i);
                    ack.Invoke(ackData.data);
                    return;
                }
            }
        }



        public void InvokeEventCallback(string eventJson) {
            EventJson eventData = JsonUtility.FromJson<EventJson>(eventJson);

            if(!eventHandlers.ContainsKey(eventData.socketEvent))
                return;
            
            for(int i = 0; i < eventHandlers[eventData.socketEvent].Count; i++) {
                SocketIOEvent socketEvent = new SocketIOEvent(eventData.socketEvent, eventData.eventData);
                eventHandlers[eventData.socketEvent][i](socketEvent);
            }
        }
        
    }
}