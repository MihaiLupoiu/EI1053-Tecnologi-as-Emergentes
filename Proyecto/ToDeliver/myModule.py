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
     self.Schema ["tweet"] = {"coordinates": "text","id":"text","text":"text"}
     self.Schema["stream"]= {"name":"text","jQuery":"text"}

     self.DBlimit=10000
     self.ID=0

     #
     consumer_key = "CjuZ88saPFcFFlHSYGJrJQ"
     consumer_secret = "JCGyXY7ZJ5JdrNwYVnBqKaB9X0FA2ZVtq8gTsN2NT4"
     access_token = "185956451-EgLG7dqJ7L46glKg1RAxAner0z4VwK6bTmbvitqH"
     access_token_secret = "iO39CV1oLzxR3FgYHmKA1Ozexd0u7FgWvzFO41nhcLoIj"
     encoding = None

     self.api = twitter.Api(consumer_key=consumer_key, consumer_secret=consumer_secret,
                      access_token_key=access_token, access_token_secret=access_token_secret,
                      input_encoding=encoding)
     #


  def checkData(self,data,schema):
     if not self.Schema.has_key(schema):
        return False
     if (set(data.keys())<=set(self.Schema[schema].keys())): 
        return True
     print data.keys(),self.Schema[schema].keys()
     return False

  def getSchema(self):
     return self.Schema

  def createStream(self,name, data):
     key=str("stream_%s"%name)
     if self.DB.has_key(key) or not self.checkData(data,"stream"):
        return False
     if len(self.DB.keys())<self.DBlimit:
        self.DB[key]=json.dumps(data)

        statuses = self.api.GetSearch(data["jQuery"])
        for status in statuses:

          createTweet(self, status["id"], name ,status)

        return {"result":"success"}
        #return True
     return False

  def createTweet(self,id,name,data):
     key=str("tweet_%s_%s"%(name,id)) # concatenar 2 cosas??
     if self.DB.has_key(key) or not self.checkData(data,"tweet"):
        return False
     if len(self.DB.keys())<self.DBlimit:
	#devolver solo el coordinate, text e ID
  #convertir a string
        self.DB[key]=json.dumps(data)
        return True
     return False

  def numero_tweets(self, name):
     key=key=str("tweet_%s"%name)
     return count([k for k in self.DB.keys() if k.startswith(key)])

  def get_streams(self):
     key=key=str("stream_")
     LStream = [k for k in self.DB.keys() if k.startswith(key)]
     return LStream

  def get_tweets(self,name):
     key=str("tweet_%s"%name) 
     LTweet = [k for k in self.DB.keys() if k.startswith(key)]
     return LTweet
#================================================ 
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
	#convertir a json
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

#if __name__=="__main__":
  #DB=DBClass()
  #DB.createUser("yo",{"email":"yo@mail.com","name":"Yo Soy Yo","passwd":"secreto"})
  #print "Your key:",DB.registerUser("yo")
  #DB.createForum("coches",{"description":"foro de coches","creator":"yo"})
  #DB.createPost("coches",{"body":"pues eso es todo","creator":"yo"})
  #DB.createPost("coches",{"body":"esto es otro post","creator":"yo"}) 
  #forums= DB.getForumNames()["result"]
  #print forums
  #for name in forums:
  #  print name, DB.getForumByName(name) 
  #  print "--------------"
  #  lposts=DB.getPosts(name)["result"]
  #  for postid in lposts:
  #    print postid,DB.getPost(postid)
  #print DB.getForumsByKeyword("coch")
  #print DB.getPostsByKeyword("coches","es")
  #print DB.DB.keys()
  #DB.finishUser("yo")

  #DB.close()
