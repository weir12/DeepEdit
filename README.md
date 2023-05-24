# DeepEdit

RNA editing is a universal and critical post-transcriptional event discovered in diverse life forms. The electrical signals recorded by Nanopore sequencers are susceptible to base modifications. We present DeepEdit, a neural network model for single-molecule detection and phasing of A-to-I RNA editing events using nanopore direct RNA sequencing. 

Please check updates on https://github.com/weir12/DeepEdit. 

## Getting Started

We have provided the scripts and required files in DeepEdit/Getting_Started folders. You can run DeepEdit following the steps described below. 

### 1. Basecalling and mapping

***Requisites:***

​	softwares: guppy, minimap2 (version 2.10-r761)

​	files: .fast5 nanopore reads

```bash
# basecalling
guppy_basecaller -i DeepEdit/Getting_Started/nanopore_reads/ -s DeepEdit/Getting_Started/nanopore_reads/ --flowcell FLO-MIN106 --kit SQK-RNA001 --cpu_threads_per_caller 1 --qscore_filtering --fast5_out
# mapping
minimap2 -t 16 -ax map-ont -p 1.0 --secondary=no -u f -a DeepEdit/Getting_Started/GCF_000002945.1_ASM294v2_rna.fna DeepEdit/Getting_Started/nanopore.fastq > nanopore.sam
```

***Note***

​	The .fast5 files provided by sequencing company usually have been basecalled by guppy.

### 2. Resquiggle

***Requisites:***

​	softwares: Tombo (version 1.5.1)

​	files: basecalled .fast5 nanopore reads

```bash
tombo resquiggle DeepEdit/Getting_Started/nanopore_reads/ DeepEdit/Getting_Started/GCF_000002945.1_ASM294v2_rna.fna --processes 64 --corrected-group RawGenomeCorrected_001 --basecall-group Basecall_1D_001 --include-event-stdev --overwrite
```

### 3. Feature extraction

***Requisites:***

​	Python(3.8.3) modules: re, sys, h5py(2.10.0)

​    samtools

​	files: 

​		1. target_site.bed: This is a .bed file containing the sites of your interest. The first column of this file is the transcript id, the second and third column are the site location. Please refer to the example file (DeepEdit/Getting_Started/target_site.bed) for detail. 

```bash
# 1. Get the nanopore reads that mapped to the target sites
# Please provide the absolute path of BamPath and Fast5Dir
sh 1.Reads_extract.sh --SiteFile target_site.bed \
--BamPath DeepEdit/Getting_Started/nanopore.sam \
--Fast5Dir DeepEdit/Getting_Started/nanopore_reads \
--Output target_site_reads.txt
# 2. Extract features
# Get the values in 'RawGenomeCorrected_001' slot. 
python 2.feature_extract.py target_site_reads.txt > target_site_features.csv
```

***Note***

1. Please provide the absolute path of BamPath and Fast5Dir

2. The columns of target_site_features.csv file are:

   1, target sites of interest;
   2, uuid of nanopore reads;
   3, motifs of the target sites. Flanking from -3 to +2 positions (0 for target site). 

   ***It is challenging for DeepEdit to predict RNA editings located in untrained motif contexts. Please check whether the motifs of target sites have been trained in the our provided model. The trained motifs were listed in the Trained_motifs_v1.0.txt file in DeepEdit/Docs folder***

   4--27, recoding of motifs. ‘A’ was recoded as 1-0-0-0, ‘T’ as 0-1-0-0, ‘C’ as 0-0-1-0, and ‘G’ as 0-0-0-1;
   28--33, Norm_mean values of electrical signals corresponding to the bases in motifs;
   34--39, Norm_std values of electrical signals corresponding to the bases in motifs;
   40--45, normalized Length feature values of each base in motifs. The 'length' features were normalized by dividing the values by 100;

3. In step two, the ***--corrected-group*** parameter was set to ***RawGenomeCorrected_001***, so the resquiggling information would be saved in that slot. The correct values can also be extracted here. If the --corrected-group parameter is set to a different value in step two, then the RawGenomeCorrected_001 in the 2.feature_extract.py script should be changed to the specific location accordingly.	

4. Features can also be extracted using ***tombo-python-api***. The feature file can be used as input of DeepEdit as long as it conforms to the file format described above. Please refer to https://nanoporetech.github.io/tombo/tombo.html#tombo-python-api for detail. 

### 4. Prediction and statistics

***Requisites:***

​	Python(3.8.3) modules: keras(2.4.3), argparse, os, sys, pandas(1.0.5), joblib(0.16.0),numpy(1.18.5)

```bash
# Predict editing status
python DeepEdit.py --mode=predict --predict_csv=target_site_features.csv --output_fold=. --model_name=S.pombe_model.h5
```

You will get a ***DeepEdit_result.txt*** file after this step. 

The columns of DeepEdit_result.txt file are:

​	1, target sites of interest;

​	2, uuid of nanopore reads;

​	3, the motifs of the target sites. Flanking from -3 to +2 position (0 for target sites);

​	4, probability of A-to-I editing occurrence. 

```bash
# Calculate the editing ratio of each site
perl EditingRatioCal.pl DeepEdit_result.txt Editing_ratio.txt
# Check the editing status of each nanopore read
perl NanoReads_status.pl DeepEdit_result.txt NanoReads_status.txt
```



### 5. Train your own models

If you want to train a new model using your own data, please do:

```bash
python DeepEdit.py --mode=train --train_csv=train.csv --test_csv=test.csv --output_fold=. --model_name=Your_model.h5
```

The format of train.csv and test.csv files were shown in DeepEdit/Docs/Train.csv and DeepEdit/Docs/Test.csv, which own the labels (1 for editing and 0 non-editing) at the last column of the files.

## Contact

Any questions or suggestions, please send emails to lxchen.gogo@gmail.com. 