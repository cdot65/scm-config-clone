# SCM Config Clone

![Banner Image](https://raw.githubusercontent.com/cdot65/scm-config-clone/refs/heads/main/docs/images/logo.svg)

[![Build Status](https://github.com/cdot65/scm-config-clone/actions/workflows/ci.yml/badge.svg)](https://github.com/cdot65/scm-config-clone/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/scm-config-clone.svg)](https://badge.fury.io/py/scm-config-clone)
[![Python versions](https://img.shields.io/pypi/pyversions/scm-config-clone.svg)](https://pypi.org/project/scm-config-clone/)
[![License](https://img.shields.io/github/license/cdot65/scm-config-clone.svg)](https://github.com/cdot65/scm-config-clone/blob/main/LICENSE)

`scm-config-clone` is a command-line tool designed to seamlessly clone configuration objects between Palo Alto Networks
Strata Cloud Manager (SCM) tenants. From addresses and tags to application groups and security rules, this tool
streamlines migration tasks and reduces manual errors.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Docker](#docker)
- [Basic Usage](#basic-usage)
- [Creating the Settings File](#creating-the-settings-file)
- [Cloning Objects](#cloning-objects)
- [Testing](#testing)
- [Further Reading](#further-reading)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Simple Setup**: Store credentials and defaults in a `settings.yaml` file for reuse.
- **Robust Cloning**: Supports multiple object types (addresses, tags, services, security rules, IKE & IPsec VPN configurations, and more).
- **Extensive Filters**: Exclude specific folders, snippets, or devices to narrow down cloned objects.
- **Flexible Controls**: Run in `dry-run` mode, auto-approve changes, suppress console output, and create reports.
- **Commit & Push**: Automatically commit changes after objects are cloned.

## Installation

**Requirements**:

- Python 3.10 or higher

Install directly from PyPI:

```bash
pip install scm-config-clone
```

## Docker

### Build Locally

```powershell
# From repository root
docker build -t scm-config-clone -f ./docker/Dockerfile .
```

### Pull from GitHub Container Registry

```powershell
docker pull ghcr.io/cdot65/scm-config-clone:latest
```

### Run the CLI

```powershell
docker run --rm ghcr.io/cdot65/scm-config-clone --help
```

### Create a settings.yaml (Windows example)

`scm-clone` stores credentials in a `settings.yaml`. If you prefer, copy `settings.example.yaml` to `settings.yaml` and edit manually.

To generate it interactively, mount the current working directory into `/app` inside the container:

```powershell
# PowerShell (directory on Windows drive, e.g. C:)
docker run -it --rm -v "${PWD}:/app" ghcr.io/cdot65/scm-config-clone settings

# Windows CMD
docker run --rm -v "%cd%":/app ghcr.io/cdot65/scm-config-clone settings
```

A `settings.yaml` will be generated in your current directory. Subsequent commands should include the same mount so the CLI can read the file.

### Working example (clone addresses)

```powershell
PS C:\Users\cdot\Documents> docker run -it --rm -v "${PWD}:/app" ghcr.io/cdot65/scm-config-clone addresses
🚀 Starting address objects cloning...
Name of source folder where objects are located: Austin
Name of destination folder where objects will go: Texas
INFO:scm_config_clone.commands.objects.address:Authenticated with source SCM tenant: 1527824794
INFO:scm_config_clone.commands.objects.address:Authenticated with destination SCM tenant: 1540792209
INFO:scm_config_clone.commands.objects.address:Retrieved 47 address objects from source folder 'Austin'.
INFO:scm_config_clone.commands.objects.address:Retrieved 15248 objects from destination folder 'Texas'
╒════════════════════╤══════════════════════╕
│ Name               │ Destination Status   │
╞════════════════════╪══════════════════════╡
│ snippet-object-1-1 │ x                    │
│ snippet-object-1   │ x                    │
│ snippet-object-2   │ x                    │
│ snippet-object-3   │ x                    │
│ dhcp_pool          │ x                    │
│ bulk_address_1     │ x                    │
│ bulk_address_2     │ x                    │
│ bulk_address_3     │ x                    │
│ bulk_address_4     │ x                    │
│ bulk_address_5     │ x                    │
│ bulk_address_6     │ x                    │
│ bulk_address_7     │ x                    │
│ bulk_address_8     │ x                    │
│ bulk_address_9     │ x                    │
│ bulk_address_10    │ x                    │
│ bulk_address_11    │ x                    │
│ bulk_address_12    │ x                    │
│ bulk_address_13    │ x                    │
│ bulk_address_14    │ x                    │
│ bulk_address_15    │ x                    │
│ bulk_address_16    │ x                    │
│ bulk_address_17    │ x                    │
│ bulk_address_18    │ x                    │
│ bulk_address_19    │ x                    │
│ bulk_address_20    │ x                    │
│ bulk_address_21    │ x                    │
│ bulk_address_22    │ x                    │
│ bulk_address_23    │ x                    │
│ bulk_address_24    │ x                    │
│ bulk_address_25    │ x                    │
│ bulk_address_26    │ x                    │
│ bulk_address_27    │ x                    │
│ bulk_address_28    │ x                    │
│ bulk_address_29    │ x                    │
│ bulk_address_30    │ x                    │
│ bulk_address_31    │ x                    │
│ bulk_address_32    │ x                    │
│ bulk_address_33    │ x                    │
│ bulk_address_34    │ x                    │
│ bulk_address_35    │ x                    │
│ bulk_address_36    │ x                    │
│ bulk_address_37    │ x                    │
│ bulk_address_38    │ x                    │
│ bulk_address_39    │ x                    │
│ bulk_address_40    │ x                    │
│ bulk_address_41    │ x                    │
│ bulk_address_42    │ x                    │
╘════════════════════╧══════════════════════╛
Do you want to proceed with creating these objects in the destination tenant? [y/N]: y
INFO:scm_config_clone.commands.objects.address:No new address objects were created, skipping commit.
🎉 Address objects cloning completed successfully! 🎉
```

### Interactive settings file creation (full flow)

```powershell
PS C:\Users\you\Documents> docker run -it --rm -v "${PWD}:/app" ghcr.io/cdot65/scm-config-clone settings
# ...interactive prompts...
🎉 Setup complete! 🎉
```

### Docker Usage

From this point forward, you will need to mount your local `settings.yaml` file into the container at `/app/settings.yaml`.

```powershell
PS C:\Users\you\Documents> docker run -it --rm -v "${PWD}:/app" ghcr.io/cdot65/scm-config-clone addresses --source-folder "Texas"
```




## Basic Usage

Once installed, the primary command is `scm-clone`. Running `--help` displays global options and available sub-commands:

```bash
scm-clone --help
```

You’ll see a list of commands like `addresses`, `tags`, `services`, `security-rules`, and `settings`.

## Creating the Settings File

Before cloning, create a `settings.yaml` file to store SCM credentials and defaults:

```bash
scm-clone settings
```

You’ll be prompted for source/destination credentials, logging level, and defaults for `auto_approve`, `create_report`,
`dry_run`, and `quiet`. Once done, `settings.yaml` will be created in the current directory. Subsequent commands read
from it, eliminating the need to re-enter credentials or defaults.

## Cloning Objects

With `settings.yaml` ready, cloning objects typically involves specifying a folder and object type. For example, to
clone address objects:

```bash
scm-clone addresses --source-folder "Texas"
```

If `auto_approve` is disabled by default in `settings.yaml`, you’ll be prompted before actual creation. If you wish to
override this at runtime:

```bash
scm-clone addresses --source-folder "Texas" -A
```

This command auto-approves without prompting. Similarly, to run in dry-run mode or commit after creation:

```bash
scm-clone addresses --source-folder "Texas" -D --commit-and-push
```

This simulates the creation without applying changes (`-D`) and would commit changes if actually applied. Remove `-D` to
run it for real.

## Testing

The project includes a comprehensive test suite with both unit and integration tests. Tests are written using pytest and use Factory Boy for creating test objects.

To run the tests:

```bash
# Install development dependencies
poetry install

# Run all tests with coverage
./run_tests.sh

# Run only unit tests
./run_tests.sh unit

# Run only integration tests
./run_tests.sh integration
```

For more details about the test suite, see [tests/README.md](tests/README.md).

## Further Reading

- [Commands Reference](https://cdot65.github.io/scm-config-clone/user-guide/python/commands/): Detailed command flags,
  workflows, and parameters.
- [Examples](https://cdot65.github.io/scm-config-clone/user-guide/python/examples/): Practical, real-world usage
  patterns and integrations.
- [Getting Started](https://cdot65.github.io/scm-config-clone/user-guide/python/getting-started/): Step-by-step guide to
  initial setup and cloning workflows.

## Contributing

Contributions are welcome! Please see the [CONTRIBUTING](CONTRIBUTING.md) file for guidelines.

## License

`scm-config-clone` is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for more details.
