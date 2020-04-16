#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;

use feature 'say';
use File::Copy;
use File::Find::Rule;


my $ERR_INVALID_USAGE = 1;
my $ERR_PARAM_NOT_DIR = 2;

sub print_help {
    say 'Usage: copy-cpp.pl SOURCE_DIR DESTINATION_DIR';
    say 'Move all .cpp files in subdirectories of SOURCE_DIR to DESTINATION_DIR';
}

sub print_invalid_usage {
    say STDERR 'Invalid number of parameters!';
    say STDERR "Try 'copy-cpp.pl -h' for more information.";
}

my $argc = scalar @ARGV;

if ($argc >= 1 && $ARGV[0] eq "-h") {
    print_help;
    exit 0;
} elsif ($argc != 2) {
    print_invalid_usage;
    exit $ERR_INVALID_USAGE;
}


my ($source_dir, $destination_dir) = @ARGV;

unless (-d $source_dir) {
    say STDERR 'First parameters is not a directory!';
    exit $ERR_PARAM_NOT_DIR;
}

unless (-d $destination_dir) {
    say STDERR 'Second parameters is not a directory!';
    exit $ERR_PARAM_NOT_DIR;
}


my @subdirs = File::Find::Rule
    ->directory
    ->in($source_dir);
shift @subdirs;

my @cpp_files = File::Find::Rule
    ->file()
    ->name('*.cpp')
    ->in(@subdirs);

for (@cpp_files) {
    move($_, $destination_dir);
}
