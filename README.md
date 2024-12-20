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
- [Basic Usage](#basic-usage)
- [Creating the Settings File](#creating-the-settings-file)
- [Cloning Objects](#cloning-objects)
- [Further Reading](#further-reading)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Simple Setup**: Store credentials and defaults in a `settings.yaml` file for reuse.
- **Robust Cloning**: Supports multiple object types (addresses, tags, services, security rules, and more).
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
