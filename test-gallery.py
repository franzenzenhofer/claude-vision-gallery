#!/usr/bin/env python3
"""Test the Claude Vision Gallery website"""
import urllib.request
import urllib.error
import os
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"

def test_website():
    """Run basic tests on the gallery website"""
    results = {
        "timestamp": datetime.now().isoformat(),
        "tests": [],
        "passed": 0,
        "failed": 0
    }
    
    print("🧪 Testing Claude Vision Gallery\n")
    
    # Test 1: Homepage loads
    print("Testing: Homepage loads...")
    try:
        response = urllib.request.urlopen(BASE_URL)
        content = response.read().decode('utf-8')
        if "Claude Vision Gallery" in content:
            print("✅ Homepage loads successfully")
            results["tests"].append({"name": "Homepage loads", "status": "passed"})
            results["passed"] += 1
        else:
            print("❌ Homepage missing expected content")
            results["tests"].append({"name": "Homepage loads", "status": "failed"})
            results["failed"] += 1
    except Exception as e:
        print(f"❌ Failed to load homepage: {e}")
        results["tests"].append({"name": "Homepage loads", "status": "failed", "error": str(e)})
        results["failed"] += 1
    
    # Test 2: All required sections exist
    print("\nTesting: All sections present...")
    sections = ["hero", "about", "gallery", "process"]
    for section in sections:
        if f'id="{section}"' in content:
            print(f"✅ {section.capitalize()} section found")
            results["tests"].append({"name": f"{section} section exists", "status": "passed"})
            results["passed"] += 1
        else:
            print(f"❌ {section.capitalize()} section missing")
            results["tests"].append({"name": f"{section} section exists", "status": "failed"})
            results["failed"] += 1
    
    # Test 3: All gallery images exist
    print("\nTesting: Gallery images...")
    images = [
        "neural_network.png",
        "data_flow.png", 
        "algorithm_crystal.png",
        "system_architecture.png",
        "code_universe.png"
    ]
    
    for img in images:
        img_path = f"/home/franz/dev/claude-vision-gallery/public/{img}"
        if os.path.exists(img_path):
            size = os.path.getsize(img_path) / 1024 / 1024  # MB
            print(f"✅ {img} exists ({size:.2f} MB)")
            results["tests"].append({"name": f"{img} exists", "status": "passed"})
            results["passed"] += 1
        else:
            print(f"❌ {img} missing")
            results["tests"].append({"name": f"{img} exists", "status": "failed"})
            results["failed"] += 1
    
    # Test 4: CSS and JS files load
    print("\nTesting: Assets load...")
    assets = ["styles.css", "script.js"]
    for asset in assets:
        try:
            response = urllib.request.urlopen(f"{BASE_URL}/{asset}")
            if response.getcode() == 200:
                print(f"✅ {asset} loads successfully")
                results["tests"].append({"name": f"{asset} loads", "status": "passed"})
                results["passed"] += 1
            else:
                print(f"❌ {asset} returned status {response.getcode()}")
                results["tests"].append({"name": f"{asset} loads", "status": "failed"})
                results["failed"] += 1
        except Exception as e:
            print(f"❌ Failed to load {asset}: {e}")
            results["tests"].append({"name": f"{asset} loads", "status": "failed", "error": str(e)})
            results["failed"] += 1
    
    # Summary
    print(f"\n📊 Test Summary:")
    print(f"   Total Tests: {results['passed'] + results['failed']}")
    print(f"   ✅ Passed: {results['passed']}")
    print(f"   ❌ Failed: {results['failed']}")
    
    # Save results
    with open('test-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n📄 Results saved to test-results.json")
    
    return results['failed'] == 0

if __name__ == "__main__":
    import sys
    success = test_website()
    sys.exit(0 if success else 1)