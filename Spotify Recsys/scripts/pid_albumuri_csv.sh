egrep '"pid"|"album_uri"' $1 | sed 's/"pid": /\n/g' | sed 's/"album_uri": //g' | sed -E -e 's/\s+//g' | tr '",\n' '",'  | sed 's/,,,/\n/g' | sed 's/,,/,/g' | sed 's/^,//g'
