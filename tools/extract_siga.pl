#!/usr/bin/perl

use warnings;
use strict;
use v5.14;
use utf8::all;

use JSON::Parse 'json_file_to_perl';
use JSON::Create 'create_json';

my $total = json_file_to_perl('../res/basic.json');

my @final_siga_list;

my $json_list = $total->{'feed'}->{'entry'};

my $count = @{$json_list};

foreach my $dirty_siga (@{$json_list}) {
    my $dirty_text = $dirty_siga->{'content'}{'$t'};
    my ($authorid, $text) = ($dirty_text =~ m/^authorid: (\d+), name: (.*)$/);

    my $entry = {
        'text' => $text,
        'authorid' => $authorid,
        'id' => $dirty_siga->{'title'}{'$t'},
    };

    push (@final_siga_list, $entry);
}

my $final_json = create_json(\@final_siga_list);

print $final_json;