# Demo Script - GitHub Issue Context Analyzer

## Pre-Demo Setup (5 minutes before)

### Environment Check
```bash
# Verify repository is up to date
cd /path/to/Bobathon-2026
git pull origin main

# Check GitHub token is set
echo $GITHUB_TOKEN

# Verify Bob is running
bob --version

# Test with a simple issue
bob analyze-github-issue --url "https://github.com/OpenLiberty/open-liberty/issues/TEST"
```

### Test Issues Prepared
1. **Simple Issue**: Single package mention
2. **Complex Issue**: Multiple packages with relationships
3. **Edge Case**: No package mentions

### Backup Materials
- Screenshots of successful runs
- Pre-generated diagrams
- Video recording of working demo

---

## Demo Flow (10 minutes)

### Introduction (1 minute)

**Script**:
> "Hi everyone! Today we're demonstrating Bob's GitHub Issue Context Analyzer - a tool that automatically analyzes Liberty issues, identifies affected packages, generates architecture diagrams, and posts the analysis back to GitHub. All in one command."

**Show**: Title slide with project overview

---

### Problem Statement (1 minute)

**Script**:
> "When investigating Liberty issues, developers spend time manually:
> - Reading through issue descriptions
> - Identifying which packages are affected
> - Understanding component relationships
> - Documenting their findings
> 
> Our tool automates this entire workflow."

**Show**: Example of a complex Liberty issue on screen

---

### Demo Part 1: Simple Analysis (3 minutes)

**Script**:
> "Let's start with a straightforward issue. I'll ask Bob to analyze issue #12345."

**Command**:
```bash
bob analyze-github-issue --url "https://github.com/OpenLiberty/open-liberty/issues/12345"
```

**Expected Output**:
```
🤖 Analyzing GitHub Issue #12345...

✓ Fetching issue from GitHub...
  Title: "NullPointerException in JWT token validation"
  
✓ Identifying Liberty packages...
  Found 2 packages:
  - io.openliberty.security.jwt (confidence: 95%)
  - com.ibm.ws.security.token (confidence: 87%)

✓ Generating architecture diagram...
  Created Mermaid component diagram

✓ Posting analysis to GitHub...
  Comment posted: https://github.com/OpenLiberty/open-liberty/issues/12345#comment-789

✅ Analysis complete in 8.3 seconds!
```

**Show**: 
1. Terminal output with progress
2. Navigate to GitHub issue
3. Show the posted comment with diagram

**Highlight**:
- Speed (< 10 seconds)
- Automatic package identification
- Visual diagram in comment

---

### Demo Part 2: Complex Analysis (3 minutes)

**Script**:
> "Now let's try a more complex issue with multiple packages and relationships."

**Command**:
```bash
bob analyze-github-issue --url "https://github.com/OpenLiberty/open-liberty/issues/23456"
```

**Expected Output**:
```
🤖 Analyzing GitHub Issue #23456...

✓ Fetching issue from GitHub...
  Title: "CDI integration with Jakarta Security fails"
  
✓ Identifying Liberty packages...
  Found 5 packages:
  - io.openliberty.security.jakartasec.3.0.internal
  - io.openliberty.cdi.4.0.internal
  - com.ibm.ws.security.authentication
  - com.ibm.ws.cdi.impl
  - io.openliberty.security.common.internal

✓ Analyzing relationships...
  - jakartasec depends on cdi
  - jakartasec depends on security.authentication
  - cdi.impl implements cdi

✓ Generating architecture diagram...
  Created Mermaid component diagram with 5 components

✓ Posting analysis to GitHub...
  Comment posted: https://github.com/OpenLiberty/open-liberty/issues/23456#comment-790
  Added label: bot-analyzed

✅ Analysis complete in 12.1 seconds!
```

**Show**:
1. Terminal output
2. GitHub comment with more complex diagram
3. Highlight the relationship arrows in diagram

**Highlight**:
- Handles multiple packages
- Shows component relationships
- Adds helpful labels

---

### Demo Part 3: Edge Case (1 minute)

**Script**:
> "What happens when an issue doesn't mention any packages? Let's see."

**Command**:
```bash
bob analyze-github-issue --url "https://github.com/OpenLiberty/open-liberty/issues/34567"
```

**Expected Output**:
```
🤖 Analyzing GitHub Issue #34567...

✓ Fetching issue from GitHub...
  Title: "Documentation update needed"
  
✓ Identifying Liberty packages...
  ⚠ No Liberty packages identified in issue description

✓ Posting analysis to GitHub...
  Comment posted with recommendation to add package information

✅ Analysis complete in 5.2 seconds!
```

