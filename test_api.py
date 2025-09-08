#!/usr/bin/env python3
"""
Test script for Carrier Sales Automation API
Run this to verify all endpoints are working correctly.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:5000"
TEST_MC_NUMBER = "MC123456"
TEST_LOAD_ID = "L001"

def print_response(endpoint, response):
    """Print formatted response for testing."""
    print(f"\n{'='*50}")
    print(f"Testing: {endpoint}")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print(f"{'='*50}")

def test_health_check():
    """Test the health check endpoint."""
    print("\n🏥 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/api/health")
        print_response("GET /api/health", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_verify_carrier():
    """Test carrier verification endpoint."""
    print("\n🚚 Testing Carrier Verification...")
    try:
        data = {"mc_number": TEST_MC_NUMBER}
        response = requests.post(f"{BASE_URL}/api/verify-carrier", json=data)
        print_response("POST /api/verify-carrier", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Carrier verification failed: {e}")
        return False

def test_search_loads():
    """Test load search endpoint."""
    print("\n🔍 Testing Load Search...")
    try:
        # Test 1: Search for Flatbed loads
        data = {
            "equipment_type": "Flatbed",
            "min_rate": 1000
        }
        response = requests.post(f"{BASE_URL}/api/search-loads", json=data)
        print_response("POST /api/search-loads (Flatbed)", response)
        
        # Test 2: Search for loads from Dallas
        data = {
            "origin_preference": "Dallas",
            "max_miles": 500
        }
        response = requests.post(f"{BASE_URL}/api/search-loads", json=data)
        print_response("POST /api/search-loads (Dallas)", response)
        
        return True
    except Exception as e:
        print(f"❌ Load search failed: {e}")
        return False

def test_load_details():
    """Test load details endpoint."""
    print("\n📋 Testing Load Details...")
    try:
        response = requests.get(f"{BASE_URL}/api/load-details/{TEST_LOAD_ID}")
        print_response(f"GET /api/load-details/{TEST_LOAD_ID}", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Load details failed: {e}")
        return False

def test_negotiate():
    """Test negotiation endpoint."""
    print("\n💰 Testing Load Negotiation...")
    try:
        data = {
            "load_id": TEST_LOAD_ID,
            "counter_offer": 1600,
            "negotiation_round": 1,
            "mc_number": TEST_MC_NUMBER
        }
        response = requests.post(f"{BASE_URL}/api/negotiate", json=data)
        print_response("POST /api/negotiate", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Negotiation failed: {e}")
        return False

def test_book_load():
    """Test load booking endpoint."""
    print("\n📝 Testing Load Booking...")
    try:
        data = {
            "load_id": "L002",  # Use different load to avoid conflicts
            "agreed_rate": 1200,
            "mc_number": TEST_MC_NUMBER
        }
        response = requests.post(f"{BASE_URL}/api/book-load", json=data)
        print_response("POST /api/book-load", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Load booking failed: {e}")
        return False

def test_store_call_data():
    """Test call data storage endpoint."""
    print("\n📞 Testing Call Data Storage...")
    try:
        data = {
            "transcript": "Hello, I'm interested in the Dallas to Houston load. What's the rate?",
            "classification": "load_inquiry",
            "sentiment": "positive",
            "extracted_data": {
                "load_interest": True,
                "origin": "Dallas",
                "destination": "Houston",
                "rate_inquiry": True
            },
            "call_timestamp": "2025-09-04T10:30:00Z",
            "call_duration": 180,
            "caller_number": "+1-555-0123"
        }
        response = requests.post(f"{BASE_URL}/api/store-call-data", json=data)
        print_response("POST /api/store-call-data", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Call data storage failed: {e}")
        return False

def test_stats():
    """Test statistics endpoint."""
    print("\n📊 Testing Statistics...")
    try:
        response = requests.get(f"{BASE_URL}/api/stats")
        print_response("GET /api/stats", response)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Statistics failed: {e}")
        return False

def run_all_tests():
    """Run all API tests."""
    print("🚛 Carrier Sales Automation API - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Carrier Verification", test_verify_carrier),
        ("Load Search", test_search_loads),
        ("Load Details", test_load_details),
        ("Negotiation", test_negotiate),
        ("Load Booking", test_book_load),
        ("Call Data Storage", test_store_call_data),
        ("Statistics", test_stats)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name}...")
        try:
            success = test_func()
            results.append((test_name, success))
            if success:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} ERROR: {e}")
            results.append((test_name, False))
        
        time.sleep(0.5)  # Small delay between tests
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n🎯 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    print("Starting API tests...")
    print(f"Testing against: {BASE_URL}")
    print("Make sure the API server is running!")
    print("\nPress Enter to continue or Ctrl+C to cancel...")
    input()
    
    run_all_tests()

