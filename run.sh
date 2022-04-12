sudo docker kill root-login-monitor 2> /dev/null ;
sudo docker rm root-login-monitor 2> /dev/null ;

sudo docker run \
--detach \
--name root-login-monitor \
--mount type=bind,source="/var/log/auth.log",target="/auth.log" \
--restart unless-stopped \
--hostname $(hostname) \
root-login-monitor:latest ;
