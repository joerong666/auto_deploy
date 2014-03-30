#!/bin/env python

from fabric.api import *
from fabric.operations import *
from fabric.colors import *

from app import *

#env.gateway = 'zhengzn@10.1.74.51:9922'
env.hosts = ['zhengzn@10.1.74.50:9922', 'zhengzn@10.1.74.51:9922', 'zhengzn@10.1.74.52:9922']
env.passwords = {
        'zhengzn@10.1.74.50:9922': 'zhengzn', 
        'zhengzn@10.1.74.51:9922': 'zhengzn', 
        'zhengzn@10.1.74.52:9922': 'zhengzn'
}
env.roledefs = {
    'web': env.hosts[2:3],
    'mgr': env.hosts[0:1],
    'ds': env.hosts,
    'proxy': env.hosts[1:2]
}


####################################################################
# Web Tasks
####################################################################
@roles('web')
@task
def install_web_all():
    install_web('web_main')
    install_web('web0')
    install_web('web1')

@roles('web')
@task
def update_web_all():
    update_web('web_main')
    update_web('web0')
    update_web('web1')
    
@roles('web')
@task
def start_web_all():
    start_web('web_main')
    start_web('web0')
    start_web('web1')

@roles('web')
@task
def stop_web_all():
    stop_web('web_main')
    stop_web('web0')
    stop_web('web1')

####################################################################
# Manager Tasks
####################################################################
@roles('mgr')
@task
def install_mgr_all():
    install_mgr('mgr0')
    install_mgr('mgr1')

@roles('mgr')
@task
def update_mgr_all():
    update_mgr('mgr0')
    update_mgr('mgr1')
    
@roles('mgr')
@task
def start_mgr_all():
    start_mgr('mgr0')
    start_mgr('mgr1')

@roles('mgr')
@task
def stop_mgr_all():
    stop_mgr('mgr0')
    stop_mgr('mgr1')

####################################################################
# DS Tasks
####################################################################
@roles('ds')
@task
def install_ds_all():
    install_ds('ds0')
    install_ds('ds1')

@hosts(env.hosts[0])
@task
def start_ds_all_host0():
    start_ds('ds0', '-i %s -p 32001 -s 10.1.74.50:32200' % env.hosts[0])
    start_ds('ds1', '-i %s -p 32002 -s 10.1.74.50:32200' % env.hosts[0])

@hosts(env.hosts[1])
@task
def start_ds_all_host1():
    start_ds('ds0', '-i %s -p 32001 -s 10.1.74.50:32200' % env.hosts[1])
    start_ds('ds1', '-i %s -p 32002 -s 10.1.74.50:32200' % env.hosts[1])

@hosts(env.hosts[2])
@task
def start_ds_all_host2():
    start_ds('ds0', '-i %s -p 32001 -s 10.1.74.50:32200' % env.hosts[2])
    start_ds('ds1', '-i %s -p 32002 -s 10.1.74.50:32200' % env.hosts[2])

@roles('ds')
@task
def stop_ds_all():
    stop('ds0')
    stop('ds1')

####################################################################
# Proxy Tasks
####################################################################
@roles('proxy')
@task
def install_proxy_all():
    install_proxy('proxy0')
    install_proxy('proxy1')

@hosts(env.hosts[1])
@task
def start_proxy_all():
    start_proxy('proxy0', '-i %s -p 32400 -s 10.1.74.50:32200' % env.hosts[1])
    start_proxy('proxy1', '-i %s -p 32401 -s 10.1.74.50:32200' % env.hosts[1])

@roles('proxy')
@task
def stop_proxy_all():
    stop('proxy0')
    stop('proxy1')

