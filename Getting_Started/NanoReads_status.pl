#! /usr/bin/perl
use strict;

die "perl <DeepEdit_result.txt> <export> \n" if (@ARGV!=2);

my($result,$out)=@ARGV;

open(RESULT,$result) || die "$!";
open(EXPORT,">$out") || die "$!";

my %site;
my %num;
<RESULT>;

while(<RESULT>) {
    chomp;
    my @line = split("\,",$_);
    my $locus = $line[0];
    my $uuid = $line[1];
    my $probability = $line[3];
    if($probability >= 0.9){
        $num{$uuid} += 1;
        $site{$uuid} = $site{$uuid}."$locus,"
    }
}
print EXPORT "uuid\tEdited_site_num\tEdited_sites\n";
foreach my $key (keys(%site)){
    print EXPORT $key,"\t",$num{$key},"\t",$site{$key},"\n";
}

close RESULT;
close EXPORT;
exit;
