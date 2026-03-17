# User Story 1: Fetch and Analyze GitHub Issue

## Story Details

**ID**: US-001  
**Title**: Fetch GitHub issue and identify affected Liberty packages  
**Priority**: P0 (Critical)  
**Estimate**: 1 hour  
**Assigned To**: Developer 1 (Backend Lead)

---

## User Story

**As a** Liberty developer  
**I need to** provide a GitHub issue URL and get automatic package identification  
**So that** I can quickly understand which components are involved without manual analysis

---

## Acceptance Criteria

### AC1: URL Validation
**Given** a user provides an issue URL  
**When** the URL format is valid (matches GitHub issue pattern)  
**Then** the system accepts the URL and proceeds with fetching  

**Given** a user provides an invalid URL  
**When** the URL format is incorrect  
**Then** the system returns a clear error message: "Invalid GitHub issue URL format"

### AC2: Issue Fetching
**Given** a valid GitHub issue URL  
**When** the system fetches the issue via GitHub API  
**Then** the system retrieves:
- Issue number
- Issue title
- Issue description/body
- Issue labels
- Issue creation date

**Given** the issue does not exist (404)  
**When** the system attempts to fetch  
**Then** the system returns: "Issue not found or not accessible"

### AC3: Authentication
**Given** a GitHub token is set in environment variable `GITHUB_TOKEN`  
**When** the system makes API calls  
**Then** the system uses authenticated requests (5000 req/hour limit)

**Given** no GitHub token is provided  
**When** the system makes API calls  
**Then** the system uses unauthenticated requests (60 req/hour limit) and logs a warning

**Given** an invalid or expired token  
**When** the system attempts authentication  
**Then** the system returns: "Authentication failed. Please check your GitHub token"

### AC4: Package Identification
**Given** an issue description containing Liberty package names  
**When** the system analyzes the text  
**Then** the system identifies packages matching patterns:
- `io.openliberty.*` (Liberty packages)
- `com.ibm.ws.*` (WebSphere packages)

**Example**:
```
Input: "NullPointerException in io.openliberty.security.jwt when validating tokens"
Output: 
- Package: io.openliberty.security.jwt
- Confidence: 95%
```

### AC5: Confidence Scoring
**Given** identified package names  
**When** the system calculates confidence scores  
**Then** the system assigns scores based on:
- Exact package name match: 95-100%
- Package name with context keywords: 85-94%
- Package name without context: 70-84%
- Partial package name: 50-69%

### AC6: Multiple Package Handling
**Given** an issue mentions multiple packages  
**When** the system analyzes the text  
**Then** the system returns all identified packages with individual confidence scores

**Example**:
```
Input: "CDI integration with Jakarta Security fails in 
        io.openliberty.security.jakartasec.3.0.internal 
        when calling com.ibm.ws.security.authentication"
Output:
- io.openliberty.security.jakartasec.3.0.internal (confidence: 95%)
- com.ibm.ws.security.authentication (confidence: 92%)
```

### AC7: No Packages Found
**Given** an issue description with no package mentions  
**When** the system analyzes the text  
**Then** the system returns:
- Empty package list
- Message: "No Liberty packages identified in issue description"
- Suggestion: "Consider adding package names to help with analysis"

### AC8: Performance
**Given** any valid issue URL  
**When** the system fetches and analyzes the issue  
**Then** the operation completes in less than 10 seconds

### AC9: Error Handling
**Given** the GitHub API is unavailable  
**When** the system attempts to fetch an issue  
**Then** the system:
- Retries once after 2 seconds
- Returns error message if retry fails
- Does not crash or hang

**Given** a rate limit is exceeded  
**When** the system makes an API call  
**Then** the system:
- Returns error: "GitHub API rate limit exceeded. Try again in X minutes"
- Logs the rate limit reset time

---

## Technical Implementation

### Components to Implement

1. **GitHubClient.java**
   ```java
   public class GitHubClient {
       private final OkHttpClient httpClient;
       private final String authToken;
       
       public Issue fetchIssue(String issueUrl);
       private String authenticate();
       private void handleRateLimit(Response response);
   }
   ```

2. **PackageAnalyzer.java**
   ```java
   public class PackageAnalyzer {
       private static final Pattern LIBERTY_PATTERN = 
           Pattern.compile("io\\.openliberty\\.[a-z0-9.]+");
       private static final Pattern IBM_PATTERN = 
           Pattern.compile("com\\.ibm\\.ws\\.[a-z0-9.]+");
       
       public List<Package> analyzePackages(String issueText);
       private double calculateConfidence(String pkg, String context);
   }
   ```

