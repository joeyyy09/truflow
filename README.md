# Truflow
**TruFlow** is a high-performance hybrid peer-to-peer (P2P) file-sharing and communication platform built in Python with a PyQt5 interface. It uses a custom binary application-layer protocol over TCP, featuring a 1-byte opcode and a 15-byte length field, allowing efficient multiplexing of real-time chat, file discovery, and heartbeat traffic over a single persistent connection.

The architecture cleanly separates the centralized control plane—responsible for fast peer discovery and fuzzy search—from the decentralized data plane, which handles direct P2P file transfers. With TCP_NODELAY and IPTOS socket optimizations and a non-blocking QThread-driven I/O model, TruFlow maintains highly concurrent, low-latency performance across all network operations.

---

## Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Detailed Feature Documentation](#detailed-feature-documentation)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Technical Details](#technical-details)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## Features

<img width="737" height="618" alt="image" src="https://github.com/user-attachments/assets/16c4eba9-e5a4-4225-8c53-ec253049557c" />

### Core Features

1. **User Registration & Authentication**

   - Unique username-based registration
   - Server-side user management
   - Automatic IP address mapping

2. **File Sharing**

   - Share entire folders and individual files
   - Automatic directory structure scanning
   - Real-time share data synchronization with server
   - File metadata tracking (size, hash)

3. **File Browsing**

   - Browse shared files of any user on the network
   - Tree-view display of directory structures
   - File information dialog with detailed metadata

4. **Global File Search**

   - Search files across all users' shared content
   - Fuzzy search with typo tolerance
   - Real-time search results
   - Search by filename matching

5. **Direct File Transfer**

   - Peer-to-peer file transfers (no server relay)
   - Resume interrupted downloads
   - Progress tracking with visual progress bars
   - Pause and resume download functionality
   - Automatic file hash verification

6. **Chat Messaging**

   - Real-time messaging between users
   - Message history per user
   - Desktop notifications for incoming messages
   - HTML-formatted message display

7. **Online Status Tracking**

   - Real-time online/offline status indicators
   - Heartbeat mechanism for status updates
   - Automatic user status refresh

8. **Download Management**

   - Multiple simultaneous downloads
   - Download queue management
   - Progress tracking for individual files
   - Download history and status tracking

9. **Settings & Configuration**
    - Customizable share folder path
    - Customizable downloads folder path
    - Server IP configuration
    - Desktop notification preferences
    - Persistent settings storage

---

## Architecture

### Client-Server Model

Truflow uses a hybrid architecture:

- **Central Server**: Facilitates peer discovery, user registration, file metadata storage, and search functionality
- **Peer-to-Peer**: Actual file transfers occur directly between clients without server relay

### Components

1. **Server (`src/server/`)**

   - Handles user registration and authentication
   - Maintains user-to-IP mappings
   - Stores shared file metadata in TinyDB
   - Provides file search and browse services
   - Manages user online status

2. **Client (`src/client/`)**

   - PyQt5-based graphical user interface
   - Handles all user interactions
   - Manages file transfers (send/receive)
   - Implements chat functionality
   - Manages local file sharing

3. **Utilities (`src/utils/`)**
   - Shared constants and configuration
   - Socket communication functions
   - Helper functions for file operations
   - Type definitions and data structures
   - Exception handling

### Communication Protocol

The application uses a custom binary protocol over TCP sockets:

- **Header-based Protocol**: Each message has a 1-byte header code and 15-byte length field
- **Header Codes**: Different message types for various operations (file transfer, chat, search, etc.)

---

## Installation

### Prerequisites

- Python 3.10 or higher
- pip or pipenv for dependency management

### Server Dependencies

The server requires the following Python packages:

- `msgpack` (1.0.3) - Binary serialization
- `tinydb` (4.7.0) - Lightweight database for storing share metadata
- `fuzzysearch` (0.7.3) - Fuzzy string matching for search
- `attrs` (21.4.0) - Python classes without boilerplate

### Client Dependencies

The client requires the following Python packages:

- `PyQt5` (5.14.1) - GUI framework
- `PyQt5-sip` (12.9.1) - PyQt5 SIP bindings
- `msgpack` (1.0.3) - Binary serialization
- `notify-py` (0.3.3) - Desktop notifications
- `jeepney` (0.7.1) - D-Bus library for notifications
- `loguru` (0.5.3) - Advanced logging

### Installation Steps

1. **Clone the repository**:

   ```bash
   git clone https://github.com/joeyyy09/truflow.git
   cd Truflow
   ```

2. **Install server dependencies**:

   ```bash
   cd src/server
   pip install msgpack tinydb fuzzysearch attrs
   # Or using pipenv:
   pipenv install
   ```

