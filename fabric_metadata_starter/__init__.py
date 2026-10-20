"""fabric-metadata-starter: the minimal metadata model that makes Fabric pipelines generatable."""
from .model import BusinessObject, Metadata, SourceObject, SourceSystem, load_metadata
from .generate import render_all

__all__ = ["BusinessObject", "Metadata", "SourceObject", "SourceSystem", "load_metadata", "render_all"]
__version__ = "0.1.0"
