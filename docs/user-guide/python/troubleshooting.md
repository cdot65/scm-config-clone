# Troubleshooting Guide

If you encounter issues while using `scm-config-clone`, this guide provides solutions to common problems.

## Common Issues and Solutions

### 1. Authentication Failures

**Problem:** Error authenticating with source or destination tenant.

**Solution:**

- Ensure that your credentials in `settings.yaml` are correct.
- Verify that your client IDs and secrets are valid.
- Check for typos in the tenant TSG values.
- For SASE deployments, ensure you're using the correct credentials in the SASE section of settings.yaml.
- Try increasing the logging level with `--logging-level DEBUG` for more detailed error information.

### 2. Network Connectivity Issues

**Problem:** Unable to connect to the SCM or SASE tenants.

**Solution:**

- Check your internet connection.
- Ensure that there are no firewall rules blocking outbound connections.
- Verify that the API endpoint URLs are accessible from your environment.
- For proxy environments, ensure proper proxy configuration is set up.

### 3. Context Type Issues

**Problem:** Errors related to folder, snippet, or device context parameters.

**Solution:**

- Ensure exactly one context type (folder, snippet, or device) is provided.
- Verify that the context name exists in both source and destination tenants.
- If using multiple context types, check that you're using the newer `--context` parameter with `--source` and `--destination`.
- For legacy parameters, ensure you're using `--source-folder` and `--destination-folder`.

### 4. Object Cloning Errors

**Problem:** Errors occur when cloning specific objects.

**Solution:**

- Check if the source object contains all required fields (use `--logging-level DEBUG`).
- Verify that there are no naming conflicts in the destination tenant.
- For complex objects (like security rules or SASE objects), ensure all referenced objects exist in the destination tenant.
- When cloning between different tenant types (e.g., from SCM to SASE), verify object compatibility.

### 5. Folder/Snippet/Device Not Found

**Problem:** Specified folder, snippet, or device does not exist.

**Solution:**

- Double-check that the specified context path exists in the tenant.
- Ensure you're using the exact name (case-sensitive).
- For nested contexts, verify the full path.
- Use the appropriate context type (`--context folder|snippet|device`).

### 6. Commit Failures

**Problem:** Unable to commit changes after object creation.

**Solution:**

- Ensure the destination tenant allows API-driven commits.
- Check if the destination folder is locked by another administrator.
- Verify that the created objects don't violate any tenant validation rules.
- Note that commit operations are not supported with snippet contexts.

### 7. Report Generation Issues

**Problem:** Result.csv file not created or incomplete when using `-R` flag.

**Solution:**

- Check write permissions in the current directory.
- Ensure no other process has the file locked.
- For large operations, verify that the file isn't being truncated.

## Advanced Troubleshooting

### Debugging with Verbose Logging

Increase the logging level to get more detailed information:

```bash
scm-clone <command> --source "Source" --logging-level DEBUG
```

This will provide detailed API request/response information and error traces.

### API Rate Limiting

If you encounter rate limiting errors:

- Reduce the batch size of operations.
- Add delays between operations.
- Contact your SCM/SASE administrator to check API quotas.

### Validating Objects Before Cloning

Use the `--dry-run` flag to validate operations without making changes:

```bash
scm-clone <command> --source "Source" --destination "Destination" -D
```

This will simulate the cloning process without actually creating objects.

## Logging

`scm-config-clone` provides comprehensive logging to help diagnose issues. Use the `--logging-level` parameter to adjust the verbosity:

- `INFO`: Standard operational information (default)
- `DEBUG`: Detailed debugging information including API requests/responses
- `WARNING`: Only warnings and errors
- `ERROR`: Only error messages
- `CRITICAL`: Only critical failures

## Getting Help

If you're unable to resolve an issue, please open an issue on
our [GitHub repository](https://github.com/cdot65/scm-config-clone/issues) with the following information:

- The exact command you ran
- Complete error messages (with --logging-level DEBUG if possible)
- Your environment details (OS, Python version)
- Description of the SCM/SASE tenant types you're working with
