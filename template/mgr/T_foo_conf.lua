foo_pool =
{
    mysqlpool =
    {
        name = "foo_sql",
        type = "mysql",
        --selection = "master_slave",
        selection = "round_robin",
        nmin = 3,
        nmax = 20,
        timeout = 5,
        comm_timeout = 10,
        check_interval = 1,
        max_idle_time = 36,

        read_timeout = 5,
        write_timeout = 5,
        conn_timeout = 5,
        reconnect = 1,
        force_use = 1,

        server_list =
        {
            --{host = "10.1.88.136", port = 3306, user = "fooyun", passwd = "fooyun", db = "fooyun", charset = "utf8", role = "master"},
            {host = "10.1.74.52", port = 33333, user = "mha", passwd = "mha", db = "fooyun_zzn${i}", charset = "utf8", role = "master"},
        },
    },
}
