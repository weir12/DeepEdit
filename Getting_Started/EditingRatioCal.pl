#! /usr/bin/perl
use strict;

die "perl <DeepEdit_result.txt> <export> \n" if (@ARGV!=2);

my($result,$out)=@ARGV;

open(RESULT,$result) || die "$!";
open(EXPORT,">$out") || die "$!";

my %site;
my %edited;
<RESULT>;

while(<RESULT>) {
    chomp;
    my @line = split("\,",$_);
    my $locus = $line[0];
    my $probability = $line[3];
    $site{$locus} += 1;
    if($probability >= 0.9){
        $edited{$locus} += 1;
    }
}

print EXPORT "Site\tMapped_reads\tEdited_reads\tEditing_ratio\n";
foreach my $key (keys(%site)){
    print EXPORT $key,"\t",$site{$key},"\t",$edited{$key},"\t",$edited{$key}/$site{$key},"\n";
}

close RESULT;
close EXPORT;
exit;
