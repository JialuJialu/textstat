#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 22:13:58 2017

@author: JLB
"""

import textstat2

kant = ""
lorem = ""
with open("Kant.txt","r") as f:
    for line in f:
        kant += line.strip()

with open("LoremIpsum.txt","r") as e:
    for line in e:
        lorem += line.strip()

kant_scores_dict,kant_text_index_dict = textstat2.readability_scores(kant,displayindex=True)
lorem_scores_dict,lorem_text_index_dict = textstat2.readability_scores(lorem,displayindex=True)
print(kant_scores_dict,kant_text_index_dict)