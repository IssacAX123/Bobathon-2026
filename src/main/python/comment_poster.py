#!/usr/bin/env python3
"""
Comment Poster - Story 3 Implementation
Posts comprehensive analysis as GitHub comments with integration points,
code changes, and test recommendations.
"""

import json
import requests
from typing import Optional, Dict, List
from dataclasses import dataclass
from datetime import datetime
from urllib.parse import urlparse


@dataclass
class CommentResult:
    """Result of posting a comment."""
    success: bool
    comment_url: Optional[str] = None
    error_message: Optional[str] = None
    comment_id: Optional[int] = None


class GitHubCommentPoster:
    """Posts comprehensive analysis comments to GitHub issues."""
    
    VERSION = "1.0.0"
    BOT_SIGNATURE = "🤖 Automated Analysis by Bob"
    
    def __init__(self, github_token: Optional[str] = None, dry_run: bool = False):
        """
        Initialize the comment poster.
        
        Args:
            github_token: GitHub personal access token (required for posting, not for dry-run)
            dry_run: If True, only preview comment without posting
        """
        import os
        self.dry_run = dry_run
        self.github_token = github_token or os.getenv('GITHUB_TOKEN')
        
        if not dry_run and not self.github_token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN environment variable.")
        
        if not dry_run:
            self.session = requests.Session()
            self.session.headers.update({
                'Authorization': f'token {self.github_token}',
                'Accept': 'application/vnd.github.v3+json'
            })
        else:
            self.session = None
    
    def post_analysis(
        self,
        issue_url: str,
        analysis_result: Dict,
        diagram: str,
        update_existing: bool = True
    ) -> CommentResult:
        """
        Post comprehensive analysis as GitHub comment.
        
        Args:
            issue_url: GitHub issue URL
            analysis_result: JSON from Story 1 (github_issue_analyzer.py)
            diagram: Mermaid diagram from Story 2 (diagram_generator.py)
            update_existing: If True, update existing Bob comment instead of creating new
            
        Returns:
            CommentResult with success status and comment URL
        """
        try:
            # Parse issue URL
            api_url, owner, repo, issue_number = self._parse_issue_url(issue_url)
            
            # Format comprehensive comment
            comment_body = self._format_comprehensive_comment(
                analysis_result,
                diagram,
                issue_number
            )
            
            # DRY RUN: Just print the markdown comment
            if self.dry_run:
                print(comment_body)
                return CommentResult(
                    success=True,
                    comment_url=issue_url,
                    comment_id=0
                )
            
            # Check for existing comment
            existing_comment_id = None
            if update_existing:
                existing_comment_id = self._find_existing_comment(api_url)
            
            # Post or update comment
            if existing_comment_id:
                result = self._update_comment(api_url, existing_comment_id, comment_body)
            else:
                result = self._create_comment(api_url, comment_body)
            
            # Add label
            if result.success:
                self._add_label(api_url, owner, repo, issue_number)
            
            return result
            
        except Exception as e:
            return CommentResult(
                success=False,
                error_message=f"Failed to post comment: {str(e)}"
            )
    
    def _parse_issue_url(self, issue_url: str) -> tuple:
        """Parse GitHub issue URL to get API endpoint."""
        parsed = urlparse(issue_url)
        path_parts = parsed.path.strip('/').split('/')
        
        if len(path_parts) != 4 or path_parts[2] != 'issues':
            raise ValueError("Invalid GitHub issue URL")
        
        owner, repo, _, issue_number = path_parts
        
        # Construct API URL
        if parsed.hostname == 'github.com':
            api_url = f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}'
        else:
            # GitHub Enterprise
            api_url = f'https://{parsed.hostname}/api/v3/repos/{owner}/{repo}/issues/{issue_number}'
        
        return api_url, owner, repo, issue_number
    
    def _format_comprehensive_comment(
        self,
        analysis_result: Dict,
        diagram: str,
        issue_number: str
    ) -> str:
        """Format comprehensive analysis comment with integration points and code changes."""
        issue = analysis_result.get('issue', {})
        packages = analysis_result.get('packages', [])
        
        # Build comment sections
        sections = []
        
        # Header
        sections.append(f"## {self.BOT_SIGNATURE}\n")
        sections.append(f"**Issue**: #{issue_number} - {issue.get('title', 'Unknown')}\n")
        
        # Architecture Context (NEW - verbose overview)
        sections.append(self._generate_architecture_context(packages, issue))
        
        # Identified Packages
        if packages:
            sections.append(f"### 📦 Identified Packages ({len(packages)})\n")
            for pkg in packages:
                sections.append(
                    f"- `{pkg['name']}` "
                    f"(confidence: {pkg['confidence']:.0%}, "
                    f"type: {pkg['package_type']})"
                )
            sections.append("")
        else:
            sections.append("### 📦 Identified Packages\n")
            sections.append("No Liberty packages automatically identified.\n")
        
        # Component Diagram
        if packages and diagram:
            sections.append("### 📊 Component Diagram\n")
            sections.append(diagram)
            sections.append("")
        
        # Integration Points (if packages found)
        if packages:
            sections.append(self._generate_integration_points(packages, issue))
        
        # Suggested Code Changes (if packages found)
        if packages:
            sections.append(self._generate_code_suggestions(packages, issue))
        
        # Manual Tests
        if packages:
            sections.append(self._generate_test_recommendations(packages, issue))
        
        # Validation Steps
        if packages:
            sections.append(self._generate_validation_steps(packages, issue))
        
        # Footer
        sections.append("---")
        sections.append(f"*Analysis generated at: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*")
        sections.append(f"*Version: {self.VERSION}*")
        sections.append(f"*Powered by Bob - Your AI Development Assistant*")
        
        return "\n".join(sections)
    
    def _generate_architecture_context(self, packages: List[Dict], issue: Dict) -> str:
        """Generate verbose architecture context section."""
        lines = ["### 🏗️ Architecture Context\n"]
        
        if not packages:
            lines.append("*No packages identified - manual analysis required.*\n")
            return "\n".join(lines)
        
        # Determine primary subsystem
        subsystems = self._group_by_subsystem(packages)
        primary_subsystem = list(subsystems.keys())[0] if subsystems else "Unknown"
        
        # Generate context based on subsystem
        issue_body = issue.get('body', '').lower()
        issue_title = issue.get('title', '').lower()
        combined_text = f"{issue_title} {issue_body}"
        
        lines.append("#### Overview\n")
        lines.append(f"This issue impacts the **{primary_subsystem}** subsystem within Open Liberty. ")
        
        # Subsystem-specific context
        if 'security' in primary_subsystem.lower():
            lines.append("The Security subsystem is responsible for authentication, authorization, and cryptographic operations. ")
            lines.append("It integrates with multiple Liberty features including LTPA tokens, JWT, SAML, and Jakarta Security.\n")
            
            lines.append("**Key Components:**")
            lines.append("- **Token Management**: LTPA token generation, validation, and propagation")
            lines.append("- **Cryptography**: AES/3DES encryption, key management, FIPS compliance")
            lines.append("- **Utilities**: CLI tools for key generation and token operations")
            lines.append("- **Integration**: WebSphere interoperability, SSO, distributed security\n")
            
        elif 'cdi' in primary_subsystem.lower():
            lines.append("The CDI subsystem provides dependency injection and contextual lifecycle management. ")
            lines.append("It's foundational for Jakarta EE and MicroProfile features.\n")
            
        elif 'jaxrs' in primary_subsystem.lower() or 'rest' in primary_subsystem.lower():
            lines.append("The JAX-RS subsystem handles RESTful web services. ")
            lines.append("It integrates with JSON-B, JSON-P, CDI, and security features.\n")
            
        elif 'jpa' in primary_subsystem.lower():
            lines.append("The JPA subsystem manages object-relational mapping and database persistence. ")
            lines.append("It integrates with transaction management, connection pooling, and CDI.\n")
            
        else:
            lines.append("This subsystem provides core functionality for Liberty applications.\n")
        
        # Architecture layers
        lines.append("#### Architectural Layers\n")
        lines.append("```mermaid")
        lines.append("graph TB")
        lines.append("    subgraph \"Application Layer\"")
        lines.append("        APP[User Application]")
        lines.append("    end")
        lines.append("    subgraph \"Liberty Runtime\"")
        lines.append("        API[Public API]")
        lines.append("        SPI[Service Provider Interface]")
        lines.append("        IMPL[Implementation]")
        lines.append("        INTERNAL[Internal Services]")
        lines.append("    end")
        lines.append("    subgraph \"Platform\"")
        lines.append("        OSGi[OSGi Framework]")
        lines.append("        JVM[Java Virtual Machine]")
        lines.append("    end")
        lines.append("    APP --> API")
        lines.append("    API --> SPI")
        lines.append("    SPI --> IMPL")
        lines.append("    IMPL --> INTERNAL")
        lines.append("    INTERNAL --> OSGi")
        lines.append("    OSGi --> JVM")
        
        # Highlight affected packages
        for pkg in packages[:3]:  # Top 3 packages
            pkg_name = pkg['name'].split('.')[-1]
            lines.append(f"    style {pkg_name.upper()} fill:#ff9,stroke:#333,stroke-width:2px")
        
        lines.append("```\n")
        
        # Data flow diagram
        lines.append("#### Request Flow\n")
        
        if 'security' in primary_subsystem.lower() and ('ltpa' in combined_text or 'token' in combined_text):
            lines.append("```mermaid")
            lines.append("sequenceDiagram")
            lines.append("    participant Client")
            lines.append("    participant Liberty")
            lines.append("    participant Security")
            lines.append("    participant Crypto")
            lines.append("    participant KeyStore")
            lines.append("    Client->>Liberty: HTTP Request + LTPA Cookie")
            lines.append("    Liberty->>Security: Authenticate Request")
            lines.append("    Security->>Crypto: Decrypt Token")
            lines.append("    Crypto->>KeyStore: Load Keys")
            lines.append("    KeyStore-->>Crypto: AES/3DES Keys")
            lines.append("    Crypto-->>Security: Decrypted Token Data")
            lines.append("    Security->>Security: Validate Token")
            lines.append("    Security-->>Liberty: Authentication Result")
            lines.append("    Liberty-->>Client: HTTP Response")
            lines.append("```\n")
            
        elif 'cdi' in primary_subsystem.lower():
            lines.append("```mermaid")
            lines.append("sequenceDiagram")
            lines.append("    participant App")
            lines.append("    participant CDI")
            lines.append("    participant Bean")
            lines.append("    participant Context")
            lines.append("    App->>CDI: Request Bean")
            lines.append("    CDI->>Context: Check Scope")
            lines.append("    Context->>Bean: Create/Retrieve Instance")
            lines.append("    Bean->>CDI: Inject Dependencies")
            lines.append("    CDI-->>App: Return Bean")
            lines.append("```\n")
            
        else:
            lines.append("*Request flow diagram varies by feature - see component diagram above.*\n")
        
        # Integration points summary
        lines.append("#### Integration Points\n")
        lines.append("This change may affect:")
        
        if 'security' in primary_subsystem.lower():
            lines.append("- **Authentication**: Login modules, identity stores, credential validation")
            lines.append("- **Authorization**: Role mapping, security constraints, method permissions")
            lines.append("- **SSO**: Cross-application authentication, token propagation")
            lines.append("- **Interoperability**: WebSphere Traditional, other Liberty servers")
            lines.append("- **Standards**: Jakarta Security, JAAS, OAuth 2.0, OpenID Connect\n")
        else:
            lines.append("- Feature interactions and dependencies")
            lines.append("- Configuration and server.xml elements")
            lines.append("- Runtime behavior and lifecycle management")
            lines.append("- API contracts and backward compatibility\n")
        
        return "\n".join(lines)
    
    def _generate_integration_points(self, packages: List[Dict], issue: Dict) -> str:
        """Generate detailed integration points with concept explanations."""
        lines = ["### 🎯 Integration Points & Technical Deep Dive\n"]
        
        # Group packages by subsystem
        subsystems = self._group_by_subsystem(packages)
        issue_body = issue.get('body', '').lower()
        issue_title = issue.get('title', '').lower()
        combined_text = f"{issue_title} {issue_body}"
        
        for subsystem, pkgs in subsystems.items():
            lines.append(f"#### {subsystem}\n")
            
            # Add subsystem-level concept explanation
            lines.extend(self._generate_subsystem_concepts(subsystem, combined_text))
            
            for pkg in pkgs:
                pkg_name = pkg['name']
                file_path = pkg_name.replace('.', '/') + '/'
                
                lines.append(f"**Package**: `{pkg_name}`")
                lines.append(f"- **Location**: `dev/{file_path}`")
                lines.append(f"- **Context**: {pkg.get('context', 'Core implementation')}")
                lines.append(f"- **Confidence**: {pkg['confidence']:.0%}\n")
                
                # Add detailed technical breakdown
                lines.extend(self._generate_package_details(pkg_name, combined_text))
                lines.append("")
        
        return "\n".join(lines)
    
    def _generate_subsystem_concepts(self, subsystem: str, issue_text: str) -> List[str]:
        """Generate concept explanations for subsystem."""
        lines = []
        
        if 'security' in subsystem.lower():
            lines.append("**Core Concepts:**\n")
            
            if 'ltpa' in issue_text or 'token' in issue_text:
                lines.append("**LTPA (Lightweight Third Party Authentication)**")
                lines.append("- **Purpose**: Enable Single Sign-On (SSO) across multiple Liberty servers")
                lines.append("- **Token Structure**: `[Encrypted Payload][RSA Signature]` → Base64 encoded")
                lines.append("- **Encryption**: AES-256 (FIPS) or 3DES (non-FIPS) for payload confidentiality")
                lines.append("- **Signing**: RSA-2048 with SHA-1 for integrity verification")
                lines.append("- **Key Distribution**: All servers must share identical `ltpa.keys` file\n")
                
                lines.append("**Token Lifecycle:**")
                lines.append("```")
                lines.append("1. User authenticates → Server A creates token")
                lines.append("2. Token encrypted with shared secret (AES-256)")
                lines.append("3. Encrypted payload hashed (SHA-1)")
                lines.append("4. Hash signed with RSA private key")
                lines.append("5. Token sent as cookie: LtpaToken2=...")
                lines.append("6. Server B receives token → verifies signature")
                lines.append("7. Server B decrypts payload → validates expiration")
                lines.append("8. User authenticated without re-login")
                lines.append("```\n")
            
            if 'jwt' in issue_text:
                lines.append("**JWT (JSON Web Token)**")
                lines.append("- **Structure**: `Header.Payload.Signature` (Base64URL encoded)")
                lines.append("- **Header**: Algorithm and token type")
                lines.append("- **Payload**: Claims (user info, expiration, issuer)")
                lines.append("- **Signature**: HMAC or RSA signature for verification")
                lines.append("- **Stateless**: No server-side session storage required\n")
        
        elif 'cdi' in subsystem.lower():
            lines.append("**Core Concepts:**\n")
            lines.append("**CDI (Contexts and Dependency Injection)**")
            lines.append("- **Purpose**: Manage bean lifecycle and dependencies")
            lines.append("- **Scopes**: @RequestScoped, @SessionScoped, @ApplicationScoped")
            lines.append("- **Injection**: @Inject for automatic dependency resolution")
            lines.append("- **Producers**: @Produces for custom bean creation")
            lines.append("- **Events**: Observer pattern for loose coupling\n")
        
        elif 'jaxrs' in subsystem.lower() or 'rest' in subsystem.lower():
            lines.append("**Core Concepts:**\n")
            lines.append("**JAX-RS (RESTful Web Services)**")
            lines.append("- **Resources**: @Path annotated classes")
            lines.append("- **HTTP Methods**: @GET, @POST, @PUT, @DELETE")
            lines.append("- **Content Negotiation**: @Produces, @Consumes")
            lines.append("- **Providers**: MessageBodyReader/Writer for serialization")
            lines.append("- **Filters/Interceptors**: Request/response processing\n")
        
        return lines
    
    def _generate_package_details(self, pkg_name: str, issue_text: str) -> List[str]:
        """Generate detailed technical information for specific package."""
        lines = []
        
        # Security/LTPA packages
        if 'crypto.ltpakeyutil' in pkg_name:
            lines.append("**Key Classes & Methods:**")
            lines.append("- `LTPACrypto.java`")
            lines.append("  - `encrypt(byte[] data, Key key)` - AES-256/3DES encryption")
            lines.append("  - `decrypt(byte[] data, Key key)` - Decrypt token payload")
            lines.append("  - `generateSharedKey()` - Create 32-byte (FIPS) or 24-byte secret")
            lines.append("  - `rsaKey()` - Generate 2048-bit RSA key pair")
            lines.append("- `LTPAKeyFileUtilityImpl.java`")
            lines.append("  - `createLTPAKeysFile()` - Generate and save ltpa.keys")
            lines.append("  - `loadLTPAKeys()` - Read and decrypt keys from file")
            lines.append("  - `KeyEncryptor` - Password-based key protection\n")
            
            lines.append("**File Format (ltpa.keys):**")
            lines.append("```properties")
            lines.append("com.ibm.websphere.ltpa.3DESKey=<base64-encrypted-shared-secret>")
            lines.append("com.ibm.websphere.ltpa.PrivateKey=<base64-encrypted-rsa-private>")
            lines.append("com.ibm.websphere.ltpa.PublicKey=<base64-rsa-public>")
            lines.append("com.ibm.websphere.ltpa.Realm=defaultRealm")
            lines.append("```\n")
            
            lines.append("**Why This Design?**")
            lines.append("- **Password Protection**: Keys encrypted at rest prevent unauthorized access if file is stolen")
            lines.append("- **SHA Hashing**: Derives encryption key from password (32 bytes FIPS, 24 bytes non-FIPS)")
            lines.append("- **Public Key Unencrypted**: Only used for verification, no confidentiality risk")
            lines.append("- **Base64 Encoding**: Makes binary keys safe for properties file format\n")
            
            lines.append("**Security Model:**")
            lines.append("```")
            lines.append("ltpa.keys file (on disk)")
            lines.append("  ├─ Encrypted shared secret (password-protected)")
            lines.append("  ├─ Encrypted private key (password-protected)")
            lines.append("  └─ Plain public key (not encrypted)")
            lines.append("         ↓ Liberty startup with correct password")
            lines.append("Liberty memory (runtime)")
            lines.append("  ├─ Decrypted shared secret (plaintext in memory)")
            lines.append("  ├─ Decrypted private key (plaintext in memory)")
            lines.append("  └─ Public key (plaintext in memory)")
            lines.append("```\n")
            
            lines.append("**Common Issues:**")
            lines.append("- ❌ **Wrong password**: Decryption fails, Liberty won't start properly")
            lines.append("- ❌ **Different keys on servers**: SSO breaks, tokens can't be validated")
            lines.append("- ❌ **Weak file permissions**: Private key exposure risk")
            lines.append("- ✅ **Solution**: Use `chmod 600 ltpa.keys` and verify password matches\n")
            
            lines.append("**Configuration Example:**")
            lines.append("```xml")
            lines.append("<server>")
            lines.append("  <ltpa keysFileName=\"${server.config.dir}/resources/security/ltpa.keys\"")
            lines.append("        keysPassword=\"{xor}Lz4sLCgwLTs=\" />")
            lines.append("</server>")
            lines.append("```\n")
        
        elif 'security.token.ltpa' in pkg_name:
            lines.append("**Key Classes & Methods:**")
            lines.append("- `LTPAToken2.java`")
            lines.append("  - `createToken(Subject subject)` - Generate new LTPA token")
            lines.append("  - `validateToken(byte[] tokenBytes)` - Verify and decrypt token")
            lines.append("  - `getExpiration()` - Check token validity period")
            lines.append("  - `sign()` - SHA-256 hash + RSA signature")
            lines.append("  - `encrypt()` - AES-256/3DES encryption of payload")
            lines.append("- `LTPAKeyInfoManager.java`")
            lines.append("  - `prepareLTPAKeyInfo()` - Load keys at server startup")
            lines.append("  - `loadLtpaKeysFile()` - Read and decrypt ltpa.keys")
            lines.append("  - `getSharedKey()` - Retrieve decrypted shared secret\n")
            
            lines.append("**Token Structure (Detailed):**")
            lines.append("```")
            lines.append("Plaintext Payload (40 bytes):")
            lines.append("┌────────────────────────────────────────┐")
            lines.append("│ user=alice|exp=1709726400|realm=def... │")
            lines.append("└────────────────────────────────────────┘")
            lines.append("         ↓ AES-256 Encryption")
            lines.append("Encrypted (48 bytes with padding):")
            lines.append("┌────────────────────────────────────────┐")
            lines.append("│ 8f3a9b2c7d1e4f5a6b8c9d0e1f2a3b4c...   │")
            lines.append("└────────────────────────────────────────┘")
            lines.append("         ↓ SHA-1 Hash")
            lines.append("Hash (20 bytes):")
            lines.append("┌────────────────────────────────────────┐")
            lines.append("│ a7f3c9d2e1b4f8a6c3d9e2f1b5a8c4d7...   │")
            lines.append("└────────────────────────────────────────┘")
            lines.append("         ↓ RSA Sign")
            lines.append("Signature (128 bytes for RSA-1024):")
            lines.append("┌────────────────────────────────────────┐")
            lines.append("│ 4d7e1f8a2b5c3d6e9f0a1b2c3d4e5f6a...   │")
            lines.append("└────────────────────────────────────────┘")
            lines.append("         ↓ Concatenate")
            lines.append("Final Token (176 bytes):")
            lines.append("┌────────────────────────────────────────┐")
            lines.append("│ [Encrypted 48][Signature 128]          │")
            lines.append("└────────────────────────────────────────┘")
            lines.append("         ↓ Base64 Encode")
            lines.append("LtpaToken2=j6ObLH0eT1pric0OHyo7TF1u...")
            lines.append("```\n")
            
            lines.append("**Token Creation Flow:**")
            lines.append("```")
            lines.append("1. User authenticates → Subject created")
            lines.append("2. Serialize user data (username, expiration, realm)")
            lines.append("3. Encrypt with shared secret (AES-256)")
            lines.append("4. Hash encrypted payload (SHA-1)")
            lines.append("5. Sign hash with RSA private key")
            lines.append("6. Concatenate: [encrypted][signature]")
            lines.append("7. Base64 encode → Set as LtpaToken2 cookie")
            lines.append("```\n")
            
            lines.append("**Token Validation Flow:**")
            lines.append("```")
            lines.append("1. Receive LtpaToken2 cookie")
            lines.append("2. Base64 decode → Split [encrypted][signature]")
            lines.append("3. Hash encrypted portion (SHA-1)")
            lines.append("4. Verify signature with RSA public key")
            lines.append("5. If valid → Decrypt with shared secret")
            lines.append("6. Check expiration time")
            lines.append("7. Reconstruct Subject → User authenticated")
            lines.append("```\n")
            
            lines.append("**Why Both Encryption AND Signing?**")
            lines.append("- **Encryption alone (AES):**")
            lines.append("  - ❌ Can be tampered with (attacker modifies encrypted data)")
            lines.append("  - ✅ Provides confidentiality")
            lines.append("- **Signing alone (RSA):**")
            lines.append("  - ❌ Data visible to eavesdroppers")
            lines.append("  - ✅ Provides integrity")
            lines.append("- **Both together:**")
            lines.append("  - ✅ Confidentiality (encryption)")
            lines.append("  - ✅ Integrity (signature)")
            lines.append("  - ✅ Tamper-proof SSO tokens\n")
            
            lines.append("**Why Hash Before Signing?**")
            lines.append("- RSA can only sign data smaller than key size (256 bytes for RSA-2048)")
            lines.append("- SHA-1 creates fixed 20-byte hash regardless of payload size")
            lines.append("- More efficient than signing entire encrypted payload")
            lines.append("- Standard practice in digital signatures (PKCS#1)\n")
            
            lines.append("**Common Issues:**")
            lines.append("- ❌ **Token expired**: Check server clocks are synchronized (NTP)")
            lines.append("- ❌ **Signature verification fails**: Different keys on servers")
            lines.append("- ❌ **Decryption fails**: Corrupted token or wrong shared secret")
            lines.append("- ✅ **Default expiration**: 120 minutes (configurable in server.xml)\n")
        
        elif 'security.utility' in pkg_name:
            lines.append("**Key Classes & Methods:**")
            lines.append("- `CreateLTPAKeysTask.java`")
            lines.append("  - `handleTask()` - CLI entry point for key generation")
            lines.append("  - `validateOptions()` - Check --password and --file args")
            lines.append("  - `execute()` - Call LTPAKeyFileUtility\n")
            
            lines.append("**Command Usage:**")
            lines.append("```bash")
            lines.append("# Generate new keys")
            lines.append("securityUtility createLTPAKeys --password=myPassword --file=ltpa.keys")
            lines.append("")
            lines.append("# Distribute to all servers")
            lines.append("scp ltpa.keys serverA:/path/to/security/")
            lines.append("scp ltpa.keys serverB:/path/to/security/")
            lines.append("scp ltpa.keys serverC:/path/to/security/")
            lines.append("")
            lines.append("# Protect the file")
            lines.append("chmod 600 ltpa.keys")
            lines.append("chown liberty:liberty ltpa.keys")
            lines.append("```\n")
            
            lines.append("**Key Generation Process:**")
            lines.append("```")
            lines.append("Phase 1: Password Processing")
            lines.append("  password → SHA-256 hash → First 32 bytes = encryption key")
            lines.append("")
            lines.append("Phase 2: Generate Keys")
            lines.append("  - RSA KeyPairGenerator → 2048-bit public/private pair")
            lines.append("  - SecureRandom → 32-byte (FIPS) or 24-byte shared secret")
            lines.append("")
            lines.append("Phase 3: Encrypt Keys")
            lines.append("  - Shared secret → AES-256 encrypt → Base64 encode")
            lines.append("  - Private key → AES-256 encrypt → Base64 encode")
            lines.append("  - Public key → Base64 encode (no encryption)")
            lines.append("")
            lines.append("Phase 4: Write to File")
            lines.append("  - Save as Java properties format")
            lines.append("  - Add metadata (creation date, host, realm)")
            lines.append("```\n")
            
            lines.append("**Generated Keys:**")
            lines.append("- **Shared Secret**: 32 bytes (FIPS) or 24 bytes (non-FIPS)")
            lines.append("- **RSA Key Pair**: 2048-bit public/private keys")
            lines.append("- **Password Protection**: Keys encrypted before storage")
            lines.append("- **Distribution**: Copy ltpa.keys to all SSO servers\n")
            
            lines.append("**Why Generate Keys This Way?**")
            lines.append("- **Secure Random**: Cryptographically strong random number generator")
            lines.append("- **2048-bit RSA**: Industry standard, balances security and performance")
            lines.append("- **Password-based encryption**: Protects keys at rest without HSM")
            lines.append("- **Properties format**: Easy to read, edit, and version control\n")
            
            lines.append("**Common Issues:**")
            lines.append("- ❌ **Weak password**: Use strong password (16+ chars, mixed case, symbols)")
            lines.append("- ❌ **Lost password**: No recovery possible, must regenerate keys")
            lines.append("- ❌ **Keys not distributed**: SSO breaks between servers")
            lines.append("- ✅ **Best practice**: Store password in secure vault, automate distribution\n")
        
        # CDI packages
        elif 'cdi' in pkg_name.lower():
            lines.append("**Key Classes & Methods:**")
            lines.append("- CDI Extension classes for bean discovery")
            lines.append("- BeanManager for programmatic bean lookup")
            lines.append("- Context implementations for scope management")
            lines.append("- Interceptor/Decorator support\n")
        
        # JAX-RS packages
        elif 'jaxrs' in pkg_name.lower():
            lines.append("**Key Classes & Methods:**")
            lines.append("- Resource class scanning and registration")
            lines.append("- Provider discovery (MessageBodyReader/Writer)")
            lines.append("- Filter/Interceptor chain execution")
            lines.append("- Exception mapping\n")
        
        return lines
    
    def _generate_code_suggestions(self, packages: List[Dict], issue: Dict) -> str:
        """Generate suggested code changes based on issue content."""
        lines = ["### 💻 Suggested Code Changes\n"]
        
        issue_body = issue.get('body', '').lower()
        issue_title = issue.get('title', '').lower()
        combined_text = f"{issue_title} {issue_body}"
        
        # Detect issue type and provide relevant suggestions
        if 'pqc' in combined_text or 'post-quantum' in combined_text:
            lines.append(self._pqc_code_suggestions())
        elif 'jwt' in combined_text:
            lines.append(self._jwt_code_suggestions())
        elif 'nullpointer' in combined_text or 'npe' in combined_text:
            lines.append(self._null_check_suggestions())
        else:
            lines.append(self._generic_code_suggestions(packages))
        
        return "\n".join(lines)
    
    def _pqc_code_suggestions(self) -> str:
        """PQC-specific code suggestions."""
        return """
#### Phase 1: Add PQC Algorithm Support

**File**: `com.ibm.ws.crypto.ltpakeyutil/src/.../LTPACrypto.java`

```java
// Add PQC algorithm constants
private static final String PQC_ALGORITHM = "ML-KEM-768"; // FIPS 203
private static final String HYBRID_MODE = "3DES+ML-KEM";

// Add PQC encryption method
public byte[] encryptWithPQC(byte[] data, Key pqcKey) throws Exception {
    // TODO: Implement ML-KEM encryption
    // Reference: NIST FIPS 203 specification
}
```

#### Phase 2: Update Key Generation

**File**: `com.ibm.ws.security.utility/src/.../CreateLTPAKeysTask.java`

```java
// Add CLI option for PQC
@Option(name = "--pqc", usage = "Generate PQC-compliant keys")
private boolean usePQC = false;

// Update key generation logic
if (usePQC) {
    generateHybridKeys(); // Both legacy and PQC
} else {
    generateLegacyKeys(); // Backward compatibility
}
```

#### Phase 3: Update ltpa.keys Format

**New Format**:
```properties
com.ibm.websphere.ltpa.version=2.0
com.ibm.websphere.ltpa.mode=hybrid

# Legacy keys
com.ibm.websphere.ltpa.3DESKey=<base64>

# PQC keys (FIPS 203-205)
com.ibm.websphere.ltpa.pqc.KEMPublicKey=<base64>
com.ibm.websphere.ltpa.pqc.KEMPrivateKey=<base64>
```
"""
    
    def _jwt_code_suggestions(self) -> str:
        """JWT-specific code suggestions."""
        return """
#### Add Null Checks

**File**: `io.openliberty.security.jwt/src/.../JwtTokenValidator.java`

```java
public boolean validate(String token) {
    if (token == null || token.isEmpty()) {
        throw new IllegalArgumentException("Token cannot be null or empty");
    }
    // ... rest of validation
}
```
"""
    
    def _null_check_suggestions(self) -> str:
        """Null pointer fix suggestions."""
        return """
#### Add Defensive Null Checks

```java
// Before
String value = object.getValue();

// After
String value = (object != null) ? object.getValue() : null;
if (value == null) {
    log.warning("Unexpected null value");
    return defaultValue;
}
```
"""
    
    def _generic_code_suggestions(self, packages: List[Dict]) -> str:
        """Generic code suggestions."""
        return f"""
Review the following packages for potential changes:

{chr(10).join(f"- `{pkg['name']}`" for pkg in packages[:3])}

Consider:
1. Adding null checks for robustness
2. Updating error handling
3. Adding logging for debugging
4. Reviewing recent changes in these packages
"""
    
    def _generate_test_recommendations(self, packages: List[Dict], issue: Dict) -> str:
        """Generate manual test recommendations."""
        lines = ["### 🧪 Manual Test Recommendations\n"]
        
        issue_body = issue.get('body', '').lower()
        
        if 'pqc' in issue_body or 'ltpa' in issue_body:
            lines.append("""
#### Test 1: Generate LTPA Keys
```bash
cd wlp/bin
./securityUtility createLTPAKeys --pqc --password=myPassword ltpa.keys
```
**Expected**: Keys file contains both legacy and PQC keys

#### Test 2: Verify Key Format
```bash
cat ltpa.keys
```
**Expected**: File contains `com.ibm.websphere.ltpa.pqc.*` properties

#### Test 3: Server Startup
```bash
./server start myServer
```
**Expected**: Server starts successfully and loads PQC keys

#### Test 4: Token Validation
- Generate token with PQC keys
- Validate token
- **Expected**: Token validates successfully
""")
        else:
            lines.append("""
#### Test 1: Reproduce Issue
- Follow steps in issue description
- **Expected**: Issue reproduces

#### Test 2: Apply Fix
- Apply suggested code changes
- Rebuild affected bundles
- **Expected**: Build succeeds

#### Test 3: Verify Fix
- Repeat reproduction steps
- **Expected**: Issue no longer occurs

#### Test 4: Regression Testing
- Run existing test suites
- **Expected**: All tests pass
""")
        
        return "\n".join(lines)
    
    def _generate_validation_steps(self, packages: List[Dict], issue: Dict) -> str:
        """Generate validation steps."""
        lines = ["### ✅ Validation Steps\n"]
        lines.append("""
1. **Code Review**
   - Review all changes in identified packages
   - Ensure backward compatibility
   - Check for security implications

2. **Unit Tests**
   - Add/update unit tests for modified code
   - Achieve >80% code coverage
   - All tests must pass

3. **Integration Tests**
   - Test interaction between modified packages
   - Verify end-to-end functionality
   - Test edge cases

4. **Performance Testing**
   - Measure performance impact
   - Ensure no regression
   - Document any performance changes

5. **Documentation**
   - Update JavaDoc
   - Update user documentation
   - Add release notes entry
""")
        
        return "\n".join(lines)
    
    def _group_by_subsystem(self, packages: List[Dict]) -> Dict[str, List[Dict]]:
        """Group packages by subsystem."""
        subsystems = {}
        
        for pkg in packages:
            name = pkg['name']
            # Extract subsystem from package name
            if 'security' in name:
                subsystem = "Security"
            elif 'crypto' in name:
                subsystem = "Cryptography"
            elif 'utility' in name:
                subsystem = "Utilities"
            elif 'token' in name:
                subsystem = "Token Management"
            else:
                subsystem = "Core"
            
            if subsystem not in subsystems:
                subsystems[subsystem] = []
            subsystems[subsystem].append(pkg)
        
        return subsystems
    
    def _find_existing_comment(self, api_url: str) -> Optional[int]:
        """Find existing Bob comment on the issue."""
        if self.dry_run or not self.session:
            return None
            
        comments_url = f"{api_url}/comments"
        response = self.session.get(comments_url, timeout=10)
        
        if response.status_code != 200:
            return None
        
        comments = response.json()
        for comment in comments:
            if self.BOT_SIGNATURE in comment.get('body', ''):
                return comment['id']
        
        return None
    
    def _create_comment(self, api_url: str, body: str) -> CommentResult:
        """Create new comment on issue."""
        if self.dry_run or not self.session:
            return CommentResult(success=False, error_message="Dry run mode")
            
        comments_url = f"{api_url}/comments"
        
        response = self.session.post(
            comments_url,
            json={'body': body},
            timeout=10
        )
        
        if response.status_code == 201:
            data = response.json()
            return CommentResult(
                success=True,
                comment_url=data['html_url'],
                comment_id=data['id']
            )
        else:
            return CommentResult(
                success=False,
                error_message=f"Failed to create comment: {response.status_code} - {response.text}"
            )
    
    def _update_comment(self, api_url: str, comment_id: int, body: str) -> CommentResult:
        """Update existing comment."""
        if self.dry_run or not self.session:
            return CommentResult(success=False, error_message="Dry run mode")
            
        # Add update timestamp
        body += f"\n\n*Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC*"
        
        # Extract base URL
        base_url = api_url.rsplit('/issues/', 1)[0]
        comment_url = f"{base_url}/issues/comments/{comment_id}"
        
        response = self.session.patch(
            comment_url,
            json={'body': body},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return CommentResult(
                success=True,
                comment_url=data['html_url'],
                comment_id=data['id']
            )
        else:
            return CommentResult(
                success=False,
                error_message=f"Failed to update comment: {response.status_code} - {response.text}"
            )
    
    def _add_label(self, api_url: str, owner: str, repo: str, issue_number: str):
        """Add 'bot-analyzed' label to issue."""
        if self.dry_run or not self.session:
            return
            
        labels_url = f"{api_url}/labels"
        
        try:
            # Try to add label
            response = self.session.post(
                labels_url,
                json={'labels': ['bot-analyzed']},
                timeout=5
            )
            
            if response.status_code == 404:
                # Label doesn't exist, create it first
                self._create_label(api_url, owner, repo)
                # Try again
                self.session.post(labels_url, json={'labels': ['bot-analyzed']}, timeout=5)
        except Exception as e:
            # Label addition is non-critical, just log
            print(f"Warning: Could not add label: {e}")
    
    def _create_label(self, api_url: str, owner: str, repo: str):
        """Create 'bot-analyzed' label in repository."""
        if self.dry_run or not self.session:
            return
            
        base_url = api_url.rsplit('/issues/', 1)[0]
        labels_url = f"{base_url}/labels"
        
        self.session.post(
            labels_url,
            json={
                'name': 'bot-analyzed',
                'color': '0E8A16',
                'description': 'Issue has been analyzed by Bob'
            },
            timeout=5
        )


def main():
    """CLI entry point."""
    import sys
    
    # Parse arguments
    dry_run = '--dry-run' in sys.argv
    if dry_run:
        sys.argv.remove('--dry-run')
    
    if len(sys.argv) < 3:
        print("Usage: python comment_poster.py [--dry-run] <issue_url> <analysis_json_file> [diagram_file]")
        print("")
        print("Options:")
        print("  --dry-run    Preview comment without posting to GitHub")
        print("")
        print("Example:")
        print("  python comment_poster.py https://github.com/org/repo/issues/123 analysis.json diagram.md")
        print("  python comment_poster.py --dry-run https://github.com/org/repo/issues/123 analysis.json diagram.md")
        sys.exit(1)
    
    issue_url = sys.argv[1]
    analysis_file = sys.argv[2]
    diagram_file = sys.argv[3] if len(sys.argv) > 3 else None
    
    # Load analysis
    with open(analysis_file, 'r') as f:
        analysis = json.load(f)
    
    # Load diagram
    diagram = ""
    if diagram_file:
        with open(diagram_file, 'r') as f:
            diagram = f.read()
    
    # Post comment (or preview if dry-run)
    poster = GitHubCommentPoster(dry_run=dry_run)
    result = poster.post_analysis(issue_url, analysis, diagram)
    
    if result.success:
        print(f"✅ Comment posted successfully!")
        print(f"URL: {result.comment_url}")
    else:
        print(f"❌ Error: {result.error_message}")
        sys.exit(1)


if __name__ == '__main__':
    main()

# Made with Bob
