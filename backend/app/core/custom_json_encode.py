from uuid import UUID
from fastapi.encoders import jsonable_encoder


def json_encoder(obj):
    if isinstance(obj, UUID):
        return str(obj)
    return jsonable_encoder(obj)