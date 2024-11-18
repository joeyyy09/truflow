# TruFlow🚀

A peer-to-peer file sharing and chat application built with Python and PyQt5. The application allows users to chat and share files directly with other peers on the network, providing a seamless experience for file transfers and real-time communication.

## Features ✨

- 🗣️ **Real-time chat** between peers
- 📁 **File sharing** capabilities
- 👥 **User status tracking** (online/offline)
- 📊 **Progress tracking** for file transfers
- 🎨 **Modern UI** built with PyQt5

## Architecture 🏗️

The application follows a **client-server architecture** for peer discovery, but uses **P2P** for actual file transfers:

```
Server
  ↙️   ↘️
Client ←→ Client
```

- **Server**: Handles peer discovery and connection brokering
- **Client**: Manages chat, file transfers, and UI
- **P2P**: Direct file transfers between peers

## Components 🧩

- `server/server.py`: Central server for peer discovery 🔍
- `client/client.py`: Core client functionality 🖥️
- `client/p2p.py`: P2P file transfer logic 📤📥
- `client/ui/`: UI components built with PyQt5 🎨
- `utils/`: Helper utilities and constants 🔧

## Setup and Running ⚙️

1. **Create and activate virtual environment**:
```sh
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. **Install dependencies**:
```sh 
pip install PyQt5
```

3. **Start the server**:
```sh
python server/server.py
```

4. **Start a client instance**:
```sh
python client/client.py
```

## How It Works 🔄

1. The **server** starts and listens for client connections 👂
2. **Clients** connect to the server to discover other peers 🔍
3. When a client wants to share a file:
   - Sender selects the file from the UI 📂
   - Receiver accepts the file transfer 📥
   - A direct **P2P connection** is established 🔗
   - **File is transferred** with progress tracking ⏳
4. **Chat messages** are sent directly between peers 💬

## UI Features 🖼️

- **File browser** with tree view 🌳
- **Active user list** with status indicators 💡
- **Chat window** with message history 💌
- **File transfer progress tracking** 📊
- **Modern and intuitive interface** 🎨

## Network Architecture 🌐

- Uses **TCP sockets** for reliable transfer 🔒
- Separate ports for **chat (5555)** and **file transfer (5556)** 💻
- **Direct P2P connections** for actual data transfer 🔗
- **Central server** only for peer discovery 🗺️

## Contributing 🤝

Feel free to submit issues and pull requests to help improve the application. Your contributions are welcome! 💻🌟
```

This version enhances the readability and engagement of your README with emojis that help visualize different sections and features. Let me know if you'd like any further modifications!
