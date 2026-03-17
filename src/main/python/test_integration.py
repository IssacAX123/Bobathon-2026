#!/usr/bin/env python3
"""
Integration Test - Stories 1 & 2
Demonstrates the complete workflow from issue analysis to diagram generation.
"""

import json
from github_issue_analyzer import GitHubIssueAnalyzer, Package as AnalyzerPackage
from diagram_generator import DiagramGenerator, format_output


def create_test_data():
    """Create test data simulating Story 1 output."""
    return {
        "success": True,
        "analysis_time_ms": 503,
        "error_message": None,
        "issue": {
            "number": 1,
            "title": "Update OpenLiberty ltpa token processing to handle PQC algorithms",
            "body": "Open Liberty has support for FIPS-140...",
            "labels": [],
            "url": "https://github.ibm.com/David-Webster1/jakarta_security/issues/1",
            "created_at": "2026-03-17T13:01:16Z",
            "author": "David-Webster1"
        },
        "packages": [
            {
                "name": "com.ibm.ws.crypto.ltpakeyutil",
                "confidence": 0.95,
                "context": "LTPA key generation and encryption",
                "package_type": "IBM",
                "location": "inferred"
            },
            {
                "name": "com.ibm.ws.security.utility",
                "confidence": 0.90,
                "context": "securityUtility command",
                "package_type": "IBM",
                "location": "inferred"
            },
            {
                "name": "com.ibm.ws.security.token.ltpa",
                "confidence": 0.90,
                "context": "LTPA token processing",
                "package_type": "IBM",
                "location": "inferred"
            },
            {
                "name": "com.ibm.ws.security.token.ltpa.internal",
                "confidence": 0.85,
                "context": "Internal LTPA implementation",
                "package_type": "IBM",
                "location": "inferred"
            },
            {
                "name": "io.openliberty.security.jakartasec.4.0.internal",
                "confidence": 0.75,
                "context": "Jakarta Security integration",
                "package_type": "LIBERTY",
                "location": "inferred"
            }
        ]
    }


def test_single_package():
    """Test diagram generation with single package."""
    print("=" * 80)
    print("TEST 1: Single Package")
    print("=" * 80)
    
    data = {
        "success": True,
        "packages": [
            {
                "name": "io.openliberty.security.jwt",
                "confidence": 0.95,
                "package_type": "LIBERTY"
            }
        ],
        "issue": {
            "number": 123,
            "title": "JWT token validation fails"
        }
    }
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(data)
    
    print(format_output(result))
    print()


def test_multiple_packages():
    """Test diagram generation with multiple packages."""
    print("=" * 80)
    print("TEST 2: Multiple Packages with Relationships")
    print("=" * 80)
    
    data = {
        "success": True,
        "packages": [
            {
                "name": "io.openliberty.security.jwt",
                "confidence": 0.95,
                "package_type": "LIBERTY"
            },
            {
                "name": "io.openliberty.security.jwt.internal",
                "confidence": 0.90,
                "package_type": "LIBERTY"
            },
            {
                "name": "com.ibm.ws.security.token",
                "confidence": 0.85,
                "package_type": "IBM"
            }
        ],
        "issue": {
            "number": 456,
            "title": "Token processing error in JWT validation"
        }
    }
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(data)
    
    print(format_output(result))
    print()


def test_ltpa_pqc_issue():
    """Test with the actual LTPA PQC issue data."""
    print("=" * 80)
    print("TEST 3: LTPA PQC Issue (Real Data)")
    print("=" * 80)
    
    data = create_test_data()
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(data)
    
    print(format_output(result))
    print()


def test_no_packages():
    """Test handling of no packages."""
    print("=" * 80)
    print("TEST 4: No Packages Found")
    print("=" * 80)
    
    data = {
        "success": True,
        "packages": [],
        "issue": {
            "number": 789,
            "title": "Generic issue with no package mentions"
        }
    }
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(data)
    
    print(format_output(result))
    print()


def test_many_packages():
    """Test with more than 5 packages."""
    print("=" * 80)
    print("TEST 5: More Than 5 Packages")
    print("=" * 80)
    
    data = {
        "success": True,
        "packages": [
            {"name": "io.openliberty.security.jwt", "confidence": 0.95, "package_type": "LIBERTY"},
            {"name": "io.openliberty.security.authentication", "confidence": 0.90, "package_type": "LIBERTY"},
            {"name": "com.ibm.ws.security.token", "confidence": 0.87, "package_type": "IBM"},
            {"name": "io.openliberty.cdi", "confidence": 0.82, "package_type": "LIBERTY"},
            {"name": "com.ibm.ws.security.registry", "confidence": 0.78, "package_type": "IBM"},
            {"name": "io.openliberty.config", "confidence": 0.75, "package_type": "LIBERTY"},
            {"name": "com.ibm.ws.logging", "confidence": 0.68, "package_type": "IBM"},
            {"name": "io.openliberty.monitoring", "confidence": 0.62, "package_type": "LIBERTY"}
        ],
        "issue": {
            "number": 999,
            "title": "Complex security issue affecting multiple components"
        }
    }
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(data)
    
    print(format_output(result))
    print()


def test_implementation_pattern():
    """Test implementation pattern detection."""
    print("=" * 80)
    print("TEST 6: Implementation Pattern Detection")
    print("=" * 80)
    
    data = {
        "success": True,
        "packages": [
            {"name": "io.openliberty.cdi", "confidence": 0.95, "package_type": "LIBERTY"},
            {"name": "io.openliberty.cdi.impl", "confidence": 0.90, "package_type": "LIBERTY"}
        ],
        "issue": {
            "number": 111,
            "title": "CDI implementation issue"
        }
    }
    
    generator = DiagramGenerator()
    result = generator.generate_diagram(data)
    
    print(format_output(result))
    print()


def main():
    """Run all tests."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 20 + "INTEGRATION TEST: STORIES 1 & 2" + " " * 26 + "║")
    print("╚" + "=" * 78 + "╝")
    print()
    
    test_single_package()
    test_multiple_packages()
    test_ltpa_pqc_issue()
    test_no_packages()
    test_many_packages()
    test_implementation_pattern()
    
    print("=" * 80)
    print("✅ All tests completed!")
    print("=" * 80)


if __name__ == '__main__':
    main()

# Made with Bob
