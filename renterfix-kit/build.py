import sys, asyncio
from playwright.async_api import async_playwright

FOOT = "General info, not legal advice. Check your lease and local law. &nbsp;·&nbsp; RenterFix Winter Kit"
CSS = """
@page { margin: 0; }
* { box-sizing: border-box; }
body { margin:0; font-family: Inter, sans-serif; color:#1d2a33; font-size:10.5pt; }
.page { width: var(--w); height: var(--h); padding: 0.6in 0.65in 0.55in; position: relative; page-break-after: always; overflow:hidden; }
.page:last-child { page-break-after: auto; }
.tag { font-size:8pt; letter-spacing:.14em; text-transform:uppercase; color:#1f7a8c; font-weight:700; }
h1 { font-size:24pt; margin:.08in 0 .06in; letter-spacing:-.01em; }
h2 { font-size:11pt; margin:.18in 0 .06in; color:#1f7a8c; }
p.lead { color:#4a5a66; margin:0 0 .12in; line-height:1.4; }
.bar { height:5px; width:1.1in; background:#1f7a8c; border-radius:3px; margin-bottom:.16in; }
ul.check { list-style:none; padding:0; margin:0; }
ul.check li { display:flex; gap:.12in; padding:.065in 0; border-bottom:1px solid #e3e8ec; line-height:1.35; }
ul.check li::before { content:""; flex:0 0 13px; height:13px; border:1.6px solid #1f7a8c; border-radius:3px; margin-top:2px; }
ul.check b { font-weight:600; }
.cols { display:grid; grid-template-columns:1fr 1fr; gap:.3in; }
table { width:100%; border-collapse:collapse; font-size:9pt; }
th { text-align:left; background:#eaf3f5; color:#16525e; font-weight:600; padding:.06in .07in; border:1px solid #c9d8de; }
td { border:1px solid #d5dee3; padding:0 .07in; height:var(--rowh,.30in); vertical-align:middle; }
.foot { position:absolute; left:.65in; right:.65in; bottom:.3in; font-size:7.5pt; color:#7b8a95; border-top:1px solid #e3e8ec; padding-top:.06in; display:flex; justify-content:space-between; }
.box { border:1.5px solid #1f7a8c; border-radius:8px; padding:.14in .18in; margin-top:.14in; background:#f5fafb; }
.fields div { display:flex; gap:.1in; align-items:flex-end; margin:.1in 0; }
.fields span { white-space:nowrap; font-weight:600; font-size:9.5pt; }
.fields i { flex:1; border-bottom:1px solid #9aabb6; height:.2in; }
.cover { background:#16525e; color:#fff; }
.cover h1 { font-size:40pt; line-height:1.02; margin:.9in 0 .2in; color:#fff; }
.cover .tag { color:#9fd8e3; }
.cover p { color:#d6ecf0; font-size:12pt; line-height:1.5; max-width:5.4in; }
.cover ol { color:#fff; font-size:11pt; line-height:1.9; padding-left:.25in; margin-top:.3in; }
.cover .foot { color:#9fd8e3; border-color:#2f6f7b; }
.warn { font-size:9pt; background:#fff4e5; border-left:4px solid #e08a1e; padding:.08in .12in; margin-top:.12in; line-height:1.4; }
"""
def foot(n): return f'<div class="foot"><span>{FOOT}</span><span>{n}</span></div>'
def table(headers, rows, widths=None):
    h = "".join(f'<th style="width:{w}">{x}</th>' if widths else f"<th>{x}</th>" for x,w in zip(headers, widths or [None]*len(headers)))
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<table><tr>{h}</tr>{body}</table>"
def checks(items): return '<ul class="check">' + "".join(f"<li><span>{i}</span></li>" for i in items) + "</ul>"

WINTER = [
 "<b>Find the main water shutoff</b> and test that you can turn it. Label it with tape.",
 "<b>Find the breaker panel.</b> Make sure the circuit labels are readable.",
 "<b>Test smoke and CO alarms.</b> Swap batteries if that's your job; report hardwired units that fail.",
 "<b>Replace the HVAC filter</b> if your lease makes it your job. Write the date on the frame.",
 "<b>Disconnect garden hoses</b> from outdoor spigots before the first freeze.",
 "<b>Freezing nights:</b> open cabinet doors under sinks on outside walls so warm air reaches the pipes.",
 "<b>Hard freezes:</b> let the faucets on outside walls drip slowly.",
 "<b>Away for the holidays?</b> Keep the heat on. Many guides say 55°F or higher.",
 "<b>Check windows and doors for drafts.</b> Use removable fixes (draft snakes, rope caulk) or ask before using adhesive.",
 "<b>Space heaters:</b> keep them 3 ft from anything that can burn, plug straight into the wall, and turn them off when you leave.",
 "<b>Report heating problems in writing now</b>, before the cold snap. Keep a copy.",
 "<b>Save the emergency maintenance number</b> in your phone, and check your renters insurance.",
]