3. **Install client dependencies**:
   ```bash
   cd src/client
   pip install PyQt5 msgpack notify-py jeepney loguru
   # Or using pipenv:
   pipenv install
   ```

---

## Getting Started

### Starting the Server

1. Navigate to the server directory:

   ```bash
   cd src/server
   ```

2. Run the server:

   ```bash
   python server.py
   ```

   The server will:

   - Display its IP address
   - Create necessary directories in `~/.Truflow/`
   - Start listening on port `1234` (configurable via `SERVER_RECV_PORT`)

### Starting the Client

1. Navigate to the client directory:

   ```bash
   cd src/client
   ```

2. Run the client:

   ```bash
   python app.py
   ```

3. **First-time setup**:
   - Enter your desired username
   - Enter the server IP address
   - Select or create a share folder path
   - Click "Continue" to proceed

### Application Directories

Upon first run, Truflow creates the following directory structure in your home directory:

```
~/.Truflow/
├── logs/          # Application logs
├── db/            # Database files and settings
│   ├── db.json    # Server share metadata database
│   └── settings.json  # User settings
├── share/         # Default share folder (if not customized)
├── compressed/    # Compressed file cache
├── tmp/           # Temporary incomplete downloads
└── direct/        # Temporary direct transfer downloads
```

---

## Detailed Feature Documentation

### 1. User Registration & Authentication

**How it works:**

- Users register with a unique username on first connection
- The server maps usernames to IP addresses
- Registration is required before any other operations
- Username uniqueness is enforced server-side

**Implementation:**

- Client sends `NEW_CONNECTION` header with username
- Server validates and stores username-IP mapping
- Server acknowledges successful registration

### 2. File Sharing

**How it works:**

- Users select a folder to share (default: `~/.Truflow/share`)
- The application recursively scans the folder structure
- Directory structure is converted to a dictionary representation
- Metadata (size, type, path) is collected for each file
- Share data is sent to the server and stored in the database

**File Metadata:**

- File path (relative to share folder)
- File size (in bytes)
- File hash (SHA-1, calculated on-demand)
- File type (file or directory)

**Sharing Options:**

- **Import Files**: Add files to share folder via file dialog
- **Import Folders**: Add entire folders to share folder
- **Share File**: Share a specific file from share folder

### 3. File Browsing

**How it works:**

- Select a user from the online users list
- Click "Browse" button to view their shared files
- Server returns the user's complete directory structure
- Files are displayed in a tree view widget
- Users can select files/folders for download

**Tree View Features:**

- Expandable/collapsible directory structure
- File icons and type indicators
- File size display

### 4. Global File Search

**How it works:**

- Click "Search" button in the main window
- Enter search query in the search dialog
- Server searches across all users' shared files

**Search Algorithm:**

1. **Exact Match**: Regular expression search for exact matches
2. **Fuzzy Match**: Levenshtein distance-based fuzzy matching (max distance: 1)
3. Case-insensitive search
4. Recursive directory traversal

**Search Features:**

- Real-time search results
- Multiple file selection
- Direct download from search results
- Owner information display

### 5. Direct File Transfer

**Transfer Modes:**

- **Browse-based Transfer**: Download files from a user's shared folder
- **Search-based Transfer**: Download files from search results
- **Direct Send**: Send files directly to another user (peer-initiated)

**Transfer Process:**

1. **File Request**:

   - Client sends file request with file path and port
   - Request includes resume offset for interrupted downloads

2. **File Sending**:

   - Sender opens dedicated socket for file transfer
   - Sends file metadata (path, size, hash)
   - Streams file data in chunks (16KB buffer)
   - Falls back to chunked send on other systems

3. **File Receiving**:
   - Receiver accepts connection on specified port
   - Creates temporary file in `tmp/` directory
   - Receives file data in chunks
   - Updates progress bar in real-time
   - Calculates hash during transfer
   - Verifies hash against metadata
   - Moves file to downloads folder on completion

**Progress Tracking:**

- Real-time progress bars per file
- Percentage completion display

**Resume Functionality:**

- Downloads can be paused at any time
- Paused downloads are stored in `tmp/` directory
- Resume uses file offset to continue from last position
- Automatic resume on application restart

### 6. Chat Messaging

**How it works:**

- Select a user from the online users list
- Type message in the message input area
- Click "Send" or press Enter
- Message is sent directly to peer (P2P)
- Messages are stored locally per conversation
- Message history persists during session

**Message Features:**

- Maximum message length: 256 characters
- Desktop notifications for new messages (if enabled)
- Message history per user

**Message Protocol:**

