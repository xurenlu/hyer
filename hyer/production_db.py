#coding:utf-8
import time
import MySQLdb
import cPickle as pickle
import hyer.tinySQL
import hyer.singleton
import hyer.vendor.phpformat
import hyer.singleton_bloom

class ProductionDb(hyer.singleton.Singleton):

    def __init__(self,config):
        if not self.__dict__.has_key("conn"):
            self.config=config
            self.conn=None
        if not self.conn:
            self.connect()
    def connect(self):
        if not self.conn:
            self.reconnect()
        pass
    def reconnect(self):
        self.conn=MySQLdb.connect(self.config["host"],self.config["user"],self.config["pass"],self.config["db"])
        self.cursor=self.conn.cursor(MySQLdb.cursors.DictCursor)
        sql="SET names utf8"
        self.cursor.execute(sql)

    def pushProduct(self,worker,product):
        if hyer.singleton_bloom.exists(product["__PRODUCT_ID__"]+":"+worker,"products"):
            return None
        else:
            hyer.singleton_bloom.add(product["__PRODUCT_ID__"]+":"+worker,"products")

        self.connect()
        try:
            #productData= hyer.vendor.phpformat.serialize(product)
            productData= pickle.dumps(product)
        except Exception,e:
            print "error occured while serializing data:",e.__class__,e
            print "error data was:",product

        tempdata={
                "product_id":product["__PRODUCT_ID__"],
                "worker":worker,
                "product_data":productData,
                "status":"NEW"
                }

        sql=hyer.tinySQL.create(self.config["table"],tempdata)
        try:
            self.cursor.execute(sql)
        except Exception,e:
            print "error while execute sql:",sql,e.__class__,e
            pass

    def lockTable(self,reason,times=1):
        hyer.log.error("table-lock")

        self.connect()

        try:
            sql="LOCK TABLES "+self.config["table"]+" WRITE"
            self.cursor.execute(sql)
            sql="FLUSH TABLES "
            self.cursor.execute(sql)
        except Exception ,e:
            print self.conn ,"lock table error,",e.__class__,e,sql,",times:",times
            hyer.log.track()
            if times<5:
                self.reconnect()
                self.lockTable(reason,times+1)

    def unlockTable(self):
        hyer.log.error("table-unlock")

        self.connect()

        try:
            sql="UNLOCK TABLES "
            self.cursor.execute(sql)
        except Exception,e:
            print "unlock table error",e.__class__,e
            hyer.log.track()

    def mark_done(self,product_id,worker):
        '''
        mark some product as done.
        delete it from products table.
        '''
        #self.lockTable("mark_done")
        try:
            sql=hyer.tinySQL.remove(self.config["table"],{ "product_id":str(product_id), "worker":worker })
            self.cursor.execute(sql)
        except:
            pass
        #self.unlockTable()

    def popProduct(self,worker):
        '''
        从产品数据库中取出一个任务来进行计算
        '''
        #self.lockTable("pop")
        #select from products db that to be handle and current unlocked;
        sql="SELECT id,product_data FROM `%s` USE INDEX (`ws`) WHERE worker='%s' AND status='NEW' AND locked='no' ORDER BY RAND()  LIMIT 1" %(self.config["table"],worker)
        try:
            n=self.cursor.execute(sql)
        except Exception,e:
            #self.unlockTable()
            print "while fetch from production_db,error:",e
            return None

        if n==0:
            #self.unlockTable()
            return None

        try:
            rows=self.cursor.fetchall()
        except Exception,e:
            #self.unlockTable()
            return None

        try:
            productData=rows[0]["product_data"]
            id=rows[0]["id"]
            usql="UPDATE `%s` SET locked='yes',lock_time='%s' WHERE id=%s" % (self.config["table"], str(int(time.time())), str(id))
            self.cursor.execute(usql)
        except Exception,e:
            pass

        #self.unlockTable()
        try:
            #product=hyer.vendor.phpformat.unserialize(productData)
            product=pickle.loads(productData)
            return product
        except Exception,e:
            print "when unserialize,error:",e.__class__,e
            print "id",id
            print "error data was:",productData
            hyer.log.track()
            return None
        
