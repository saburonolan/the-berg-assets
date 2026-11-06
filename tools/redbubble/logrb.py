import csv, sys
n, wid = int(sys.argv[1]), sys.argv[2]
url = f"https://www.redbubble.com/shop/ap/{wid}"
rows = list(csv.reader(open('pins-copy.csv')))
for r in rows[1:]:
    if r[0].startswith(f"pin-{n:02d}-"): r[5] = url
csv.writer(open('pins-copy.csv','w',newline=''), quoting=csv.QUOTE_ALL).writerows(rows)
title = list(csv.reader(open('redbubble-listings.csv')))[n][3]
open('live-listings.txt','a').write(f"{n:02d}\t{title}\t{url}\n")
print("logged", n, url)