- Client connects to peer's `CLIENT_RECV_PORT` (4321)
- Sends message with `MESSAGE` header code
- Receiver displays message in chat area
- Messages are not stored server-side (P2P only)

### 7. Online Status Tracking

**Heartbeat Mechanism:**

- Clients send heartbeat every 5 seconds (configurable)
- Server updates last-seen timestamp for each user
- Server returns status of all other users
- Users are marked offline after 10 seconds of inactivity (configurable)

**Status Display:**

- Online users shown with green indicator
- Offline users shown with gray indicator
- Status updates in real-time
- User list automatically refreshes

**Implementation:**

- `HEARTBEAT_REQUEST` header code
- Server maintains `uname_to_status` dictionary
- Client updates UI based on received status


### 8. Download Management

**Download States:**

- `NEVER_STARTED`: Download not yet initiated
- `DOWNLOADING`: Actively downloading
- `PAUSED`: Download paused by user
- `COMPLETED`: Download finished successfully
- `FAILED`: Download failed due to error

**Download Features:**

- Multiple simultaneous downloads
- Individual progress tracking per file
- Pause/resume controls
- Automatic retry on failure (future)
- Download queue management (future)

**Progress Widget:**

- Visual progress bar
- File name and size display
- Percentage completion (shown as "current/total" size)
- Pause/resume toggle button
- Widget automatically removed when download completes

### 9. Settings & Configuration

**Configurable Settings:**

- **Share Folder Path**: Directory containing files to share
- **Downloads Folder Path**: Directory for received files
- **Server IP**: IP address of the central server
- **Username**: Your display name on the network
- **Show Notifications**: Enable/disable desktop notifications


## Project Structure

```
Truflow/
├── src/
│   ├── __init__.py
│   ├── client/
│   │   ├── __init__.py
│   │   ├── app.py                    # Main client application entry point
│   │   ├── dependencies.json         # Flatpak dependencies (client)
│   │   ├── Pipfile                   # Pipenv dependencies (client)
│   │   ├── Pipfile.lock              # Locked dependencies
│   │   └── ui/                        # UI components
│   │       ├── __pycache__/
│   │       ├── BasicConfigWindow.py   # Initial configuration window
│   │       ├── ErrorDialog.py         # Error display dialog
│   │       ├── FileInfoDialog.py      # File information dialog
│   │       ├── FileProgressWidget.py  # Download progress widget
│   │       ├── FileSearchDialog.py    # Global search dialog
│   │       ├── SettingsDialog.py      # Settings configuration dialog
│   │       ├── StartWindow.py         # Welcome/username entry window
│   │       ├── TruflowMainWindow.py   # Main application window
│   │       ├── res/                   # UI resources (images, icons)
│   │       │   ├── earth.png
│   │       ├── userstatus.qrc
│   │       ├── web-off.png
│   │       └── xml/                   # Qt Designer UI files
│   │           ├── BasicConfigWindow.ui
│   │           ├── ErrorDialog.ui
│   │           ├── FileInfoDialog.ui
│   │           ├── FileSearchDialog.ui
│   │           ├── SettingsDialog.ui
│   │           ├── StartWindow.ui
│   │           └── TruflowMainWindow.ui
│   ├── server/
│   │   ├── __init__.py
│   │   ├── __pycache__/
│   │   ├── dependencies.json         # Flatpak dependencies (server)
│   │   ├── Pipfile                   # Pipenv dependencies (server)
│   │   ├── Pipfile.lock              # Locked dependencies
│   │   └── server.py                 # Main server application
│   └── utils/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── constants.py               # Application-wide constants
│       ├── exceptions.py              # Custom exception types
│       ├── helpers.py                 # Utility functions
│       ├── socket_functions.py        # Socket communication helpers
│       └── types.py                   # Type definitions and data structures
└── README.md                          # This file
```

---

## Configuration

### Server Configuration

Server settings are defined in `src/utils/constants.py`:

- `SERVER_RECV_PORT` (default: 1234): Port for server to listen on
- `ONLINE_TIMEOUT` (default: 10 seconds): Time before user marked offline
- `HEADER_TYPE_LEN` (default: 1 byte): Header code length
- `HEADER_MSG_LEN` (default: 15 bytes): Message length field size
- `FMT` (default: "utf-8"): String encoding

### Client Configuration

Client settings are defined in `src/utils/constants.py`:

- `CLIENT_SEND_PORT` (default: 5678): Port for client-to-server communication
- `CLIENT_RECV_PORT` (default: 4321): Port for peer-to-peer communication
- `FILE_BUFFER_LEN` (default: 16KB): File transfer buffer size
- `HASH_BUFFER_LEN` (default: 16MB): Hash calculation buffer size
- `HEARTBEAT_TIMER` (default: 5 seconds): Heartbeat interval
- `MESSAGE_MAX_LEN` (default: 256 bytes): Maximum message length

