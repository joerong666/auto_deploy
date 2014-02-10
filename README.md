auto_deploy
===========

one-key tool for quickly deploy multiple remote applications

Depend:
===========
python
paramiko

Usage:
===========
Step1: 
edit myapp.py、template/*、gen_conf according to your specific configuration

Step2: ./gen_conf
generate concrete configuration template base on configuration template file located in template/*

Step3: ./deploy
show usage for your deployment, for example:
./deploy [check_port|status|config|install|clean|start|stop] [mgr|web|mcproxy|ds|proxy]

Step4: ./deploy config mgr
generate final available configuration

Step4: do operations
check whether port is used on remote machine
./deploy check_port

check whether mgr application is running
./deploy status mgr

install mgr application, be sure stop the application before doing this
./deploy install mgr

remove mgr application directory, be sure stop the application before doing this
./deploy clean mgr
