# ./loop_over_all_files.sh filelist.txt
filelist=`cat $1`
for file in $filelist;
do
  echo $file
  ./pid_trackuri_csv.sh $file > ../processed_data/$file.csv
done
