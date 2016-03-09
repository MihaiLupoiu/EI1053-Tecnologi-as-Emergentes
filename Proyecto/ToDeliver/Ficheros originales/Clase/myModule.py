import time,shelve,json,base64
'''
Modulo que maneja el back-end de los servicios rest de myServidor.py
Version 2.7 de Python.
'''

class DBClass:
  def __init__(self,fname=""):
     if fname=="":
       self.DB=shelve.open("mydata.db","c")
     else:
       self.DB=shelve.open(fname)
     self.Schema={}
     self.Schema["forum"]= {"timestamp":"time","name":"text","description":"text","creator":"user"}
     self.Schema["post"] = {"timestamp":"time","body":"text","creator":"user"}
     self.Schema["user"] = {"timestamp":"time","username":"text","passwd":"secret","email":"text"}
     self.DBlimit=1000
     self.ID=0
     self.logged={}

  def getTimeStamp(self):
     return time.strftime("%Y%m%d%H%M%S", time.gmtime())

  def getSecret(self):
     return base64.urlsafe_b64encode(self.getTimeStamp())

  def checkUser(self,username,pswd):
     key=str("user_%s"%username)
     if self.DB.has_key(key):
        print self.DB[key]
        userdata=json.loads(self.DB[key])
        if userdata["passwd"]==pswd:
          return True
     return False

  def userSecret(self,username):
     if self.logged.has_key(username):
        return self.logged[username] 
     return "" 

  def registerUser(self,username):
     if not self.logged.has_key(username):
        secretKey=self.getSecret()
        self.logged[username]=secretKey
        return secretKey
     else:
        return {"error":"already registered"}

  def finishUser(self,username):
     if self.logged.has_key(username):
        del self.logged[username]
     return {"result":True}

  def checkData(self,data,schema):
     if not self.Schema.has_key(schema):
        return False
     if (set(data.keys())<=set(self.Schema[schema].keys())): 
        return True
     print data.keys(),self.Schema[schema].keys()
     return False

  def getSchema(self):
     return self.Schema

  def createUser(self,username,data):
     key=str("user_%s"%username)
     data["timestamp"]=self.getTimeStamp()
     if self.DB.has_key(key) or not self.checkData(data,"user"):
        return False
     if len(self.DB.keys())<self.DBlimit:
        self.DB[key]=json.dumps(data)
        return True
     return False

  def createForum(self,forumname, data):
     key=str("forum_%s"%forumname)
     data["timestamp"]=self.getTimeStamp()
     if self.DB.has_key(key) or not self.checkData(data,"forum"):
        return False
     if len(self.DB.keys())<self.DBlimit:
        self.DB[key]=json.dumps(data)
        return True
     return False
 
  def createPost(self,forumname,data):
     self.ID+=1
     key=str("post_%s_%d"%(forumname,self.ID))
     data["timestamp"]=self.getTimeStamp()
     if not self.checkData(data,"post"):
        return False
     if len(self.DB.keys())<self.DBlimit:
        self.DB[key]=json.dumps(data)
        return True
     return False

  def getForumNames(self):
     Lforums=[k.split("_")[-1] for k in self.DB.keys() if k.startswith("forum_")]
     return {"result":Lforums}

  def getPosts(self,forumname):
     key=str("post_%s"%forumname)
     Lposts=[k for k in self.DB.keys() if k.startswith(key)]
     Lposts.sort()
     return {"result":Lposts}

  def getForumsByKeyword(self,kywrd):
     Lforums=[k for k in self.DB.keys() if k.startswith("forum_")]
     Lforums=[k.split("_")[-1] for k in Lforums if self.DB[k].find(kywrd)!=-1]
     Lforums.sort()
     return {"result":Lforums}

  def getPostsByKeyword(self,forumname,kywrd):
     key=str("post_%s"%forumname)
     Lposts=[k for k in self.DB.keys() if k.startswith(key)]
     Lposts=[k for k in Lposts if self.DB[k].find(kywrd)!=-1]
     Lposts.sort()
     return {"result":Lposts}

  def getPost(self,postID):
     if self.DB.has_key(postID):
        return json.loads(self.DB[postID])
     else:
        return None

  def getForumByName(self,forumname): 
     key=str("forum_"+forumname)
     if self.DB.has_key(key):
        return json.loads(self.DB[key])
     else:
        return None

  def close(self):
     self.DB.close()

if __name__=="__main__":
  DB=DBClass()
  DB.createUser("yo",{"email":"yo@mail.com","name":"Yo Soy Yo","passwd":"secreto"})
  print "Your key:",DB.registerUser("yo")
  DB.createForum("coches",{"description":"foro de coches","creator":"yo"})
  DB.createPost("coches",{"body":"pues eso es todo","creator":"yo"})
  DB.createPost("coches",{"body":"esto es otro post","creator":"yo"}) 
  forums= DB.getForumNames()["result"]
  print forums
  for name in forums:
    print name, DB.getForumByName(name) 
    print "--------------"
    lposts=DB.getPosts(name)["result"]
    for postid in lposts:
      print postid,DB.getPost(postid)
  print DB.getForumsByKeyword("coch")
  print DB.getPostsByKeyword("coches","es")
  print DB.DB.keys()
  DB.finishUser("yo")
  DB.close()
