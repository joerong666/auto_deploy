#####################Global############################
g_pkg_ver = "1.0.0-beta3"
g_pkg_mgr = "fooyun-mngrserver-%s" % g_pkg_ver
g_pkg_proxy = "fooyun-proxy-%s" % g_pkg_ver
g_pkg_ds = "fooyun-dataserver-%s" % g_pkg_ver
g_pkg_web = "fooyun-web-%s" % g_pkg_ver
g_pkg_mcproxy = "mcproxy-v9"

g_app_home = "/home/zhengzn/local/fooyun-%s" % g_pkg_ver

g_lo_dist = ".."
g_lo_cnf = "./conf"

#ports on ip0
g_port0 = []
g_port0_ds = ["3151%s" % i for i in range(1, 5)]
g_port0.extend(g_port0_ds)
g_port0_mgr = ["3251%s" % i for i in range(1, 5)]
g_port0.extend(g_port0_mgr)
g_port0_mcproxy = ["3351%s" % i for i in range(1, 2)]
g_port0.extend(g_port0_mcproxy)

#ports on ip1
g_port1 = []
g_port1_ds = ["3151%s" % i for i in range(1, 5)]
g_port1.extend(g_port1_ds)
g_port1_ds_slave = ["3152%s" % i for i in range(1, 5)]
g_port1.extend(g_port1_ds_slave)
g_port1_proxy = ["3451%s" % i for i in range(1, 5)]
g_port1.extend(g_port1_proxy)

#ports on ip2
g_port2 = []
g_port2_ds = ["3151%s" % i for i in range(1, 5)]
g_port2.extend(g_port2_ds)
g_port2_web = ["3551%s" % i for i in range(1, 6)]
g_port2.extend(g_port2_web)

g_ssh_list = [
        {"host": "10.1.74.50", "port": 9922, "user": "zhengzn", "passwd": "zhengzn", "app_home": g_app_home,
         "listen_port": "|".join(g_port0)
        }, 
        {"host": "10.1.74.51", "port": 9922, "user": "zhengzn", "passwd": "zhengzn", "app_home": g_app_home, 
         "listen_port": "|".join(g_port1)
        }, 
        {"host": "10.1.74.52", "port": 9922, "user": "zhengzn", "passwd": "zhengzn", "app_home": g_app_home,
         "listen_port": "|".join(g_port2) 
        }  
      ]

#all ip
g_ds_ssh_list = g_ssh_list[:]
g_ds_inst = ["ds%s" % i for i in range(0, 4)]

#ip0
g_mgr_ssh_list = [g_ssh_list[0]]
g_mgr_inst = ["mgr%s" % i for i in range(0, 4)]

g_mcproxy_ssh_list = [g_ssh_list[0]]
g_mcproxy_inst = ["mcproxy%s" % i for i in range(0, 1)]

#ip1
g_proxy_ssh_list = [g_ssh_list[1]] 
g_proxy_inst = ["proxy%s" % i for i in range(0, 4)]

#ip2
g_web_ssh_list = [g_ssh_list[2]]
g_web_inst = ["web%s" % i for i in range(0, 5)]

#######################################################

from os import system

class AppBase(object):
    instance = None

    def __init__(self):
        self.lo_dist = g_lo_dist
        self.lo_cnf = g_lo_cnf
        
        self.apps = {}
        self.app_home = "${app_home}"
        self.bin_dir = "${bin_dir}"

    @staticmethod
    def singleton():
        if not AppBase.instance:
            AppBase.instance = AppBase()

        return AppBase.instance

    def get_apps(self):
        if not self.apps:
            self.apps = {"ds": AppDS(), "mgr": AppMgr(), "proxy": AppProxy(), 
                         "web": AppWeb(), "mcproxy": AppMcproxy()}

        return self.apps

    def get_app_ids(self):
        return self.get_apps().keys()

    def get_app_home(self):
        return self.app_home

    def get_bin_dir(self):
        #equals to: app_home/inst_name
        return self.bin_dir

    def get_ssh(self):
        return g_ssh_list

    def get_svr(self):
        pass

    def get_inst(self):
        pass

    def get_tar(self):
        pass

    def get_cnf(self):
        pass

    def config(self, inst_name):
        pass

    def clean_cmd(self):
        return "rm -r %s && cd .. && rmdir %s" % (self.get_bin_dir(), self.get_app_home())

    def status_cmd(self):
        pass

    def start_cmd(self):
        pass

    def stop_cmd(self):
        pass

