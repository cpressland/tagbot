"""Main module for Tagbot."""

import re

import click
import requests
from loguru import logger as log


def tagbot(username: str, password: str, source: str, new_tags: str) -> None:
    """Tag a container image in a registry.

    Args:
        username (str): Username for Container Registry
        password (str): Password for Container Registry
        source (str): Source Container Image and Tag
        new_tags (str): New Container Image Tags, comma seperated

    Returns:
        None

    """
    registry, image, tag = re.split("[:/]", source)

    try:
        source_image = requests.get(
            f"https://{registry}/v2/{image}/manifests/{tag}",
            headers={
                "Accept": (
                    "application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.manifest.v1+json"
                ),
            },
            auth=(username, password),
            timeout=30,
        )
        source_image.raise_for_status()
    except requests.exceptions.HTTPError:
        log.exception(source_image.text)

    for new_tag in new_tags.split(","):
        log.info(f"Tagging {registry}/{image}:{tag} to {registry}/{image}:{new_tag}")
        try:
            dest_image = requests.put(
                f"https://{registry}/v2/{image}/manifests/{new_tag}",
                headers={"Content-Type": source_image.headers["Content-Type"]},
                auth=(username, password),
                data=source_image.text,
                timeout=30,
            )
            dest_image.raise_for_status()
        except requests.exceptions.HTTPError:
            log.exception(dest_image.text)


@click.command()
@click.option("--username", "-u", required=True, help="Username for Container Registry")
@click.option("--password", "-p", required=True, help="Password for Container Registry")
@click.option("--source", "-s", required=True, help="Source Container Image")
@click.option("--tags", "-t", required=True, help="New Container Image Tags, comma seperated")
def cli(username: str, password: str, source: str, tags: str) -> None:
    """Tagbot: Tag a container image in a registry."""
    tagbot(username=username, password=password, source=source, new_tags=tags)
