# -*- coding=utf-8 -*-
"""
数据库操作
"""
import datetime
from db_session import DBOBJ
from db_model import *
from common.strUtil import md5
from settings import BASE_URL
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class datastore(object):
    def __init__(self):
        mydb = DBOBJ.instance()
        self.session = mydb.session

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def get_user_by_id(self, id):
        try:
            user = self.session.query(User).filter(User.id == id, User.is_active == 1).one()
            if user is not None:
                return user
            return None
        except Exception,e:
            self.session.rollback()

            print 'exception in id',e
            return None

        finally:
            self.session.close()

    def get_qr_by_code(self, code):
        try:
            qr = self.session.query(Qr).filter(Qr.code == code).one()
            return qr
        except Exception, e:
            self.session.rollback()

            print 'exception in id',e
            return None

        finally:
            self.session.close()

    def check_user(self, user_name, password):
        pwd = md5(password)
        try:
            user = self.session.query(User).filter(User.user_name==user_name, User.password==pwd).one()
            return user
        except Exception, e:
            self.session.rollback()

            print 'exception ',e
            return None

        finally:
            self.session.close()

    def save_qr(self, code, qr_code, name, user):
        try:
            qr = Qr()
            qr.code = code
            qr.qr_code = code+".png"
            qr.name = name
            qr.create_user = user.id
            qr.status = 1
            qr.url = BASE_URL+"app/"+code
            self.session.add(qr)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def get_qr_count(self):
        try:
            return self.session.query(Qr).filter(Qr.status == 1).count()
        except Exception, e:
            self.session.rollback()

            print 'exception ',e
            return None

        finally:
            self.session.close()


    def get_qr(self, page=1, count=10):
        try:
            offset = (page-1) * count
            return self.session.query(Qr).filter(Qr.status == 1).limit(count).offset(offset).all()

        except Exception, e:
            self.session.rollback()

            print 'exception ', e
            return None

        finally:
            self.session.close()

    ### type 1:android 2:ios
    ### qr foreign Qr
    def save_ScanData(self, qr, createtime, sysType, count):
        try:
            scanHistory = ScanHistory()
            scanHistory.qr_id = qr
            scanHistory.createtime = createtime
            scanHistory.type = sysType
            scanHistory.count = count
            self.session.add(scanHistory)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    ### type 1:android 2:ios
    ### qr foreign Qr
    def save_Download(self, qr, createtime, type, count):
        try:
            download = Download()
            download.qr_id = qr
            download.createtime = createtime
            download.type = type
            download.count = count
            self.session.add(download)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
        finally:
            self.session.close()

    def queryQrs(self, qrType):
        try:
            if qrType == '0':
                sql = "select name from app_qr_qr"
                return self.session.execute(sql, {})
            else:
                sql = "select name from app_qr_qr where name = :qrType"
                return self.session.execute(sql, {'qrType': qrType})
        except:
            self.session.rollback()

        finally:
            self.session.close()

    def queryScanDataWithBeginAndEnd(self, beginDate=None,endDate=None,osType=None,qrType=None):
        if beginDate == None:
            beginDate = datetime.datetime.min
        if endDate == None:
            endDate = datetime.datetime.max

        try:
            if osType != "0" and qrType != "0":
                sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr.name = :qrType and type = :osType"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType, 'qrType': qrType})
            elif osType != "0":
                sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and type = :osType"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType})
            elif qrType != "0":
                sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr.name = :qrType"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'qrType': qrType})
            else:
                sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate})

        except:
            self.session.rollback()

        finally:
            self.session.close()

    def queryDownloadDataWithBeginAndEnd(self,beginDate=None,endDate=None,osType=None,qrType=None):
        if beginDate == None:
            beginDate = datetime.datetime.min
        if endDate == None:
            endDate = datetime.datetime.max


        try:
            if osType != "0" and qrType != "0":
                sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr.name = :qrType and type = :osType"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType, 'qrType': qrType})
            elif osType != "0":
                sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and type = :osType"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType})
            elif qrType != "0":
                sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr.name = :qrType"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'qrType': qrType})
            else:
                sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate"
                return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate})


        except:
            self.session.rollback()

        finally:
            self.session.close()

if __name__ == '__main__':
    pass
    # example for sqlalchemy
    # query self.session.query().filter().all()
    # add self.session.add(commentObj)
    # commit self.session.commit()
    # sql self.session.execute(sql1, {'pic_id': id})
    # update self.session.merge(picContent)
    # 事务: session.rollback() see also http://docs.sqlalchemy.org/en/rel_1_0/orm/session_transaction.html
