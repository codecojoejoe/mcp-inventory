# MCP Server Inventory

Internal registry of approved MCP (Model Context Protocol) servers. Browse the catalog, check out servers for your projects, and follow the setup instructions below.

## Servers

| Server | Source | Transport | Tools | Version |
|--------|--------|-----------|-------|---------|
| [Okta MCP](servers/okta-mcp/config.json) | Custom | STDIO | 6 | 2.1.0 |
| [GitHub MCP](servers/github-mcp/config.json) | Official | STDIO | 5 | 1.0.0 |
| [Glean MCP](servers/glean-mcp/config.json) | Custom | SSE | 2 | 1.0.0 |
| [Jira MCP](servers/jira-mcp/config.json) | Community | STDIO | 5 | 1.0.0 |
| [Confluence MCP](servers/confluence-mcp/config.json) | Community | STDIO | 4 | 1.0.0 |
| [Atlassian MCP](servers/atlassian-mcp/config.json) | Community | STDIO | 4 | 1.0.0 |
| [Asana MCP](servers/asana-mcp/config.json) | Community | STDIO | 5 | 1.0.0 |

## How to Use

### 1. Browse the Catalog

Each server has a `config.json` in its directory under `servers/`. This file contains:
- Server metadata (name, version, description, transport type)
- Available tools with descriptions and access levels
- Required environment variables
- Version changelog

### 2. Check Out a Server

Clone this repo and reference the server config in your MCP client configuration:

```bash
git clone https://github.com/codecojoejoe/mcp-inventory.git
```

For Claude Desktop or similar MCP clients, add the server to your config:

```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "jira-mcp"],
      "env": {
        "JIRA_INSTANCE_URL": "https://your-instance.atlassian.net",
        "JIRA_USER_EMAIL": "you@company.com",
        "JIRA_API_KEY": "your-api-key"
      }
    }
  }
}
```

### 3. Set Up Credentials

Each server requires specific environment variables. Check the `envVars` section in the server's `config.json`. Variables marked `"secret": true` should be stored securely (keychain, vault, etc.) and never committed to repos.

## Access Levels

Tools within each server have an access level:

| Level | Meaning |
|-------|---------|
| `allowed` | Free to use, no restrictions |
| `requires_approval` | Must be approved by a team lead before use |
| `blocked` | Not available for use — contact the MCP governance team |

## Governance

This inventory is managed by the NHI Monitor app. All checkouts, access evaluations, and version changes are tracked and audited. If you need access to a restricted tool or want to request a new server, contact the platform team.

## Structure

```
mcp-inventory/
├── README.md
├── registry.json              # Machine-readable index of all servers
└── servers/
    ├── okta-mcp/config.json
    ├── github-mcp/config.json
    ├── glean-mcp/config.json
    ├── jira-mcp/config.json
    ├── confluence-mcp/config.json
    ├── atlassian-mcp/config.json
    └── asana-mcp/config.json
```
