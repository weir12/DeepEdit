# DeepEdit: Single-molecule detection of A-to-I RNA editing events using Nanopore direct RNA sequencing
## Introduction to DeepEdit
RNA editing regulates genomic functions epigenetically. The electrical signals recorded by Nanopore sequencers are susceptible to base modifications. We present DeepEdit, a neural network model for single-molecule detection of RNA editing events. We trained DeepEdit using the S.pombe datasets, but it still work well in H.sapiens datasets. Thus, we encourage you to use our tools in much more species. 

Unlike previous methods, their are mainly two benefits of DeepEdit -- long read-length and single-molecule resolution. Thus, if you want to check the editing status of a genunie transcript from 5' start to 3' end, or phasing the editing sites to determine whether multiple edited bases co-located on the same or different transcripts, or even check the relationship between specific editing and splicing events, use it!   DeepEdit will give us more opportunity to interpret the biological characteristics and functions of RNA editing events from a new perspective.

## Input and Output
The input of DeeEdit is a .csv file which mainly contain the features of electrical signals spanning target sites. 
These features could be extracted from .fast5 files using Tombo.
An example of input file could be found in DeepEdit/Examples folder.   
### The colomns of input file are:  
1: target sites you want to predict whether they were edited or not;  
2: uuid of Nanopore reads;  
3: the motifs of the target sites. Flanking from -3 to +2 position (0 for target sites).  
4--27: recoding of motifs. ‘A’ was recoded as 1-0-0-0, ‘T’ as 0-1-0-0, ‘C’ as 0-0-1-0, and ‘G’ as 0-0-0-1;  
28--33: Norm_mean values of electrical signals corresponding to the bases in motifs;  
34--39: Norm_std values of electrical signals corresponding to the bases in motifs;  
40--45: normalized Length feature values of each base in motifs. The 'length' features were normalized by dividing the values by 100;  
The output of DeepEdit is the editing probability of target sites. An example of output file could be find in DeepEdit/Examples/Output.csv. It adds the probability value in the 46th column of input file.  

## Usage
### Predict
As we have trained two models using our data, you can use directly by employing the .h5 model file in DeepEdit/trained_models.  
The AI_model could be used to predict whether an 'A' base was edited or not; while the IG_model could be used for distinguishing whether a A-to-G SNV detected on nanopore reads was caused by an A-to-I RNA editing site or a by-product of A-to-G genomic SNPs.  
To predict, please do:  
python DeepEdit.py --mode=predict --predict_csv=your_input.csv --output_fold=your_output.csv --model_name=AI_model.h5
### Train
If you wanna train a new model using your own data, please do:  
python DeepEdit.py --mode=train --train_csv=train.csv --test_csv=test.csv --output_fold=. --model_name=Your_model.h5  

The format of train.csv and test.csv files were shown in DeepEdit/Examples/Train.csv and DeepEdit/Examples/Test.csv, which own the labels (1 for editing and 0 non-editing) at the last column of the files.

## Notations
Currently, DeepEdit gives accurate predictions on trained motifs. But for these un-trained ones, it may perform uncertainly because the electrical signals as the critical element for prediction depend a lot on base sequences. So it is not recommended to predict the sites located in untrained motifs. The trained motifs were listed in the Trained_motifs file in DeepEdit/Examples folder.

