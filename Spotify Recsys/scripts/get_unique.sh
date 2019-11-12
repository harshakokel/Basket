cat $1 | while read line; do echo $line | sed 's/,/\n/g' | sort -r -u | gawk '{line=line $0","} END {print line}' ; done
