from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Maintain a list of active WebSocket connections
active_connections: List[WebSocket] = []

@app.get("/")
async def get():
    return {"message": "WebSocket server is running"}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the websocket connection
    await websocket.accept()
    try:
        # Add the new connection to the list
        active_connections.append(websocket)
        print(f"New Connection added. Total Connections: {len(active_connections)}")

        while True:
            # Receive a message from the client
            data = await websocket.receive_text()
            
            # Broadcast the message to all connected clients
            for i, connection in enumerate(active_connections):
                await connection.send_text(f"{data} to {i+1}")

    except WebSocketDisconnect:
        # Remove the disconnected client from the list
        active_connections.remove(websocket)
        print(f"Connection closed. Remaining connections: {len(active_connections)}")

    except Exception as e:
        print(f"WebSocket connection closed: {e}")
