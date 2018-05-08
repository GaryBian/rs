bash /home/ec2-user/run_pack.sh

echo "pack done"

TODAY=$(TZ=":US/Eastern" date)
echo $TODAY >> /home/ec2-user/log/incremental_log.txt

echo "start incremental"

python3.6 /home/ec2-user/rs/src/run_incremental_download.py >> /home/ec2-user/log/incremental_log.txt
TODAY=$(TZ=":US/Eastern" date)
echo $TODAY >> /home/ec2-user/log/incremental_log.txt
now=$(date +"%T")
echo "UTC time : $now" >> /home/ec2-user/log/incremental_log.txt

