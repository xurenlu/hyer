#coding:utf-8
import stackless
import hyer.log
import hyer.error

'''
以stackless 方式运行任务.
'''
channels={}

def worker_run(wname,config):
    global channels
    print "worker ",wname,"started"
    print config["post"]
    while True:
        print "While loop entered"
        product=channels[config["post"]].receive()
        print "msg received"
        try:
            for tool in config["tools"]:
                currentTool=tool
                try:
                    product=tool["class"](tool).run(product)
                except hyer.error.IgnoreError,en:
                    #error can be ignored
                    hyer.log.debug("got error class:[%s] \nerror msg:%s \n worker:%s\ntool:[%s] " % ( str(en.__class__), en, config["post"], currentTool))
                    hyer.log.track()
                    pass
                except hyer.error.ExitLoopError,ex:
                    hyer.log.track()
                    raise hyer.error.ExitLoopError(str(ex))
                except Exception,ec:
                    hyer.log.info(  "got error class:[%s] \nerror msg:%s \n worker:%s\ntool:[%s] " % ( str(ec.__class__), ec, config["post"], currentTool))
                    hyer.log.track()
                    #print product
                    raise hyer.error.ExitLoopError( \
                            "got error:%s while tools process:%s,%s->[%s] " % ( str(ec.__class__), ec, config["post"], currentTool)
                            )
                    pass
        except hyer.error.ExitLoopError,e1:
            continue
        except Exception,e2:
            pass
    
        if isinstance(config["nextWorker"],list):
            for nw in config["nextWorker"]:
                if isinstance(product,list):
                    for outproduct in product:
                        try:
                            channels[nw].send(outproduct)
                        except Exception,ep:
                            hyer.log.error("pushProduct error:%s" % ep)
                else:
                    try:
                        channels[nw].send(product)
                    except Exception,ep:
                        hyer.log.error("pushProduct error:%s" % ep)

def workers_init(workers):
    global channels
    for w in workers :
        print w["post"]
        channels[w["post"]]=stackless.channel()
        stackless.tasklet(worker_run)(w["post"],w)

def init_tasks(post,product):
    global channels
    channels[post].send(product)


#channels["proc_start_page"].send({
#                    "url":"http://act1.baobao.sohu.com/expert/index.php",
#                    "text":"",
#                    "__PRODUCT_ID__":"start"+str(time.time()),
#                })

