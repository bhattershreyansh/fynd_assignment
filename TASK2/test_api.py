"""
Test script for the new priority queue and export endpoints
Run this after starting the server to verify everything works
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_submit_reviews():
    """Submit some test reviews with different ratings"""
    print("\n" + "="*60)
    print("Testing: Submit Reviews")
    print("="*60)
    
    test_reviews = [
        {"rating": 1, "review_text": "Terrible service! Very disappointed with the quality and long wait times."},
        {"rating": 2, "review_text": "Not good. The product was damaged and customer service was unhelpful."},
        {"rating": 5, "review_text": "Absolutely amazing! Best experience ever. Highly recommend to everyone!"},
        {"rating": 4, "review_text": "Pretty good overall. Minor issues but generally satisfied with the service."},
        {"rating": 1, "review_text": "Worst experience ever. Will never come back. Complete waste of money."},
    ]
    
    for review in test_reviews:
        try:
            response = requests.post(f"{BASE_URL}/api/reviews", json=review)
            if response.status_code == 200:
                data = response.json()
                print(f"✓ Submitted {review['rating']}-star review (ID: {data['id'][:8]}...)")
            else:
                print(f"✗ Failed to submit review: {response.status_code}")
        except Exception as e:
            print(f"✗ Error: {str(e)}")


def test_priority_queue():
    """Test the priority queue endpoint"""
    print("\n" + "="*60)
    print("Testing: Priority Queue Endpoint")
    print("="*60)
    
    try:
        response = requests.get(f"{BASE_URL}/api/reviews/priority?limit=10")
        if response.status_code == 200:
            data = response.json()
            print(f"✓ Priority endpoint working!")
            print(f"  Total urgent reviews: {data['total_urgent']}")
            print(f"  Message: {data['message']}")
            print(f"  Returned {len(data['urgent_reviews'])} urgent reviews")
            
            if data['urgent_reviews']:
                print("\n  Urgent Reviews:")
                for review in data['urgent_reviews'][:3]:  # Show first 3
                    print(f"    - {review['rating']}⭐: {review['review_text'][:50]}...")
        else:
            print(f"✗ Failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_export():
    """Test the export endpoint"""
    print("\n" + "="*60)
    print("Testing: Export to CSV Endpoint")
    print("="*60)
    
    try:
        # Export all reviews
        response = requests.get(f"{BASE_URL}/api/reviews/export")
        if response.status_code == 200:
            print(f"✓ Export all reviews working!")
            print(f"  Content-Type: {response.headers.get('Content-Type')}")
            print(f"  File size: {len(response.content)} bytes")
            
            # Save to file
            filename = "test_export_all.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  Saved to: {filename}")
        else:
            print(f"✗ Failed: {response.status_code}")
        
        # Export only 1-star reviews
        response = requests.get(f"{BASE_URL}/api/reviews/export?rating=1")
        if response.status_code == 200:
            print(f"✓ Export filtered (rating=1) working!")
            filename = "test_export_1star.csv"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"  Saved to: {filename}")
        else:
            print(f"✗ Failed: {response.status_code}")
            
    except Exception as e:
        print(f"✗ Error: {str(e)}")


def test_all_endpoints():
    """Test all endpoints"""
    print("\n" + "="*60)
    print("Testing: All Endpoints")
    print("="*60)
    
    try:
        # Health check
        response = requests.get(f"{BASE_URL}/")
        print(f"✓ Health check: {response.json()['status']}")
        
        # Get all reviews
        response = requests.get(f"{BASE_URL}/api/reviews")
        data = response.json()
        print(f"✓ Get all reviews: {data['total']} total reviews")
        
        # Get analytics
        response = requests.get(f"{BASE_URL}/api/analytics")
        data = response.json()
        print(f"✓ Analytics: Avg rating {data['average_rating']}, {data['total_reviews']} total")
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")


if __name__ == "__main__":
    print("\n" + "="*60)
    print("REVIEW SYSTEM API - TEST SUITE")
    print("="*60)
    print(f"Testing API at: {BASE_URL}")
    print("Make sure the server is running (python main.py)")
    
    # Run tests
    test_submit_reviews()
    test_all_endpoints()
    test_priority_queue()
    test_export()
    
    print("\n" + "="*60)
    print("TESTS COMPLETED!")
    print("="*60)
    print("\nCheck the generated CSV files:")
    print("  - test_export_all.csv")
    print("  - test_export_1star.csv")
