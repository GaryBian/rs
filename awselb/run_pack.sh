log=/home/ec2-user/log/pack.log
data_dir=/home/ec2-user/rs/data/

TODAY=$(TZ=":US/Eastern" date)
echo $TODAY >> $log

rm $data_dir/copy.h5
cp $data_dir/daily.h5 $data_dir/copy.h5
rm $data_dir/daily.h5

echo "copy done"
ls -la $data_dir >> $log

ptrepack --chunkshape=auto --propindexes --complevel=9 --complib=blosc $data_dir/copy.h5 $data_dir/daily.h5

echo "ptrepack done" >> $log
rm $data_dir/copy.h5
ls -la $data_dir >> $log

TODAY=$(TZ=":US/Eastern" date)
echo $TODAY >> /$log
now=$(date +"%T")
echo "UTC time : $now" >> $log

