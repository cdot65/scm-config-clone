# Getting Started with scm-config-clone

This guide will help you get started with `scm-config-clone`, from initial configuration to your first cloning
operation.

## Step 1: Create a Settings File

Before cloning configurations, you need to create a `settings.yaml` file containing your SCM credentials, logging
preferences, and default operational flags (e.g., `auto_approve`, `dry_run`, `quiet`, `create_report`).

To create the `settings.yaml` file, run:

<div class="termy">
<!-- termynal -->
```bash
scm-clone settings
```

</div>

You will be prompted to enter:

- Source SCM credentials (client_id, client_secret, tsg_id)
- Destination SCM credentials (client_id, client_secret, tsg_id)
- Logging level (e.g., INFO)
- Additional options like `auto_approve`, `create_report`, `dry_run`, and `quiet`.

After completion, `settings.yaml` is generated in your current directory, it should look like:

```yaml
oauth:
  source:
    client_id: "source_client_id"
    client_secret: "source_client_secret"
    tsg: "source_tsg_id"
  destination:
    client_id: "dest_client_id"
    client_secret: "dest_client_secret"
    tsg: "dest_tsg_id"
logging: INFO
auto_approve: false
create_report: false
dry_run: false
quiet: false
```

Once `settings.yaml` is in place, all subsequent commands will use these defaults.

## Step 2: Cloning Configurations

With `settings.yaml` ready, you can clone various objects without having to re-enter credentials. For example, to clone
address objects:

<div class="termy">
<!-- termynal -->
```bash
scm-clone addresses --folder "Texas"
```
</div>

If `auto_approve` is `false`, you'll be prompted before actually creating the objects. The tool retrieves objects from
the specified folder (`Texas`), displays them (unless `quiet` is enabled), and asks for confirmation (if
`auto_approve` is not set to true).

If you decide you want to run in dry-run mode or commit changes after creation, simply add the corresponding flags:

- Dry-run:

  <div class="termy">
  <!-- termynal -->
  ```bash
  scm-clone addresses --folder "Texas" -D
  ```
  </div>

- Commit after creation:

  <div class="termy">
  <!-- termynal -->
  ```bash
  scm-clone addresses --folder "Texas" --commit-and-push
  ```
  </div>

## Step 3: Cloning Other Objects

Just like addresses, you can clone:

- Tag objects: `scm-clone tags --folder "Texas"`
- Services: `scm-clone services --folder "Texas"`
- Security rules: `scm-clone security-rules --folder "cdot65"`

Each command respects the defaults in `settings.yaml`, and you can override them at runtime with flags like `-A` for
auto-approve or `-Q` for quiet mode.

## Next Steps

With your `settings.yaml` in place and an understanding of how to run commands, you can:

- Leverage filtering flags (`--exclude-folders`, `--exclude-snippets`, `--exclude-devices`) to narrow down what gets
  cloned.
- Use `--create-report` to record the outcome of cloning operations in `result.csv`.
- Adjust `--logging-level` for more or less verbosity.

For more detailed reference on commands and their arguments, see the [Commands Reference](commands.md)
and [Examples](examples.md) pages.
