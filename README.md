# Tagbot

Tagbot is a tool for retagging OCI Container Images directly using the registry API, eliminating the need for a full Docker Pull/Push workflow.

## Features

- Add multiple tags to an image without pulling or pushing.
- Efficient and API-driven.

## Usage

### Local Usage

To use Tagbot locally, run:

```shell
tagbot \
    --username <your-username> \
    --password <your-password> \
    --source <registry>/<image>:<tag> \
    --tags <tag1>,<tag2>
```

#### Example:
```shell
tagbot \
    --username example \
    --password password \
    --source example.azurecr.io/debian:latest \
    --tags v1.0.0,1.0.0
```

This command adds the tags `v1.0.0` and `1.0.0` to `example.azurecr.io/debian:latest`. The image can then be pulled using any of the following tags:

- `example.azurecr.io/debian:latest`
- `example.azurecr.io/debian:v1.0.0`
- `example.azurecr.io/debian:1.0.0`

### GitHub Actions Usage

```yaml
name: release

on:
  push:
    tags: ["v[0-9]+.[0-9]+.[0-9]+"]

jobs:
  release:
    uses: cpressland/tagbot/.github/workflows/retag.yaml@master
    with:
      username: example
      source: example.azurecr.io/${{ github.event.repository.name }}:${{ github.ref_name }}
      tags: ${{ matrix.environment }}-v1.0.0,${{ matrix.environment }}
      environment:  ${{ matrix.environment }}
    secrets:
      password: ${{ secrets.ACR_PASSWORD }}
    strategy:
      matrix:
        environment: [staging, production]
```

## FAQ

- **Q**: Are registries other than Azure Container Registry supported?<br>
  **A**: Azure Container Registry is the only officially supported registry. However, other registries, such as Docker Hub, Amazon ECR, and Google Container Registry, are likely to work if they conform to standard OCI APIs.
- **Q**: Does Tagbot require admin-level credentials for the registry?<br>
  **A**: No, it only requires permissions to read and write tags for the specified images.
- **Q**: Can I retag multiple images in a single command?<br>
  **A**: No, Tagbot currently supports retagging one image at a time. Use a script or automation tool to process multiple images.
- **Q**: Are there any size limitations for the images being retagged?<br>
  **A**: No, since Tagbot operates at the registry level, the image size is irrelevant.
- **Q**: Is Tagbot secure to use with my credentials?<br>
  **A**: Tagbot does not store your credentials and only uses them for the duration of the operation. For additional security, use environment variables or secret management tools.
- **Q**: Can I remove a tag from an image using Tagbot?<br>
  **A**: No, Tagbot only supports adding new tags. To remove tags, use your registry's management tools.
- **Q**: What happens if the specified tag already exists?<br>
  **A**: If the tag already exists, Tagbot will reassign it to the source image.
- **Q**: Is there a dry-run mode to test without making changes?<br>
  **A**: Currently, Tagbot does not support a dry-run mode.
