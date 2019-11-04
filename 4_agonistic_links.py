# -*- coding: utf-8 -*-

output_tmp = "/Users/janarthdheenadhayalan/School/CMU/18-755/Project/output_with_interaction_2.txt"
agonist_links = "/Users/janarthdheenadhayalan/School/CMU/18-755/Project/agonist_links.txt"

if __name__ == "__main__":
        with open(output_tmp) as f, open(agonist_links, "w") as o:
            for line in f:
                data = line.split('|')
                if len(data) > 2:
                    drug = data[0].replace(' ', '_')
                    line_type = data[1]
                    info = data[2]

                if line_type == 'interaction':
                    other_drug = info.replace(' ', '_')
                    if float(data[4]) > 0:
                        o.write(drug + "\t" + other_drug + "\n")
