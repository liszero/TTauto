import allure,pytest,re,sys,getopt
from commons.base_req import base_request
from commons.dosql import get_db
from commons.sql_info import *
from commons.ext_data import *
from base_tool import get_test_data
from base_tool.assert_type import *

class Test_interface():
    global nums

    # 获取命令行变量
    try:
        argvs = sys.argv[1:]
        options, args = getopt.getopt(argvs, "s:", ["suite="])
    except getopt.GetoptError:
        sys.exit()

    for option, value in options:
        if option in ("--suite"):
            nums = value

    # 获取测试名称，测试用例，测试用例编号
    name,datas,case_id = get_test_data.get_tt_data(int(nums))

    @allure.feature(name)
    @pytest.mark.parametrize("case_describe,req_method,req_host,req_params,req_headers,"
                             "req_datatype,req_body,cache_extract_data,"
                             "assert_extract_data,expected_value,contrast,"
                             "sql_info,sql_method,sql_statements",datas,ids=case_id)
    def test_cases(self,request,case_describe,req_method,req_host,req_params,req_headers,
                  req_datatype,req_body,cache_extract_data,
                  assert_extract_data,expected_value,contrast,
                  sql_info,sql_method,sql_statements):

        # 定义变量，及正则规则
        checklist = []
        checkstrings = ""
        s = re.compile("{{(.*?)}}")

        # 获取断言方法中文
        if contrast != None:
            tmpstring = as_type(contrast)
        else:
            tmpstring = ""

        # 执行sql语句，如果是查询保存查询结果到函数变量checkstrings中
        if sql_info != None and sql_info != "":
            sql_infos = get_sql_info(sql_info)
            if sql_method == 2:
                checkstrings = get_db(sql_infos).mysql_rows(sql_statements)
            else:
                get_db(sql_infos).mysql_execute(sql_statements)

        # 判断请求地址不为空，走请求分支
        if req_host != None and req_host != "":

            # 根据正则规则，在params中匹配，有变量从缓存中提取,替换成完整请求数据
            if req_params != None and req_params != "":
                if s.search(req_params) != None:
                    tmplist = s.findall(req_params)
                    for i in tmplist:
                        d = request.config.cache.get(i,None)
                        req_params = re.sub(i,d,req_params,1)

            # 根据正则规则，在headers中匹配，有变量从缓存中提取,替换成完整请求数据
            if req_headers != None and req_headers != "":
                if s.search(req_headers) != None:
                    tmplist = s.findall(req_headers)
                    for i in tmplist:
                        d = request.config.cache.get(i,None)
                        req_headers = re.sub("{{%s}}" % i,d,req_headers,1)

            # 根据正则规则，在bodys中匹配，有变量从缓存中提取,替换成完整请求数据
            if req_body != None and req_body != "":
                if s.search(req_body) != None:
                    tmplist = s.findall(req_body)
                    for i in tmplist:
                        d = request.config.cache.get(i,None)
                        req_body = re.sub(i,d,req_body,1)

            # 接口发送请求，获取数据
            res = base_request(req_method, req_host, req_params, req_headers, req_datatype, req_body)
            r_dt = res.run_request()

            # 判断是否提取缓存数据，存在则判断是否是sql提取，是在查询sql中提取，不是则在响应数据中提取
            if cache_extract_data != None and cache_extract_data != "":
                tmplist = cache_extract_data.split(",")
                for i in tmplist:
                    tmpdict = eval(i)
                    _, val = list(tmpdict.items())[0]
                    if re.search("sql(.*?)",val):
                        key, value = cache_ex_data(checkstrings, i)
                    else:
                        key, value = cache_ex_data(r_dt,i)
                    request.config.cache.set(key, value)

            # 判断是否提取断言数据，如存在从响应数据中断言数据，添加到断言列表中,不存在赋值给函数变量checkstrings
            if assert_extract_data != None and assert_extract_data != "":
                tmplist = assert_extract_data.split(",")
                for i in tmplist:
                    a = ass_ex_data(r_dt,i)
                    checklist.append(a)
            else:
                checkstrings = str(r_dt["body"])

            # 将断言提取数据变为字符串
            tmpstrs = ",".join(checklist)

            # 测试报告中数据输出
            with allure.step("测试数据"):
                allure.attach("%s" % case_describe, "测试用例描述")
                allure.attach("%s" % r_dt["costtime"], "接口响应时间")
                allure.attach("%s" % req_method,"请求方法")
                allure.attach("%s" % req_host,"请求路径")
                allure.attach("%s" % req_params,"请求参数")
                allure.attach("%s" % req_headers,"请求头")
                allure.attach("%s" % req_datatype,"请求数据方式")
                allure.attach("%s" % req_body,"请求体")
                allure.attach("%s" % str(r_dt["header"]),"响应头")
                allure.attach("%s" % str(r_dt["body"]),"响应体")
                allure.attach("%s" % tmpstrs,"断言提取数据")
                allure.attach("%s" % expected_value, "预期结果")
                allure.attach("%s" % tmpstring, "断言方式")

        # 走数据库分支
        else:
            # 判断是否提取缓存数据，如存在从数据库查询返回数据中提取，并加入缓存
            if cache_extract_data != None and cache_extract_data != "":
                tmplist = cache_extract_data.split(",")
                for i in tmplist:
                    key, value = cache_ex_data(checkstrings, i)
                    request.config.cache.set(key, value)

            # 判断是否提取断言数据，如存在从数据库查询返回数据中提取断言数据
            if assert_extract_data != None and assert_extract_data != "":
                tmplist = assert_extract_data.split(",")
                for i in tmplist:
                    a = ass_ex_data(checkstrings, i)
                    checklist.append(a)

            # 测试报告中数据输出
            with allure.step("测试数据"):
                allure.attach("%s" % case_describe, "测试用例描述")
                allure.attach("%s" % str(sql_statements), "数据库操作语句")
                allure.attach("%s" % str(checkstrings), "数据库数据")
                allure.attach("%s" % str(checklist), "断言提取数据")
                allure.attach("%s" % expected_value, "预期结果")
                allure.attach("%s" % tmpstring, "断言方式")

        # 判断是否有预期值，存在预期值，判断断言提取是否存在，存在断言列表与预期值列表比较，
        # 如不存在预期值，直接使用函数变量checkstrings和预期值进行比较
        # 如果判断没有预期值，忽略断言
        if expected_value != None and expected_value != "":
            if assert_extract_data != None and assert_extract_data != "":
                for i in range(len(checklist)):
                    assert assert_result(i,checklist,expected_value,contrast) == True
            else:
                tmplist = []
                tmplist.append(checkstrings)
                for i in range(len(tmplist)):
                    assert assert_result(i,tmplist, expected_value, contrast) == True
        else:
            pass
