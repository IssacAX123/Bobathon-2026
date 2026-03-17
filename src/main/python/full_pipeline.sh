#!/bin/bash
# Complete Pipeline: Stories 1 → 2 → 3
# Analyzes GitHub issue and posts comprehensive analysis as comment

set -e  # Exit on error

# Redirect all echo statements to stderr so only markdown goes to stdout in dry-run
echo "╔══════════════════════════════════════════════════════════════════════════════╗" >&2
echo "║              BOBATHON 2026: COMPLETE ANALYSIS PIPELINE                       ║" >&2
echo "║                    Stories 1 → 2 → 3                                         ║" >&2
echo "╚══════════════════════════════════════════════════════════════════════════════╝" >&2
echo "" >&2

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
    echo "Usage: $0 [--dry-run] <github_issue_url>" >&2
    echo "" >&2
    echo "Options:" >&2
    echo "  --dry-run    Preview comment without posting to GitHub" >&2
    echo "" >&2
    echo "Example:" >&2
    echo "  $0 https://github.com/OpenLiberty/open-liberty/issues/12345" >&2
    echo "  $0 --dry-run https://github.com/OpenLiberty/open-liberty/issues/12345" >&2
    echo "" >&2
    echo "Requirements:" >&2
    echo "  - GITHUB_TOKEN environment variable must be set (not needed for --dry-run)" >&2
    echo "  - Token must have 'repo' or 'public_repo' scope" >&2
    exit 1
fi

# Check for GitHub token (not needed for dry-run)
if [ "$DRY_RUN" = false ] && [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ Error: GITHUB_TOKEN environment variable not set" >&2
    echo "" >&2
    echo "To set your token:" >&2
    echo "  export GITHUB_TOKEN='your_token_here'" >&2
    echo "" >&2
    echo "To create a token:" >&2
    echo "  1. Go to GitHub Settings → Developer settings → Personal access tokens" >&2
    echo "  2. Generate new token with 'repo' scope" >&2
    echo "" >&2
    echo "Or use --dry-run to preview without posting" >&2
    exit 1
fi

if [ "$DRY_RUN" = true ]; then
    echo "🔍 DRY RUN MODE: Will preview comment without posting" >&2
    echo "" >&2
fi

echo "📋 Step 1: Analyzing GitHub Issue" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "" >&2

# Create temp files
TEMP_ANALYSIS=$(mktemp)
TEMP_DIAGRAM=$(mktemp)

# Run Story 1: Analyze issue
python github_issue_analyzer.py --json-only "$ISSUE_URL" > "$TEMP_ANALYSIS" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error analyzing issue:" >&2
    cat "$TEMP_ANALYSIS" >&2
    rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
    exit 1
fi

echo "✅ Analysis complete!" >&2
echo "" >&2

echo "📊 Step 2: Generating Component Diagram" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "" >&2

# Run Story 2: Generate diagram
python diagram_generator.py "$TEMP_ANALYSIS" > "$TEMP_DIAGRAM" 2>&1

if [ $? -ne 0 ]; then
    echo "❌ Error generating diagram:" >&2
    cat "$TEMP_DIAGRAM" >&2
    rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
    exit 1
fi

echo "✅ Diagram generated!" >&2
echo "" >&2

if [ "$DRY_RUN" = true ]; then
    echo "🔍 Step 3: Previewing Comment (DRY RUN - will not post to GitHub)" >&2
else
    echo "💬 Step 3: Posting Comprehensive Analysis to GitHub" >&2
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
echo "" >&2

# Run Story 3: Post comment (or preview if dry-run)
if [ "$DRY_RUN" = true ]; then
    python comment_poster.py "$ISSUE_URL" "$TEMP_ANALYSIS" "$TEMP_DIAGRAM" --dry-run
else
    python comment_poster.py "$ISSUE_URL" "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
fi

if [ $? -ne 0 ]; then
    if [ "$DRY_RUN" = true ]; then
        echo "❌ Error previewing comment" >&2
    else
        echo "❌ Error posting comment" >&2
    fi
    rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"
    exit 1
fi

echo "" >&2
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" >&2
if [ "$DRY_RUN" = true ]; then
    echo "✅ DRY RUN complete!" >&2
else
    echo "✅ Pipeline complete!" >&2
fi
echo "" >&2
echo "📝 Summary:" >&2
echo "  - Issue analyzed" >&2
echo "  - Packages identified" >&2
echo "  - Diagram generated" >&2
if [ "$DRY_RUN" = true ]; then
    echo "  - Comment previewed (not posted to GitHub)" >&2
else
    echo "  - Comprehensive analysis posted to GitHub" >&2
    echo "  - Label 'bot-analyzed' added" >&2
fi
echo "" >&2
if [ "$DRY_RUN" = true ]; then
    echo "Next steps:" >&2
    echo "  1. Review the preview output above" >&2
    echo "  2. If satisfied, run without --dry-run to post to GitHub:" >&2
    echo "     $0 $ISSUE_URL" >&2
else
    echo "🔗 View the analysis at: $ISSUE_URL" >&2
fi
echo "" >&2

# Cleanup
rm "$TEMP_ANALYSIS" "$TEMP_DIAGRAM"

# Made with Bob
