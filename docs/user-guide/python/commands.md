# SCM Config Clone CLI Commands Reference

## Table of Contents

- [Overview](#overview)
- [Basic Configuration](#basic-configuration)
- [Usage Examples](#usage-examples)
- [Best Practices](#best-practices)

## Overview

The `scm-clone` command-line interface (CLI) facilitates the cloning of configuration objects between Palo Alto Networks
Strata Cloud Manager (SCM) tenants. It supports multiple configuration object types, enabling you to easily replicate
addresses, tags, applications, security profiles, and more.

The CLI reads configurations and credentials from a `settings.yaml` file, which you create once using the
`scm-clone settings` command. After initial setup, you can use flags and options for further customization or overrides.

**Global Options:**

- `--help`: Display the help message and exit.

**Key Features:**

- Load credentials and configuration from `settings.yaml`.
- Override defaults at runtime using command-line flags.
- Retrieve and filter configuration objects based on folders, snippets, devices, and other criteria.
- Dry-run mode to simulate actions before applying them.
- Quiet mode to suppress console output except for logs.
- Auto-approve mode to skip confirmation prompts.
- Ability to commit changes after cloning objects.
- Options to create a CSV report of the results.

## Basic Configuration

Before using any of the CLI commands to clone objects, you must create a `settings.yaml` file. This file stores
authentication credentials, logging preferences, and other configuration options.

**Command to create settings file:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone settings
```

</div>

You will be prompted for source and destination SCM credentials, logging level, and additional options like
`auto_approve`, `create_report`, `dry_run`, and `quiet`. These become defaults for subsequent commands.

**Example `settings.yaml`:**

```yaml
oauth:
  source:
    client_id: source_client_id
    client_secret: source_client_secret
    tsg: source_tsg_id
  destination:
    client_id: destination_client_id
    client_secret: destination_client_secret
    tsg: destination_tsg_id
logging: INFO
auto_approve: false
create_report: false
dry_run: false
quiet: false
```

With `settings.yaml` in place, you can run commands without repeatedly supplying credentials and default parameters.

## Commands

The `scm-clone` CLI provides multiple sub-commands, each handling a different class of SCM objects. Below are the
available commands and their primary purposes.

### Objects and Security Services

| Command                | Description                             |
|------------------------|-----------------------------------------|
| addresses              | Clone address objects                   |
| address-groups         | Clone address groups                    |
| applications           | Clone application objects               |
| application-filters    | Clone application filters               |
| application-groups     | Clone application groups                |
| edls                   | Clone external dynamic lists            |
| hip-objects            | Clone HIP objects                       |
| services               | Clone services                          |
| service-groups         | Clone service groups                    |
| tags                   | Clone tag objects                       |
| anti-spyware-profiles  | Clone anti-spyware profiles             |
| decryption-profiles    | Clone decryption profiles               |
| dns-security-profiles  | Clone DNS security profiles             |
| security-rules         | Clone security rules                    |
| url-categories         | Clone URL categories                    |
| vulnerability-profiles | Clone vulnerability protection profiles |
| wildfire-profiles      | Clone Wildfire AV profiles              |

**Common Flags and Arguments:**

| Argument/Flag          | Description                                                                  | Default             |
|------------------------|------------------------------------------------------------------------------|---------------------|
| `--source-folder`      | The folder from which to retrieve and clone objects.                         | None (prompted)     |
| `--destination-folder` | The folder where the cloned objects will be created.                         | None (prompted)     |
| `--exclude-folders`    | Comma-separated list of folders to exclude from retrieval.                   | None                |
| `--exclude-snippets`   | Comma-separated list of snippets to exclude from retrieval.                  | None                |
| `--exclude-devices`    | Comma-separated list of devices to exclude from retrieval.                   | None                |
| `--commit-and-push`    | If set, commit changes on the destination tenant after creating objects.     | False               |
| `--auto-approve, -A`   | If set (or configured in settings), skip confirmation prompt before cloning. | Value from settings |
| `--create-report, -R`  | If set (or configured in settings), append results to `result.csv`.          | Value from settings |
| `--dry-run, -D`        | If set (or configured in settings), simulate without applying changes.       | Value from settings |
| `--quiet-mode, -Q`     | If set (or configured in settings), hide console output except logs.         | Value from settings |
| `--logging-level, -L`  | Override logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).              | Value from settings |
| `--settings-file, -s`  | Path to the YAML settings file.                                              | `settings.yaml`     |

## Usage Examples

Below are some real-world scenarios demonstrating how to use `scm-clone` with various commands and options.

### Basic Initialization

1. **Create the `settings.yaml` File**:

   <div class="termy">
   <!-- termynal -->
   ```bash
   scm-clone settings
   ```
   </div>

   Follow the prompts to provide source/destination credentials and defaults.

2. **Cloning Addresses**:

   Once `settings.yaml` is created, you can clone addresses with minimal input:

   <div class="termy">
   <!-- termynal -->
   ```bash
   scm-clone addresses --source-folder "Texas"
   ```
   </div>

   If `auto_approve` is set to false in settings, you'll be prompted before proceeding. If `quiet_mode` is false, you
   will see a table of retrieved addresses.

### Overriding Defaults at Runtime

If you set `auto_approve: false` in `settings.yaml`, you can override it at runtime:

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas" -A
```
</div>

This auto-approves changes without prompting.

Similarly, if you want to run in dry-run mode (coming soon):

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas" -D
```
</div>

This will simulate the creation without applying changes.

### Filtering Objects

You can exclude certain folders, snippets, or devices from retrieval:

<div class="termy">
<!-- termynal -->
```bash
scm-clone tags --source-folder "Texas" \
               --exclude-folders "All,Default" \
               --exclude-snippets "predefined" \
               --exclude-devices "DeviceA"
```
</div>

This command retrieves tag objects from `"Texas"`, excluding any from the `"All"` or `"Default"` folders,
any that come from snippet `"predefined"`, and any associated with `DeviceA`.

### Commit and Push Changes

If you want to commit your changes automatically after creation:

<div class="termy">
<!-- termynal -->
```bash
scm-clone address-groups --source-folder "Texas" --commit-and-push
```
</div>

After cloning address groups, this command commits changes to the destination tenant automatically.

### Generating Reports

If `create_report` is enabled, results will be appended to `result.csv`. To override at runtime:

<div class="termy">
<!-- termynal -->
```bash
scm-clone applications --source-folder "Texas" -R
```
</div>

This ensures a CSV report is generated/appended with the cloned results.

## Best Practices

- **Use a Single Settings File**: Maintain one `settings.yaml` per environment. This centralizes credentials and default
  behaviors.
- **Set Logical Defaults**: In `settings.yaml`, configure `auto_approve` and `quiet` according to your regular workflow
  to minimize prompts or unwanted noise.
- **Dry Runs**: Use `--dry-run` to test changes before applying them, especially in production environments.
- **Selective Cloning**: Leverage `--exclude-folders`, `--exclude-snippets`, and `--exclude-devices` to narrowly target
  your cloning operation, avoiding unnecessary objects.
- **Logging and Reporting**: Adjust the logging level and use `--create-report` to keep a record of operations and
  outcomes for auditing and troubleshooting.
- **Commit after Cloning**: Using `--commit-and-push` ensures that once objects are cloned successfully, the changes are
  applied and committed, saving time and reducing manual steps.

For more detailed examples and advanced use cases, refer to the [Examples](examples.md) section.
