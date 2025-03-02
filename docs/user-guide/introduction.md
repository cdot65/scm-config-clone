# Introduction

## Purpose of the Project

The `scm-config-clone` tool is designed to simplify the process of migrating configuration objects between Palo Alto
Networks Strata Cloud Manager (SCM) tenants. Whether you're consolidating environments, migrating to a new tenant, or
replicating configurations for testing, this tool streamlines the process.

## Problem Statement

Manually copying configurations between SCM tenants can be time-consuming and error-prone. `scm-config-clone` addresses
these challenges by automating the cloning process, ensuring consistency and reducing the potential for mistakes.

## Key Features

- **Automated Cloning**: Eliminates the need for manual copying of configurations.
- **Secure Credentials Handling**: Uses a `settings.yaml` file to store credentials securely.
- **Comprehensive Coverage**: Supports a wide range of object types, security services, network services, and deployment services.
- **Customizable**: Allows specifying folders and snippets with flexible filtering options.
- **User-Friendly**: Provides clear prompts and informative logging.

## Supported Configuration Types

The tool supports cloning various types of configurations:

1. **Objects**: Address objects, address groups, applications, tags, services, service groups, HIP objects, and many more.
2. **Security Services**: Security rules, URL categories, anti-spyware profiles, decryption profiles, and other security-related configurations.
3. **Network Services**: NAT rules and related network configurations.
4. **Deployment Services**: Remote network objects and other deployment-related configurations.

For a complete list of supported commands, see the [Commands Reference](python/commands.md).

## Workflow

1. **Authentication**: Set up your credentials and project settings using the `settings` command.
2. **Cloning Operations**: Use the available commands to clone various configuration objects between tenants.
3. **Verification**: Confirm that configurations have been successfully cloned to the destination tenant.

## Next Steps

Proceed to the [Installation Guide](python/installation.md) to set up `scm-config-clone` and begin cloning
configurations between your SCM tenants.
