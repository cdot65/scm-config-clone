# Getting Started with scm-config-clone

Welcome to the `scm-config-clone` tool! This guide will walk you through the initial setup and basic usage of the tool.

## Step 1: Create a Secrets File

Before cloning configurations, you need to create a `.secrets.yaml` file containing your SCM credentials.

Run the following command:

<div class="termy">

<!-- termynal -->
```bash
$ scm-clone create-secrets-file
```
</div>

You'll be prompted to enter your source and destination SCM credentials.

**Sample Interaction:**

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

## Step 2: Clone Address Objects

To clone address objects from the source to the destination tenant, run:

<div class="termy">

<!-- termynal -->
```bash
$ scm-clone clone-address-objects
```
</div>

The tool will use the credentials from `.secrets.yaml`.

## Step 3: Clone Address Groups

To clone address groups, run:

<div class="termy">

<!-- termynal -->
```bash
$ scm-clone clone-address-groups
```
</div>

---

You've successfully set up and used `scm-config-clone` to clone configurations between SCM tenants. For more advanced usage and options, refer to the [Commands](commands.md) section.
