#!/bin/bash
# Usage: ./Reads_extract2.sh --SiteFile site.bed --BamPath /public/chenlx/nanopore/DeepEdit_manual/Map2trans.sam --Fast5Dir /public/chenlx/nanopore/DeepEdit_manual/nanopore_reads --Output extracted_reads.txt

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

find $Fast5 -name "*.fast5" > .fast5Index.tmp
for ((i=1; i<=`wc -l $Site | awk '{print $1}'`; i++))  
do
head -n $i $Site | tail -n 1 > .bed.tmp
cat .bed.tmp | awk '{print ">"$1"\t"$2}' >> $Out
samtools view -L .bed.tmp -o .reads.tmp $Bam
editsites_reads=`cat .reads.tmp | awk '{print $1"\n"}'`
for reads in $editsites_reads
do
  grep $reads .fast5Index.tmp >> $Out
done
done

