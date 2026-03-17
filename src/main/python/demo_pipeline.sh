#!/bin/bash
# Demo: Complete Story 1 → Story 2 Pipeline
# Shows how to analyze a GitHub issue and generate a diagram

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║                    BOBATHON 2026: STORY 1 → STORY 2 DEMO                    ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Check if issue URL provided
if [ $# -eq 0 ]; then
    echo "Usage: $0 <github_issue_url>"
    echo ""
    echo "Example:"
    echo "  $0 https://github.com/OpenLiberty/open-liberty/issues/12345"
    echo ""
    echo "Note: For GitHub Enterprise, set GITHUB_TOKEN environment variable"
    exit 1
fi

ISSUE_URL="$1"

echo "📋 Step 1: Analyzing GitHub Issue"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Story 1 with --json-only flag and save to temp file
TEMP_JSON=$(mktemp)
python github_issue_analyzer.py --json-only "$ISSUE_URL" > "$TEMP_JSON" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error analyzing issue:"
    cat "$TEMP_JSON"
    rm "$TEMP_JSON"
    exit 1
fi

echo "✅ Analysis complete! JSON saved to: $TEMP_JSON"
echo ""

echo "📊 Step 2: Generating Component Diagram"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Story 2 with the JSON output
python diagram_generator.py "$TEMP_JSON"

if [ $? -ne 0 ]; then
    echo "❌ Error generating diagram"
    rm "$TEMP_JSON"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Pipeline complete!"
echo ""
echo "💡 Tip: Copy the Mermaid diagram above and paste it into:"
echo "   - GitHub issue comment"
echo "   - README.md file"
echo "   - Mermaid Live Editor: https://mermaid.live"
echo ""

# Cleanup
rm "$TEMP_JSON"

# Made with Bob
