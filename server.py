#!/usr/bin/env python3
"""
Simple HTTP server to serve loads.json for testing purposes.
This server provides CORS headers to allow cross-origin requests.
"""

import http.server
import socketserver
import json
import os
from urllib.parse import urlparse, parse_qs

class LoadsHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Add CORS headers to allow cross-origin requests
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()

    def do_GET(self):
        if self.path == '/loads.json' or self.path == '/loads':
            self.serve_loads()
        else:
            super().do_GET()

    def do_OPTIONS(self):
        # Handle preflight requests
        self.send_response(200)
        self.end_headers()

    def serve_loads(self):
        try:
            # Load the JSON data
            with open('loads.json', 'r') as f:
                loads_data = json.load(f)
            
            # Parse query parameters for filtering
            parsed_url = urlparse(self.path)
            query_params = parse_qs(parsed_url.query)
            
            # Apply filters if provided
            filtered_loads = loads_data
            
            if 'equipment_type' in query_params:
                equipment_filter = query_params['equipment_type'][0]
                filtered_loads = [load for load in filtered_loads 
                                if load.get('equipment_type', '').lower() == equipment_filter.lower()]
            
            if 'origin' in query_params:
                origin_filter = query_params['origin'][0]
                filtered_loads = [load for load in filtered_loads 
                                if origin_filter.lower() in load.get('origin', '').lower()]
            
            if 'destination' in query_params:
                dest_filter = query_params['destination'][0]
                filtered_loads = [load for load in filtered_loads 
                                if dest_filter.lower() in load.get('destination', '').lower()]
            
            if 'min_rate' in query_params:
                min_rate = float(query_params['min_rate'][0])
                filtered_loads = [load for load in filtered_loads 
                                if load.get('loadboard_rate', 0) >= min_rate]
            
            if 'max_rate' in query_params:
                max_rate = float(query_params['max_rate'][0])
                filtered_loads = [load for load in filtered_loads 
                                if load.get('loadboard_rate', 0) <= max_rate]
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(filtered_loads, indent=2).encode())
            
        except FileNotFoundError:
            self.send_error(404, "loads.json file not found")
        except Exception as e:
            self.send_error(500, f"Server error: {str(e)}")

def run_server(port=8000):
    """Run the HTTP server on the specified port."""
    handler = LoadsHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🚛 Load API Mock Server running on http://localhost:{port}")
        print(f"📄 Loads data available at: http://localhost:{port}/loads.json")
        print(f"🔍 Filter examples:")
        print(f"   - By equipment: http://localhost:{port}/loads.json?equipment_type=Flatbed")
        print(f"   - By origin: http://localhost:{port}/loads.json?origin=Dallas")
        print(f"   - By rate range: http://localhost:{port}/loads.json?min_rate=1000&max_rate=1500")
        print(f"⏹️  Press Ctrl+C to stop the server")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 Server stopped.")

if __name__ == "__main__":
    import sys
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
        except ValueError:
            print("Invalid port number. Using default port 8000.")
    
    run_server(port)