### User Settings

User settings are stored in `~/.Truflow/db/settings.json`:

```json
{
  "uname": "username",
  "server_ip": "192.168.1.100",
  "share_folder_path": "/path/to/share",
  "downloads_folder_path": "/path/to/downloads",
  "show_notifications": true
}
```

---

## Technical Details

### Communication Protocol

**Message Format:**

```
[Header Code (1 byte)][Message Length (15 bytes)][Message Data (variable)]
```

**Header Codes:**

- `n`: New connection (registration)
- `r`: Request IP (username lookup)
- `R`: Request username (IP lookup)
- `d`: Share data (upload file metadata)
- `D`: Update share data
- `b`: File browse (get user's files)
- `s`: File search (global search)
- `h`: Update hash (file hash update)
- `H`: Heartbeat request (status update)
- `m`: Message (chat message)
- `F`: File request (request file transfer)
- `t`: Direct transfer request (initiate direct send)
- `T`: Direct transfer (file data)
- `e`: Error (error message)

### Data Structures

**DirData** (Directory/File representation):

```python
{
    "name": str,           # File/folder name
    "path": str,           # Relative path from share folder
    "type": str,           # "file" or "directory"
    "size": int | None,    # File size (None for directories)
    "hash": str | None,    # SHA-1 hash (None if not calculated)
    "compression": int,    # CompressionMethod enum value
    "children": list[DirData] | None  # Child items (None for files)
}
```

**FileMetadata** (File transfer metadata):

```python
{
    "path": str,           # File path relative to share folder
    "size": int,           # File size in bytes
    "hash": str | None,    # SHA-1 hash for verification
    "compression": CompressionMethod  # Compression method (currently always NONE)
}
```

**Note:** While the type definition includes a `compression` field, the current implementation does not set this field when creating FileMetadata instances. All files are transferred without compression.

**TransferProgress** (Download progress):

```python
{
    "status": TransferStatus,  # Current transfer state
    "progress": int,           # Bytes transferred
    "percent_progress": float  # Percentage complete
}
```

### Socket Configuration

### Threading Model

**Worker Threads:**

- `ReceiveHandler`: Handles incoming peer connections
- `SendFileWorker`: Sends files to peers
- `RequestFileWorker`: Requests and receives files
- `HandleFileRequestWorker`: Handles incoming file requests
- `ReceiveDirectTransferWorker`: Handles direct file transfers
- `HeartbeatWorker`: Sends periodic heartbeat to server

**Thread Pool:**

- Uses Qt's `QThreadPool` for task management
- All file operations run in worker threads
- UI updates via Qt signals/slots

### Database

**TinyDB Structure:**

```json
{
  "uname": "username",
  "share": [
    {
      "name": "file.txt",
      "path": "file.txt",
      "type": "file",
      "size": 1024,
      "hash": "abc123...",
      "compression": 0,
      "children": null
    }
  ]
}
```

---

## Troubleshooting

### Common Issues

**1. Server won't start:**

- Check if port 1234 is already in use
- Verify Python version (3.10+)
- Check firewall settings
- Ensure all dependencies are installed

**2. Client can't connect to server:**

- Verify server IP address in settings
- Check server is running
- Verify network connectivity
- Check firewall allows connections on ports 1234, 5678, 4321

**3. File transfers fail:**

- Check firewall allows peer-to-peer connections
- Verify both users are online
- Check available disk space
- Verify file permissions

**4. Search returns no results:**

- Ensure users have shared files
- Check server database is populated
- Verify search query spelling

**5. Messages not received:**

- Verify both users are online
- Check desktop notification permissions
- Verify message length < 256 characters

### Log Files

**Server Logs:**

- Location: `~/.Truflow/logs/server_YYYY-MM-DD_HH-MM-SS.log`
- Contains: Connection events, errors, debug information

**Client Logs:**

- Location: `~/.Truflow/logs/client_YYYY-MM-DD_HH-MM-SS.log`
- Contains: UI events, transfer progress, errors


## Contributing

### Development Setup

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request


## Acknowledgments

- Built with PyQt5 for the GUI framework
- Uses MessagePack for efficient serialization
- TinyDB for lightweight database storage
- FuzzySearch for typo-tolerant search

---

## Future Enhancements

Potential features for future versions:

- [ ] File encryption for secure transfers
- [ ] Cancel download functionality
- [ ] Group chat functionality
- [ ] File versioning
- [ ] Transfer speed display
- [ ] Estimated time remaining
