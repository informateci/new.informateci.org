from config import api_version
from functools import wraps
import dicttoxml
import yaml
import phpserialize
from flask import Response
import json
import StringIO
from flask import jsonify, request


def out_format(view_function):
        """
            Decora la risposta di una chiamata API
            - restituisce nel formato specificato dal parametro f= (xml, ...) con massima priorita'
            - se il client invia un accept header e non specifica il parametro f= fa fede l'header
            - json e' comunque il default

        """
        @wraps(view_function)
        def decorated_function(*args, **kwargs):

            replyjson = jsonify(view_function(*args, **kwargs))
            oi = json.loads(replyjson.data)

            def xml_f(i, o):
                r = dicttoxml.dicttoxml(i)
                return Response(r, mimetype=o)

            def yaml_f(i, o):
                r = yaml.safe_dump(i, allow_unicode=True)
                return Response(r, mimetype=o)

            def php_f(i, o):
                output = StringIO.StringIO()
                phpserialize.dump(i, output, charset='utf-8')
                r = output.getvalue()
                output.close()
                return Response(r, mimetype=o)

            def json_f(i, o):
                return replyjson

            fun_f = {"application/xml":  xml_f,
                     "application/x-yaml": yaml_f,
                     "application/vnd.php.serialized":  php_f,
                     "application/json": json_f}

            acc_name = {"xml": "application/xml",
                        "yaml": "application/x-yaml",
                        "php": "application/vnd.php.serialized",
                        "json": "application/json"
                        }

            frmt = request.args.get('f', None)

            if frmt is None:
                frmt = request.accept_mimetypes.best_match(["application/json", "application/xml", "application/x-yaml",
                                                            "application/vnd.php.serialized"]) or "application/json"
            else:
                frmt = acc_name.get(frmt, "application/json")

            return (fun_f.get(frmt, json_f))(oi, frmt)

        return decorated_function


def err_resp(name, msg):
    return {"v": api_version, "Error": "True", "Name": name, "msg": msg}


def ok_resp(**d):
    d.update({"v": api_version, "Error": "None"})
    return d