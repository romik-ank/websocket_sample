from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import List

from utils.websocket_utils import websocket_manager

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
    try:
        # Accept the websocket connection
        await websocket_manager.connect(websocket)

        while True:
            # Receive a message from the client
            data = await websocket.receive_text()
            
            # Broadcast the message to all connected clients
            await websocket_manager.broadcast(data)

    except WebSocketDisconnect:
        # Handle WebSocket disconnection
        websocket_manager.disconnect(websocket)

    except Exception as e:
        print(f"WebSocket connection closed: {e}")


# Example route to broadcast a message from an HTTP endpoint
@app.post("/broadcast")
async def broadcast_message(message: dict):
    """
    Broadcast a message to all connected WebSocket clients.
    Expects a JSON payload with a 'message' key.
    """
    msg = message.get("message", "")
    if msg:
        await websocket_manager.broadcast(msg)
        return {"status": "Message broadcasted"}
    return {"status": "No message provided"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        ssl_certfile="cert.pem",  # Replace with the path to your SSL certificate
        ssl_keyfile="key.pem"    # Replace with the path to your SSL key
    )
