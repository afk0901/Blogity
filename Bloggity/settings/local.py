"""Extends Django settings for Bloggity project intended to be used for local
environment."""

from Bloggity.settings.base import *  # noqa: F403, F401

INTERNAL_IPS = [
    "127.0.0.1",
]
