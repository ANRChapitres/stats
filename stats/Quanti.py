__author__      = "OdysseusPolymetis"

# coding: utf-8

import sys
import os
import os.path
import fnmatch
from lxml import etree
from lxml.etree import tostring
import re
from collections import defaultdict
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import argparse

help_text = """
Programme Python 3
Usage : python 'path/to/your/program/file.py' -- path 'path/to/your/source/folder/' (do not forget the last slash)
"""

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                   help=help_text)
parser.add_argument("--path", help="path/to/your/source/folder/",
                    type=str)
args = parser.parse_args()
pathToFolder=args.path

stats=defaultdict(list)
plot=OrderedDict()
bugs=list()

for tmpFile in fnmatch.filter(os.listdir(pathToFolder), '*.xml'):
    execute=False
    words=list()
    tmpFile=tmpFile.replace("/",":")
    fullPath=pathToFolder+tmpFile
    
    print("\nProcessing file "+tmpFile)
    
    if os.path.isfile(fullPath):
        tree=etree.parse(fullPath)
        
    yearKey=int(tmpFile[:3]+"0")
    
    if tree.findall(".//div[@type='chapter']"):
        for chapter in tree.findall(".//div[@type='chapter']"):
            tmp="".join(chapter.itertext())
            numWords=len(re.split('[\n\s]+',tmp))
            words.append(numWords)
            execute=True
    elif tree.findall(".//div[@type='part']"):
        for chapter in tree.findall(".//div[@type='part']"):
            tmp="".join(chapter.itertext())
            numWords=len(re.split('[\n\s]+',tmp))
            words.append(numWords)
            execute=True
    
    else :
        bugs.append(tmpFile+" ; ")
        execute=False
    
    if execute==True:
        average=sum(words)/len(words)
        stats[yearKey].append(average)

for year in sorted(stats.keys()):
    if len(stats[year])>0:
        plot[year]=sum(stats[year])/len(stats[year])

plt.xlim(min(plot),max(plot))
plt.ylim(min(plot.values()),max(plot.values()))

#print(bugs)

x = list(plot.keys())
y = list(plot.values())
plt.title('Nombre de mots par chapitre dans le temps')
plt.plot(x,y,'-')
plt.show()
