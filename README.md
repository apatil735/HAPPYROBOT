# Load API Mock Server

A simple local HTTP server that serves sample load data for testing HappyRobot webhook integrations.

## Files

- `loads.json` - Sample load data in JSON format
- `server.py` - Python HTTP server with filtering capabilities
- `README.md` - This documentation

## Quick Start

### Option 1: Using Python's built-in server (Simple)

```bash
# Navigate to the project directory
cd path/to/HappyRobot

# Start the simple server
python3 -m http.server 8000
```

Your loads data will be available at: `http://localhost:8000/loads.json`

### Option 2: Using the custom server (Advanced with filtering)

```bash
# Navigate to the project directory
cd path/to/HappyRobot

# Start the custom server
python3 server.py

# Or specify a custom port
python3 server.py 3000
```

## API Endpoints

### GET /loads.json
Returns all load data or filtered results based on query parameters.

**Query Parameters:**
- `equipment_type` - Filter by equipment type (e.g., "Flatbed", "Reefer", "Dry Van")
- `origin` - Filter by origin city (partial match)
- `destination` - Filter by destination city (partial match)
- `min_rate` - Minimum loadboard rate
- `max_rate` - Maximum loadboard rate

**Examples:**
```
# Get all loads
http://localhost:8000/loads.json

# Get only Flatbed loads
http://localhost:8000/loads.json?equipment_type=Flatbed

# Get loads from Dallas
http://localhost:8000/loads.json?origin=Dallas

# Get loads with rate between $1000-$1500
http://localhost:8000/loads.json?min_rate=1000&max_rate=1500

# Combine filters
http://localhost:8000/loads.json?equipment_type=Reefer&origin=Chicago&min_rate=1000
```

## Sample Load Data Structure

Each load entry contains:

```json
{
  "load_id": "L001",
  "origin": "Dallas, TX",
  "destination": "Houston, TX",
  "pickup_datetime": "2025-09-10T08:00:00",
  "delivery_datetime": "2025-09-11T18:00:00",
  "equipment_type": "Flatbed",
  "loadboard_rate": 1500,
  "notes": "Fragile equipment",
  "weight": 10000,
  "commodity_type": "Machinery"
}
```

## HappyRobot Integration

### Webhook Node Configuration

1. **URL**: `http://localhost:8000/loads.json`
2. **Method**: `GET`
3. **Authentication**: None required
4. **Headers**: None required

### Filtering in HappyRobot

You can filter loads in two ways:

1. **Server-side filtering** (using the custom server):
   - Add query parameters to the URL
   - Example: `http://localhost:8000/loads.json?equipment_type=Flatbed`

2. **Client-side filtering** (using HappyRobot conditions):
   - Fetch all loads and use condition nodes to filter
   - Use scripting nodes for complex filtering logic

### Example HappyRobot Workflow

1. **Webhook Node**: Fetch from `http://localhost:8000/loads.json`
2. **Condition Node**: Check if `equipment_type` equals "Flatbed"
3. **Action Node**: Process matching loads

## CORS Support

The custom server includes CORS headers to allow cross-origin requests, making it compatible with web-based HappyRobot workflows.

## Stopping the Server

Press `Ctrl+C` in the terminal to stop the server.

## Troubleshooting

- **Port already in use**: Try a different port: `python3 server.py 3000`
- **File not found**: Ensure `loads.json` is in the same directory as `server.py`
- **Permission denied**: Make sure you have permission to bind to the port (try ports 3000+ if 8000 fails)
