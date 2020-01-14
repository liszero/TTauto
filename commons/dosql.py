import pymysql
from commons.decorator_log import logs

class get_db():
    @logs
    def __init__(self,db_info):
        self.conn = pymysql.connect(host=db_info["host"],port=db_info["port"],
                                    user=db_info["user"],password=db_info["passwd"],
                                    database=db_info["db_name"],charset="utf8")
        self.redis_info = db_info

    # 读取测试数据方法
    def mysql_rows_init(self, sql):
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cur.close()
        return rows

    # 查询返回所有结果
    @logs
    def mysql_rows(self, sql):
        tmplist = []
        cur = self.conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = cur.description
        for i in rows:
            num = 0
            tmpdict = {}
            for j in cols:
                tmpdict[j[0]] = i[num]
                num += 1
            tmplist.append(tmpdict)
        cur.close()
        self.conn.close()
        return tmplist

    # 执行增/删/改命令
    @logs
    def mysql_execute(self, sql):
        cur = self.conn.cursor()
        try:
            cur.execute(sql)
        except Exception as e:
            self.conn.rollback()
            return e
        else:
            self.conn.commit()
            cur.close()
            self.conn.close()
            return ""

    def mysql_close(self):
        self.conn.close()
