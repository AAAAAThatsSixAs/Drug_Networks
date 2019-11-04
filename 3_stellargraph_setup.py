# -*- coding: utf-8 -*-
import numpy as np

categories = "/Users/janarthdheenadhayalan/School/CMU/18-755/Project/categories_sorted.txt"
output_tmp = "/Users/janarthdheenadhayalan/School/CMU/18-755/Project/output_with_interaction_2.txt"
stellargraph_output = "/Users/janarthdheenadhayalan/School/CMU/18-755/Project/stellargraph_output.txt"

if __name__ == "__main__":
    mapping = {}
    i = 0

    with open(categories) as f:
        for category in f:
            mapping[str(category)] = i
            i += 1

    drug_vector_mapping = {}
    superclass = ""
    drug = ""
    previous_drug = ""

np.set_printoptions(linewidth=np.inf)    
firstTime = True
with open(output_tmp) as f, open(stellargraph_output, "w") as o:
        for line in f:
            data = line.split('|')
            if len(data) > 2:

                drug = data[0].replace(' ', '_')
                line_type = data[1].replace(' ', '_')
                info = data[2].replace(' ', '_')

                if firstTime:
                    previous_drug = drug
                    firstTime = False

                if drug not in drug_vector_mapping.keys():
                    drug_vector_mapping[drug] = np.zeros(i)

                if not previous_drug == drug:
                    o.write(previous_drug + '\t')
                    # o.write(np.array2string(drug_vector_mapping[previous_drug],precision=1,separator=', ',threshold=10000))
                    o.write('\t'.join([str(int(x)) for x in drug_vector_mapping[previous_drug]]))
                    o.write('\t' + superclass + '\n')
                    previous_drug = drug

                if line_type == 'category':
                    drug_vector_mapping[drug][mapping[info]] = 1

                elif line_type == 'classification':
                    superclass = data[3].replace(' ', '_')