def kit():
    p=[]
    p.append(f'''<div class="page cover"><div class="tag">RenterFix · Winter Kit</div>
<h1>The Renter's<br>Winter Kit</h1>
<p>Six printable pages to protect your apartment through the cold months and protect your deposit when you move.</p>
<ol><li>Winter Prep Checklist</li><li>Move-In Photo Log</li><li>Room-by-Room Inspection</li><li>Move-Out Deposit Checklist</li><li>Maintenance Request Log</li><li>Shutoffs &amp; Emergency Map</li></ol>
<p style="margin-top:.35in;font-size:10pt">Print what you need, fill it in by hand, and keep it with your lease. Snap a photo of each finished page as a backup.</p>
{foot("")}</div>''')
    p.append(f'''<div class="page"><div class="tag">Page 1</div><h1>Winter Prep Checklist</h1><div class="bar"></div>
<p class="lead">Work through this before the first freeze. Most of it takes under an hour, and none of it needs tools you don't own.</p>
{checks(WINTER)}
<div class="warn">Frozen pipe or water coming in? Shut off the main water valve first, then call emergency maintenance. Take photos as you go.</div>
{foot(1)}</div>''')
    rows=[["","","","",""] for _ in range(17)]
    p.append(f'''<div class="page"><div class="tag">Page 2</div><h1>Move-In Photo Log</h1><div class="bar"></div>
<p class="lead">Photograph every existing scratch, stain and dent <b>before you unpack</b>. Log each photo here so you can find it at move-out.</p>
<div class="fields" style="display:grid;grid-template-columns:1fr 1fr;gap:.2in"><div><span>Address</span><i></i></div><div><span>Move-in date</span><i></i></div></div>
{table(["Room","Item / spot","Photo # or file name","Existing issue","Reported to landlord? (date)"], rows, ["14%","20%","20%","28%","18%"])}
{foot(2)}</div>''')
    rooms=[("Living room",["Walls & ceiling","Floors / carpet","Windows & screens","Doors & locks","Outlets & switches","Lights / fixtures"]),
           ("Kitchen",["Fridge & freezer","Stove / oven / hood","Dishwasher","Sink & disposal","Cabinets & counters","Floor"]),
           ("Bathroom",["Toilet (flush, base)","Tub / shower & caulk","Sink & faucet","Exhaust fan","Hot water & pressure","Mirror / cabinet"]),
           ("Bedroom(s)",["Walls & ceiling","Floors / carpet","Closet & doors","Windows & blinds","Outlets & lights","Smoke alarm"])]
    blocks=""
    for name,items in rooms:
        blocks+=f'<h2>{name}</h2>'+table(["Item","Good","Fair","Damaged","Notes"],[[i,"","","",""] for i in items],["30%","8%","8%","10%","44%"])
    p.append(f'''<div class="page" style="--rowh:.235in"><div class="tag">Page 3</div><h1>Room-by-Room Inspection</h1><div class="bar" style="margin-bottom:.04in"></div>
{blocks}
<div class="fields" style="display:grid;grid-template-columns:1fr 1fr;gap:.25in;margin-top:.08in"><div><span>Tenant signature / date</span><i></i></div><div><span>Landlord signature / date</span><i></i></div></div>
{foot(3)}</div>''')
    out=["<b>Give written notice</b> by the deadline in your lease. Keep a copy.",
         "<b>Give your forwarding address in writing</b> so your deposit and any itemized deductions can reach you.",
         "<b>Ask for a walk-through</b> and attend if you can.",
         "<b>Deep clean:</b> inside the oven and fridge, bathroom grout, baseboards, window tracks, floors.",
         "<b>Small fixes</b> (nail holes, bulbs, loose handles), only where your lease allows tenant repairs.",
         "<b>Remove everything:</b> belongings, trash and anything left in storage, garage or mailbox.",
         "<b>Photograph every room after cleaning</b> from the same angles as your move-in photos.",
         "<b>Record final meter readings</b> and schedule your utility shutoffs or transfers.",
         "<b>Return every key, fob and remote.</b> Get a receipt or send a dated email confirming it.",
         "<b>Look up your state's deposit-return deadline</b> and write it below."]
    p.append(f'''<div class="page"><div class="tag">Page 4</div><h1>Move-Out Deposit Checklist</h1><div class="bar"></div>
<p class="lead">Your move-in log from pages 2–3 is your best evidence. Start this list 30 days before you move.</p>
{checks(out)}
<div class="box fields"><div><span>Notice given (date + how)</span><i></i></div><div><span>Walk-through date</span><i></i></div><div><span>Keys returned (date + to whom)</span><i></i></div><div><span>Deposit amount</span><i></i><span>State return deadline</span><i></i></div><div><span>Deposit received (date + amount)</span><i></i></div></div>
{foot(4)}</div>''')
    p.append(f'''<div class="page" style="--rowh:.40in"><div class="tag">Page 5</div><h1>Maintenance Request Log</h1><div class="bar"></div>
<p class="lead">Report problems in writing (portal, email or text) and log them here. A dated record helps if a problem comes back or a deposit question comes up.</p>
{table(["Date reported","Issue","How reported","Ref # / who","Response date","Fixed date","Notes"],[[""]*7 for _ in range(13)],["11%","22%","12%","12%","11%","10%","22%"])}
{foot(5)}</div>''')
    p.append(f'''<div class="page"><div class="tag">Page 6</div><h1>Shutoffs &amp; Emergency Map</h1><div class="bar"></div>
<p class="lead">Fill this in on move-in day and stick it inside a kitchen cabinet door. In an emergency nobody wants to go hunting.</p>
<div class="cols"><div class="fields">
<h2>Where things are</h2>
<div><span>Main water shutoff</span><i></i></div><div><span>Water heater + its shutoff</span><i></i></div><div><span>Breaker panel</span><i></i></div><div><span>Gas meter / shutoff (if any)</span><i></i></div><div><span>Fire extinguisher</span><i></i></div><div><span>HVAC filter (size)</span><i></i></div>
<h2>Who to call</h2>
<div><span>Emergency maintenance</span><i></i></div><div><span>Landlord / manager</span><i></i></div><div><span>Electric utility</span><i></i></div><div><span>Gas utility</span><i></i></div><div><span>Renters insurance + policy #</span><i></i></div>
</div><div>
<h2>Breaker labels</h2>
{table(["#","Controls"],[[str(i),""] for i in range(1,17)],["14%","86%"])}
</div></div>
<div class="warn"><b>Smell gas?</b> Don't flip switches or use flames. Leave first, then call your gas utility or 911 from outside.</div>
{foot(6)}</div>''')
    return p

