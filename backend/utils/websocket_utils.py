from fastapi import WebSocket
from typing import List

class WebSocketManager:
    #Single instance to ensure only one WebSocketManager exists globally
    _instance = None

    def __new__(cls):
        """
        Overrides the __new__ method to implement the singleton pattern.
        This ensures that only one instance of WebSocketManager is created.
        """
        if cls._instance is None: # Check id an instance already exists
            cls._instance = super(WebSocketManager, cls).__new__(cls) # Create a new instance
            # Initialize the list of active WebSocket connections
            cls._instance.active_connections: List[WebSocket] = []
        return cls._instance # Return the singleton instance
    
    async def connect(self, websocket: WebSocket):
        """
        Accept a new WebSocket connection and add it to the list of active connections.
        This method is called when a client establishes a WebSocket connection
        """
        await websocket.accept() # Accept the incoming WebSocket connection
        self.active_connections.append(websocket) # Add the connection to the list
        print(f"New connection added. Total connections: {len(self.active_connections)}") # Log the total connections

    async def disconnect(self, websocket: WebSocket):
        """
        Remove a WebSocket connection from the list of active connections.
        This method is called when a client disconnects.
        """
        self.active_connections.remove(websocket)
        print(f"Connection closed. Remaining connections: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        """
        Broadcast a message to all active WebSocket connections.
        This method iterates over all active connections and sends the message to each one.
        """
        for connection in self.active_connections: # Loop through all active WebSocket connections
            await connection.send_text(message)

        
# Create a global instance of WebSocketManager
# This instance can be imported and used anywhere in the application
websocket_manager = WebSocketManager()
