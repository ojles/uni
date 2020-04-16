#!/usr/bin/perl

use strict;
use warnings;
use diagnostics;

use feature 'say';
use File::Find::Rule;


my $ERR_INVALID_PARAM_NUMBER = 1;
my $ERR_PARAM_NOT_DIR = 2;


sub get_file_stats {
    my ($file_path) = @_;
    open(INFILE, $file_path);

    my $line_count = 0;
    my $chars_count = 0;

    my $line;
    while ($line = <INFILE>) {
        $line_count++;
        $chars_count += length($line);
    }

    close(INFILE);
    return ($line_count, $chars_count);
}


my $argc = scalar @ARGV;

if ($argc >= 1 && $ARGV[0] eq "-h") {
    say 'Usage: search-files.pl DIRECTORY';
    say 'Searches for files with most lines and most characters';
    exit 0;
}

unless ($argc == 1) {
    say STDERR 'Invalid number of parameters!';
    say STDERR "Try 'search-files.pl -h' for more information.";
    exit $ERR_INVALID_PARAM_NUMBER;
}

my ($dir) = @ARGV;

unless (-d $dir) {
    say STDERR "'$dir' is not a directory!";
    exit $ERR_PARAM_NOT_DIR;
}

my @files = File::Find::Rule
    ->file()
    ->in($dir);

if (scalar(@files) eq 0) {
    say 'No files found.';
    exit 0;
}

my %most_lines_file = (
    "path" => $files[0],
    "line_count" => 0
);

my %most_chars_file = (
    "path" => $files[0],
    "chars_count" => 0
);

for (@files) {
    my ($line_count, $chars_count) = get_file_stats($_);
    if ($most_lines_file{line_count} < $line_count) {
        $most_lines_file{path} = $_;
        $most_lines_file{line_count} = $line_count;
    }
    if ($most_chars_file{chars_count} < $chars_count) {
        $most_chars_file{path} = $_;
        $most_chars_file{chars_count} = $chars_count;
    }
}

say "Most lines: $most_lines_file{line_count} $most_lines_file{path}";
say "Most chars: $most_chars_file{chars_count} $most_chars_file{path}";
