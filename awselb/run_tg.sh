log=/home/ec2-user/log/tg_data.log

echo $(TZ=":US/Eastern" date) >> $log
echo "start tg_data_download" >> $log

python3.6 /home/ec2-user/rs/src/run_tg_data.py >> $log

echo "end tg_data_download" >> $log
echo $(TZ=":US/Eastern" date) >> $log
echo "start tg select" >> $log

python3.6 /home/ec2-user/rs/src/print_tg_select_result.py >> $log

echo "end tg select" >> $log
echo $(TZ=":US/Eastern" date) >> $log

