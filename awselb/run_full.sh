TODAY=$(TZ=":US/Eastern" date)
echo $TODAY >> /home/ec2-user/log/full_log.txt
python3.6 /home/ec2-user/rs/src/run_full_download_manually.py >> /home/ec2-user/log/full_log.txt
TODAY=$(TZ=":US/Eastern" date)
echo $TODAY >> /home/ec2-user/log/full_log.txt
now=$(date +"%T")
echo "UTC time : $now" >> /home/ec2-user/log/full_log.txt

