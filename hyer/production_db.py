#coding:utf-8
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
            self.conn=MySQLdb.connect(config["host"],config["user"],config["pass"],config["db"])
            self.cursor=self.conn.cursor(MySQLdb.cursors.DictCursor)
        pass
    def pushProduct(self,worker,product):
        if hyer.singleton_bloom.exists(product["__PRODUCT_ID__"]+":"+worker,"products"):
            print "reject by product_db bloom test."+product["__PRODUCT_ID__"]+",worker:"+worker
            return None
        else:
            hyer.singleton_bloom.add(product["__PRODUCT_ID__"]+":"+worker,"products")

        productData= hyer.vendor.phpformat.serialize(product)
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
            print "pushProduct error:",e
            pass
    def popProduct(self,worker):
        print "popProduct called"
        sql="SELECT id,product_data FROM `%s` USE INDEX (`ws`) WHERE worker='%s' AND status='NEW' ORDER BY RAND() LIMIT 1" %(self.config["table"],worker)
        n=self.cursor.execute(sql)
        if n==0:
            return None
        try:
            rows=self.cursor.fetchall()
        except Exception,e:
            print "fetchall error."
            return None
        try:
            productData=rows[0]["product_data"]
            id=rows[0]["id"]
            usql="UPDATE `%s` SET status='FIXED' WHERE id=%s" % (self.config["table"],str(id))
            self.cursor.execute(usql)
        except Exception,e:
            print "productData copy error:",e
            pass
        try:
            product=hyer.vendor.phpformat.unserialize(productData)
            return product
        except Exception,e:
            print productData
            print "unserialize error:",e
            return None
        
