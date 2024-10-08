# Introduction

## Purpose of the Project

The `scm-config-clone` tool is designed to simplify the process of migrating configuration objects between Palo Alto Networks Strata Cloud Manager (SCM) tenants. Whether you're consolidating environments, migrating to a new tenant, or replicating configurations for testing, this tool streamlines the process.

## Problem Statement

Manually copying configurations between SCM tenants can be time-consuming and error-prone. `scm-config-clone` addresses these challenges by automating the cloning process, ensuring consistency and reducing the potential for mistakes.

## Key Features

- **Automated Cloning**: Eliminates the need for manual copying of configurations.
- **Secure Credentials Handling**: Uses a `.secrets.yaml` file to store credentials securely.
- **Customizable**: Allows specifying folders and is designed to be extended with additional commands.
- **User-Friendly**: Provides clear prompts and informative logging.

## Workflow

1. **Authentication**: Set up your credentials using the `create-secrets-file` command.
2. **Cloning Operations**: Use the available commands to clone address objects and groups.
3. **Verification**: Confirm that configurations have been successfully cloned to the destination tenant.

## Next Steps

### Python based workflows

Proceed to the [Installation Guide](python/installation.md) to set up `scm-config-clone` and begin cloning configurations between your SCM tenants.

### Docker based workflows

Proceed to the [Installation Guide](docker/installation.md) to set up `scm-config-clone` and begin cloning configurations between your SCM tenants.
