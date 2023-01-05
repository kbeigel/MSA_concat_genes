#!/usr/bin/python

# Concatenage multiple genes from multiple sequence alginments

import re

def Read_File(file_name):

	data = {}
	with open(file_name, 'r') as infile:

	    text = infile.readlines()

	    previous_key = ''
	    for line in text:
	        if line.startswith('>'):
	            previous_key = line.strip()
	            previous_key = previous_key.replace(" ", "_")
	            suffix = re.compile("(_[a-zA-Z0-9]+$)")	         
	            std_key = suffix.sub("", previous_key)
	            prefix = re.compile("([^>][a-zA-Z0-9]+_)")
	            std_key = prefix.sub("", std_key)
	            dot_num = re.compile("(\\.[0-9])")
	            std_key = dot_num.sub("", std_key)
	        elif std_key != '':
	            data[std_key] = line.strip()
	            std_key = ''
	return data

if __name__ == '__main__':

	working_dir = '5spp_TaTpTsMtTi_alignments/5spp_fasta-out/'
	Ef1a_raw = Read_File(working_dir+'TaTpTsMtTi_Ef1a_Atexana-outgroup_trimmed-alignment.fas')
	LwRh_raw = Read_File(working_dir+'TaTpTsMtTi_LWR_Atexana-outgroup_trimmed-alignment.fas')
	Wg_raw = Read_File(working_dir+'TaTpTsMtTi_Wg_Atexana-outgroup_trimmed-alignment.fas')

	output_dir = '5spp_TaTpTsMtTi_alignments/5spp_fasta-out/'
	with open(output_dir+'F_ordered_Atta_outgroup_final.fas', 'w') as outfile:
	    for key in Ef1a_raw.keys():
	        outfile.write(key)
	        outfile.write('\n')
	        outfile.write(Ef1a_raw[key])
	        outfile.write('\n')

	with open(output_dir+'LR_ordered_Atta_outgroup_final.fas', 'w') as outfile:
	    for key in LwRh_raw.keys():
	        outfile.write(key)
	        outfile.write('\n')
	        outfile.write(LwRh_raw[key])
	        outfile.write('\n')

	with open(output_dir+'WG_ordered_Atta_outgroup_final.fas', 'w') as outfile:
	    for key in Wg_raw.keys():
	        outfile.write(key)
	        outfile.write('\n')
	        outfile.write(Wg_raw[key])
	        outfile.write('\n')


	Ef1a = Read_File(output_dir+'F_ordered_Atta_outgroup_final.fas')
	LwRh = Read_File(output_dir+'LR_ordered_Atta_outgroup_final.fas')
	Wg = Read_File(output_dir+'WG_ordered_Atta_outgroup_final.fas')


	concatenated_data = {}
	for key in Ef1a.keys():
	    print(key)
	    concatenated_data[key] = Ef1a[key] + LwRh[key] + Wg[key]


	with open(output_dir+'Ef1a_LwRh_Wg_5spp_concat.fas', 'w') as outfile:
	    for key in concatenated_data.keys():
	        outfile.write(key)
	        outfile.write('\n')
	        outfile.write(concatenated_data[key])
	        outfile.write('\n')


	Ef1a_length = len(list(Ef1a.values())[0])
	Ef1a_start = 1
	Ef1a_end = Ef1a_length 
	print(Ef1a_length)

	LwRh_length = len(list(LwRh.values())[0])
	LwRh_start = 1 + Ef1a_end
	LwRh_end = LwRh_start + LwRh_length - 1
	print(LwRh_length)

	Wg_length = len(list(Wg.values())[0])
	Wg_start = 1 + LwRh_end
	Wg_end = Wg_start + Wg_length - 1
	print(Wg_length)

	with open(output_dir+'partition.nex.txt', 'w') as outfile:
		outfile.write('#nexus\n')
		outfile.write('begin sets;\n')
		outfile.write('charset part1 = {0}-{1}\n'.format(Ef1a_start, Ef1a_end))
		outfile.write('charset part2 = {0}-{1}\n'.format(LwRh_start, LwRh_end))
		outfile.write('charset part3 = {0}-{1}\n'.format(Wg_start, Wg_end))
		outfile.write('charpartition mine = XXX:part1, XXX:part2, XXX:part3;\n')
		outfile.write('end;')