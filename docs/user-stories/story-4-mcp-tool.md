# User Story 4: Simple MCP Tool Implementation

## Story Details

**ID**: US-004  
**Title**: Implement single MCP tool that orchestrates the workflow  
**Priority**: P0 (Critical)  
**Estimate**: 1 hour  
**Assigned To**: Developer 2 (Integration Lead)

---

## User Story

**As a** Bob MCP Server developer  
**I need to** create one MCP tool that executes the entire workflow  
**So that** users can trigger analysis with a single command

---

## Acceptance Criteria

### AC1: Tool Definition
**Given** the MCP tool specification  
**When** the tool is registered with Bob  
**Then** the tool has:
- Name: `analyze-github-issue`
- Description: "Analyzes a GitHub issue, identifies Liberty packages, generates diagram, and posts results"
- Single parameter: `issueUrl` (required, string)
- Clear usage examples

**Example Tool Definition**:
```json
{
  "name": "analyze-github-issue",
  "description": "Analyzes a GitHub issue, identifies Liberty packages, generates architecture diagram, and posts analysis as a comment",
  "inputSchema": {
    "type": "object",
    "properties": {
      "issueUrl": {
        "type": "string",
        "description": "Full URL of the GitHub issue to analyze",
        "pattern": "^https://github\\.com/[^/]+/[^/]+/issues/\\d+$"
      }
    },
    "required": ["issueUrl"]
  }
}
```

### AC2: Workflow Orchestration
**Given** a valid issue URL  
**When** the tool executes  
**Then** the tool orchestrates these steps in order:
1. Validate URL format
2. Fetch issue from GitHub
3. Analyze packages
4. Generate diagram
5. Post comment to GitHub
6. Return success status

### AC3: Progress Feedback
**Given** the tool is executing  
**When** each step completes  
**Then** the tool provides progress updates:

```
🔍 Fetching issue from GitHub...
✓ Issue #12345 fetched: "NullPointerException in JWT token validation"

🔎 Identifying Liberty packages...
✓ Found 2 packages

📊 Generating architecture diagram...
✓ Diagram generated

📝 Posting analysis to GitHub...
✓ Comment posted: https://github.com/.../issues/12345#comment-789
✓ Label added: bot-analyzed

✅ Analysis complete in 8.3 seconds!
```

### AC4: Error Handling at Each Step
**Given** an error occurs at any step  
**When** the tool handles the error  
**Then** the tool:
- Stops execution at the failed step
- Returns partial results if available
- Provides clear error message
- Suggests remediation action
- Does not crash

**Example Error Response**:
```json
{
  "success": false,
  "step": "fetch-issue",
  "error": "Issue not found or not accessible",
  "suggestion": "Verify the issue URL and ensure you have access",
  "partialResults": null
}
```

### AC5: Success Response
**Given** all steps complete successfully  
**When** the tool returns results  
**Then** the response includes:
- Success status
- Issue summary
- Package count
- Diagram preview (first 5 lines)
- Comment URL
- Execution time

**Example Success Response**:
```json
{
  "success": true,
  "issue": {
    "number": 12345,
    "title": "NullPointerException in JWT token validation"
  },
  "packagesFound": 2,
  "diagramGenerated": true,
  "commentUrl": "https://github.com/.../issues/12345#comment-789",
  "executionTimeMs": 8300
}
```

### AC6: Timeout Handling
**Given** the tool execution exceeds 30 seconds  
**When** the timeout is reached  
**Then** the tool:
- Cancels remaining operations
- Returns timeout error
- Includes partial results
- Logs timeout details

### AC7: Concurrent Execution
**Given** multiple users invoke the tool simultaneously  
**When** both executions target different issues  
**Then** both executions complete successfully without interference

