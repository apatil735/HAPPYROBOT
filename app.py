#!/usr/bin/env python3
"""
Flask API for Carrier Sales Automation System
Provides endpoints for carrier verification, load search, negotiation, and booking.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import uuid
from datetime import datetime, timedelta
import random
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# In-memory storage for demonstration (use database in production)
carriers_db = {}
loads_db = {}
negotiations_db = {}
bookings_db = {}
call_analytics_db = {}

# Initialize mock data when the app starts
def initialize_mock_data():
    """Initialize the system with mock data for demonstration."""
    
    # Mock carriers
    carriers_db.update({
        "MC123456": {
            "mc_number": "MC123456",
            "company_name": "Swift Transportation",
            "status": "active",
            "insurance_valid": True,
            "safety_rating": "A",
            "verified": True,
            "contact_info": {
                "phone": "+1-555-0123",
                "email": "dispatch@swifttrans.com"
            }
        },
        "MC789012": {
            "mc_number": "MC789012",
            "company_name": "Schneider National",
            "status": "active",
            "insurance_valid": True,
            "safety_rating": "A+",
            "verified": True,
            "contact_info": {
                "phone": "+1-555-0456",
                "email": "operations@schneider.com"
            }
        },
        "MC345678": {
            "mc_number": "MC345678",
            "company_name": "J.B. Hunt Transport",
            "status": "suspended",
            "insurance_valid": False,
            "safety_rating": "C",
            "verified": False,
            "contact_info": {
                "phone": "+1-555-0789",
                "email": "info@jbhunt.com"
            }
        }
    })
    
    # Mock loads
    loads_db.update({
        "L001": {
            "load_id": "L001",
            "origin": "Dallas, TX",
            "destination": "Houston, TX",
            "pickup_datetime": "2025-09-10T08:00:00",
            "delivery_datetime": "2025-09-11T18:00:00",
            "equipment_type": "Flatbed",
            "loadboard_rate": 1500,
            "negotiated_rate": None,
            "notes": "Fragile equipment",
            "weight": 10000,
            "commodity_type": "Machinery",
            "status": "available",
            "miles": 240,
            "deadhead_miles": 15
        },
        "L002": {
            "load_id": "L002",
            "origin": "Chicago, IL",
            "destination": "Detroit, MI",
            "pickup_datetime": "2025-09-12T07:00:00",
            "delivery_datetime": "2025-09-13T20:00:00",
            "equipment_type": "Reefer",
            "loadboard_rate": 1200,
            "negotiated_rate": None,
            "notes": "Perishable goods",
            "weight": 8000,
            "commodity_type": "Food",
            "status": "available",
            "miles": 280,
            "deadhead_miles": 25
        },
        "L003": {
            "load_id": "L003",
            "origin": "Los Angeles, CA",
            "destination": "Phoenix, AZ",
            "pickup_datetime": "2025-09-14T09:00:00",
            "delivery_datetime": "2025-09-15T16:00:00",
            "equipment_type": "Dry Van",
            "loadboard_rate": 800,
            "negotiated_rate": None,
            "notes": "General freight",
            "weight": 15000,
            "commodity_type": "Electronics",
            "status": "available",
            "miles": 370,
            "deadhead_miles": 30
        },
        "L004": {
            "load_id": "L004",
            "origin": "Miami, FL",
            "destination": "Atlanta, GA",
            "pickup_datetime": "2025-09-16T06:00:00",
            "delivery_datetime": "2025-09-17T14:00:00",
            "equipment_type": "Flatbed",
            "loadboard_rate": 1100,
            "negotiated_rate": None,
            "notes": "Construction materials",
            "weight": 12000,
            "commodity_type": "Building Materials",
            "status": "available",
            "miles": 660,
            "deadhead_miles": 20
        },
        "L005": {
            "load_id": "L005",
            "origin": "Seattle, WA",
            "destination": "Portland, OR",
            "pickup_datetime": "2025-09-18T10:00:00",
            "delivery_datetime": "2025-09-19T15:00:00",
            "equipment_type": "Reefer",
            "loadboard_rate": 600,
            "negotiated_rate": None,
            "notes": "Temperature controlled",
            "weight": 5000,
            "commodity_type": "Pharmaceuticals",
            "status": "available",
            "miles": 175,
            "deadhead_miles": 10
        }
    })

# Initialize data when the app starts
initialize_mock_data()

@app.route('/api/verify-carrier', methods=['POST'])
def verify_carrier():
    """
    Verify carrier status using MC number.
    Critical for ensuring only legitimate carriers can book loads.
    """
    try:
        data = request.get_json()
        mc_number = data.get('mc_number')
        
        if not mc_number:
            return jsonify({
                'success': False,
                'error': 'MC number is required'
            }), 400
        
        # Check if carrier exists
        carrier = carriers_db.get(mc_number)
        
        if not carrier:
            return jsonify({
                'success': False,
                'verified': False,
                'message': 'Carrier not found in database',
                'mc_number': mc_number
            }), 404
        
        # Return verification status
        return jsonify({
            'success': True,
            'verified': carrier['verified'],
            'carrier_info': {
                'mc_number': carrier['mc_number'],
                'company_name': carrier['company_name'],
                'status': carrier['status'],
                'insurance_valid': carrier['insurance_valid'],
                'safety_rating': carrier['safety_rating']
            },
            'message': 'Carrier verification completed'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Verification failed: {str(e)}'
        }), 500

@app.route('/api/search-loads', methods=['POST'])
def search_loads():
    """
    Search for available loads based on criteria.
    Core functionality for matching carriers with suitable loads.
    """
    try:
        data = request.get_json()
        
        # Extract search criteria
        equipment_type = data.get('equipment_type')
        origin_preference = data.get('origin_preference')
        destination_preference = data.get('destination_preference')
        min_rate = data.get('min_rate')
        max_rate = data.get('max_rate')
        max_miles = data.get('max_miles')
        commodity_type = data.get('commodity_type')
        
        # Filter loads based on criteria
        matching_loads = []
        
        for load_id, load in loads_db.items():
            if load['status'] != 'available':
                continue
                
            # Apply filters
            if equipment_type and load['equipment_type'].lower() != equipment_type.lower():
                continue
                
            if origin_preference and origin_preference.lower() not in load['origin'].lower():
                continue
                
            if destination_preference and destination_preference.lower() not in load['destination'].lower():
                continue
                
            if min_rate and load['loadboard_rate'] < min_rate:
                continue
                
            if max_rate and load['loadboard_rate'] > max_rate:
                continue
                
            if max_miles and load['miles'] > max_miles:
                continue
                
            if commodity_type and commodity_type.lower() not in load['commodity_type'].lower():
                continue
            
            matching_loads.append(load)
        
        # Sort by rate (highest first)
        matching_loads.sort(key=lambda x: x['loadboard_rate'], reverse=True)
        
        return jsonify({
            'success': True,
            'loads': matching_loads,
            'total_count': len(matching_loads),
            'search_criteria': {
                'equipment_type': equipment_type,
                'origin_preference': origin_preference,
                'destination_preference': destination_preference,
                'min_rate': min_rate,
                'max_rate': max_rate,
                'max_miles': max_miles,
                'commodity_type': commodity_type
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Search failed: {str(e)}'
        }), 500

@app.route('/api/load-details/<load_id>', methods=['GET'])
def get_load_details(load_id):
    """
    Get detailed information about a specific load.
    Essential for carriers to make informed booking decisions.
    """
    try:
        load = loads_db.get(load_id)
        
        if not load:
            return jsonify({
                'success': False,
                'error': 'Load not found'
            }), 404
        
        # Add additional details for carrier decision-making
        load_details = load.copy()
        load_details.update({
            'pickup_window': '2 hours',
            'delivery_window': '4 hours',
            'required_documents': ['Bill of Lading', 'Insurance Certificate'],
            'special_requirements': load.get('notes', ''),
            'fuel_surcharge': 'Included',
            'detention_policy': 'Free time: 2 hours, then $50/hour',
            'tarp_required': load['equipment_type'] == 'Flatbed'
        })
        
        return jsonify({
            'success': True,
            'load_details': load_details
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to retrieve load details: {str(e)}'
        }), 500

@app.route('/api/negotiate', methods=['POST'])
def negotiate_load():
    """
    Handle rate negotiations between carriers and brokers.
    Critical for maximizing revenue and carrier satisfaction.
    """
    try:
        data = request.get_json()
        load_id = data.get('load_id')
        counter_offer = data.get('counter_offer')
        negotiation_round = data.get('negotiation_round', 1)
        mc_number = data.get('mc_number')
        
        if not all([load_id, counter_offer, mc_number]):
            return jsonify({
                'success': False,
                'error': 'load_id, counter_offer, and mc_number are required'
            }), 400
        
        load = loads_db.get(load_id)
        if not load:
            return jsonify({
                'success': False,
                'error': 'Load not found'
            }), 404
        
        # Simulate negotiation logic
        original_rate = load['loadboard_rate']
        negotiation_id = str(uuid.uuid4())
        
        # Store negotiation attempt
        negotiations_db[negotiation_id] = {
            'negotiation_id': negotiation_id,
            'load_id': load_id,
            'mc_number': mc_number,
            'original_rate': original_rate,
            'counter_offer': counter_offer,
            'negotiation_round': negotiation_round,
            'timestamp': datetime.now().isoformat()
        }
        
        # Simulate broker response (mock logic)
        if counter_offer >= original_rate * 0.85:  # Accept if within 15% of original
            accepted = True
            final_rate = counter_offer
            message = "Rate accepted!"
        elif negotiation_round >= 3:  # Max 3 rounds
            accepted = False
            final_rate = original_rate
            message = "Maximum negotiation rounds reached. Final rate: original rate."
        else:
            accepted = False
            final_rate = original_rate * 0.95  # Counter with 5% reduction
            message = f"Counter-offer: ${final_rate}. Round {negotiation_round + 1} available."
        
        # Update load with negotiated rate if accepted
        if accepted:
            loads_db[load_id]['negotiated_rate'] = final_rate
            loads_db[load_id]['status'] = 'negotiated'
        
        return jsonify({
            'success': True,
            'negotiation_id': negotiation_id,
            'accepted': accepted,
            'final_rate': final_rate,
            'message': message,
            'negotiation_round': negotiation_round,
            'can_negotiate_again': not accepted and negotiation_round < 3
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Negotiation failed: {str(e)}'
        }), 500

@app.route('/api/book-load', methods=['POST'])
def book_load():
    """
    Book a load for a verified carrier.
    Final step in the carrier-broker transaction process.
    """
    try:
        data = request.get_json()
        load_id = data.get('load_id')
        agreed_rate = data.get('agreed_rate')
        mc_number = data.get('mc_number')
        
        if not all([load_id, agreed_rate, mc_number]):
            return jsonify({
                'success': False,
                'error': 'load_id, agreed_rate, and mc_number are required'
            }), 400
        
        # Verify carrier
        carrier = carriers_db.get(mc_number)
        if not carrier or not carrier['verified']:
            return jsonify({
                'success': False,
                'error': 'Carrier not verified or not found'
            }), 403
        
        # Check load availability
        load = loads_db.get(load_id)
        if not load or load['status'] not in ['available', 'negotiated']:
            return jsonify({
                'success': False,
                'error': 'Load not available for booking'
            }), 409
        
        # Create booking
        booking_id = str(uuid.uuid4())
        booking = {
            'booking_id': booking_id,
            'load_id': load_id,
            'mc_number': mc_number,
            'agreed_rate': agreed_rate,
            'booking_timestamp': datetime.now().isoformat(),
            'status': 'confirmed',
            'carrier_info': {
                'company_name': carrier['company_name'],
                'contact_phone': carrier['contact_info']['phone'],
                'contact_email': carrier['contact_info']['email']
            },
            'load_info': {
                'origin': load['origin'],
                'destination': load['destination'],
                'pickup_datetime': load['pickup_datetime'],
                'delivery_datetime': load['delivery_datetime'],
                'equipment_type': load['equipment_type']
            }
        }
        
        bookings_db[booking_id] = booking
        
        # Update load status
        loads_db[load_id]['status'] = 'booked'
        loads_db[load_id]['booked_by'] = mc_number
        loads_db[load_id]['final_rate'] = agreed_rate
        
        return jsonify({
            'success': True,
            'booking_id': booking_id,
            'booking': booking,
            'message': 'Load successfully booked!'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Booking failed: {str(e)}'
        }), 500

@app.route('/api/store-call-data', methods=['POST'])
def store_call_data():
    """
    Store call analytics data for performance tracking.
    Essential for improving sales processes and training.
    """
    try:
        data = request.get_json()
        
        required_fields = [
            'transcript', 'classification', 'sentiment', 
            'extracted_data', 'call_timestamp', 'call_duration', 'caller_number'
        ]
        
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({
                'success': False,
                'error': f'Missing required fields: {", ".join(missing_fields)}'
            }), 400
        
        # Create call analytics record
        call_id = str(uuid.uuid4())
        call_record = {
            'call_id': call_id,
            'transcript': data['transcript'],
            'classification': data['classification'],
            'sentiment': data['sentiment'],
            'extracted_data': data['extracted_data'],
            'call_timestamp': data['call_timestamp'],
            'call_duration': data['call_duration'],
            'caller_number': data['caller_number'],
            'stored_timestamp': datetime.now().isoformat(),
            'processing_status': 'completed'
        }
        
        call_analytics_db[call_id] = call_record
        
        return jsonify({
            'success': True,
            'call_id': call_id,
            'message': 'Call data stored successfully',
            'analytics_summary': {
                'classification': data['classification'],
                'sentiment_score': data['sentiment'],
                'duration': data['call_duration'],
                'data_points_extracted': len(data['extracted_data']) if isinstance(data['extracted_data'], list) else 1
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f'Failed to store call data: {str(e)}'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'endpoints': [
            '/api/verify-carrier',
            '/api/search-loads',
            '/api/load-details/<load_id>',
            '/api/negotiate',
            '/api/book-load',
            '/api/store-call-data'
        ]
    })

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get system statistics for monitoring."""
    return jsonify({
        'total_carriers': len(carriers_db),
        'verified_carriers': len([c for c in carriers_db.values() if c['verified']]),
        'total_loads': len(loads_db),
        'available_loads': len([l for l in loads_db.values() if l['status'] == 'available']),
        'booked_loads': len([l for l in loads_db.values() if l['status'] == 'booked']),
        'total_bookings': len(bookings_db),
        'total_negotiations': len(negotiations_db),
        'total_calls_analyzed': len(call_analytics_db)
    })

if __name__ == '__main__':
    # Initialize mock data
    initialize_mock_data()
    
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5000))
    
    print("🚛 Carrier Sales Automation API Starting...")
    print(f"📊 Loaded {len(loads_db)} loads")
    print(f"🚚 Loaded {len(carriers_db)} carriers")
    print(f"🌐 Server running on port {port}")
    print("📋 Available endpoints:")
    print("   POST /api/verify-carrier")
    print("   POST /api/search-loads")
    print("   GET  /api/load-details/<load_id>")
    print("   POST /api/negotiate")
    print("   POST /api/book-load")
    print("   POST /api/store-call-data")
    print("   GET  /api/health")
    print("   GET  /api/stats")
    
    app.run(host='0.0.0.0', port=port, debug=True)

