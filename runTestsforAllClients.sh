sh runTestClients.sh compression hexo-server 2>>Data/test_compression_hexo-server_func_error.log >> Data/test_compression_hexo-server_func.log
sh runTestClients.sh compression koop-core 2>>Data/test_compression_koop-core_func_error.log >> Data/test_compression_koop-core_func.log
sh runTestClients.sh compression kraken-js 2>>Data/test_compression_kraken-js_func_error.log >> Data/test_compression_kraken-js_func.log
sh runTestClients.sh compression molstar 2>>Data/test_compression_molstar_func_error.log >> Data/test_compression_molstar_func.log
sh runTestClients.sh compression router 2>>Data/test_compression_router_func_error.log >> Data/test_compression_router_func.log

# sh runTestClients.sh compression hexo-server 2>>Data/test_compression_hexo-server_file_error.log >> Data/test_compression_hexo-server_file.log
# sh runTestClients.sh compression koop-core 2>>Data/test_compression_koop-core_file_error.log >> Data/test_compression_koop-core_file.log
# sh runTestClients.sh compression kraken-js 2>>Data/test_compression_kraken-js_file_error.log >> Data/test_compression_kraken-js_file.log
# sh runTestClients.sh compression molstar 2>>Data/test_compression_molstar_file_error.log >> Data/test_compression_molstar_file.log
# sh runTestClients.sh compression router 2>>Data/test_compression_router_file_error.log >> Data/test_compression_router_file.log