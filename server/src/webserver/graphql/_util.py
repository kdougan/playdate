import json
from graphene.types import Scalar


class Asset(Scalar):
    @staticmethod
    def serialize(asset):
        paths = {}
        for k, v in asset.items():
            if k.endswith('path'):
                paths[k] = v
        return paths


class Meta(Scalar):
    @staticmethod
    def serialize(meta):
        return meta
