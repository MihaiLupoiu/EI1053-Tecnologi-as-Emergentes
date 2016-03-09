import requests,json,sys

if "create-user" in sys.argv:
  url="http://localhost:8085/user"
  newuser={"username":"fulanito","passwd":"xx1xx"}
  headers = {'content-type': 'application/json'}
  r = requests.post(url, data=json.dumps(newuser), headers=headers)
  print r.status_code


url="http://localhost:8085/user/login"
userdata={"username":"fulanito","passwd":"xx1xx"}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(userdata), headers=headers)
reply=json.loads(r.text)
if reply.has_key("error"):
  print reply
  sys.exit()
else:
  tokenID=reply["tokenID"]

url="http://localhost:8085/forum?tokenID=%s"%tokenID
description={"name":"motos","creator":"fulanito"}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(description),headers=headers)
print "nuevo foro:",r.text

url="http://localhost:8085/forum/motos?tokenID=%s"%tokenID
description={"body":"mi moto mola mucho","creator":"fulanito"}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(description),headers=headers)
print "nuevo post:",r.text

listaforos= requests.get('http://localhost:8085/forum')

for foro in json.loads(listaforos.text)["result"]:
  data= requests.get('http://localhost:8085/forum/%s'%foro)
  print "FORO:",foro,data.text
  posts= requests.get('http://localhost:8085/forum/%s/posts'%foro)
  for postid in json.loads(posts.text)["result"]:
     datapost=requests.get('http://localhost:8085/forum/%s/posts/%s'%(foro,postid))
     print datapost.text
  print ".........."

print requests.get('http://localhost:8085/user/logout?username=fulanito')
