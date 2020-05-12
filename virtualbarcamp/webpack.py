import json
import os

import requests
from django.conf import settings
from django.http import HttpRequest


def assets_from_manifest(manifest, static_base, include_integrity):
    return {
        entrypoint: {
            "css": [
                {
                    "url": f"{static_base}{chunk}",
                    "integrity": manifest["assets"][chunk]["integrity"]
                    if include_integrity
                    else "",
                }
                for chunk in chunks
                if chunk.endswith(".css")
            ],
            "js": [
                {
                    "url": f"{static_base}{chunk}",
                    "integrity": manifest["assets"][chunk]["integrity"]
                    if include_integrity
                    else "",
                }
                for chunk in chunks
                if chunk.endswith(".js")
            ],
        }
        for entrypoint, chunks in manifest["chunks"].items()
    }


if settings.WEBPACK_DEV_SERVER_MANIFEST:

    def load_assets():
        response = requests.get(settings.WEBPACK_DEV_SERVER_MANIFEST)
        response.raise_for_status()
        return assets_from_manifest(response.json(), "http://localhost:3000/", False)


else:
    with open(os.path.join(settings.STATIC_ROOT), "manifest.json") as manifest_file:
        _assets = assets_from_manifest(json.load(manifest_file), settings.STATIC_URL, True)

    def load_assets():
        return _assets


def context_processor(request: HttpRequest):
    return {"webpack_assets": load_assets()}
