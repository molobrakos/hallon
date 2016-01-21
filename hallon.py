#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract usage data from hallon mobile broadband
"""

from mechanize import Browser
from bs4 import BeautifulSoup as Soup
from os import path
import sys
import yaml

with open(path.join(path.dirname(sys.argv[0]),
                    ".hallon-credentials.yaml")) as f:
    CREDENTIALS = yaml.safe_load(f)

URL = "https://www.hallon.se/mina-sidor"
br = Browser()
br.open(URL)
br.form = [fr for fr in br.forms() if "logga-in" in fr.action][0]
br.form["UserName"] = CREDENTIALS["username"]
br.form["Password"] = CREDENTIALS["password"]
br.submit()

page = Soup(br.response().read())
usage = page.select("p.usage")[0].text.replace(",", ".").split()

left = float(usage[0])
total = int(usage[2])
used = total-left
used_pct = int(round(used*100/total))
daysleft = page.select("p.usage-daysleft")[0].text.split()[0]

print "total left used used_pct daysleft"
print total, left, used, used_pct, daysleft
