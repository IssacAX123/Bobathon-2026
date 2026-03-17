# Contributing to GitHub Issue Context Analyzer

Thank you for your interest in contributing to the Bobathon 2026 project! This guide will help you get started.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Workflow](#development-workflow)
3. [Code Standards](#code-standards)
4. [Testing Guidelines](#testing-guidelines)
5. [Commit Guidelines](#commit-guidelines)
6. [Pull Request Process](#pull-request-process)
7. [Team Communication](#team-communication)

---

## Getting Started

### Prerequisites

- Java 11 or higher
- Gradle 7.0+
- Git
- GitHub account with access to the repository
- GitHub Personal Access Token

### Initial Setup

```bash
# Clone the repository
git clone git@github.ibm.com:your-org/Bobathon-2026.git
cd Bobathon-2026

# Set up environment
export GITHUB_TOKEN="your_github_personal_access_token"

# Build the project
./gradlew build

# Run tests
./gradlew test

# Verify setup
./gradlew check
```

### IDE Setup

**IntelliJ IDEA**:
1. Open project as Gradle project
2. Enable annotation processing
3. Install Lombok plugin (if used)
4. Configure code style (see `.editorconfig`)

**Eclipse**:
1. Import as Gradle project
2. Install Buildship plugin
3. Configure Java 11+ compiler

---

## Development Workflow

### 1. Pick a Task

Check the project board or TIMELINE.md for available tasks:
- Hour 1 tasks: Core functionality
- Hour 2 tasks: Integration
- Hour 3 tasks: Polish and demo prep

### 2. Create a Branch

```bash
# Update main branch
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/your-feature-name

# Examples:
# feature/github-api-client
# feature/mermaid-generator
# fix/rate-limit-handling
# docs/api-documentation
```

### 3. Develop

- Write code following our standards (see below)
- Write tests for new functionality
- Update documentation as needed
- Commit frequently with clear messages

### 4. Test

```bash
# Run unit tests
./gradlew test

# Run specific test class
./gradlew test --tests GitHubClientTest

# Run integration tests
./gradlew integrationTest

# Check code coverage
./gradlew jacocoTestReport
```

### 5. Submit

```bash
# Push your branch
git push origin feature/your-feature-name

# Create pull request on GitHub
# Request review from team member
```

---

## Code Standards

### Java Style Guide

Follow standard Java conventions:

```java
// Class names: PascalCase
public class GitHubClient {
    
    // Constants: UPPER_SNAKE_CASE
    private static final String API_BASE_URL = "https://api.github.com";
    
    // Variables: camelCase
    private String authToken;
    
    // Methods: camelCase
    public Issue fetchIssue(String issueUrl) {
        // Implementation
    }
    
    // Private methods: camelCase with descriptive names
    private String buildApiUrl(String owner, String repo, int number) {
        return String.format("%s/repos/%s/%s/issues/%d", 
            API_BASE_URL, owner, repo, number);
    }
}
```

### Code Organization

```java
public class ExampleClass {
    // 1. Static constants
    private static final String CONSTANT = "value";
    
    // 2. Instance variables
    private String instanceVar;
    
    // 3. Constructors
    public ExampleClass() {
        // Constructor
    }
    
    // 4. Public methods
    public void publicMethod() {
        // Implementation
    }
    
    // 5. Private methods
    private void privateMethod() {
        // Implementation
    }
    
    // 6. Inner classes (if needed)
    private static class InnerClass {
        // Implementation
    }
}
```

### Documentation

```java
/**
 * Fetches a GitHub issue by URL.
 * 
 * @param issueUrl The full URL of the GitHub issue
 * @return Issue object containing issue details
 * @throws GitHubApiException if the API call fails
 * @throws IllegalArgumentException if the URL is invalid
 */
public Issue fetchIssue(String issueUrl) {
    // Implementation
}
```

### Error Handling

```java
// Good: Specific exceptions with context
public Issue fetchIssue(String issueUrl) {
    try {
        validateUrl(issueUrl);
        Response response = makeApiCall(issueUrl);
        return parseResponse(response);
    } catch (IOException e) {
        throw new GitHubApiException(
            "Failed to fetch issue: " + issueUrl, e);
    }
}

// Bad: Swallowing exceptions
public Issue fetchIssue(String issueUrl) {
    try {
        // ...
    } catch (Exception e) {
        return null;  // Don't do this!
    }
}
```

### Logging

```java
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class GitHubClient {
    private static final Logger logger = 
        LoggerFactory.getLogger(GitHubClient.class);
    
    public Issue fetchIssue(String issueUrl) {
        logger.info("Fetching issue: {}", issueUrl);
        
        try {
            Issue issue = doFetch(issueUrl);
            logger.debug("Successfully fetched issue #{}", issue.getNumber());
            return issue;
        } catch (Exception e) {
            logger.error("Failed to fetch issue: {}", issueUrl, e);
            throw new GitHubApiException("Fetch failed", e);
        }
    }
}
```

---

## Testing Guidelines

### Unit Tests

```java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.*;

class GitHubClientTest {
    
    private GitHubClient client;
    private HttpClient mockHttpClient;
    
    @BeforeEach
    void setUp() {
        mockHttpClient = mock(HttpClient.class);
        client = new GitHubClient(mockHttpClient);
    }
    
    @Test
    void testFetchIssue_Success() {
        // Arrange
        String issueUrl = "https://github.com/owner/repo/issues/123";
        String mockResponse = "{\"number\":123,\"title\":\"Test\"}";
        when(mockHttpClient.get(anyString())).thenReturn(mockResponse);
        
        // Act
        Issue issue = client.fetchIssue(issueUrl);
        
        // Assert
        assertNotNull(issue);
        assertEquals(123, issue.getNumber());
        assertEquals("Test", issue.getTitle());
    }
    
    @Test
    void testFetchIssue_InvalidUrl() {
        // Arrange
        String invalidUrl = "not-a-url";
        
        // Act & Assert
        assertThrows(IllegalArgumentException.class, 
            () -> client.fetchIssue(invalidUrl));
    }
}
```

### Test Coverage Goals

- **Unit Tests**: 80%+ code coverage
- **Integration Tests**: Cover main workflows
- **Edge Cases**: Test error conditions

### Test Naming

```java
// Pattern: test[MethodName]_[Scenario]_[ExpectedResult]

@Test
void testFetchIssue_ValidUrl_ReturnsIssue() { }

@Test
void testFetchIssue_InvalidUrl_ThrowsException() { }

@Test
void testFetchIssue_RateLimitExceeded_RetriesOnce() { }
```

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Test additions or modifications
- `refactor`: Code refactoring
- `style`: Code style changes (formatting)
- `chore`: Build process or auxiliary tool changes

### Examples

```bash
# Good commit messages
git commit -m "feat(github): implement issue fetching with authentication"
git commit -m "fix(analyzer): handle packages with numeric suffixes"
git commit -m "docs(api): add GitHub API integration guide"
git commit -m "test(diagram): add edge case tests for empty package list"

# Bad commit messages
git commit -m "fixed stuff"
git commit -m "WIP"
git commit -m "updates"
```

### Commit Frequency

- Commit after completing a logical unit of work
- Don't commit broken code
- Commit before switching tasks
- Aim for 5-10 commits per feature

---

## Pull Request Process

### Before Creating PR

1. **Update from main**:
   ```bash
   git checkout main
   git pull origin main
   git checkout feature/your-feature
   git rebase main
   ```

2. **Run all tests**:
   ```bash
   ./gradlew clean test
   ```

3. **Check code style**:
   ```bash
   ./gradlew checkstyleMain checkstyleTest
   ```

### Creating PR

1. Push your branch to GitHub
2. Create pull request with clear title and description
3. Link to related issues or user stories
4. Request review from appropriate team member

### PR Template

```markdown
## Description
Brief description of changes

## Related Issues
- Closes #123
- Related to #456

## Changes Made
- Added GitHub API client
- Implemented authentication
- Added unit tests

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] No breaking changes
```

### Review Process

**As Author**:
- Respond to feedback promptly
- Make requested changes
- Re-request review after updates

**As Reviewer**:
- Review within 30 minutes (hackathon pace)
- Check code quality, tests, documentation
- Provide constructive feedback
- Approve when satisfied

### Merging

- Squash commits if many small commits
- Use merge commit for feature branches
- Delete branch after merge

---

## Team Communication

### Channels

- **Slack**: #bobathon-2026-team (async updates)
- **Zoom**: Team room (sync meetings)
- **GitHub**: Issues and PRs (technical discussion)

### Daily Sync Points

During the 3-hour hackathon:
- **0:30**: Quick status check
- **1:00**: Hour 1 review
- **1:40**: Integration checkpoint
- **2:00**: Hour 2 review
- **2:30**: Demo dry run

### Communication Guidelines

- **Blockers**: Escalate immediately
- **Questions**: Ask in Slack, don't wait
- **Updates**: Post progress every 30 minutes
- **Help**: Offer assistance proactively

---

## Troubleshooting

### Common Issues

**Build Fails**:
```bash
# Clean and rebuild
./gradlew clean build --refresh-dependencies
```

**Tests Fail**:
```bash
# Run with more detail
./gradlew test --info

# Run specific test
./gradlew test --tests GitHubClientTest --info
```

**GitHub API Rate Limit**:
```bash
# Check rate limit status
curl -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/rate_limit
```

**Merge Conflicts**:
```bash
# Update from main
git checkout main
git pull origin main
git checkout feature/your-feature
git rebase main

# Resolve conflicts in files
# Then continue
git rebase --continue
```

---

## Resources

### Documentation
- [README.md](README.md) - Project overview
- [TEAM.md](TEAM.md) - Team structure
- [TIMELINE.md](TIMELINE.md) - Implementation timeline
- [docs/architecture/](docs/architecture/) - Architecture docs
- [docs/user-stories/](docs/user-stories/) - User stories

### External Resources
- [GitHub REST API](https://docs.github.com/en/rest)
- [Mermaid Documentation](https://mermaid-js.github.io/)
- [JUnit 5 Guide](https://junit.org/junit5/docs/current/user-guide/)
- [Mockito Documentation](https://javadoc.io/doc/org.mockito/mockito-core/latest/org/mockito/Mockito.html)

---

## Questions?

If you have questions:
1. Check this guide and other documentation
2. Ask in Slack #bobathon-2026-team
3. Reach out to your team lead
4. Create a GitHub issue for discussion

---

**Thank you for contributing! Let's build something amazing together! 🚀**