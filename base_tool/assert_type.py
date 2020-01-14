import re

def as_type(num):
    str = ""
    if num == 1:
        str = "等于"
    elif num == 2:
        str = "小于"
    elif num == 3:
        str = "小于等于"
    elif num == 4:
        str = "大于"
    elif num == 5:
        str = "大于等于"
    elif num == 6:
        str = "包含"
    elif num == 7:
        str = "不包含"
    return str

# 断言封装
def assert_result(nums,source_list,expected_data,contrast):
    global s_data,e_data
    expected_list = expected_data.split(",")
    if is_number(source_list[nums]):
        s_data = float(source_list[nums])
        if len(expected_list) == 1:
            e_data = float(expected_list[0])
        else:
            e_data = float(expected_list[nums])
    else:
        s_data = source_list[nums]
        if len(expected_list) == 1:
            e_data = expected_list[0]
        else:
            e_data = expected_list[nums]

        if contrast == 1:
            if e_data == s_data:
                return True
            else:
                return False

        if contrast == 2:
            if e_data < s_data:
                return True
            else:
                return False

        if contrast == 3:
            if e_data <= s_data:
                return True
            else:
                return False

        if contrast == 4:
            if e_data > s_data:
                return True
            else:
                return False

        if contrast == 5:
            if e_data >= s_data:
                return True
            else:
                return False

        if contrast == 6:
            if re.search(str(e_data),str(s_data)):
                return True
            else:
                return False

        if contrast == 7:
            if not re.search(str(e_data),str(s_data)):
                return True
            else:
                return False

        if contrast == "" or contrast == None:
            return True

def is_number(strs):
    pattern = re.compile(r'^[-+]?[-0-9]\d*\.\d*|[-+]?\.?[0-9]\d*$')
    result = pattern.match(str(strs))
    if result:
        return True
    else:
        return False

