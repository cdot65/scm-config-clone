---
hide:
    - navigation
---

<style>
.md-content .md-typeset h1 { display: none; }
</style>

<p align="center">
    <a href="https://paloaltonetworks.com"><img src="https://github.com/cdot65/scm-config-clone/blob/main/docs/images/logo.svg?raw=true" alt="PaloAltoNetworks"></a>
</p>
<p align="center">
    <em><code>scm-config-clone</code>: Clone configuration objects between SCM tenants</em>
</p>
<p align="center">
<a href="https://github.com/cdot65/scm-config-clone/graphs/contributors" target="_blank">
    <img src="https://img.shields.io/github/contributors/cdot65/scm-config-clone.svg?style=for-the-badge" alt="Contributors">
</a>
<a href="https://github.com/cdot65/scm-config-clone/network/members" target="_blank">
    <img src="https://img.shields.io/github/forks/cdot65/scm-config-clone.svg?style=for-the-badge" alt="Forks">
</a>
<a href="https://github.com/cdot65/scm-config-clone/stargazers" target="_blank">
    <img src="https://img.shields.io/github/stars/cdot65/scm-config-clone.svg?style=for-the-badge" alt="Stars">
</a>
<a href="https://github.com/cdot65/scm-config-clone/issues" target="_blank">
    <img src="https://img.shields.io/github/issues/cdot65/scm-config-clone.svg?style=for-the-badge" alt="Issues">
</a>
<a href="https://github.com/cdot65/scm-config-clone/blob/main/LICENSE" target="_blank">
    <img src="https://img.shields.io/github/license/cdot65/scm-config-clone.svg?style=for-the-badge" alt="License">
</a>
</p>

---

**Documentation**: <a href="https://cdot65.github.io/scm-config-clone/" target="_blank">https://cdot65.github.io/scm-config-clone/</a>

**Source Code**: <a href="https://github.com/cdot65/scm-config-clone" target="_blank">https://github.com/cdot65/scm-config-clone</a>

---

`scm-config-clone` is a command-line tool designed to seamlessly clone configuration objects between Palo Alto Networks Strata Cloud Manager (SCM) tenants. It simplifies the process of migrating configurations such as address objects and address groups from a source tenant to a destination tenant, enhancing efficiency and reducing manual efforts.

## Key Features

- **Effortless Cloning**: Seamlessly clone address objects and address groups from one SCM tenant to another.
- **User-Friendly CLI**: Built with [Typer](https://typer.tiangolo.com/) for an intuitive command-line experience.
- **Secure Authentication**: Generate a `.secrets.yaml` file to securely store your SCM credentials.
- **Customizable Folders**: Specify source and destination folders to organize your configurations.
- **Extensible Design**: Structured to allow easy addition of new commands and features in the future.

## Workflow

1. **Authentication**: Use the `create-secrets-file` command to generate a `.secrets.yaml` file with your SCM credentials.
2. **Cloning**: Use the `clone-address-objects` or `clone-address-groups` commands to clone configurations from the source to the destination tenant.
3. **Verification**: Verify the cloned configurations in the destination SCM tenant.

---

## Execution

`scm-config-clone` can be executed using Python in a virtual environment:

<div class="termy">

<!-- termynal -->
```bash
$ pip install scm-config-clone
$ scm-clone --help
Usage: scm-clone [OPTIONS] COMMAND [ARGS]...

  Clone configuration from one Strata Cloud Manager tenant to another.

Options:
  --help  Show this message and exit.

Commands:
  clone-address-groups    Clone address groups from source to destination SCM tenant.
  clone-address-objects   Clone address objects from source to destination SCM tenant.
  create-secrets-file     Create authentication file.
```
</div>

For more detailed usage instructions and examples, refer to the [User Guide](user-guide/introduction.md).

---

## Contributing

Contributions are welcome and greatly appreciated. Visit the [Contributing](about/contributing.md) page for guidelines on how to contribute.

## License

This project is licensed under the Apache 2.0 License - see the [License](about/license.md) page for details.
