id=$2
echo "ssh into csews$id for launching daemons"
ssh -q -o ConnectTimeout=2 csews$id python3 ~/UGP/eagle/livehosts/livehostsd.py $1
echo " "