def free():
    return [f'''<div class="page"><div class="tag">RenterFix · Free Printable</div><h1>Renter Winter Checklist</h1><div class="bar"></div>
<p class="lead">12 quick jobs to do before the first freeze. Check them off and stick this on the fridge.</p>
{checks(WINTER)}
<div class="box" style="font-size:9.5pt;line-height:1.45"><b>Want the full kit?</b> The Renter's Winter Kit adds a move-in photo log, a room-by-room inspection, a move-out deposit checklist, a maintenance request log and a shutoff map. Link on the RenterFix channel page.</div>
<div class="foot"><span>General info, not legal advice. Check your lease and local law. &nbsp;·&nbsp; RenterFix</span><span>Free to print and share</span></div></div>''']

SIZES={"letter":("8.5in","11in"),"a4":("210mm","297mm")}
async def render(pages, name):
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page()
        for sz,(w,h) in SIZES.items():
            html=f"<html><head><style>:root{{--w:{w};--h:{h}}}{CSS}</style></head><body>{''.join(pages)}</body></html>"
            await pg.set_content(html); await pg.wait_for_timeout(200)
            await pg.pdf(path=f"{name}-{sz}.pdf", width=w, height=h, print_background=True)
        await b.close()
asyncio.run(render(kit(),"RenterFix-Winter-Kit"))
asyncio.run(render(free(),"RenterFix-Free-Winter-Checklist"))
