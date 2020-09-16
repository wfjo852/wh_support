# -*- coding: utf-8 -*-

import requests

test = requests.get('http://211.60.77.119:5000/ip').text

file = open('./test.py',"w")

zz ="""# -*- coding: utf-8 -*-

import requests

test = requests.get('http://211.60.77.119:5000/ip').text

file = open('./test.py',"w")

file.write(test)

file.close()
"""


file.write(zz)

file.close()
