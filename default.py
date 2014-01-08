import os,sys,urllib,urllib2,re,json
import xbmcplugin,xbmcgui,xbmcaddon

#StereoMood - by Marius Baron 2013.

__scriptid__ = 'plugin.stereomood'
__site__= 'http://www.stereomood.com'
__settings__ = xbmcaddon.Addon(id=__scriptid__)
__version__ = __settings__.getAddonInfo('version')
__resourcesDir__ = xbmc.translatePath(os.path.join(__settings__.getAddonInfo('path'), 'resources' ))

RootDir =__settings__.getAddonInfo('path')
if RootDir[-1]==';': RootDir=RootDir[0:-1]
if RootDir[0] == '/':
    if RootDir[-1] != '/': RootDir = RootDir+'/'
    SEPARATOR = '/'    
else:
    if RootDir[-1] != '\\': RootDir=RootDir+'\\'
    SEPARATOR = '\\'

__imagesDir__ = __resourcesDir__+SEPARATOR+'images'+SEPARATOR
print '__imagesDir__:'+__imagesDir__

def CATEGORIES():
        addDir( 'WHAT\'S HOT',__site__+'/inc/popularcloud-html.php',1,__imagesDir__+'top.jpg')
        addDir( 'RANDOM',__site__+'/inc/tagcloud-html.php',1,__imagesDir__+'random.jpg')
        addDir( 'USER CHOICE',__site__+'/inc/usercloud-html.php',1,__imagesDir__+'top.jpg')
        
def INDEX(url):
        req = urllib2.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        match=re.compile('<li><a href="(.+?)" title="(.+?)" class="tag-type-mood tag-dimension-(.+?)" id="(.+?)">(.+?)</a></li>').findall(link)
        for url,title,poids,lid,name in match:
                addDir(name.upper(),__site__+url,2,'')
                
def PLAYLIST(url,index):
        req = urllib2.Request(url+str(index))
        req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
        response = urllib2.urlopen(req)
        link=response.read()
        response.close()
        jdata = json.loads(link)
        tracksTotal = jdata.get('tracksTotal')
        trackList = jdata.get('trackList')       
        for item in trackList:
                trackNum = item.get('trackNum')
                addLink(item.get('title'),item.get('creator'),item.get('location'),item.get('image'))
                
        #limit of 100 songs for loading time (must be improve)    
        if (int(trackNum) < int(tracksTotal) and int(trackNum) < 100 ):
                PLAYLIST(url,index+1)
               

             
def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


def addLink(name,artist,url,iconimage):
        ok=True
        liz=xbmcgui.ListItem(name+' - '+artist, iconImage="DefaultMusic.png", thumbnailImage=iconimage)
        liz.setInfo( type="Music", infoLabels={ "Title": name, "Artist": artist } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=url,listitem=liz)
        return ok


def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setInfo( type="Music", infoLabels={ "Title": name } )
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok
        
              
params=get_params()
url=None
name=None
mode=None


try:
        url=urllib.unquote_plus(params["url"])
except:
        pass
try:
        name=urllib.unquote_plus(params["name"])
except:
        pass
try:
        mode=int(params["mode"])
except:
        pass

print "Mode: "+str(mode)
print "URL: "+str(url)
print "Name: "+str(name)

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        print ""+url
        INDEX(url)

elif mode==2:
        print ""+url
        PLAYLIST(url+'/playlist.json?index=',1)
        

xbmcplugin.endOfDirectory(int(sys.argv[1]))