class AppDS(AppBase):

    def __init__(self):
        super(AppDS, self).__init__()

    def get_svr(self):
        return g_ds_ssh_list 

    def get_ssh(self):
        return g_ds_ssh_list

    def get_inst(self):
        return g_ds_inst

    def get_tar(self):
        tar = []
        for i in g_ds_inst:
            tar.append({"lo": self.lo_dist, "re": i, "file": "%s.tar.gz" % g_pkg_ds, "cb": self.config}) 

        return tar

    def get_cnf(self):
        cnf = []
        for i in g_ds_inst:
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s" % (i, g_pkg_ds), 
                "file": "ds.conf"})

        return cnf

    def config(self, inst_name):
        cnf = "ds.conf"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "sed"
        for i in range(len(g_ssh_list)):
            cmd = cmd + " -e 's/${server%d}/%s/g'" % (i, (g_ssh_list[0])["host"])

        for i in range(len(g_port0_ds)):
            cmd = cmd + " -e 's/${port_ds%d}/%s/g'" % (i, g_port0_ds[i])

        for i in range(len(g_port0_mgr)):
            cmd = cmd + " -e 's/${port_mgr%d}/%s/g'" % (i, g_port0_mgr[i])

        system("%s %s >%s/%s/%s" % (cmd, cnf_template, g_lo_cnf, inst_name, cnf))
                    
    def status_cmd(self):
        return "ps x|grep data-server |grep -v 'grep'"

    def start_cmd(self):
        return "cd %s/%s && ./data-server -f %s/%s/ds.conf" \
                  % (self.bin_dir, g_pkg_ds, self.bin_dir, g_pkg_ds)   

    def stop_cmd(self):
        return "ps -ef |fgrep '%s/%s/ds.conf' |grep -v 'fgrep' |awk '{print $2}' |xargs kill" \
                  % (self.bin_dir, g_pkg_ds)


class AppMgr(AppBase):

    def __init__(self):
        super(AppMgr, self).__init__()

    def get_svr(self):
        return g_mgr_ssh_list

    def get_ssh(self):
        return g_mgr_ssh_list

    def get_inst(self):
        return g_mgr_inst 

    def get_tar(self):
        tar = []
        for i in g_mgr_inst:
            tar.append({"lo": self.lo_dist, "re": i, "file": "%s.tar.gz" % g_pkg_mgr, "cb": self.config}) 

        return tar

    def get_cnf(self):
        cnf = []
        for i in g_mgr_inst:
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s/script" % (i, g_pkg_mgr), "file": "foo_conf.lua"})
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s/script/bin" % (i, g_pkg_mgr), "file": "fooyun_mngr.ini"})

        return cnf

    def config(self, inst_name):
        #import pdb
        #pdb.set_trace()
        cnf = "fooyun_mngr.ini"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "sed"
        for i in range(len(g_ssh_list)):
            cmd = cmd + " -e 's/${server%d}/%s/g'" % (i, (g_ssh_list[0])["host"])

        for i in range(len(g_port0_mgr)):
            cmd = cmd + " -e 's/${port_mgr%d}/%s/g'" % (i, g_port0_mgr[i])

        system("%s %s >%s/%s/%s" % (cmd, cnf_template, g_lo_cnf, inst_name, cnf))

        cnf = "foo_conf.lua"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "cp %s %s/%s/%s" % (cnf_template, g_lo_cnf, inst_name, cnf)
        system(cmd)
 
    def status_cmd(self):
        return "ps x|grep uchas|grep mngr |grep -v 'grep'"

    def start_cmd(self):
        return "cd %s/%s/script/bin && ./uchas -f %s/%s/script/bin/fooyun_mngr.ini -d" \
                  % (self.bin_dir, g_pkg_mgr, self.bin_dir, g_pkg_mgr)

    def stop_cmd(self):
        return "ps -ef |fgrep '%s/%s/script/bin/fooyun_mngr.ini' |grep -v 'fgrep' |awk '{print $2}' |xargs kill -9" \
                  % (self.bin_dir, g_pkg_mgr)


class AppProxy(AppBase):

    def __init__(self):
        super(AppProxy, self).__init__()

    def get_svr(self):
        return g_proxy_ssh_list

    def get_ssh(self):
        return g_proxy_ssh_list

    def get_inst(self):
        return g_proxy_inst 

    def get_tar(self):
        tar = []
        for i in g_proxy_inst:
            tar.append({"lo": self.lo_dist, "re": i, "file": "%s.tar.gz" % g_pkg_proxy, "cb": self.config}) 

        return tar

    def get_cnf(self):
        cnf = []
        for i in g_proxy_inst:
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s" % (i, g_pkg_proxy), "file": "proxy.ini"})

        return cnf

    def config(self, inst_name):
        cnf = "proxy.ini"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "sed"
        for i in range(len(g_ssh_list)):
            cmd = cmd + " -e 's/${server%d}/%s/g'" % (i, (g_ssh_list[0])["host"])

        for i in range(len(g_port1_proxy)):
            cmd = cmd + " -e 's/${port_proxy%d}/%s/g'" % (i, g_port1_proxy[i])

        for i in range(len(g_port0_mgr)):
            cmd = cmd + " -e 's/${port_mgr%d}/%s/g'" % (i, g_port0_mgr[i])

        system("%s %s >%s/%s/%s" % (cmd, cnf_template, g_lo_cnf, inst_name, cnf))
 
    def status_cmd(self):
        return "ps x|grep proxy_d |grep -v 'grep'"

    def start_cmd(self):
        return "cd %s/%s && (nohup ./proxy_d -f %s/%s/proxy.ini >/dev/null 2>&1 &)" \
                 % (self.bin_dir, g_pkg_proxy, self.bin_dir, g_pkg_proxy)

    def stop_cmd(self):
        return "ps -ef |fgrep '%s/%s/proxy.ini' |grep -v 'fgrep' |awk '{print $2}' |xargs kill" \
                 % (self.bin_dir, g_pkg_proxy)


