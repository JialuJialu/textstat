#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 22:13:58 2017

@author: JLB
"""
import old_textstat

kant = ""
lorem = ""
with open("Kant.txt","r") as f:
    for line in f:
        kant += line.strip()

with open("LoremIpsum.txt","r") as e:
    for line in e:
        lorem += line.strip()

kant_scores = old_textstat.textstat.text_standard(kant)
lorem_scores = old_textstat.textstat.text_standard(lorem)
print(kant_scores)
print(lorem_scores)