3. **Data Models**
   ```java
   public class Issue {
       private int number;
       private String title;
       private String body;
       private List<String> labels;
       private String url;
       private Date createdAt;
   }
   
   public class Package {
       private String name;
       private double confidence;
       private String context;
       private PackageType type; // LIBERTY, IBM, UNKNOWN
   }
   ```

---

## Test Cases

### Test Case 1: Valid Issue with Single Package
```java
@Test
void testFetchIssue_ValidUrl_SinglePackage() {
    String url = "https://github.com/OpenLiberty/open-liberty/issues/12345";
    Issue issue = githubClient.fetchIssue(url);
    List<Package> packages = packageAnalyzer.analyzePackages(issue.getBody());
    
    assertEquals(1, packages.size());
    assertEquals("io.openliberty.security.jwt", packages.get(0).getName());
    assertTrue(packages.get(0).getConfidence() > 0.90);
}
```

### Test Case 2: Invalid URL Format
```java
@Test
void testFetchIssue_InvalidUrl_ThrowsException() {
    String url = "not-a-valid-url";
    
    assertThrows(IllegalArgumentException.class, 
        () -> githubClient.fetchIssue(url));
}
```

### Test Case 3: Issue Not Found
```java
@Test
void testFetchIssue_NotFound_ThrowsException() {
    String url = "https://github.com/OpenLiberty/open-liberty/issues/999999";
    
    assertThrows(GitHubApiException.class, 
        () -> githubClient.fetchIssue(url));
}
```

### Test Case 4: Multiple Packages
```java
@Test
void testAnalyzePackages_MultiplePackages() {
    String text = "Issue in io.openliberty.cdi and com.ibm.ws.security";
    List<Package> packages = packageAnalyzer.analyzePackages(text);
    
    assertEquals(2, packages.size());
    assertTrue(packages.stream()
        .anyMatch(p -> p.getName().equals("io.openliberty.cdi")));
    assertTrue(packages.stream()
        .anyMatch(p -> p.getName().equals("com.ibm.ws.security")));
}
```

### Test Case 5: No Packages Found
```java
@Test
void testAnalyzePackages_NoPackages() {
    String text = "This is a documentation update";
    List<Package> packages = packageAnalyzer.analyzePackages(text);
    
    assertTrue(packages.isEmpty());
}
```

### Test Case 6: Rate Limit Handling
```java
@Test
void testFetchIssue_RateLimitExceeded() {
    // Mock rate limit response
    mockWebServer.enqueue(new MockResponse()
        .setResponseCode(403)
        .setHeader("X-RateLimit-Remaining", "0"));
    
    assertThrows(RateLimitException.class, 
        () -> githubClient.fetchIssue(validUrl));
}
```

---

## Edge Cases

| Scenario | Expected Behavior |
|----------|-------------------|
| Issue body is empty | Return empty package list with message |
| Issue body is very large (>100KB) | Process first 50KB only, log warning |
| Package name has typo | Lower confidence score (50-70%) |
| Package name in code block | Identify with high confidence (90%+) |
| Package name in URL | Identify with medium confidence (70-80%) |
| Private repository | Return auth error if no token provided |
| Network timeout | Retry once, then fail with timeout error |
| Malformed JSON response | Return parsing error with details |

---

## Definition of Done

- [ ] GitHubClient implemented and tested
- [ ] PackageAnalyzer implemented and tested
- [ ] All acceptance criteria met
- [ ] Unit tests passing (>80% coverage)
- [ ] Edge cases handled
- [ ] Error messages are clear and actionable
- [ ] Performance target met (<10 seconds)
- [ ] Code reviewed and approved
- [ ] Documentation updated

---

## Dependencies

- OkHttp library for HTTP client
- Jackson for JSON parsing
- JUnit 5 for testing
- Mockito for mocking

---

## Demo Scenario

```
User: "Bob, analyze this issue: 
       https://github.com/OpenLiberty/open-liberty/issues/12345"

Bob: "Fetching issue #12345..."
     "Issue: NullPointerException in JWT token validation"
     "Identified 2 Liberty packages:"
     "  - io.openliberty.security.jwt (confidence: 95%)"
     "  - com.ibm.ws.security.token (confidence: 87%)"
     "Analysis complete in 3.2 seconds"
```

---

## Notes

- This is the foundation for the entire workflow
- Must be rock-solid and fast
- Error handling is critical for demo success
- Consider caching for repeated requests during demo