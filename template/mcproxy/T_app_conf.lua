
pool_example = 
{
    pool0 =
    {
        name = "mc_proxy0",
        type = "memcached",
        selection = "ketama",
        nmin = 1,
        nmax = 10,
        timeout = 50,
        comm_timeout = 50,
        check_interval = 0,
        max_idle_time = 20,

        force_use = 1,
        server_list =
        {
            --{host = "10.1.74.51", port = 9880, weight = 100},
            {host = "${server1}", port = ${port_proxy0}, weight = 100},
            --{host = "127.0.0.1", port = 10090, weight = 101},
            --{host = "127.0.0.1", port = 10030, weight = 102},
        },
    }, 

    pool1 =
    {
        name = "mc_proxy1",
        type = "memcached",
        selection = "ketama",
        nmin = 1,
        nmax = 10,
        timeout = 50,
        comm_timeout = 50,
        check_interval = 0,
        max_idle_time = 20,

        force_use = 1,
        server_list =
        {
            --{host = "10.1.74.51", port = 9880, weight = 100},
            {host = "${server1}", port = ${port_proxy1}, weight = 100},
            --{host = "127.0.0.1", port = 10090, weight = 101},
            --{host = "127.0.0.1", port = 10030, weight = 102},
        },
    }, 

    pool2 =
    {
        name = "mc_proxy2",
        type = "memcached",
        selection = "ketama",
        nmin = 1,
        nmax = 10,
        timeout = 50,
        comm_timeout = 50,
        check_interval = 0,
        max_idle_time = 20,

        force_use = 1,
        server_list =
        {
            --{host = "10.1.74.51", port = 9880, weight = 100},
            {host = "${server1}", port = ${port_proxy2}, weight = 100},
            --{host = "127.0.0.1", port = 10090, weight = 101},
            --{host = "127.0.0.1", port = 10030, weight = 102},
        },
    }, 

    pool3 =
    {
        name = "mc_proxy3",
        type = "memcached",
        selection = "ketama",
        nmin = 1,
        nmax = 10,
        timeout = 50,
        comm_timeout = 50,
        check_interval = 0,
        max_idle_time = 20,

        force_use = 1,
        server_list =
        {
            --{host = "10.1.74.51", port = 9880, weight = 100},
            {host = "${server1}", port = ${port_proxy3}, weight = 100},
            --{host = "127.0.0.1", port = 10090, weight = 101},
            --{host = "127.0.0.1", port = 10030, weight = 102},
        },
    }, 


}
