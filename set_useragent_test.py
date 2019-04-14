import json



with open('user-agent.txt','r',encoding="utf-8")as fp:
    s = fp.read()
    uli = json.loads(s, strict=False)
print(type(uli))

#data = r'{"user-agent":["Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50"]}'
#js = json.loads(data, strict=False)
#print(js)