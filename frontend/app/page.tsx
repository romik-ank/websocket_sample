"use client";

import { useState, useEffect, useRef } from "react";

export default function Home() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<string[]>([]);
  const [connected, setConnected] = useState(false);
  const socketRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    // Connect to WebSocket server using wss (secure WebSocket)
    socketRef.current = new WebSocket("wss://localhost:8000/ws");

    socketRef.current.onopen = () => {
      console.log("WebSocket connected");
      setConnected(true);
    };

    socketRef.current.onmessage = (event) => {
      setMessages((prev) => [...prev, event.data]);
    };

    socketRef.current.onclose = () => {
      console.log("WebSocket disconnected");
      setConnected(false);
    };

    return () => {
      socketRef.current?.close();
    };
  }, []);

  const sendMessage = () => {
    if (socketRef.current && message) {
      socketRef.current.send(message);
      setMessage("");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-between font-mono text-sm">
        <h1 className="text-4xl font-bold mb-8">
          FastAPI + Next.js WebSocket Demo
        </h1>

        <div className="mb-4">
          <div
            className={`inline-block w-4 h-4 mr-2 rounded-full ${
              connected ? "bg-green-500" : "bg-red-500"
            }`}
          ></div>
          <span>{connected ? "Connected" : "Disconnected"}</span>
        </div>

        <div className="flex mb-4">
          <input
            type="text"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-grow p-2 border border-gray-300 rounded-l"
            placeholder="Type a message..."
          />
          <button
            onClick={sendMessage}
            className="bg-blue-500 text-white p-2 rounded-r"
          >
            Send
          </button>
        </div>

        <div className="border border-gray-300 rounded p-4 h-80 overflow-y-auto">
          {messages.map((msg, index) => (
            <div key={index} className="mb-2 p-2 bg-gray-100 rounded">
              {msg}
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}
