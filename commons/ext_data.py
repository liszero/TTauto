import jsonpath,re
from commons.decorator_log import logs

@logs
def ass_ex_data(sourcedata,jspath):
    rule = ""
    if re.search("sql(.*?)",jspath):
        rule = re.sub("sql","$",jspath,1)
    elif re.search("header(.*?)",jspath):
        rule = "$." + jspath
    elif re.search("body(.*?)",jspath):
        rule = "$." + jspath
    result = jsonpath.jsonpath(sourcedata,rule)
    return result[0]


@logs
def cache_ex_data(sourcedata,jspath):
    rule = ""
    tmpdict = eval(jspath)
    key,value = list(tmpdict.items())[0]
    if re.search("sql(.*?)",value):
        rule = re.sub("sql","$",value,1)
    elif re.search("header(.*?)",value):
        rule = "$." + value
    elif re.search("body(.*?)",value):
        rule = "$." + value
    result = jsonpath.jsonpath(sourcedata,rule)
    return key,result[0]
