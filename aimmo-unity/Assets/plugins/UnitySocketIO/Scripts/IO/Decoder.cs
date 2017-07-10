#region License
/*
 * Decoder.cs
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
using System.Text;
using System.Collections;
using UnitySocketIO.Packet;
using WebSocketSharp;

namespace UnitySocketIO.IO {
    public class Decoder {
        
        public SocketPacket Decode(MessageEventArgs e) {
            string data = e.Data;

            SocketPacket packet = new SocketPacket();

            int offset = 0;

            int enginePacketType = int.Parse(data.Substring(offset, 1));
            packet.enginePacketType = (EnginePacketType)enginePacketType;

            if(enginePacketType == (int)EnginePacketType.MESSAGE) {
                int socketPacketType = int.Parse(data.Substring(++offset, 1));
                packet.socketPacketType = (SocketPacketType)socketPacketType;
            }

            if(data.Length <= 2)
                return packet;

            StringBuilder builder;

            if(data[offset + 1] == ',') {
                builder = new StringBuilder();

                while(offset < data.Length - 1 && data[++offset] != ',') {
                    builder.Append(data[offset]);
                }

                packet.nsp = builder.ToString();
            } else {
                packet.nsp = "/";
            }

            char next = data[offset + 1];

            if(next != ' ' && char.IsNumber(next)) {
                builder = new StringBuilder();

                while(offset < data.Length - 1) {
                    char c = data[++offset];

                    if(char.IsNumber(c)) {
                        builder.Append(c);
                    } else {
                        --offset;
                        break;
                    }
                }

                packet.id = int.Parse(builder.ToString());
            }

            if(++offset < data.Length - 1) {
                packet.json = data.Substring(offset);
            }

            return packet;
        }

    }
}