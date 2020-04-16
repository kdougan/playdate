import io
from flask import Response
from flask import request
from flask import abort
from flask import send_file


from depot.manager import DepotManager


def asset_store_route(path):
    depot = DepotManager.get()

    stored_file = DepotManager.get_file(path)
    contents = stored_file.read()
    return send_file(io.BytesIO(contents),
                     mimetype=stored_file.content_type)
