class MongodbBase(object):
    """数据库操作基本类，包含与业务无关的数据库操作方法"""
    def __init__(self):
        pass

    def conn(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def select(self):
        pass

    # TODO: 可以加一些聚合操作等方法


class MongodbClient(MongodbBase):
    """与业务有关的数据库操作方法类"""
    def __init__(self):
        # TODO: 从配置文件读取数据库连接信息
        super().__init__()

    # TODO: 这里写与业务有关的数据库操作方法
