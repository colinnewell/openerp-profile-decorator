use strict;
use warnings;
use List::MoreUtils qw/uniq/;
my $in_trace = 0;
my $trace;
my @traces;
while(<>)
{
    if($in_trace)
    {
        if(/end stack trace/)
        {
            $in_trace = 0;
            push @traces, $trace;
        }
        else
        {
            s/^.* DEBUG \w+ openerp.addons.account.account_move_line://;
            push @$trace, $_;
        }
    }
    else
    {
        if(/start stack trace/)
        {
            $in_trace = 1;
            $trace = [];
        }
    }
}
my @unique = uniq map { join "", @{$_} } @traces;
for my $trace (@unique)
{
    print $trace, "\n";
    print "-"x60,"\n";
}
