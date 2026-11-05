
window.alert=()=>{};window.confirm=()=>true;
window.TP={
 data:null,
 async init(){ if(!this.data) this.data=await (await fetch('https://raw.githubusercontent.com/saburonolan/the-berg-assets/main/everydayiprint/tp-data.json?'+Date.now())).json(); },
 ev(e){e.dispatchEvent(new Event('input',{bubbles:true}));e.dispatchEvent(new Event('change',{bubbles:true}));},
 async load(n){ await this.init(); const D=this.data[n];
  const h=[...document.querySelectorAll('h1,h2,h3,h4,div,a,span')].find(e=>e.children.length===0&&e.textContent.trim()==='Single File Upload');if(h)h.click();
  await new Promise(x=>setTimeout(x,1500));
  const r=await fetch('https://raw.githubusercontent.com/saburonolan/the-berg-assets/main/everydayiprint/'+D.f);if(!r.ok)throw new Error('fetch '+r.status);
  const b=await r.blob();const inp=document.querySelector('input[type=file]');const dt=new DataTransfer();dt.items.add(new File([b],D.f,{type:'image/png'}));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true}));
  for(let i=0;i<40;i++){await new Promise(x=>setTimeout(x,500));const t=document.querySelector('input[name="design[design_title]"]');if(t&&t.offsetParent)break;}
  await new Promise(x=>setTimeout(x,8000)); return location.href; },
 async upload(n){ await this.init(); const D=this.data[n];
  const h=[...document.querySelectorAll('h1,h2,h3,h4,div,a,span')].find(e=>e.children.length===0&&e.textContent.trim()==='Single File Upload');if(h)h.click();
  await new Promise(x=>setTimeout(x,1000));
  const r=await fetch('https://raw.githubusercontent.com/saburonolan/the-berg-assets/main/everydayiprint/'+D.f);if(!r.ok)throw new Error('fetch '+r.status);
  const b=await r.blob();const inp=document.querySelector('input[type=file]');const dt=new DataTransfer();dt.items.add(new File([b],D.f,{type:'image/png'}));inp.files=dt.files;inp.dispatchEvent(new Event('change',{bubbles:true})); return 'uploading '+D.f; },
 async ready(){ for(let i=0;i<60;i++){const t=document.querySelector('input[name="design[design_title]"]');if(t&&t.offsetParent){await new Promise(x=>setTimeout(x,3000));return 'ready '+location.href;} await new Promise(x=>setTimeout(x,500));} throw new Error('not ready'); },
 fill(n){ const D=this.data[n], ev=this.ev;
  const t=document.querySelector('input[name="design[design_title]"]');t.value=D.title;ev(t);
  const d=document.querySelector('textarea[name="design[design_description]"]');d.value=D.desc;ev(d);
  const m=document.querySelector('input[name="design[primary_tag]"]');m.value=D.main;ev(m);
  const cf=document.querySelector('input[name="design[content_flag]"][value=false]');cf.click();cf.checked=true;ev(cf);
  [...document.querySelectorAll('input[name="additional_colors[]"]')].forEach(x=>{if(x.checked!==(x.dataset.brightness==='light'))x.click();});
  for(const id of [58,56,55]){const h=document.getElementById('canvas-option_'+id);if(h&&h.value==='true')h.parentElement.click();}
  const st=document.querySelector('input[name="design[mockup_config_sticker_attributes][config_style]"][value=print]');if(st){st.click();st.checked=true;ev(st);}
  const sb=document.getElementById('design_mockup_config_print_attributes_bg_color');if(sb&&!sb.value){sb.value='#ffffff';ev(sb);}
  const lab=[...document.querySelectorAll('*')].find(e=>e.children.length===0&&e.textContent.trim()==='Supporting Tags');let box=lab;for(let k=0;k<5&&box&&!box.querySelector('input[type=text]:not([name])');k++)box=box.parentElement;
  const si=box.querySelector('input[type=text]:not([name])');si.focus();si.click(); return D.sup.join(', ')+','; },
 pub(n){ const D=this.data[n];
  const t=document.querySelector('input[name="design[design_title]"]').value;const tags=document.querySelectorAll('input[name="design[secondary_tags][]"]').length;
  const cb=document.getElementById('terms');if(!cb.checked)cb.click();
  if(t!==D.title||tags<5||!cb.checked||!document.querySelector('input[name="design[content_flag]"]:checked'))throw new Error('GUARD FAIL '+t+' tags='+tags);
  const btn=[...document.querySelectorAll('button,input[type=submit]')].find(b=>/^publish$/i.test((b.innerText||b.value||'').trim()));setTimeout(()=>btn.click(),50); return 'clicked '+tags; }
};'TP ready'
