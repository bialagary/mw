# -*- coding: utf-8 -*-
#------------------------------------------------------------

import traceback
import plugintools

def load_json(data):
    plugintools.log("jsontools.load_json Probando simplejson en directorio lib")

    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct

    try:
        plugintools.log("jsontools.load_json Probando simplejson en directorio lib")
        from lib import simplejson
        json_data = simplejson.loads(data, object_hook=to_utf8)
        plugintools.log("jsontools.load_json -> "+repr(json_data))
        return json_data
    except:
        plugintools.log(traceback.format_exc())

        try:
            plugintools.log("jsontools.load_json Probando simplejson incluido en el interprete")
            import simplejson
            json_data = simplejson.loads(data, object_hook=to_utf8)
            plugintools.log("jsontools.load_json -> "+repr(json_data))
            return json_data
        except:
            plugintools.log(traceback.format_exc())
            
            try:
                plugintools.log("jsontools.load_json Probando json incluido en el interprete")
                import json
                json_data = json.loads(data, object_hook=to_utf8)
                plugintools.log("jsontools.load_json -> "+repr(json_data))
                return json_data
            except:
                plugintools.log(traceback.format_exc())

                try:
                    plugintools.log("jsontools.load_json Probando JSON de Plex")
                    json_data = JSON.ObjectFromString(data, encoding="utf-8")
                    plugintools.log("jsontools.load_json -> "+repr(json_data))
                    return json_data
                except:
                    plugintools.log(traceback.format_exc())

    plugintools.log("jsontools.load_json No se ha encontrado un parser de JSON valido")
    plugintools.log("jsontools.load_json -> (nada)")
    return ""

