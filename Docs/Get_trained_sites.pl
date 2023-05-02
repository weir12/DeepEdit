#! /usr/bin/perl
use strict;

die "perl <ref_transcriptome.fa> <trained_motif> <trained_site.bed> \n" if (@ARGV!=3);

my($ref,$motif,$out)=@ARGV;

open(REF,$ref) || die "$!";
open(MOTIF,$motif) || die "$!";
open(EXPORT,">$out") || die "$!";

my @trained_motif;

while(<MOTIF>) {
    chomp;
    push(@trained_motif,$_);
}

$/="\>";
<REF>;
while(<REF>){
    chomp;
    my($trans_line,$seq) = split /\n/, $_, 2;
    my $trans = (split / /, $trans_line)[0];
    $seq =~ s/[\n]//g;
    my $length = length($seq);
    for(my $i=4; $i<=$length-2; $i++){
        my $motif = substr($seq,$i-4,6);
        if(grep (/$motif/, @trained_motif)){
            print EXPORT $trans,"\t",$i,"\t",$i,"\n";
        }
    }
}

close REF;
close MOTIF;
close EXPORT;
exit;
