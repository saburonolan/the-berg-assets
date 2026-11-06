import json,sys
D=json.load(open(__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','everydayiprint','tp-data.json')))
T=int(sys.argv[2]) if len(sys.argv)>2 else 1897921713; L="await (0,eval)(await (await fetch('https://raw.githubusercontent.com/saburonolan/the-berg-assets/2284f774e220a8861fc2a5342fdb2aef17011b10/everydayiprint/tp.js')).text());"
out=[]
for n in sys.argv[1].split(','):
    d=D[n]
    out+=[{"name":"navigate","input":{"tabId":T,"url":"https://www.teepublic.com/design/quick_create"}},
     {"name":"computer","input":{"action":"wait","duration":3,"tabId":T}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":L+f"await TP.upload({n})"}},
     {"name":"computer","input":{"action":"wait","duration":8,"tabId":T}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":"await TP.ready()"}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":f"TP.fill({n})"}},
     {"name":"computer","input":{"action":"type","text":", ".join(d['sup'])+",","tabId":T,"action_summary":"Types the supporting tags"}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":f"TP.pub({n})"}},
     {"name":"computer","input":{"action":"wait","duration":9,"tabId":T}},
     {"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":"location.href"}}]
print(json.dumps(out))
