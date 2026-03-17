#!/bin/bash
# Complete Pipeline: Stories 1 → 2 → 3
# Analyzes GitHub issue and posts comprehensive analysis as comment

set -e  # Exit on error

echo "╔══════════════════════════════════════════════════════════════════════════════╗"
echo "║              BOBATHON 2026: COMPLETE ANALYSIS PIPELINE                       ║"
echo "║                    Stories 1 → 2 → 3                                         ║"
echo "╚══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Parse arguments
DRY_RUN=false
ISSUE_URL=""

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        *)
            ISSUE_URL="$1"
            shift
            ;;
    esac
done

# Check if issue URL provided
if [ -z "$ISSUE_URL" ]; then
    echo "Usage: $0 [--dry-run] <github_issue_url>"
    echo ""
    echo "Options:"
    echo "  --dry-run    Preview comment without posting to GitHub"
    echo ""
    echo "Example:"
    echo "  $0 https://github.com/OpenLiberty/open-liberty/issues/12345"
    echo "  $0 --dry-run https://github.com/OpenLiberty/open-liberty/issues/12345"
    echo ""
    echo "Requirements:"
    echo "  - GITHUB_TOKEN environment variable must be set (not needed for --dry-run)"
    echo "  - Token must have 'repo' or 'public_repo' scope"
    exit 1
fi

# Check for GitHub token (not needed for dry-run)
if [ "$DRY_RUN" = false ] && [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set"
    echo ""
    echo "To set your token:"
    echo "  export GITHUB_TOKEN='your_token_here'"
    echo ""
    echo "To create a token:"
    echo "  1. Go to GitHub Settings → Developer settings → Personal access tokens"
    echo "  2. Generate new token with 'repo' scope"
    echo ""
    echo "Or use --dry-run to preview without posting"
    exit 1
fi

if [ "$DRY_RUN" = true ]; then
    echo "🔍 DRY RUN MODE: Will preview comment without posting"
    echo ""
fi

echo "📋 Step 1: Analyzing GitHub Issue"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Create temp files
TEMP_ANALYSIS=$(mktemp)
TEMP_DIAGRAM=$(mktemp)

# Run Story 1: Analyze issue
python github_issue_analyzer.py --json-only "$ISSUE_URL" > "$TEMP_ANALYSIS" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error analyzing issue:"
    cat "$TEMP_ANALYSIS"
    rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
    exit 1
fi

echo "✅ Analysis complete!"
echo ""

echo "📊 Step 2: Generating Component Diagram"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Story 2: Generate diagram
python diagram_generator.py "$TEMP_ANALYSIS" > "$TEMP_DIAGRAM" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error generating diagram:"
    cat "$TEMP_DIAGRAM"
    rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
    exit 1
fi

echo "✅ Diagram generated!"
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "🔍 Step 3: Previewing Comment (DRY RUN - will not post to GitHub)"
else
    echo "💬 Step 3: Posting Comprehensive Analysis to GitHub"
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Run Story 3: Post comment (or preview if dry-run)
if [ "$DRY_RUN" = true ]; then
    python comment_poster.py "$ISSUE_URL" "$TEMP_ANALYSIS" "$TEMP_DIAGRAM" --dry-run
else
    python comment_poster.py "$ISSUE_URL" "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
fi

if [ $? -ne 0 ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "❌ Error previewing comment"
    else
        echo "❌ Error posting comment"
    fi
    rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
    exit 1
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ "$DRY_RUN" = true ]; then
    echo "✅ DRY RUN complete!"
else
    echo "✅ Pipeline complete!"
fi
echo ""
echo "📝 Summary:"
echo "  - Issue analyzed"
echo "  - Packages identified"
echo "  - Diagram generated"
if [ "$DRY_RUN" = true ]; then
    echo "  - Comment previewed (not posted to GitHub)"
else
    echo "  - Comprehensive analysis posted to GitHub"
    echo "  - Label 'bot-analyzed' added"
fi
echo ""
if [ "$DRY_RUN" = true ]; then
    echo "Next steps:"
    echo "  1. Review the preview output above"
    echo "  2. If satisfied, run without --dry-run to post to GitHub:"
    echo "     $0 $ISSUE_URL"
else
    echo "🔗 View the analysis at: $ISSUE_URL"
fi
echo ""

# Cleanup
rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"

# Made with Bob
