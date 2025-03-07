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

**Documentation
**: <a href="https://cdot65.github.io/scm-config-clone/" target="_blank">https://cdot65.github.io/scm-config-clone/</a>

**Source Code
**: <a href="https://github.com/cdot65/scm-config-clone" target="_blank">https://github.com/cdot65/scm-config-clone</a>

---

`scm-config-clone` is a command-line tool designed to seamlessly clone configuration objects between Palo Alto Networks
Strata Cloud Manager (SCM) tenants. It simplifies the process of migrating configurations such as address objects and
address groups from a source tenant to a destination tenant, enhancing efficiency and reducing manual efforts.

## Key Features

- **Effortless Cloning**: Seamlessly clone configuration objects (addresses, services, security profiles, VPN configurations, and more) from one SCM tenant to another.
- **User-Friendly CLI**: Built with [Typer](https://typer.tiangolo.com/) for an intuitive command-line experience.
- **Secure Authentication**: Generate a `settings.yaml` file to securely store your SCM credentials.
- **Customizable Folders**: Specify source and destination folders to organize your configurations.
- **Extensible Design**: Structured to allow easy addition of new commands and features in the future.

## Workflow

1. **Authentication**: Use the `settings` command to generate a `settings.yaml` file with your SCM
   credentials, and other tool options.
2. **Cloning**: Use the appropriate command to clone configurations from the
   source to the destination tenant.
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
                                                                                                                                                                                                                                                        
╭─ Options ────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ --install-completion          Install completion for the current shell.                                                                                                                                                                              │
│ --show-completion             Show completion for the current shell, to copy it or customize the installation.                                                                                                                                       │
│ --help                        Show this message and exit.                                                                                                                                                                                            │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ address-groups           Clone address groups                                                                                                                                                                                                        │
│ addresses                Clone address objects                                                                                                                                                                                                       │
│ anti-spyware-profiles    Clone anti-spyware profiles                                                                                                                                                                                                 │
│ application-filters      Clone application filters                                                                                                                                                                                                   │
│ application-groups       Clone application groups                                                                                                                                                                                                    │
│ applications             Clone application objects                                                                                                                                                                                                   │
│ decryption-profiles      Clone decryption profiles                                                                                                                                                                                                   │
│ dns-security-profiles    Clone DNS security profiles                                                                                                                                                                                                 │
│ dynamic-user-groups      Clone dynamic user groups                                                                                                                                                                                                   │
│ edls                     Clone external dynamic lists                                                                                                                                                                                                │
│ hip-objects              Clone HIP objects                                                                                                                                                                                                           │
│ hip-profiles             Clone HIP profiles                                                                                                                                                                                                          │
│ http-server-profiles     Clone HTTP server profiles                                                                                                                                                                                                  │
│ ike-crypto-profiles      Clone IKE crypto profiles                                                                                                                                                                                                   │
│ ike-gateways             Clone IKE gateways                                                                                                                                                                                                          │
│ ipsec-crypto-profiles    Clone IPsec crypto profiles                                                                                                                                                                                                 │
│ log-forwarding-profiles  Clone log forwarding profiles                                                                                                                                                                                               │
│ nat-rules                Clone NAT rules                                                                                                                                                                                                             │
│ quarantined-devices      Clone quarantined devices                                                                                                                                                                                                   │
│ regions                  Clone region objects                                                                                                                                                                                                        │
│ remote-networks          Clone remote network objects                                                                                                                                                                                                │
│ schedules                Clone schedule objects                                                                                                                                                                                                      │
│ security-rules           Clone security rules                                                                                                                                                                                                        │
│ service-groups           Clone service groups                                                                                                                                                                                                        │
│ services                 Clone service objects                                                                                                                                                                                                       │
│ settings                 Create a `settings.yaml` file with configuration needed to accomplish our tasks (required one-time setup)                                                                                                                   │
│ syslog-server-profiles   Clone syslog server profiles                                                                                                                                                                                                │
│ tags                     Clone tag objects                                                                                                                                                                                                           │
│ url-categories           Clone URL categories                                                                                                                                                                                                        │
│ vulnerability-profiles   Clone vulnerability protection profiles                                                                                                                                                                                     │
│ wildfire-profiles        Clone Wildfire AV profiles                                                                                                                                                                                                 │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯

```

</div>

For more detailed usage instructions and examples, refer to the [User Guide](user-guide/introduction.md).

---

## Contributing

Contributions are welcome and greatly appreciated. Visit the [Contributing](about/contributing.md) page for guidelines
on how to contribute.

## License

This project is licensed under the Apache 2.0 License - see the [License](about/license.md) page for details.
