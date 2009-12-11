import re
bad_symbols=[("@","40%"),("*","2A%")]
def fix_url(u):
    '''change the url from http://www.sohu.com/../i/fin/./../index.html 
    to http://www.sohu.com/i/index.html'''
    a=u.split("/")
    n=[]
    for v in a:
        if v == ".":
            continue 
        if v==".." and len(n)>3:
            n.pop()
        if v=="..":
            continue
        n.append(v)
    l="/".join(n)
    for k,v in  bad_symbols:
        l=l.replace(k,v)
    return l

def get_dir(u):
    '''get the dirname of url'''
    if re.match(r'\/$',u):
        return u
    else:
        a=u.split("/")
        la=len(a)
        if la==3:
            return u+"/"
        else:
            a.pop()
            return "/".join(a)+"/"  
def get_base_dir(document,url):
    ''' get the link-base of document '''
    base_url=document["base"] and document["base"] or url
    return get_dir(base_url)   
def get_domain_seg(url):
    ''' get string http://www.sohu.com from http://www.sohu.com/dso/fdfdf.html'''
    a=url.split("/")
    target=[]
    for i in a:
        if len(target)==3:
            break;
        else:
            target.append(i)
    return "/".join(target)
def get_full_url(original_url,base_dir):
    '''get full,validate url from all various url(absolute,relative..) '''
    try:
        r=re.compile(r'([^#]+)#(.*)')
        original_url=r.sub('\1',original_url)
    except:
        pass

    try:
        r=re.compile("^\/")
        if r.match(original_url):
            return get_domain_seg(base_dir)+original_url
    except:
        pass
    try:
        r=re.compile(r'^[a-z]{3,6}:\/\/',re.I)
        if r.match(original_url):
            return original_url
    except:
        pass

    return base_dir+original_url
def remove_bad_links(links):
    ''' remove the javascript:,mailto:,ftp:,news: links or something else'''
    validated_urls=[]
    for u in links:
        if isinstance(u,dict):
            if re.match(r'^javascript:',u["url"],re.I):
                continue
            if re.match(r'^mailto:',u["url"],re.I):
                continue
            if re.match(r'^ftp:',u["url"],re.I):
                continue
            if re.match(r'^news:',u["url"],re.I):
                continue
            if re.match(r'^gopher:',u["url"],re.I):
                continue
            #if not re.match(r'^http:',u["url"],re.I):
            #    continue;
            validated_urls.append(u)
        else:
            if re.match(r'^javascript:',u,re.I):
                continue
            if re.match(r'^mailto:',u,re.I):
                continue
            if re.match(r'^ftp:',u,re.I):
                continue
            if re.match(r'^news:',u,re.I):
                continue
            if re.match(r'^gopher:',u,re.I):
                continue
            #if not re.match(r'^http:',u,re.I):
            #    continue;
            validated_urls.append(u)
    return validated_urls	
    
def extract_links(content):
    reg=re.compile(r'href\s*=\s*[\'\"]?([+:%\/\?~=&;\\\(\),._a-zA-Z0-9-]*)(#[.a-zA-Z0-9-]*)?[\'\" ]?(\s*rel\s*=\s*[\'\"]?(nofollow)[\'\"]?)?[^>]*[>]?([^<]*)',re.I|re.M|re.UNICODE)
    matches=reg.findall(content)
    res=[]
    for mt in matches:
        #res.append(mt[0])
        #continue
        if mt[0]!="":
            res.append({"url":mt[0],"text":mt[4]})
    return res
def get_base(html,url):
    r=re.compile("<base +href *= *[\"']?([^<>'\"]+)[\"']?",re.M|re.I)
    matches=r.findall(html)
    base=url
    try:
        base=matches.pop()
        base =base and base or url
    except:
        pass
    return base
    
    


