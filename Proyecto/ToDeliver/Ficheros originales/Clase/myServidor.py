import json
from bottle import *
from myModule import DBClass

DB=DBClass("mydata.db")

@post("/user")
def create_user():
  if request.headers["Content-Type"]!="application/json":
    return {"error":"no json format"} 
  data=request.json
  if data.has_key("username"):
    DB.createUser(data["username"],data)
  else:
    return {"error":"no username given."}

@post("/user/login")
def do_login():
  if request.headers["Content-Type"]!="application/json":
    return {"error":"no json format"}
  data=request.json
  if data.has_key("username"):
     if DB.checkUser(data["username"],data["passwd"]):
        secretKey=DB.registerUser(data["username"])
        return {"tokenID":secretKey}
     else:
        return {"error":"unauthorized"}
  else:
     return {"error":"not username provided"}

@get("/user/logout")
def do_logout():
  usr=request.query["username"]
  DB.finishUser(usr)
  return {"message":"logged out"}

@get("/forum")
def get_forums():
  return DB.getForumNames()

@get("/forum/search")
def search_forum():
  if not request.query.has_key("keyword"):
     return {"error":"no keyword provided"}
  kywd=request.query["keyword"]
  return DB.getForumsByKeyword(kywd)

@post("/forum")
def create_forum():
  if request.headers["Content-Type"]!="application/json":
    return {"error":"no json format"}
  data=request.json
  signedToken=request.query["tokenID"]
  if signedToken==DB.userSecret(data["creator"]):
    if DB.createForum(data["name"],data):
       return {"message":"ok"}
    else:
       return {"error":"some DB error"}
  else:
    return {"error":"not forum name provided"}

@get("/forum/<name>")
def get_forum_data(name):
  return DB.getForumByName(name)

@get("/forum/<name>/posts")
def get_posts(name):
  return DB.getPosts(name)

@get("/forum/<name>/posts/<postID>")
def get_postID(name,postID):
  return DB.getPost(postID)

@get("/forum/<name>/search")
def search_posts(name):
  if not request.query.has_key("keyword"):
    return {"error":"no keyword provided"}
  kywd=request.query["keyword"]
  return DB.getPostsByKeyword(name,kywd)

@post("/forum/<name>")
def create_post(name):
  if request.headers["Content-Type"]!="application/json":
    return {"error":"no json format"}
  data=request.json
  signedToken=request.query["tokenID"]
  if signedToken==DB.userSecret(data["creator"]) and name!="":
    if DB.createPost(name,request.json):
       return {"message":"ok"}
    else:
       return {"error":"some DB error"}
  else:
    return {"error":"not logged yet"}

run(host='localhost', port=8085)
