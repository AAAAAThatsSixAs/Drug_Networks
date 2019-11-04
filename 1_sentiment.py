# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import re


xml_file = open("/Users/janarthdheenadhayalan/School/CMU/18-755/Project/db_5.xml", "rb")
output = open("/Users/janarthdheenadhayalan/School/CMU/18-755/Project/output_5.txt", "w+")
not_approved = open("/Users/janarthdheenadhayalan/School/CMU/18-755/Project/not_approved_5.txt", "w+")
xml_data = xml_file.read()
xml_file.close()

class XML_Parser:

    def __init__(self, xml_data):
        self.root         = ET.XML(xml_data)
        self.curr_db_name = ""
        self.approved     = False
        
        # must update weights based on some other analysis of PD/interactions/description/etc.
        # e.g. local anesthetic increasing serum concentration is bad but anticoagulant increasing serum conocentration is good
        self.weights = {
                        "[tT]he risk or severity of.*can be increased.*"     : 0.5,
                        "[tT]he risk or severity of.*can be decreased.*"     : 1.5,
                        "[tT]he metabolism of.*can be increased"             : 0.2,
                        "[tT]he metabolism of.*can be decreased"             : 1.2,
                        ".*may increase.*reduction in efficacy"              : 0.75,
                        ".*may decrease.*higher serum level"                 : 1.2,
                        ".*may increase.*higher serum level"                 : 1.2,
                        ".*serum.*decreased"                                 : 0.2,
                        ".*serum.*increased"                                 : 1.2,
                        "[tT]he therapeutic efficacy of .* can be decreased" : 0.75,
                        "[tT]he therapeutic efficacy of .* can be increased" : 1.75, 
                        "may increase the .* activities of"                  : 1.75,
                        "may decrease the .* activities of"                  : 0.75,
                        ".*bioavailability.*decreased"                       : 0.75,
                        ".*bioavailability.*increased"                       : 1.75,
                        ".*decrease.*absorption"                             : 0.75,
                        ".* worsening of adverse effects"                    : 0.75,
                        ".*loss.*efficacy"                                   : 0.5,
                        ".*excretion.*decreased"                             : 0.3,
                        ".*decrease.*effectiveness"                          : 0.5,
                        ".*risk.*hypersensitivity.*increased"                : 0.75,
                        ".*protein binding.*decreased"                       : 0.3,
                        ".*absorption.*decreased"                            : 0.2,
                        ".*excretion.*increased"                             : 0.3
        }

    def get_sentiment(self, s):
        for key,val in self.weights.items():
            if(re.search(key, s)):
                return str(val)

        return str(99)

    def parse_root(self, root):
        for child in iter(root):
            self.curr_db_name     = ""
            self.approved         = False
            self.found_name       = False
            self.pharmacodynamics = ""
            self.indication       = ""
            self._class           = ""
            self.superclass       = ""
            self.subclass         = ""
            self.direct_parent    = ""

            self.parse_element(child)


    def parse_element(self, element):
      
        if element.text:
            tag = element.tag.encode("ascii",errors="ignore").decode()
            text = element.text.encode("ascii",errors="ignore").decode()
            if tag == 'groups':
                for child in list(element):
                    if child.tag == 'group' and child.text == 'approved':
                        self.approved = True
                        break

                if not self.approved:
                  not_approved.write(self.curr_db_name + "\n")

            elif not self.found_name and tag == 'name':
                self.curr_db_name = text.encode("ascii",errors="ignore").decode()
                self.found_name=True

            elif tag == 'pharmacodynamics' and self.approved:
                self.pharmacodynamics = text.encode("ascii",errors="ignore").decode()
                output.write(self.curr_db_name + "|pharmacodynamics|" + self.pharmacodynamics + "\n")
                
            elif tag == 'indication' and self.approved:
                self.indication = text.encode("ascii",errors="ignore").decode()
                output.write(self.curr_db_name + "|indication|" + self.indication + "\n")
            
            elif tag == 'categories' and self.approved:
                for child in list(element):
                    if child.tag == 'category':
                        for gchild in list(child):
                            if gchild.tag == 'category' and gchild.text:
                                gchild_text = gchild.text.encode("ascii",errors="ignore").decode()
                                output.write(self.curr_db_name + "|category|" + gchild_text + "\n")
        found_class = False
        superclass_found = False
        for child in list(element):
            if tag == 'drug-interactions':
                curr_interaction = ""
                if self.approved:
                    for gchild in list(child):
                        if gchild.tag == 'name':
                            curr_interaction=self.curr_db_name + "|interaction|" + gchild.text.encode("ascii",errors="ignore").decode()

                        elif gchild.tag == 'description':
                            gchild_text = gchild.text.encode("ascii",errors="ignore").decode()
                            curr_interaction += "|" + gchild_text + "|"
                            curr_interaction += self.get_sentiment(gchild_text)
                            output.write(curr_interaction + "\n")

            elif tag == 'classification':
                try:
                    superclass_found = True
                    if self.approved:
                        found_class = True
                        if child.tag == 'superclass':
                            self.superclass = child.text.encode("ascii",errors="ignore").decode()
                        if child.tag == 'direct-parent':
                            self.direct_parent = child.text.encode("ascii",errors="ignore").decode()
                        if child.tag == 'subclass':
                            self.subclass = str(child.text).encode("ascii",errors="ignore").decode()
                        if child.tag == 'class':
                            self._class = child.text.encode("ascii",errors="ignore").decode()
                except:
                    superclass_found = False
                    
            else:         
                self.parse_element(child)

        if found_class and superclass_found:
            output.write(self.curr_db_name + '|classification|' + self._class + '|' + self.superclass + '|' + self.subclass + '|' + self.direct_parent + '\n')

    def process_data(self):
        self.parse_root(self.root)

