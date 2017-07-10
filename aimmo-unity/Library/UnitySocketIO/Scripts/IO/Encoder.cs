#region License
/*
 * Encoder.cs
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

namespace UnitySocketIO.IO {
    public class Encoder {
        
        public string Encode(SocketPacket packet) {
            StringBuilder builder = new StringBuilder();

            builder.Append((int)packet.enginePacketType);

            if(packet.enginePacketType != EnginePacketType.MESSAGE) {
                return builder.ToString();
            }

            builder.Append((int)packet.socketPacketType);

            if(packet.socketPacketType == SocketPacketType.BINARY_EVENT || packet.socketPacketType == SocketPacketType.BINARY_ACK) {
                builder.Append(packet.attachments);
                builder.Append("-");
            }

            if(!string.IsNullOrEmpty(packet.nsp) && packet.nsp != "/") {
                builder.Append(packet.nsp);
                builder.Append(",");
            }

            if(packet.id > -1) {
                builder.Append(packet.id);
            }

            if(packet.json != "") {
                builder.Append(packet.json);
            }

            return builder.ToString();
        }

    }
}