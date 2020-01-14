import pytest
import re
import os

def run_main():
    # 运行测试用例
    pytest.main()
    # 生成测试报告
    curpath = os.path.dirname(os.path.realpath(__file__))
    os.chdir(curpath)
    lists = os.listdir("report")
    attach = re.compile(".*?\.attach")
    jso = re.compile(".*?\.json")
    txt = re.compile(".*?\.txt")
    os.system(r"allure generate --clean report\ -o report\report_html")

    report_dirpath = os.path.join(curpath, "report")
    os.chdir(report_dirpath)
    for j in lists:
        t = txt.findall(j)
        if t != []:
            os.remove(t[0])
        m = attach.findall(j)
        if m != []:
            os.remove(m[0])
        n = jso.findall(j)
        if n != []:
            os.remove(n[0])

if __name__ == "__main__":
    run_main()