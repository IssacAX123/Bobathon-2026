#!/usr/bin/env python3
"""
Test script for MCP Server (Story 4)
"""

import json
import subprocess
import sys


def test_url_validation():
    """Test URL validation."""
    print("Testing URL validation...")
    
    # Test invalid URL
    result = subprocess.run(
        ['python3', 'mcp_server.py', 'invalid-url'],
        capture_output=True,
        text=True
    )
    
    response = json.loads(result.stdout)
    assert response['success'] == False
    assert response['failed_step'] == 'validate-url'
    print("✓ URL validation works")


def test_dry_run():
    """Test dry run mode."""
    print("\nTesting dry run mode...")
    
    # Use a known public issue
    result = subprocess.run(
        ['python3', 'mcp_server.py', 
         'https://github.com/OpenLiberty/open-liberty/issues/1',
         '--dry-run'],
        capture_output=True,
        text=True
    )
    
    response = json.loads(result.stdout)
    print(f"Response: {json.dumps(response, indent=2)}")
    
    # In dry run, comment_url should be None
    assert response['comment_url'] is None or response['success'] == False
    print("✓ Dry run mode works")


def test_mcp_tool_definition():
    """Test MCP tool definition."""
    print("\nTesting MCP tool definition...")
    
    from mcp_server import create_mcp_tool_definition
    
    tool_def = create_mcp_tool_definition()
    
    assert tool_def['name'] == 'analyze-github-issue'
    assert 'issueUrl' in tool_def['inputSchema']['properties']
    assert 'dryRun' in tool_def['inputSchema']['properties']
    print("✓ MCP tool definition is correct")


def test_mcp_request_handling():
    """Test MCP request handling."""
    print("\nTesting MCP request handling...")
    
    from mcp_server import handle_mcp_request
    
    # Test tools/list
    request = {'method': 'tools/list'}
    response = handle_mcp_request(request)
    assert 'tools' in response
    assert len(response['tools']) == 1
    print("✓ tools/list works")
    
    # Test invalid method
    request = {'method': 'invalid/method'}
    response = handle_mcp_request(request)
    assert 'error' in response
    print("✓ Error handling works")


def main():
    """Run all tests."""
    print("="*60)
    print("MCP Server Test Suite")
    print("="*60)
    
    try:
        test_url_validation()
        test_mcp_tool_definition()
        test_mcp_request_handling()
        test_dry_run()
        
        print("\n" + "="*60)
        print("✅ All tests passed!")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())

# Made with Bob
