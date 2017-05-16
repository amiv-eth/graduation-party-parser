#!/usr/bin/env python
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

# This function searches for the names of the participants in the html text
def getParticipants(text, tag, endTag):
    participants = []
    index = text.find(tag)
    while index < len(text) and index != -1:
        # get the location of the endtag
        index_end = text.find(endTag, index+len(tag))
        if index_end != index+len(tag):
            participants.append(text[index+len(tag):index_end])
        index = text.find(tag, index+1)

    return participants

# This function tries to split names in forename and surname
#
# It simply searches for the last space in the string and splits the string
# at that position.
def splitNames(name):
    index = name.rfind(" ")
    if index != -1:
        return (name[0:index], name[index+1:])
    else:                       # assume only forename
        return (name, "")

# open file
with open(filename, 'r') as html:
    text = html.read();

participants_primary = getParticipants(text, primaryguest_tag, primaryguest_endtag)
# filter unconrfirmed
for i in range(0, len(participants_primary)):
    index = participants_primary[i].find(" <span>(unconfirmed)</span>")
    if index != -1:
        participants_primary[i] = participants_primary[i][0:index]

participants_male = getParticipants(text, maleguest_tag, maleguest_endtag)

participants_female = []
for i in range(0, len(femaleguest_tags)):
    participants_female.extend(getParticipants(text, femaleguest_tags[i],
                                               femaleguest_endtags[i]))

participants = participants_primary
participants.extend(participants_male)
participants.extend(participants_female)

part_female_split = [splitNames(name) for name in participants_female]
part_male_split = [splitNames(name) for name in participants_male]
part_primary_split = [splitNames(name) for name in participants_primary]
part_split = [splitNames(name) for name in participants]

# sort for lastnames
part_female_split.sort(key=lambda t: t[1])
part_male_split.sort(key=lambda t: t[1])
part_primary_split.sort(key=lambda t: t[1])
part_split.sort(key=lambda t: t[1])

#print(part_split)

with open("complete_list.csv", "w") as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='|',
                           quoting=csv.QUOTE_MINIMAL)
    for name in part_split:
        writer.writerow(name)
