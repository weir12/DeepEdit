#python x.py <sites_and_reads>

import re
import h5py
import sys

file=sys.argv[1]

#output=open('feature.txt','a', encoding = 'utf-8')
with open(file,'r') as file_obj:
    for content in file_obj:
        try:
            content=content.strip()
            m = re.search('>(\S+)\s*(.*)', content)
            if m:
                transi = m.group(1)
                position = m.group(2)
#               output.write('{0}\n'.format(content))
            else:
                fast5_fn=content
                fast5_line=fast5_fn.split("/")
                uuid=fast5_line[-1].split(".")[0]
                fast5_data=h5py.File(fast5_fn,'r')
                chrom=fast5_data['Analyses']['RawGenomeCorrected_001']['BaseCalled_template']['Alignment'].attrs['mapped_chrom']
                start=fast5_data['Analyses']['RawGenomeCorrected_001']['BaseCalled_template']['Alignment'].attrs['mapped_start']
                locus_on_reads=int(position)-start
                if locus_on_reads <= 6:
                    continue
                else:
                    signal_mean=fast5_data['Analyses']['RawGenomeCorrected_001']['BaseCalled_template']['Events']['norm_mean']
                    signal_std=fast5_data['Analyses']['RawGenomeCorrected_001']['BaseCalled_template']['Events']['norm_stdev']
                    signal_length=fast5_data['Analyses']['RawGenomeCorrected_001']['BaseCalled_template']['Events']['length']
                    signal_motif=fast5_data['Analyses']['RawGenomeCorrected_001']['BaseCalled_template']['Events']['base']
                    if len(signal_motif[locus_on_reads-4:locus_on_reads+2]) != 6 or len(signal_mean[locus_on_reads-4:locus_on_reads+2]) != 6 or len(signal_std[locus_on_reads-4:locus_on_reads+2]) != 6 or len(signal_length[locus_on_reads-4:locus_on_reads+1]) != 6:
                        continue
                    print(transi,end='-')
                    print(position,end=',')
                    print(uuid,end=',')
                    for i in signal_motif[locus_on_reads-4:locus_on_reads+2]:
                        print(str(i.decode("gbk")),end='')
                    print(',',end='')
                    for i in signal_motif[locus_on_reads-4:locus_on_reads+2]:
                        base = str(i.decode("gbk")).upper()
                        if 'A' in base:
                            print("1,0,0,0",end=',')
                        elif 'T' in base:
                            print("0,1,0,0",end=',')
                        elif 'G' in base:
                            print("0,0,1,0",end=',')
                        else:
                            print("0,0,0,1",end=',')
                    for i in signal_mean[locus_on_reads-4:locus_on_reads+2]:
                        print(i,end=',')
                    for i in signal_std[locus_on_reads-4:locus_on_reads+2]:
                        print(i,end=',')
                    for i in signal_length[locus_on_reads-4:locus_on_reads+1]:
                        print(i/100,end=',')
                    print(signal_length[locus_on_reads+1]/100,end='')
                    print('\n',end='')
        except:
            continue
