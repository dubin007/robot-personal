import os
import sqlalchemy as db
from src.util.log import LogSupport

ls = LogSupport()
class SQLiteConnect:
    '''SQLite 数据库接口封装类'''

    def __init__(self, db_file):
        create_tables = not os.path.isfile(db_file)
        self.engine = db.create_engine('sqlite:///{}'.format(db_file))
        self.conn = self.engine.connect()
        self.metadata = db.MetaData()
        self.cities_list = []
        self.initialize_tables(create_tables)

    def initialize_tables(self, create_tables=False):
        self.subscriptions = db.Table('subscriptions', self.metadata,
                                      db.Column('id', db.Integer(), primary_key=True, nullable=False),
                                      db.Column('uid', db.String(255), nullable=False),
                                      db.Column('city', db.String(255), nullable=False),
                                      )
        self.update_flag = db.Table('update_flag', self.metadata,
                                    db.Column('id', db.Integer(), primary_key=True, nullable=False),
                                    db.Column("flag", db.Integer()))

        if create_tables:
            try:
                self.metadata.create_all(self.engine)
                query = db.insert(self.update_flag).values(id=1, flag=0)
                res = self.conn.execute(query)
                ls.logging.info("初始化数据库成功: {}".format(res.rowcount))
            except BaseException as e:
                ls.logging.error("初始化数据库出错")
                ls.logging.exception(e)

    def do_update_flag(self, flag):
        try:
            update = db.update(self.update_flag).where(self.update_flag.columns.id==1).values(flag=flag)
            res = self.conn.execute(update)
            return res.rowcount
        except BaseException as e:
            ls.logging.error("更新update flag出错")
            ls.logging.exception(e)
            return 0

    def get_update_flag(self):
        try:
            query = db.select([self.update_flag]).where(self.update_flag.columns.id==1)
            result_proxy = self.conn.execute(query)
            result = result_proxy.fetchone()
            return result[1]
        except BaseException as e:
            ls.logging.error("获取update flag 出错")
            ls.logging.exception(e)
            return 0

    def save_subscription(self, uid, city):
        '''保存一个用户对于制定城市的订阅'''
        # TODO: add feedback for invalid input
        try:
            # 插入数据
            query = db.insert(self.subscriptions).values(uid=uid, city=city)
            self.conn.execute(query)
            return 0
        except BaseException as e:
            raise e

    def query_subscription(self, uid, city):
        query = db.select([self.subscriptions]).where(
            db.and_(
                self.subscriptions.columns.uid == uid,
                self.subscriptions.columns.city == city
            )
        )
        result_proxy = self.conn.execute(query)
        result = result_proxy.fetchone()
        return result

    def cancel_subscription(self, uid, city):
        """
        '''取消一个用户对于指定城市的订阅'''
        成功删除返回一个对象，否则返回影响的行数
        :param uid:
        :param city:
        :return:
        """
        query = db.delete(self.subscriptions).where(
            db.and_(
                self.subscriptions.columns.uid == uid,
                self.subscriptions.columns.city == city
            )
        )
        res = self.conn.execute(query)

        return res.rowcount

    def get_subscribed_users(self, city):
        '''获取所有订阅指定城市的用户'''
        # TODO: add feedback for invalid input
        query = db.select([self.subscriptions]).where(self.subscriptions.columns.city == city)
        result_proxy = self.conn.execute(query)
        results = result_proxy.fetchall()

        return [sub[1] for sub in results]
