#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import csv

filename = sys.argv[1]

# TAGS
primaryguest_tag = "<td>*</td><td>"
primaryguest_endtag = "</td>"
maleguest_tag = "<span>maleguest:</span> "
maleguest_endtag = "<br>"
femaleguest_tags = ["<span>femaleguest1:</span> ", "<span>femaleguest2:</span> "]
femaleguest_endtags = ["<br>", "<br>"]

def getAllParticipants(text):
    guests = {}
    index = text.find(primaryguest_tag)
    while index < len(text) and index != -1:
        tag = primaryguest_tag
        # found primary, now search for male and female guests
        index_end = text.find(primaryguest_endtag, index+len(tag))
        if index_end != index+len(tag):
            prim_name = reverseName(text[index+len(tag):index_end])

        # searching for next tag
        male_name = searchNextName(text, index, maleguest_tag, maleguest_endtag)

        female_names = []
        for i in range(0, len(femaleguest_tags)):
            female_names.append(searchNextName(text, index, femaleguest_tags[i],
                                               femaleguest_endtags[i]))

        # set new index
        index = text.find(primaryguest_tag, index+len(primaryguest_tag))
        guests[prim_name] = {'male': male_name, 'female': female_names}

    return guests

def searchNextName(text, index, tag, endTag):
    index = text.find(tag, index)
    index_end = text.find(endTag, index+len(tag))
    if index != -1 and index_end != -1:
        return reverseName(text[index+len(tag):index_end])
    return ""

# This function tries to split names in forename and surname
#
# It simply searches for the last space in the string and splits the string
# at that position.
def splitNames(name):
    index = name.rstrip().rfind(" ")
    if index != -1:
        return (name[0:index], name[index+1:])
    else:                       # assume only forename
        return (name, "")

def reverseName(name):
    if name == "":
        return ""
    split = splitNames(name)
    return "{}, {}".format(split[1].title(), split[0].title())

# open file
with open(filename, encoding='utf-8') as html:
    text = html.read()

# remove all unconfirmed
text = text.replace(u' <span>(unconfirmed)</span>', '')

guests = getAllParticipants(text)

with open("complete_list.txt", "w", encoding='utf-8') as complete_list, \
    open("related_list.txt", "w", encoding='utf-8') as related_list:

    guests_all = []
    for k in sorted(guests.keys()):
        related_list.write("{}:\n\tmaleguest: {}".format(k, guests[k]['male']))
        related_list.write("\n\tfemaleguest1: {}\n\tfemaleguest2: {}\n".format(guests[k]['female'][0], guests[k]['female'][1]))
        guests_all.extend([k, guests[k]['male'], guests[k]['female'][0], guests[k]['female'][1]])

    # strip empty names
    guests_all = [x for x in guests_all if x]
    guests_all.sort()
    for name in guests_all:
        complete_list.write("{}\n".format(name))