parsed = XML_Parser(xml_data)
parsed.process_data()


"""
head -7000000 full_db.xml > db_1.xml
head -14000000 full_db.xml | tail -7000000 > db_2.xml
head -21000000 full_db.xml | tail -7000000 > db_3.xml
head -28000000 full_db.xml | tail -7000000 > db_4.xml
tail -4200000 full_db.xml > db_5.xml

"[tT]he risk or severity of.*can be increased.*" -0.5 (991K times)
"[tT]he risk or severity of.*can be decreased.*" 0.5 (1k times)

"[tT]he metabolism of.*can be increased" ?? (88k times)
"[tT]he metabolism of.*can be decreased" ?? (351k times)

".*may increase.*reduction in efficacy" -0.5 (46k times)
".*may decrease.*higher serum level" -0.5 (401k times)

"[tT]he therapeutic efficacy of .* can be decreased" -1 (220K times)
"[tT]he therapeutic efficacy of .* can be increased" 1 (70K times)

"may increase the .* activities of" 1
"may decrease the .* activities of" -1

grep interaction  output.txt | awk -F'|' '{sum[substr($NF,0,23)] += 1; } END { for (s in sum) print s, sum[s];}'  | sort > strings.txt

<description>Potassium may increase the excretion rate of Iodixanol which could result in a lower serum level and potentially a reduction in efficacy.</description>
<description>Goserelin may decrease the excretion rate of Etoperidone which could result in a higher serum level.</description>
$ grep -i "reduction in efficacy"  full_db.xml | wc
  46372 1035062 8218312

DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep -i "reduction in efficacy"  full_db.xml | egrep 'metabolism|risk|severity|theraputic efficacy'

DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep "may increase.*reduction in efficacy"  full_db.xml | wc
  46372 1035062 8218312

DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep "may increase.*" full_db.xml | grep -v "reduction in efficacy"  | wc
 232898 2337952 27448996
It has anticoagulant/antiplatelete activities etc.
DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep "may increase.*" full_db.xml | grep -v "reduction in efficacy"  | less

DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep  "may decrease the .*"  full_db.xml | grep -v activities | less

DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep  "may decrease the .*"  full_db.xml | grep -v activities | grep 'higher serum level' | wc
 401692 6607144 55530786

DEEN@DEEN-HP /cygdrive/c/janarth/CMU/network_proj
$ grep  "may decrease the .*"  full_db.xml | egrep -v 'activities|higher serum level' | wc
     17     941    7158
$ grep  "[tT]he risk or severity of.*increase.*"  full_db.xml | wc
 991874 15964394 137819046

$ grep "[tT]he therapeutic efficacy of .* can be decreased" full_db.xml | wc
 220680 3440938 32069770

$ grep "[tT]he therapeutic efficacy of .* can be increased" full_db.xml | wc
  70218 1001878 9501558

$ grep "[tT]he metabolism of.*can be increased"  full_db.xml | wc
  88800  995182 10075510

$ grep "[tT]he metabolism of.*can be decreased"  full_db.xml | wc
 351094 3915836 39639672

"""