**Show**: GitHub comment suggesting to add package information

**Highlight**:
- Graceful handling of edge cases
- Helpful suggestions to users

---

### Technical Deep Dive (1 minute)

**Script**:
> "Under the hood, this is powered by:
> - GitHub REST API for issue fetching
> - Regex-based package extraction
> - Mermaid diagram generation
> - MCP tool orchestration
> 
> All implemented in Java to align with the Liberty ecosystem."

**Show**: Quick code walkthrough (optional)
- `GitHubClient.java` - API integration
- `PackageAnalyzer.java` - Regex patterns
- `DiagramGenerator.java` - Mermaid templates
- `MCPTool.java` - Workflow orchestration

---

### Wrap-up & Q&A (2 minutes)

**Script**:
> "To summarize:
> - ✅ Automated issue analysis in seconds
> - ✅ Accurate package identification
> - ✅ Visual architecture diagrams
> - ✅ Automatic GitHub integration
> - ✅ Handles edge cases gracefully
> 
> This saves developers time and provides immediate context for issue investigation.
> 
> Questions?"

**Show**: Summary slide with metrics
- Speed: < 15 seconds
- Accuracy: 80%+ package identification
- Automation: Zero manual steps

---

## Backup Plans

### If Live Demo Fails

**Plan A**: Use pre-recorded video
```
"Let me show you a recording of the tool in action..."
```

**Plan B**: Use screenshots
```
"Here's what the output looks like when it works..."
```

**Plan C**: Walk through code
```
"Let me show you how it works under the hood..."
```

### If GitHub API is Down

**Plan A**: Use cached responses
```bash
bob analyze-github-issue --url "..." --use-cache
```

**Plan B**: Use mock data
```bash
bob analyze-github-issue --url "..." --mock-mode
```

---

## Q&A Preparation

### Expected Questions & Answers

**Q: How accurate is the package identification?**
> A: In our testing, we achieve 80%+ accuracy for packages explicitly mentioned in issue descriptions. We use regex patterns for `io.openliberty.*` and `com.ibm.ws.*` packages.

**Q: Can it handle private repositories?**
> A: Yes, as long as you provide a GitHub token with appropriate permissions via the `GITHUB_TOKEN` environment variable.

**Q: What if the issue is very large?**
> A: We limit diagram complexity to 5 packages for readability. Additional packages are listed in text format.

**Q: Does it work with other projects besides Liberty?**
> A: Currently optimized for Liberty packages, but the regex patterns can be easily adapted for other Java projects.

**Q: How does it determine package relationships?**
> A: For the MVP, we use simple heuristics based on package naming conventions and common patterns. Post-hackathon, we plan to add deeper analysis using Git history and code structure.

**Q: Can it analyze multiple issues at once?**
> A: Not in the MVP, but that's a great feature for future iterations!

**Q: What about rate limiting?**
> A: We use authenticated GitHub API requests which provide 5,000 requests per hour, more than sufficient for typical usage.

**Q: How long did this take to build?**
> A: This MVP was built in 3 hours during our hackathon by a team of 4 developers!

---

## Demo Checklist

### Before Demo
- [ ] GitHub token configured
- [ ] Test issues prepared and accessible
- [ ] Bob tool running and tested
- [ ] Backup materials ready
- [ ] Screen sharing tested
- [ ] Audio/video working

### During Demo
- [ ] Speak clearly and at moderate pace
- [ ] Show terminal output
- [ ] Navigate to GitHub to show results
- [ ] Highlight key features
- [ ] Handle questions confidently

### After Demo
- [ ] Thank the audience
- [ ] Share repository link
- [ ] Collect feedback
- [ ] Note improvement ideas

---

## Success Metrics

### Demo Success
- ✅ All 3 test cases run successfully
- ✅ Audience understands the value
- ✅ Questions answered satisfactorily
- ✅ Positive feedback received

### Technical Success
- ✅ Analysis completes in < 15 seconds
- ✅ Diagrams render correctly
- ✅ Comments post successfully
- ✅ No crashes or errors

---

## Post-Demo

### Immediate Actions
1. Share repository link with audience
2. Collect feedback and questions
3. Note feature requests
4. Thank the team

### Follow-up
1. Send demo recording to attendees
2. Create GitHub issues for feedback
3. Plan next iteration
4. Celebrate success! 🎉

---

**Remember**: Stay calm, speak clearly, and have fun! The audience wants you to succeed.

**Good luck! 🚀**