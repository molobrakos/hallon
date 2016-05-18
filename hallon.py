#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
extract usage data from hallon mobile broadband
"""

from robobrowser import RoboBrowser
from bs4 import BeautifulSoup as Soup
from os import path
import sys
import yaml
import json

with open(path.join(path.dirname(sys.argv[0]),
                    ".hallon-credentials.yaml")) as f:
    CREDENTIALS = yaml.safe_load(f)

URL = "https://www.hallon.se/mina-sidor"
br = RoboBrowser(parser="lxml")
br.open(URL)
form = br.get_form(action="/logga-in")
form["UserName"].value = CREDENTIALS["username"]
form["Password"].value = CREDENTIALS["password"]
br.submit_form(form)

usage = br.select("p.usage")[0].text.replace(",", ".").split()

remaining = round(float(usage[0]), 2)
total = int(usage[2])
used = round(float(total-remaining), 2)
used_pct = round(used*100/total, 1)
days_remaining = int(br.select("p.usage-daysleft")[0].text.split()[0])

print(json.dumps({"total": total,
                  "remaining": remaining,
                  "used": used,
                  "used_pct": used_pct,
                  "days_remaining": days_remaining}))
