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
- **Multiple Context Support**: Works with folders, snippets, and device contexts to provide flexible configuration management.
- **Advanced Filtering**: Allows excluding specific folders, snippets, or devices from cloning operations.
- **User-Friendly**: Provides clear prompts and informative logging.
- **Dry-Run Mode**: Simulates operations without making actual changes for risk-free testing.

## Supported Configuration Types

The tool supports cloning various types of configurations:

1. **Objects**: Address objects, address groups, applications, tags, services, service groups, HIP objects, and many more.
2. **Security Services**: Security rules, URL categories, anti-spyware profiles, decryption profiles, and other security-related configurations.
3. **Network Services**: NAT rules and related network configurations.
4. **Deployment Services**: Remote network objects and other deployment-related configurations.

For a complete list of supported commands, see the [Commands Reference](python/commands.md).

## Workflow

1. **Settings Setup**: Configure your credentials and project settings using the `settings` command.
2. **Context Selection**: Choose the appropriate context type (folder, snippet, or device) for your configuration objects.
3. **Object Identification**: Determine which objects need to be cloned and their dependencies.
4. **Cloning Operations**: Use the appropriate commands to clone objects in the correct dependency order.
5. **Commit Changes**: Use the `--commit-and-push` option to apply changes to the destination tenant.
6. **Verification**: Confirm that all configurations have been successfully cloned and committed.

For a complete end-to-end example of migrating an entire tenant's configuration, see the [Complete Tenant Migration Workflow](python/examples.md#complete-tenant-migration-workflow) in the Examples section.

## Next Steps

Proceed to the [Installation Guide](python/installation.md) to set up `scm-config-clone` and begin cloning
configurations between your SCM tenants.
