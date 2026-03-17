# Team Structure & Responsibilities

## Team Overview

**Project**: GitHub Issue Context Analyzer  
**Duration**: 3-hour hackathon  
**Team Size**: 4 developers  
**Goal**: Working MVP with live demo

---

## Team Members & Roles

### 👨‍💻 Developer 1: Backend Lead
**Name**: [Your Name]  
**Primary Focus**: GitHub API Integration & Package Analysis

#### Responsibilities
- Implement `GitHubClient.java` for API integration
- Build `PackageAnalyzer.java` for regex-based package extraction
- Handle authentication and rate limiting
- Create data models for issue and package information
- Write unit tests for API client

#### Deliverables (Hour 1)
- ✅ Working GitHub API client
- ✅ Package name extraction (regex for `io.openliberty.*`, `com.ibm.ws.*`)
- ✅ Basic error handling
- ✅ Unit tests with mock responses

#### Key Files
- `src/main/java/com/ibm/liberty/analyzer/GitHubClient.java`
- `src/main/java/com/ibm/liberty/analyzer/PackageAnalyzer.java`
- `src/main/java/com/ibm/liberty/analyzer/model/Issue.java`
- `src/main/java/com/ibm/liberty/analyzer/model/Package.java`

---

### 🎨 Developer 2: Integration Lead
**Name**: [Your Name]  
**Primary Focus**: Mermaid Generation & MCP Tool Orchestration

#### Responsibilities
- Implement `DiagramGenerator.java` for Mermaid syntax
- Build `MCPTool.java` to orchestrate workflow
- Create component relationship logic
- Validate Mermaid syntax
- Integrate all components

#### Deliverables (Hour 2)
- ✅ Mermaid diagram generation
- ✅ Component relationship mapping
- ✅ MCP tool implementation
- ✅ End-to-end workflow orchestration

#### Key Files
- `src/main/java/com/ibm/liberty/analyzer/DiagramGenerator.java`
- `src/main/java/com/ibm/liberty/analyzer/MCPTool.java`
- `src/main/java/com/ibm/liberty/analyzer/RelationshipMapper.java`
- `docs/api/mcp-tool-spec.md`

---

### 🧪 Developer 3: Testing Lead
**Name**: [Your Name]  
**Primary Focus**: Test Coverage & Error Handling

#### Responsibilities
- Write comprehensive unit tests
- Implement `CommentPoster.java` with error handling
- Create integration tests
- Test edge cases and failure scenarios
- Document test coverage

#### Deliverables (Hour 3)
- ✅ Unit tests for all components
- ✅ Integration tests for workflow
- ✅ Error handling implementation
- ✅ Test documentation

#### Key Files
- `src/test/java/com/ibm/liberty/analyzer/GitHubClientTest.java`
- `src/test/java/com/ibm/liberty/analyzer/PackageAnalyzerTest.java`
- `src/test/java/com/ibm/liberty/analyzer/DiagramGeneratorTest.java`
- `src/test/java/com/ibm/liberty/analyzer/IntegrationTest.java`
- `src/main/java/com/ibm/liberty/analyzer/CommentPoster.java`

---

### 📚 Developer 4: Demo Lead
**Name**: [Your Name]  
**Primary Focus**: Documentation & Demo Preparation

#### Responsibilities
- Create comprehensive documentation
- Prepare demo script and test issues
- Set up demo environment
- Create presentation materials
- Handle demo execution

#### Deliverables (Throughout)
- ✅ Complete documentation
- ✅ Demo script with 3 test issues
- ✅ Presentation slides
- ✅ Backup screenshots/videos

#### Key Files
- `docs/DEMO_SCRIPT.md`
- `docs/architecture/system-overview.md`
- `docs/api/github-api-integration.md`
- `docs/api/mermaid-generation.md`
- `.github/workflows/ci.yml`

---

## Collaboration Guidelines

### Communication
- **Slack Channel**: #bobathon-2026-team
- **Stand-ups**: Every 30 minutes (quick sync)
- **Code Reviews**: Pair review before merge
- **Blockers**: Escalate immediately

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Commit frequently with clear messages
git commit -m "feat: implement GitHub API client"

# Push and create PR
git push origin feature/your-feature-name

# Request review from team member
```

### Branch Naming Convention
- `feature/github-api` - New features
- `fix/rate-limit-handling` - Bug fixes
- `docs/api-documentation` - Documentation
- `test/integration-tests` - Test additions

### Commit Message Format
```
<type>: <description>

Types:
- feat: New feature
- fix: Bug fix
- docs: Documentation
- test: Test additions
- refactor: Code refactoring
```

---

## Hour-by-Hour Coordination

### Hour 1 (0:00 - 1:00)
**Focus**: Core Backend Functionality

| Developer | Tasks |
|-----------|-------|
| Dev 1 | GitHub API + Package extraction |
| Dev 2 | Design MCP tool interface |
| Dev 3 | Set up test framework |
| Dev 4 | Create documentation structure |

**Sync Point**: 0:30 - Quick status check

---

### Hour 2 (1:00 - 2:00)
**Focus**: Integration & Diagram Generation

| Developer | Tasks |
|-----------|-------|
| Dev 1 | Finalize API client, support Dev 2 |
| Dev 2 | Mermaid generation + MCP orchestration |
| Dev 3 | Unit tests for completed components |
| Dev 4 | API documentation + demo prep |

**Sync Point**: 1:30 - Integration checkpoint

---

### Hour 3 (2:00 - 3:00)
**Focus**: Polish & Demo Preparation

| Developer | Tasks |
|-----------|-------|
| Dev 1 | Code review + bug fixes |
| Dev 2 | Final integration + error handling |
| Dev 3 | Comment posting + integration tests |
| Dev 4 | Demo script + presentation |

**Sync Point**: 2:30 - Demo dry run

---

## Success Criteria

### Individual Success
- ✅ All assigned components completed
- ✅ Unit tests passing
- ✅ Code reviewed and merged
- ✅ Documentation complete

### Team Success
- ✅ End-to-end workflow functional
- ✅ Demo runs smoothly
- ✅ All acceptance criteria met
- ✅ Wow factor achieved

---

## Emergency Protocols

### If Behind Schedule
1. **Prioritize**: Focus on core demo path
2. **Simplify**: Cut non-essential features
3. **Parallelize**: Redistribute tasks
4. **Backup Plan**: Use screenshots if live demo fails

### If Ahead of Schedule
1. **Polish**: Improve error messages
2. **Enhance**: Add confidence scores
3. **Document**: Expand documentation
4. **Test**: Add more edge cases

---

## Contact Information

| Developer | Role | Email | Slack |
|-----------|------|-------|-------|
| Dev 1 | Backend Lead | dev1@ibm.com | @dev1 |
| Dev 2 | Integration Lead | dev2@ibm.com | @dev2 |
| Dev 3 | Testing Lead | dev3@ibm.com | @dev3 |
| Dev 4 | Demo Lead | dev4@ibm.com | @dev4 |

---

## Post-Hackathon

### Immediate Follow-up
- Code cleanup and refactoring
- Comprehensive documentation
- Performance optimization
- Security review

### Future Enhancements
- Deep package structure analysis
- Git history mining
- Multi-issue pattern analysis
- Custom templates
- Advanced caching

---

**Remember**: Communication is key! Don't hesitate to ask for help or offer assistance to teammates.

**Good luck, team! Let's build something amazing! 🚀**