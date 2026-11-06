import json, sys
q={d['n']:d for d in json.load(open('/home/claude/queue.json'))}
d=q[int(sys.argv[1])]; T=1897921713
inj=("const f=%s;const r=await fetch('https://raw.githubusercontent.com/saburonolan/the-berg-assets/main/everydayiprint/'+f);if(!r.ok)throw new Error('fetch '+r.status);const b=await r.blob();const inp=document.querySelector('input[type=file]');const dt=new DataTransfer();dt.items.add(new File([b],f,{type:'image/png'}));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));for(let i=0;i<30&&!document.querySelector('input[placeholder=\"Example: Great Wave of Trees\"]');i++)await new Promise(x=>setTimeout(x,500));await new Promise(x=>setTimeout(x,4000));'loaded'")%json.dumps(d['file'])
guard=("const set=(sel)=>{const r=document.querySelector(sel);if(!r)throw new Error('missing '+sel);r.checked=true;r.dispatchEvent(new Event('input',{bubbles:true}));r.dispatchEvent(new Event('change',{bubbles:true}))};const pick={'mens-hoodie':'white','mens-hoodie-with-zipper':'heather_grey','pullover-sweatshirt':'white','raglan-t-shirt':'white_black'};Object.entries(pick).forEach(([n,v])=>set(`input[type=radio][name=\"work[product_type_options][${n}][body_color]\"][value=\"${v}\"]`));set('input[type=radio][name=\"work[product_type_options][trucker-hat][color]\"][value=\"creme\"]');set('input[type=radio][name=\"work[safe_for_work]\"][value=\"true\"]');const cb=document.querySelector('input[name=rights_declaration]');if(!cb.checked)cb.click();const t=document.querySelector('input[placeholder=\"Example: Great Wave of Trees\"]').value;if(t!==%s||!cb.checked||!document.querySelector('textarea').value)throw new Error('GUARD FAIL '+t);'guard ok'")%json.dumps(d['title'])
A=[{"name":"navigate","input":{"tabId":T,"url":"https://www.redbubble.com/portfolio/images/new"}},
{"name":"computer","input":{"action":"wait","duration":3,"tabId":T}},
{"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":inj}},
{"name":"find","input":{"tabId":T,"query":"Save work button"}},
{"name":"form_input","input":{"ref":"ref_96","value":d['title'],"tabId":T,"action_summary":"Sets the design title"}},
{"name":"computer","input":{"action":"scroll_to","ref":"ref_103","tabId":T}},
{"name":"computer","input":{"action":"left_click","ref":"ref_103","tabId":T,"action_summary":"Focuses the Main Tag field"}},
{"name":"computer","input":{"action":"type","text":d['main'],"tabId":T,"action_summary":"Types the main tag"}},
{"name":"computer","input":{"action":"key","text":"Enter","tabId":T,"action_summary":"Confirms the main tag"}},
{"name":"computer","input":{"action":"left_click","ref":"ref_108","tabId":T,"action_summary":"Focuses the Supporting Tags field"}},
{"name":"computer","input":{"action":"type","text":d['support'],"tabId":T,"action_summary":"Types 14 supporting tags"}},
{"name":"form_input","input":{"ref":"ref_113","value":d['desc'],"tabId":T,"action_summary":"Sets the description"}},
{"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":guard}},
{"name":"computer","input":{"action":"scroll_to","ref":"ref_2088","tabId":T}},
{"name":"computer","input":{"action":"left_click","ref":"ref_2088","tabId":T,"action_summary":"Saves and publishes design #%d"%d['n']}},
{"name":"computer","input":{"action":"wait","duration":8,"tabId":T}},
{"name":"javascript_tool","input":{"action":"javascript_exec","tabId":T,"text":"({title: document.title, view: [...document.querySelectorAll('a')].map(a=>a.getAttribute('href')).filter(h=>h&&h.includes('/shop/ap/'))[0]})"}}]
print(json.dumps(A))
