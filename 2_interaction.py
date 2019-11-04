# -*- coding: utf-8 -*-

'''
RUN THESE COMMANDS FIRST

grep '|interaction|' output.txt | awk -F'|' '{ print $1; }' | /usr/bin/sort -u > drugs_with_interaction.txt

#### fgrep -f drugs_with_interaction.txt output.txt > output_with_interaction.txt

python ./2_interaction.py  drugs_with_interaction.txt output.txt > output_with_interaction_2.txt
'''


import sys

drugs_with_interaction=set([])

skip_arr = set([
# 'Hydrocarbon derivatives',
# 'Organic 1,3-dipolar compounds',
# 'Organometallic compounds',
# ‘Organophosphorus compounds’
'Benznidazole',
'Colchicine',
'Amifostine',
'Activated charcoal',
'Oxiconazole',
'Chlorphenesin',
'Rimexolone',
'Prednicarbate',
'Desonide',
'Dimethicone'
])


if __name__ == "__main__":
	for l in open(sys.argv[1]):
	        drugs_with_interaction.add(l.strip())

	for l in open(sys.argv[2]):
	        l=l.strip()
	        flds=l.split("|")
	        if flds[0] not in drugs_with_interaction or flds[0] in skip_arr:
	                continue
	        if len(flds) > 3 and flds[1] == "interaction":
	                if flds[2] in drugs_with_interaction:
	                        print(l)
	        else:
	                print(l)
