# MVP User Stories: GitHub Issue Context Analyzer (3-Hour Hackathon)

## Epic: Minimal Viable Demo - Issue Context Analyzer

**Goal**: Demonstrate Bob's ability to fetch a GitHub issue, analyze affected Liberty packages, and post a formatted technical analysis comment - all in one automated workflow.

---

## Story 1: Fetch and Analyze GitHub Issue

**Title**: Fetch GitHub issue and identify affected Liberty packages

**As a** Liberty developer  
**I need to** provide a GitHub issue URL and get automatic package identification  
**So that** I can quickly understand which components are involved

### Acceptance Criteria

- ✅ Tool accepts GitHub issue URL as input parameter
- ✅ Fetches issue title and description via GitHub API
- ✅ Parses description for package names (regex: `io.openliberty.*`, `com.ibm.ws.*`)
- ✅ Returns list of identified packages with confidence scores
- ✅ Handles authentication via GitHub token from environment variable
- ✅ Returns error message for invalid URLs or inaccessible issues
- ✅ Completes analysis in under 10 seconds

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Issue description contains no package names | Return "No packages identified" |
| GitHub API rate limit exceeded | Return cached result or error |
| Invalid issue URL format | Return validation error |
| Private repository without proper token | Return auth error |

### Demo Value
Shows Bob can integrate with external APIs and parse technical content

---

## Story 2: Generate Simple Component Diagram

**Title**: Create basic Mermaid diagram showing package relationships

**As a** developer investigating an issue  
**I need to** see a visual diagram of identified packages  
**So that** I can understand component relationships at a glance

### Acceptance Criteria

- ✅ Generates Mermaid component diagram for identified packages
- ✅ Shows up to 5 packages to keep diagram readable
- ✅ Includes basic relationships (depends-on, implements)
- ✅ Diagram syntax is valid and renders in GitHub markdown
- ✅ Includes title with issue number
- ✅ Handles case where no packages are found (returns text explanation)
- ✅ Diagram fits within 50 lines of Mermaid code

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Only one package identified | Show standalone component |
| Circular dependencies detected | Show with bidirectional arrows |
| No clear relationships found | Show packages as separate components |

### Demo Value
Showcases Bob's ability to generate visual content programmatically

---

## Story 3: Post Analysis as GitHub Comment

**Title**: Publish formatted analysis as issue comment

**As a** developer  
**I need to** have the analysis automatically posted to the GitHub issue  
**So that** the entire team can see the context without running tools

### Acceptance Criteria

- ✅ Posts formatted markdown comment to the specified issue
- ✅ Comment includes: issue summary, identified packages, Mermaid diagram
- ✅ Adds "bot-analyzed" label to issue
- ✅ Comment has clear header: "🤖 Automated Analysis by Bob"
- ✅ Includes timestamp and analysis version
- ✅ Handles permission errors gracefully (log error, don't crash)
- ✅ Updates existing comment if re-run on same issue

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| User lacks comment permission | Return error message |
| Issue is locked | Return appropriate error |
| Comment exceeds size limit | Truncate with "see full analysis" link |
| Network failure during post | Retry once, then fail gracefully |

### Demo Value
Demonstrates end-to-end automation and GitHub integration

---

## Story 4: Simple MCP Tool Implementation

**Title**: Implement single MCP tool that orchestrates the workflow

**As a** Bob MCP Server developer  
**I need to** create one MCP tool that executes the entire workflow  
**So that** users can trigger analysis with a single command

### Acceptance Criteria

- ✅ Tool named `analyze-github-issue` with single parameter: `issueUrl`
- ✅ Tool orchestrates: fetch → analyze → diagram → post
- ✅ Returns success/failure status with summary
- ✅ Follows MCP tool specification format
- ✅ Includes clear description and parameter documentation
- ✅ Handles errors at each step without crashing
- ✅ Provides progress feedback (e.g., "Fetching issue...", "Generating diagram...")

### Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Step fails mid-workflow | Return partial results with error |
| Multiple simultaneous calls to same issue | Queue or reject duplicate |
| Tool timeout after 30 seconds | Return timeout error |

### Demo Value
Shows Bob's MCP architecture and tool composition

---

## Implementation Priority (3-Hour Timeline)

### Hour 1: Core Functionality
- GitHub API integration (fetch issue)
- Basic package name extraction (regex parsing)
- Simple data structures for results

### Hour 2: Diagram Generation
- Mermaid syntax generation
- Basic component relationship logic
- Format validation

### Hour 3: GitHub Integration & Polish
- Post comment functionality
- Error handling
- Demo script and test cases

---

## Demo Script

```
User: "Bob, analyze this issue: https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Executes analyze-github-issue tool]
     "Fetching issue #12345..."
     "Identified 3 Liberty packages..."
     "Generating architecture diagram..."
     "Posting analysis to issue..."
     "✅ Analysis complete! View at: [issue URL]"

[GitHub issue now has formatted comment with diagram]
```

---

## Success Metrics for Demo

| Metric | Target |
|--------|--------|
| **Speed** | Complete analysis in under 15 seconds |
| **Accuracy** | Correctly identify at least 80% of mentioned packages |
| **Visual Impact** | Diagram renders properly in GitHub |
| **Reliability** | Handle 3 different test issues without errors |
| **Wow Factor** | Audience sees value immediately |

---

## Out of Scope (Post-Hackathon)

- ❌ Deep package structure analysis
- ❌ Git history mining
- ❌ Design rationale extraction
- ❌ Multi-issue pattern analysis
- ❌ Advanced caching
- ❌ Comprehensive error recovery
- ❌ Custom templates
- ❌ Performance optimization beyond basic needs

---

## Technical Stack (Recommended)

- **Language**: Java (matches Liberty ecosystem)
- **GitHub API**: OkHttp or GitHub Java SDK
- **Mermaid**: String template generation
- **MCP**: Standard MCP Java implementation
- **Testing**: JUnit with mock GitHub responses

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| GitHub API rate limits | Use authenticated requests (5000/hour vs 60/hour) |
| Complex package relationships | Start with simple "mentioned in issue" relationships |
| Mermaid syntax errors | Use tested templates, validate before posting |
| Demo environment issues | Pre-test with 3 real Liberty issues, have screenshots as backup |