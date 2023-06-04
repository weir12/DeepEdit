#!/bin/bash
# Usage: ./Reads_extract2.sh --SiteFile site.bed --BamPath /absolute/path/to/nanopore.sam --Fast5Dir /absolute/path/to/nanopore_reads --Output /absolute/path/to/extracted_reads.txt

while [[ $# -gt 0 ]];do
  key=${1}
  case ${key} in
    --SiteFile)
      Site=${2}
      shift 2
      ;;
    --BamPath)
      Bam=${2}
      shift 2
      ;;
    --Fast5Dir)
      Fast5=${2}
      shift 2
      ;;
    --Output)
      Out=${2}
      shift 2
      ;;
    *)
  esac
done

Outpath=`echo $Out | awk -F"/" 'OFS="/"{$NF="";print}' `
Siteline=`wc -l $Site | awk '{print $1}'`
echo -n "" > $Out

find $Fast5 -name "*.fast5" > $Outpath/fast5Index.txt
for ((i=1; i<=$Siteline; i++))  
do
head -n $i $Site | tail -n 1 > $Outpath/.bed.tmp
cat $Outpath/.bed.tmp | awk '{print ">"$1"\t"$2}' >> $Out
samtools view -F 16 -L $Outpath/.bed.tmp -o $Outpath/.reads.tmp $Bam
editsites_reads=`cat $Outpath/.reads.tmp | awk '{print $1"\n"}'`
for reads in $editsites_reads
do
  grep $reads $Outpath/fast5Index.txt >> $Out
done
done

