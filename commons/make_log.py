import time
import logging

def get_logger():
    # 获取logger实例，如果参数为空则返回root logger
    logname = '%s.log' % time.strftime('%Y_%m_%d')
    logger = logging.getLogger()
    if not logger.handlers:
        # 指定logger输出格式
        formatter = logging.Formatter()

        # 文件日志
        file_handler = logging.FileHandler(logname,encoding="utf8")
        file_handler.setFormatter(formatter)  # 可以通过setFormatter指定输出格式

        # 为logger添加的日志处理器
        logger.addHandler(file_handler)

        # 指定日志的最低输出级别，默认为WARN级别
        logger.setLevel(logging.INFO)
    #  添加下面一句，在记录日志之后移除句柄
    return logger