**Given** multiple users invoke the tool for the same issue  
**When** both executions run concurrently  
**Then** the tool:
- Queues the second request
- Or allows both to run (second updates first's comment)
- Handles race conditions gracefully

### AC8: Dry Run Mode
**Given** the tool is invoked with `dryRun: true` parameter  
**When** the tool executes  
**Then** the tool:
- Performs all analysis steps
- Does NOT post to GitHub
- Returns what would have been posted
- Useful for testing

### AC9: Validation
**Given** invalid input parameters  
**When** the tool is invoked  
**Then** the tool validates and returns errors:

| Invalid Input | Error Message |
|---------------|---------------|
| Empty URL | "Issue URL is required" |
| Invalid URL format | "Invalid GitHub issue URL format" |
| Non-GitHub URL | "URL must be a GitHub issue" |
| Missing issue number | "Issue number not found in URL" |

### AC10: Logging
**Given** the tool executes  
**When** operations occur  
**Then** the tool logs:
- Tool invocation with parameters
- Each step start and completion
- Errors with stack traces
- Performance metrics
- Final result

---

## Technical Implementation

### Components to Implement

1. **MCPTool.java**
   ```java
   public class MCPTool {
       private final GitHubClient githubClient;
       private final PackageAnalyzer packageAnalyzer;
       private final DiagramGenerator diagramGenerator;
       private final CommentPoster commentPoster;
       
       public AnalysisResult analyzeIssue(String issueUrl);
       public AnalysisResult analyzeIssue(String issueUrl, boolean dryRun);
       private void validateUrl(String url);
       private void logProgress(String message);
       private void handleStepError(String step, Exception e);
   }
   ```

2. **WorkflowOrchestrator.java**
   ```java
   public class WorkflowOrchestrator {
       private final List<WorkflowStep> steps;
       
       public AnalysisResult execute(String issueUrl);
       private void executeStep(WorkflowStep step);
       private void handleTimeout();
       private AnalysisResult createPartialResult(int completedSteps);
   }
   ```

3. **Data Models**
   ```java
   public class AnalysisResult {
       private boolean success;
       private Issue issue;
       private List<Package> packages;
       private String diagram;
       private String commentUrl;
       private long executionTimeMs;
       private String errorMessage;
       private String failedStep;
   }
   
   public interface WorkflowStep {
       String getName();
       void execute(WorkflowContext context);
       void rollback(WorkflowContext context);
   }
   ```

---

## Test Cases

### Test Case 1: Successful End-to-End
```java
@Test
void testAnalyzeIssue_ValidUrl_Success() {
    String url = "https://github.com/OpenLiberty/open-liberty/issues/12345";
    
    AnalysisResult result = mcpTool.analyzeIssue(url);
    
    assertTrue(result.isSuccess());
    assertNotNull(result.getCommentUrl());
    assertTrue(result.getExecutionTimeMs() < 30000);
}
```

### Test Case 2: Invalid URL
```java
@Test
void testAnalyzeIssue_InvalidUrl_ReturnsError() {
    String url = "not-a-valid-url";
    
    AnalysisResult result = mcpTool.analyzeIssue(url);
    
    assertFalse(result.isSuccess());
    assertEquals("validate-url", result.getFailedStep());
    assertTrue(result.getErrorMessage().contains("Invalid"));
}
```

### Test Case 3: Fetch Failure
```java
@Test
void testAnalyzeIssue_FetchFails_ReturnsPartialResult() {
    when(githubClient.fetchIssue(anyString()))
        .thenThrow(new GitHubApiException("404 Not Found"));
    
    AnalysisResult result = mcpTool.analyzeIssue(validUrl);
    
    assertFalse(result.isSuccess());
    assertEquals("fetch-issue", result.getFailedStep());
    assertNull(result.getPackages());
}
```

### Test Case 4: Progress Feedback
```java
@Test
void testAnalyzeIssue_ExecutesSteps_LogsProgress() {
    mcpTool.analyzeIssue(validUrl);
    
    verify(logger).info(contains("Fetching issue"));
    verify(logger).info(contains("Identifying packages"));
    verify(logger).info(contains("Generating diagram"));
    verify(logger).info(contains("Posting analysis"));
}
```

### Test Case 5: Timeout
```java
@Test
void testAnalyzeIssue_Timeout_ReturnsError() {
    // Mock slow operation
    when(githubClient.fetchIssue(anyString()))
        .thenAnswer(inv -> {
            Thread.sleep(35000);
            return new Issue();
        });
    
    AnalysisResult result = mcpTool.analyzeIssue(validUrl);
    
    assertFalse(result.isSuccess());
    assertTrue(result.getErrorMessage().contains("timeout"));
}
```

### Test Case 6: Dry Run Mode
```java
@Test
void testAnalyzeIssue_DryRun_DoesNotPost() {
    AnalysisResult result = mcpTool.analyzeIssue(validUrl, true);
    
    assertTrue(result.isSuccess());
    assertNotNull(result.getDiagram());
    verify(commentPoster, never()).postAnalysis(any(), any());
}
```

### Test Case 7: Concurrent Execution
```java
@Test
void testAnalyzeIssue_ConcurrentCalls_BothSucceed() {
    String url1 = "https://github.com/OpenLiberty/open-liberty/issues/1";
    String url2 = "https://github.com/OpenLiberty/open-liberty/issues/2";
    
    CompletableFuture<AnalysisResult> future1 = 
        CompletableFuture.supplyAsync(() -> mcpTool.analyzeIssue(url1));
    CompletableFuture<AnalysisResult> future2 = 
        CompletableFuture.supplyAsync(() -> mcpTool.analyzeIssue(url2));
    
    AnalysisResult result1 = future1.join();
    AnalysisResult result2 = future2.join();
    
    assertTrue(result1.isSuccess());
    assertTrue(result2.isSuccess());
}
```

### Test Case 8: Partial Failure
```java
@Test
void testAnalyzeIssue_DiagramFails_PostsWithoutDiagram() {
    when(diagramGenerator.generateDiagram(any(), any()))
        .thenThrow(new DiagramException("Mermaid syntax error"));
    
    AnalysisResult result = mcpTool.analyzeIssue(validUrl);
    
    assertTrue(result.isSuccess()); // Still posts comment
    assertNull(result.getDiagram());
    verify(commentPoster).postAnalysis(any(), any());
}
```

---

## Workflow Steps

### Step 1: Validate URL
```java
public class ValidateUrlStep implements WorkflowStep {
    @Override
    public void execute(WorkflowContext context) {
        String url = context.getIssueUrl();
        if (!isValidGitHubIssueUrl(url)) {
            throw new ValidationException("Invalid GitHub issue URL");
        }
        context.logProgress("✓ URL validated");
    }
}
```

### Step 2: Fetch Issue
```java
public class FetchIssueStep implements WorkflowStep {
    @Override
    public void execute(WorkflowContext context) {
        context.logProgress("🔍 Fetching issue from GitHub...");
        Issue issue = githubClient.fetchIssue(context.getIssueUrl());
        context.setIssue(issue);
        context.logProgress("✓ Issue #" + issue.getNumber() + " fetched");
    }
}
```

### Step 3: Analyze Packages
```java
public class AnalyzePackagesStep implements WorkflowStep {
    @Override
    public void execute(WorkflowContext context) {
        context.logProgress("🔎 Identifying Liberty packages...");
        List<Package> packages = packageAnalyzer.analyzePackages(
            context.getIssue().getBody()
        );
        context.setPackages(packages);
        context.logProgress("✓ Found " + packages.size() + " packages");
    }
}
```

### Step 4: Generate Diagram
```java
public class GenerateDiagramStep implements WorkflowStep {
    @Override
    public void execute(WorkflowContext context) {
        context.logProgress("📊 Generating architecture diagram...");
        String diagram = diagramGenerator.generateDiagram(
            context.getPackages(),
            context.getIssue()
        );
        context.setDiagram(diagram);
        context.logProgress("✓ Diagram generated");
    }
}
```

### Step 5: Post Comment
```java
public class PostCommentStep implements WorkflowStep {
    @Override
    public void execute(WorkflowContext context) {
        if (context.isDryRun()) {
            context.logProgress("🔍 Dry run mode - skipping post");
            return;
        }
        
        context.logProgress("📝 Posting analysis to GitHub...");
        CommentResult result = commentPoster.postAnalysis(
            context.getIssueUrl(),
            context.getAnalysisResult()
        );
        context.setCommentUrl(result.getCommentUrl());
        context.logProgress("✓ Comment posted: " + result.getCommentUrl());
    }
}
```

---

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| GitHub API down | Return error after retry, don't crash |
| Very large issue (>1MB) | Process first 100KB, log warning |
| Issue with 1000+ comments | Efficiently find existing Bob comment |
| Network interruption mid-execution | Retry failed step once |
| Invalid GitHub token | Return auth error immediately |
| Rate limit exceeded | Return error with reset time |
| Malformed issue data | Handle gracefully, return error |
| Tool invoked without parameters | Return validation error |

---

## Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| Total execution time | <15s | Start to finish |
| URL validation | <10ms | Regex check |
| Issue fetch | <3s | API call |
| Package analysis | <1s | Regex processing |
| Diagram generation | <1s | String manipulation |
| Comment posting | <5s | API call |
| Timeout threshold | 30s | Hard limit |

---

## Definition of Done

- [ ] MCPTool implemented and tested
- [ ] WorkflowOrchestrator implemented
- [ ] All workflow steps implemented
- [ ] All acceptance criteria met
- [ ] Unit tests passing (>80% coverage)
- [ ] Integration tests passing
- [ ] Error handling robust
- [ ] Progress feedback working
- [ ] Performance targets met
- [ ] Code reviewed and approved
- [ ] Documentation updated
- [ ] MCP tool registered with Bob

---

## Dependencies

- Story 1 (US-001) must be complete
- Story 2 (US-002) must be complete
- Story 3 (US-003) must be complete
- MCP server framework
- Bob integration

---

## Demo Scenario

```
User: "Bob, analyze this issue: 
       https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: [Invokes analyze-github-issue tool]

     🔍 Fetching issue from GitHub...
     ✓ Issue #12345 fetched: "NullPointerException in JWT token validation"
     
     🔎 Identifying Liberty packages...
     ✓ Found 2 packages
     
     📊 Generating architecture diagram...
     ✓ Diagram generated
     
     📝 Posting analysis to GitHub...
     ✓ Comment posted: https://github.com/.../issues/12345#comment-789
     ✓ Label added: bot-analyzed
     
     ✅ Analysis complete in 8.3 seconds!
     
     View the full analysis at: 
     https://github.com/OpenLiberty/open-liberty/issues/12345#comment-789
```

---

## MCP Tool Registration

```java
@MCPTool(
    name = "analyze-github-issue",
    description = "Analyzes a GitHub issue, identifies Liberty packages, " +
                  "generates architecture diagram, and posts analysis as a comment"
)
public class AnalyzeGitHubIssueTool {
    
    @MCPParameter(
        name = "issueUrl",
        description = "Full URL of the GitHub issue to analyze",
        required = true,
        pattern = "^https://github\\.com/[^/]+/[^/]+/issues/\\d+$"
    )
    private String issueUrl;
    
    @MCPParameter(
        name = "dryRun",
        description = "If true, performs analysis but does not post to GitHub",
        required = false,
        defaultValue = "false"
    )
    private boolean dryRun;
    
    @Override
    public AnalysisResult execute() {
        return mcpTool.analyzeIssue(issueUrl, dryRun);
    }
}
```

---

## Monitoring & Metrics

### Key Metrics to Track
- Total executions
- Success rate
- Average execution time
- Failure rate by step
- Most common errors
- API call counts
- Cache hit rate

### Logging Format
```
[2026-03-17 12:00:00] INFO  MCPTool - Tool invoked: analyze-github-issue
[2026-03-17 12:00:00] INFO  MCPTool - Parameter: issueUrl=https://github.com/.../12345
[2026-03-17 12:00:01] INFO  MCPTool - Step 1/5: Validate URL - COMPLETE
[2026-03-17 12:00:03] INFO  MCPTool - Step 2/5: Fetch Issue - COMPLETE
[2026-03-17 12:00:04] INFO  MCPTool - Step 3/5: Analyze Packages - COMPLETE (2 found)
[2026-03-17 12:00:05] INFO  MCPTool - Step 4/5: Generate Diagram - COMPLETE
[2026-03-17 12:00:08] INFO  MCPTool - Step 5/5: Post Comment - COMPLETE
[2026-03-17 12:00:08] INFO  MCPTool - Analysis complete in 8300ms
```

---

## Notes

- This is the glue that ties everything together
- Must be rock-solid and provide excellent UX
- Progress feedback is critical for user confidence
- Error messages must be actionable
- Consider adding telemetry for post-hackathon analysis
- Future: Support for batch analysis of multiple issues