
import json

from datetime import datetime

from flask import abort
from flask import request


class RequestParser(object):

    dte_frmt = '%Y-%m-%d %H:%M:%S'

    def __init__(self):
        """Initialize."""
        self.args = {}

    @classmethod
    def _bool(cls, ans):
        return str(ans).lower() in ['true', '1', 't', 'y', 'yes', 'on']

    def add_argument(self, key, type=None, required=False,
                     help='', force=True, **kwargs):
        """Add argument."""
        self.args[key] = {'type': type,
                          'required': required,
                          'help': help,
                          'force': force}
        if 'default' in kwargs:
            self.args[key].setdefault('default', kwargs['default'])
        if 'format' in kwargs:
            self.args[key].setdefault('format', kwargs['format'])

    def parse_args(self, location=None):
        """Parse args."""
        data = {}
        errors = []

        if location and isinstance(location, dict):
            data = location
        else:
            if ('Content-Type' in request.headers and
                    'text/plain' in request.headers['Content-Type']):
                try:
                    data.update(json.loads(request.data))
                except Exception as e:
                    print(e)
                    data.update({'_data': request.data})
            if request.is_json:
                data.update(request.get_json())
            data.update(request.args.to_dict())
            data.update(request.form.to_dict())

        for key, value in self.args.items():

            _type = value['type']
            _required = value['required']
            _help = value['help']
            _force = value['force']

            if (_required and key not in data):
                errors.append(_help + '.' if _help[-1] is not '.' else _help)

            if key in data:
                if _type == bool:
                    data[key] = RequestParser._bool(data[key])
                if _type == datetime:
                    frmt = RequestParser.dte_frmt
                    if 'format' in value:
                        frmt = value['format']
                    try:
                        data[key] = datetime.strptime(data[key], frmt)
                    except Exception as e:
                        errors.append(f'{key} {e}')
                        break
                if _type and _force:
                    if _type == list and not isinstance(data[key], list):
                        data[key] = [data[key]]
                    try:
                        if _type == str and data[key] is None:
                            data[key] = ''
                        else:
                            data[key] = _type(data[key])
                    except:
                        pass
                if (_type and not isinstance(data[key], _type)):
                    print(data[key])
                    errors.append(f'{key} not of type "{_type.__name__}", '
                                  f'received "{type(data[key]).__name__}."')
            elif 'default' in value:
                data[key] = value['default']

        if errors:
            abort(400, errors)
        return data
