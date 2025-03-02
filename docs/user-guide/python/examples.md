# Examples

This section provides practical scenarios to help you understand how to use `scm-clone` effectively. Each example
demonstrates a real-world usage pattern, from initial setup to cloning various object types (addresses, tags, security
rules, services) with different filters and runtime overrides.

## Table of Contents

- [Overview](#overview)
- [Flags and Parameters](#flags-and-parameters)
- [Initial Setup (Creating the Settings File)](#initial-setup-creating-the-settings-file)
- [Cloning Addresses](#cloning-addresses)
- [Cloning Tags](#cloning-tags)
- [Cloning Services](#cloning-services)
- [Cloning Security Rules](#cloning-security-rules)
- [Cloning Remote Networks](#cloning-remote-networks)
- [Cloning Syslog Server Profiles](#cloning-syslog-server-profiles)
- [Advanced Examples](#advanced-examples)

## Overview

Before running clone operations, ensure you have a `settings.yaml` file configured. This file stores default
credentials, logging preferences, and default flags like `auto_approve` or `quiet`. All commands read from
`settings.yaml` first, allowing you to run most operations without constantly re-entering credentials or options.

If needed, you can override any setting at runtime using the provided flags.

## Flags and Parameters

All commands share a common set of flags that interact with the defaults defined in `settings.yaml`. At runtime, if a
flag is not provided, the CLI falls back on the values from `settings.yaml`.

| Flag/Option            | Description                                                                                     | Default from YAML |
|------------------------|-------------------------------------------------------------------------------------------------|-------------------|
| `--source-folder`      | Folder to focus on when retrieving and cloning objects. If omitted, the CLI will prompt for it. | None              |
| `--destination-folder` | Folder to create objects in the destination tenant. If omitted, the CLI will prompt for it.     | None              |
| `--exclude-folders`    | Comma-separated folders to exclude from retrieval.                                              | None              |
| `--exclude-snippets`   | Comma-separated snippets to exclude from retrieval.                                             | None              |
| `--exclude-devices`    | Comma-separated devices to exclude from retrieval.                                              | None              |
| `--commit-and-push`    | Commit changes in the destination tenant after creation if objects are successfully cloned.     | False             |
| `--auto-approve, -A`   | If set or in `settings.yaml`, skip confirmation prompts before creating objects.                | From settings     |
| `--create-report, -R`  | If set or in `settings.yaml`, append results to `result.csv` after completion.                  | From settings     |
| `--dry-run, -D`        | If set or in `settings.yaml`, simulate operations without applying changes.                     | From settings     |
| `--quiet-mode, -Q`     | If set or in `settings.yaml`, suppress console output except log messages.                      | From settings     |
| `--logging-level, -L`  | Override the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).                             | From settings     |
| `--settings-file, -s`  | Specify a custom `settings.yaml` file path.                                                     | `settings.yaml`   |

## Initial Setup (Creating the Settings File)

The first step is to generate the `settings.yaml` file that stores your SCM credentials, default logging preferences,
and behaviors like `auto_approve` or `quiet_mode`.

<div class="termy">
<!-- termynal -->
```bash
scm-clone settings
```
</div>

Follow the prompts to enter:

- Source and destination SCM credentials (client_id, client_secret, tsg_id).
- Logging level (e.g., INFO).
- Additional flags (auto_approve, create_report, dry_run, quiet) as defaults.

Once the file is created, all commands will use these defaults unless overridden at runtime.

## Cloning Addresses

Addresses are one of the most common object types. After creating `settings.yaml`, you can clone addresses from a source
folder.

**Example: Cloning addresses from folder "Texas" with no additional filters:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas"
```
</div>

If `auto_approve` is `false` in your settings, you'll be prompted before actually creating the objects. If `quiet_mode`
is `false`, you'll see a table of retrieved addresses and, after creation, a table of successfully created objects.

**Overriding to run a dry-run:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas" -D
```
</div>

This simulates the process without applying changes.

**Using filters and committing changes after creation:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas" --exclude-folders "All,Default" --exclude-snippets "predefined" -A --commit-and-push
```
</div>

This excludes addresses from the `All` and `Default` folders, snippet `predefined`, auto-approves the operation, and
commits changes after successful creation.

## Cloning Tags

For tags, assume we have a similar workflow. Just specify the folder and any filters:

<div class="termy">
<!-- termynal -->
```bash
scm-clone tags --source-folder "Texas" --exclude-devices "DeviceA" -A
```
</div>

This auto-approves and excludes any tag objects associated with `DeviceA`, prompting no confirmations since `-A` was
used.

If you want a dry-run scenario for tags:

<div class="termy">
<!-- termynal -->
```bash
scm-clone tags --source-folder "Texas" -D
```
</div>

This will show you what would happen without making any changes.

## Cloning Services

For services, you may want to exclude certain snippets or folders. Additionally, you might want to run quietly to avoid
console clutter:

<div class="termy">
<!-- termynal -->
```bash
scm-clone services --source-folder "Texas" --exclude-snippets "legacy-snippet" -Q
```
</div>

This command suppresses console output, relying on logs for progress. If you have `auto_approve` enabled in
`settings.yaml`, it will skip prompts as well.

To commit changes after cloning services:

<div class="termy">
<!-- termynal -->
```bash
scm-clone services --source-folder "Texas" --commit-and-push
```
</div>

## Cloning Security Rules

Security rules often require careful filtering and a dry-run before applying. Suppose you want to clone rules from
folder `cdot65` in the `pre` rulebase, and you'd like a prompt before proceeding:

<div class="termy">
<!-- termynal -->
```bash
scm-clone security-rules --source-folder "cdot65" --rulebase "pre"
```
</div>

If you want to exclude certain devices or snippets while cloning security rules:

<div class="termy">
<!-- termynal -->
```bash
scm-clone security-rules --source-folder "cdot65" --rulebase "pre" --exclude-devices "DeviceX" --exclude-snippets "snipA,snipB"
```
</div>

To automatically approve and commit the changes:

<div class="termy">
<!-- termynal -->
```bash
scm-clone security-rules --source-folder "cdot65" --rulebase "pre" -A --commit-and-push
```
</div>

## Cloning Remote Networks

Remote Networks are a key component of SASE deployments. After setting up your `settings.yaml` file with proper SASE credentials, you can use the following commands to clone Remote Network objects between tenants.

**Basic cloning of remote networks from a source folder:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone remote-networks --source "Remote Networks"
```
</div>

This will list all remote networks in the source folder, prompting for confirmation before cloning.

**Specifying both source and destination folders:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone remote-networks --source "Remote Networks" --destination "Branch Offices"
```
</div>

This retrieves remote networks from "Remote Networks" folder in the source tenant and creates them in the "Branch Offices" folder in the destination tenant.

**Excluding specific folders and auto-approving:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone remote-networks --source "Remote Networks" --exclude-folders "Deprecated,Testing" -A
```
</div>

This excludes any remote networks in the "Deprecated" and "Testing" folders, and skips confirmation prompts.

**Running a dry run with automatic commit after creation:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone remote-networks --source "Remote Networks" -D --commit-and-push
```
</div>

This will simulate the creation without applying changes. Note that `--commit-and-push` has no effect during a dry run.

**Complete example with reporting and commit:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone remote-networks --source "Remote Networks" --destination "Production" --exclude-folders "Testing" -A -R --commit-and-push
```
</div>

This command:
- Retrieves remote networks from "Remote Networks" folder, excluding any in the "Testing" folder
- Creates them in the "Production" folder in the destination tenant
- Auto-approves without prompting for confirmation
- Creates/appends results to result.csv
- Commits changes to the destination tenant after successful creation

## Cloning Syslog Server Profiles

Syslog server profiles define configurations for forwarding logs to external syslog servers. The following examples demonstrate how to clone these configurations between SCM tenants.

**Basic cloning of syslog server profiles from a source folder:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --source "Logging"
```
</div>

This lists all syslog server profiles in the source folder and prompts for confirmation before cloning.

**Using a specific context type and folder:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --context folder --source "Logging" --destination "Security" 
```
</div>

This explicitly specifies that we're working with folders, retrieves profiles from the "Logging" folder, and creates them in the "Security" folder.

**Working with snippets instead of folders:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --context snippet --source "logging-snippet" --destination "security-snippet"
```
</div>

This retrieves profiles from a source snippet and creates them in a destination snippet, instead of working with folders.

**Excluding specific profiles and auto-approving:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --source "Logging" --exclude-folders "Test,Development" -A
```
</div>

This excludes profiles from the "Test" and "Development" folders, automatically proceeding without confirmation.

**Performing a dry run:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --source "Logging" -D
```
</div>

This simulates the cloning operation without making any changes, showing what would be created.

**Creating a report, committing changes, and enabling quiet mode:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --source "Logging" --destination "Production" -A -R -Q --commit-and-push
```
</div>

This command:
- Retrieves syslog server profiles from the "Logging" folder
- Creates them in the "Production" folder
- Auto-approves without prompting for confirmation
- Creates/appends results to result.csv
- Runs in quiet mode with minimal console output
- Commits changes after successful creation

**Debugging issues with verbose logging:**

<div class="termy">
<!-- termynal -->
```bash
scm-clone syslog-server-profiles --source "Logging" --logging-level DEBUG
```
</div>

This increases the logging level to DEBUG to help diagnose any issues that might occur during the cloning process.

## Advanced Examples

**Using a Custom Settings File**: If you have multiple environments, you might have different settings files:

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas" --settings-file "production_settings.yaml"
```
</div>

This command uses `production_settings.yaml` instead of the default `settings.yaml`.

**Generating a Report**: If you want to record all cloned addresses into `result.csv` for auditing:

> Note: this feature is not yet implemented.

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --source-folder "Texas" -R
```
</div>

After cloning, the CLI will append the results to `result.csv`.

**Combining Flags**: For a scenario where you want to exclude folders, run quietly, auto-approve, and create a report
all at once:

<div class="termy">
<!-- termynal -->
```bash
scm-clone tags --source-folder "Texas" --exclude-folders "All,Default" -A -R -Q
```
</div>

This command retrieves and clones tags from the `"Texas"`, excluding `"All"` and `"Default"` folders, auto-approves
without prompts, creates a CSV report, and runs quietly without console output.

---
