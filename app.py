#!/bin/env python

from fabric.api import *
from fabric.operations import *
from fabric.colors import *

#env.gateway = 'zhengzn@10.1.74.51:9922'
#env.hosts = ['zhengzn@10.1.74.50:9922', 'zhengzn@10.1.74.51:9922', 'zhengzn@10.1.74.52:9922']
#env.roledefs = {
#    'web': env.hosts[2:],
#    'manager': env.hosts[0],
#    'proxy': env.hosts[1],
#    'ds': env.hosts
#}

g_pkg_ver = "beta"
g_pkg_mgr = "fooyun-mngrserver-%s" % g_pkg_ver
g_pkg_proxy = "fooyun-proxy-%s" % g_pkg_ver
g_pkg_ds = "fooyun-dataserver-%s" % g_pkg_ver
g_pkg_web = "fooyun-web-%s" % g_pkg_ver

#remote
g_remote_path = "local/fooyun-robot-%s" % g_pkg_ver
g_app_home = "~/%s" % g_remote_path 

#local
g_local_pkg_path = "/home/joerong/work/fooyun/fooyun/source/dev/dist"
g_local_cnf_path = "/home/joerong/work/fooyun/fooyun/source/dev/testing/env_robot/conf"

####################################################################
# Common Tasks
####################################################################
@task
def init(version=None, lo_pkg_path=None, lo_cnf_path=None, re_path=None):
    if version: g_pkg_ver = version
    if lo_pkg_path: g_local_pkg_path = lo_pkg_path
    if lo_cnf_path: g_local_cnf_path = lo_cnf_path
    if re_path: g_remote_path = re_path

@task
def call(cmd):
    with settings(warn_only=True):
        run(cmd)

@task
def status(id):
    with settings(warn_only=True):
        run("ls -ld %s/%s" % (g_app_home, id))
        run("ps -ef |fgrep '/%s/%s/' |grep -v 'fgrep'" % (g_remote_path, id))

@task
def stop(id, force=False):
    with settings(warn_only=True):
        sig = "-9" if force else "" 
        run("ps -ef |fgrep '/%s/%s/' |grep -v 'fgrep' |awk '{print $2}' |xargs kill %s" % 
            (g_remote_path, id, sig))

@task
def clean(id):
    with settings(warn_only=True):
        stop(id, True)
        run("rm -rf %s/%s && rmdir %s" % (g_app_home, id, g_app_home))

@task
def show():
    with settings(warn_only=True):
        run("ls -l %s" % g_app_home)

def _install(id, pkg):
    clean(id)

    run("mkdir -p %s/%s" % (g_app_home, id))
    put("%s/%s.tar.gz" % (g_local_pkg_path, pkg), "%s/%s/" % (g_app_home, id))
    run("cd %s/%s && tar xf %s.tar.gz" % (g_app_home, id, pkg))

####################################################################
# Web Tasks
####################################################################
@task
def install_web(id):
    with settings(warn_only=True):
        _install(id, g_pkg_web)

        with lcd("%s/%s" % (g_local_cnf_path, id)):
            put("application.conf", "%s/%s/%s/conf/" % (g_app_home, id, g_pkg_web))

@task
def update_web(id):
    with settings(warn_only=True):
        stop(id, True)

        with lcd("%s/%s" % (g_local_cnf_path, id)):
            put("application.conf", "%s/%s/%s/conf/" % (g_app_home, id, g_pkg_web))

        start_web(id)

@task
def start_web(id):
    with settings(warn_only=True):
        with cd("%s/%s/%s" % (g_app_home, id, g_pkg_web)):
            run("rm server.pid")
            run("(nohup play run &) && sleep 1")

####################################################################
# Manager Tasks
####################################################################
@task
def install_mgr(id):
    with settings(warn_only=True):
        _install(id, g_pkg_mgr)

        with lcd("%s/%s" % (g_local_cnf_path, id)):
            put("fooyun_mngr.ini", "%s/%s/%s/bin/" % (g_app_home, id, g_pkg_mgr))
            put("foo_conf.lua", "%s/%s/%s/script/" % (g_app_home, id, g_pkg_mgr))

@task
def update_mgr(id):
    with settings(warn_only=True):
        stop(id, True)

        with lcd("%s/%s" % (g_local_cnf_path, id)):
            put("fooyun_mngr.ini", "%s/%s/%s/bin/" % (g_app_home, id, g_pkg_mgr))
            put("foo_conf.lua", "%s/%s/%s/script/" % (g_app_home, id, g_pkg_mgr))

        start_mgr(id)

@task
def start_mgr(id):
    with settings(warn_only=True):
        with cd("%s/%s/%s" % (g_app_home, id, g_pkg_mgr)):
            run("cd bin && `pwd`/uchas -f fooyun_mngr.ini -d")

####################################################################
# DS Tasks
####################################################################
@task
def install_ds(id):
    with settings(warn_only=True):
        _install(id, g_pkg_ds)

@task
def start_ds(id, args):
    with settings(warn_only=True):
        with cd("%s/%s/%s" % (g_app_home, id, g_pkg_ds)):
            run("`pwd`/data-server %s" % args)

####################################################################
# Proxy Tasks
####################################################################
@task
def install_proxy(id):
    with settings(warn_only=True):
        _install(id, g_pkg_proxy)
        
@task
def start_proxy(id, args):
    with settings(warn_only=True):
        with cd("%s/%s/%s" % (g_app_home, id, g_pkg_proxy)):
            run("`pwd`/fy_proxy %s" % args)

