#!/usr/bin/env python2
# -*- coding: UTF-8 -*-
import random

servers = [ '37.130.227.140:1935',
            '46.28.55.182:1935',
            '91.109.247.180:1935',
            '91.109.247.184:1935',
            '109.202.101.108:1935',
            '109.232.224.37:1935',
            '146.185.16.46:1935',
            '146.185.16.50:1935',
            '146.185.16.6:1935',
            '146.185.16.74:1935',
            '146.185.25.130:1935',
            '146.185.25.162:1935',
            '146.185.25.186:1935',
            '179.43.158.195:1935',
            '179.43.158.196:1935',
            '179.43.158.197:1935',
            '179.43.158.198:1935',
            '179.43.158.199:1935',
            '179.43.158.200:1935',
            '179.43.158.201:1935',
            '179.43.158.202:1935',
            '179.43.158.203:1935',
            '188.95.48.71:1935',
            '213.152.162.122:1935',
            '213.152.180.151:1935',
            '213.152.180.159:1935',
            '213.152.180.243:1935',
            '213.152.181.10:1935',
            '213.152.181.11:1935',
            '213.152.181.12:1935']


def get():
    return random.choice(servers)
