# Release Notes

Welcome to the release notes for the `scm-config-clone` tool. This document provides a detailed record of changes,
enhancements, and fixes in each version of the tool.

---

## Version 0.2.6

**Release Date:** February 23rd, 2025

### Introduction

- **dependency update**:
    - Update `pan-scm-sdk` and `setuptools` to latest versions.
- **NAT rule update**:
    - Added support for cloning NAT rules.

---

## Version 0.2.2

**Release Date:** December 18th, 2024

### Introduction

- **dependency update**:
    - Forgot to add `pyyaml` to list of dependencies.

---

## Version 0.2.1

**Release Date:** December 15th, 2024

### Introduction

- **Docs**:
    - Forgot to update the project's README before pushing to pypi.

---

## Version 0.2.0

**Release Date:** December 15th, 2024

### Introduction

- **Features**:
    - **Massive Overhaul**: Using the new `pan-scm-sdk` library
    - **Coverage increased**: Added support for many new configuration items to be cloned.

## Version 0.1.1

**Release Date:** October 8, 2024

### Introduction

- **Features**:
    - **Security Profile Groups**: Adding a new command for security profile groups.
    - **Limit Update**: Update the limit parameter within the request to 5000.

---

## Version 0.1.0

**Release Date:** October 8, 2024

### Introduction

- **Initial Release**: Launched the first version of `scm-config-clone`.
- **Features**:
    - Clone address objects between SCM tenants.
    - Clone address groups between SCM tenants.
    - Generate a `.secrets.yaml` file for secure authentication.
- **Improvements**:
    - User-friendly CLI with helpful prompts.
    - Secure handling of credentials.
    - Logging and error handling enhancements.

---

For more detailed information on each release, visit
the [GitHub repository](https://github.com/cdot65/scm-config-clone/releases) or check
the [commit history](https://github.com/cdot65/scm-config-clone/commits/main).
