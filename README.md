# SCM Config Clone

![Banner Image](https://raw.githubusercontent.com/cdot65/scm-config-clone/refs/heads/main/docs/images/logo.svg)

[![Build Status](https://github.com/cdot65/scm-config-clone/actions/workflows/ci.yml/badge.svg)](https://github.com/cdot65/scm-config-clone/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/scm-config-clone.svg)](https://badge.fury.io/py/scm-config-clone)
[![Python versions](https://img.shields.io/pypi/pyversions/scm-config-clone.svg)](https://pypi.org/project/scm-config-clone/)
[![License](https://img.shields.io/github/license/cdot65/scm-config-clone.svg)](https://github.com/cdot65/scm-config-clone/blob/main/LICENSE)

A command-line tool to clone configuration objects between Palo Alto Networks Strata Cloud Manager (SCM) tenants.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Clone Address Objects](#clone-address-objects)
  - [Clone Address Groups](#clone-address-groups)
  - [Create Secrets File](#create-secrets-file)
- [Contributing](#contributing)
- [License](#license)
- [Support](#support)

## Features

- **Effortless Cloning**: Seamlessly clone address objects and address groups from one SCM tenant to another.
- **User-Friendly CLI**: Built with [Typer](https://typer.tiangolo.com/) for an intuitive command-line experience.
- **Secure Authentication**: Generate a `.secrets.yaml` file to securely store your SCM credentials.
- **Customizable Folders**: Specify source and destination folders to organize your configurations.
- **Extensible Design**: Structured to allow easy addition of new commands and features in the future.

## Installation

**Requirements**:

- Python 3.10 or higher

Install the package via pip:

```bash
pip install scm-config-clone
```

## Usage

The `scm-clone` utility offers several commands:

- [`clone-address-objects`](#clone-address-objects): Clone address objects between SCM tenants.
- [`clone-address-groups`](#clone-address-groups): Clone address groups between SCM tenants.
- [`create-secrets-file`](#create-secrets-file): Generate a secrets file for authentication.

### Clone Address Objects

Clone address objects from the source SCM tenant to the destination tenant.

```bash
scm-clone clone-address-objects --settings-file <path_to_secrets_yaml>
```

**Options**:

- `--settings-file`, `-s`: Path to the YAML file containing SCM credentials (default: `.secrets.yaml`).

**Example**:

```bash
scm-clone clone-address-objects
```

**Sample Output**:

```
Starting address objects migration...
Retrieved 15 address objects from source.
Successfully created 15 address objects in destination.
Address objects migration completed successfully.
```

### Clone Address Groups

Clone address groups from the source SCM tenant to the destination tenant.

```bash
scm-clone clone-address-groups --settings-file <path_to_secrets_yaml>
```

**Options**:

- `--settings-file`, `-s`: Path to the YAML file containing SCM credentials (default: `.secrets.yaml`).

**Example**:

```bash
scm-clone clone-address-groups
```

**Sample Output**:

```
Starting address groups migration...
Retrieved 8 address groups from source.
Successfully created 8 address groups in destination.
Address groups migration completed successfully.
```

### Create Secrets File

Generate a `.secrets.yaml` file to store your SCM credentials securely.

```bash
scm-clone create-secrets-file --output-file <path_to_secrets_yaml>
```

**Options**:

- `--output-file`, `-o`: Path where the secrets YAML file will be saved (default: `.secrets.yaml`).

**Example**:

```bash
scm-clone create-secrets-file
```

**Sample Interaction**:

```
Creating authentication file...
Enter source Strata Cloud Manager credentials:
Source Client ID: <your_source_client_id>
Source Client Secret: <your_source_client_secret>
Source Tenant TSG: <your_source_tsg>
Source Folder [Prisma Access]:
Enter destination Strata Cloud Manager credentials:
Destination Client ID: <your_destination_client_id>
Destination Client Secret: <your_destination_client_secret>
Destination Tenant TSG: <your_destination_tsg>
Destination Folder [Prisma Access]:
Token URL [https://auth.apps.paloaltonetworks.com/oauth2/access_token]:
Authentication file written to .secrets.yaml
Authentication file created successfully.
```

## Contributing

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature/your-feature`).
5. Open a Pull Request.

Ensure your code adheres to the project's coding standards and includes tests where appropriate.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](./LICENSE) file for details.

## Support

For support and questions, please refer to the [SUPPORT.md](./SUPPORT.md) file in this repository.

---

*Detailed documentation will be provided on our GitHub Pages site soon.*