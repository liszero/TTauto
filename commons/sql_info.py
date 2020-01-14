import re
from commons.decorator_log import logs

db_info = {
    "host":"47.110.245.238",
    "port":3306,
    "user":"autotest",
    "passwd":"Autotest@123",
    "db_name":"autotest"
}

@logs
def get_sql_info(sql_info):
    tmpdict = {}
    a = re.compile("^(.*?):(.*?)--(.*?):(.*?)_(.*?)$")
    result = a.search(sql_info).groups(0)
    tmpdict["user"] = result[0]
    tmpdict["passwd"] = result[1]
    tmpdict["host"] = result[2]
    tmpdict["port"] = int(result[3])
    tmpdict["db_name"] = result[4]
    return tmpdict
