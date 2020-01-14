from commons.dosql import get_db
from commons.sql_info import *
from commons.decorator_log import logs

@logs
def get_tt_data(suite_num):
    tidlist = []
    sql1 = "select project_name,test_suite_name from project_list,test_suite_list " \
          "where test_suite_list.id = %d and project_list.id = test_suite_list.suite_relation_project" % suite_num
    sql2 = "select case_describe,req_method,req_host,req_params,req_headers,req_datatype,req_body," \
           "cache_extract_data,assert_extract_data,expected_value,contrast,sql_info,sql_method,sql_statements" \
           " from test_case_list where case_relation_suite = %d order by case_code" % suite_num
    sql3 = "select case_code from test_case_list where case_relation_suite = %d order by case_code" % suite_num
    conn = get_db(db_info)
    name_row = conn.mysql_rows_init(sql1)
    tdata_row = conn.mysql_rows_init(sql2)
    case_id = conn.mysql_rows_init(sql3)
    conn.mysql_close()
    suite_name = name_row[0][0] + "---" + name_row[0][1]
    tdata = tdata_row
    for i in case_id:
        for j in i:
            tidlist.append(j)
    return suite_name,tdata,tidlist