class AppWeb(AppBase):

    def __init__(self):
        super(AppWeb, self).__init__()

    def get_svr(self):
        return g_web_ssh_list

    def get_ssh(self):
        return g_web_ssh_list

    def get_inst(self):
        return g_web_inst 

    def get_tar(self):
        tar = []
        for i in g_web_inst:
            tar.append({"lo": self.lo_dist, "re": i, "file": "%s.tar.gz" % g_pkg_web, "cb": self.config}) 

        return tar

    def get_cnf(self):
        cnf = []
        for i in g_web_inst:
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s/conf" % (i, g_pkg_web), "file": "application.conf"})

        return cnf

    def config(self, inst_name):
        cnf = "application.conf"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "sed"
        for i in range(len(g_port2_web)):
            cmd = cmd + " -e 's/${port_web%d}/%s/g'" % (i, g_port2_web[i])

        system("%s %s >%s/%s/%s" % (cmd, cnf_template, g_lo_cnf, inst_name, cnf))
 
    def status_cmd(self):
        return "ps x|grep play |grep -v 'grep'"

    def start_cmd(self):
        return "source /etc/profile && source ~/.bash_profile \
                && cd %s/%s && (play restart >/dev/null 2>&1 &) \
                && sleep 1 && tail -3 logs/info/info.log" % (self.bin_dir, g_pkg_web)

    def stop_cmd(self):
        return "cd %s/%s && source ~/.bash_profile && play stop" % (self.bin_dir, g_pkg_web)

class AppMcproxy(AppBase):

    def __init__(self):
        super(AppMcproxy, self).__init__()

    def get_svr(self):
        return g_mcproxy_ssh_list

    def get_ssh(self):
        return g_mcproxy_ssh_list

    def get_inst(self):
        return g_mcproxy_inst 

    def get_tar(self):
        tar = []
        for i in g_mcproxy_inst:
            tar.append({"lo": self.lo_dist, "re": i, "file": "%s.tar.gz" % g_pkg_mcproxy, "cb": self.config}) 

        return tar

    def get_cnf(self):
        cnf = []
        for i in g_mcproxy_inst:
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s/script" % (i, g_pkg_mcproxy), "file": "app_conf.lua"})
            cnf.append({"lo": "%s/%s" % (self.lo_cnf, i), "re": "%s/%s/bin" % (i, g_pkg_mcproxy), "file": "mcproxy.ini"})

        return cnf

    def config(self, inst_name):
        cnf = "mcproxy.ini"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "sed"
        for i in range(len(g_port0_mcproxy)):
            cmd = cmd + " -e 's/${port_mcproxy%d}/%s/g'" % (i, g_port0_mcproxy[i])

        system("%s %s >%s/%s/%s" % (cmd, cnf_template, g_lo_cnf, inst_name, cnf))
        
        cnf = "app_conf.lua"
        cnf_template = "%s/%s/T_%s" % (g_lo_cnf, inst_name, cnf)
        cmd = "sed"
        for i in range(len(g_ssh_list)):
            cmd = cmd + " -e 's/${server%d}/%s/g'" % (i, (g_ssh_list[0])["host"])

        for i in range(len(g_port1_proxy)):
            cmd = cmd + " -e 's/${port_proxy%d}/%s/g'" % (i, g_port1_proxy[i])

        system("%s %s >%s/%s/%s" % (cmd, cnf_template, g_lo_cnf, inst_name, cnf))
 
    def status_cmd(self):
        return "ps x|grep uchas|grep mcproxy|grep -v 'grep'"

    def start_cmd(self):
        return "cd %s/%s/bin && ./uchas -f %s/%s/bin/mcproxy.ini -d" \
                  % (self.bin_dir, g_pkg_mcproxy, self.bin_dir, g_pkg_mcproxy)

    def stop_cmd(self):
        return "ps -ef |fgrep '%s/%s/bin/mcproxy.ini' |grep -v 'fgrep' |awk '{print $2}' |xargs kill -9" \
                  % (self.bin_dir, self.pkg_mgr)


