# sh runTestClients.sh compression hexo-server 2>>Data/test_compression_hexo-server_func_error.log >> Data/test_compression_hexo-server_func.log
# sh runTestClients.sh compression koop-core 2>>Data/test_compression_koop-core_func_error.log >> Data/test_compression_koop-core_func.log
# sh runTestClients.sh compression kraken-js 2>>Data/test_compression_kraken-js_func_error.log >> Data/test_compression_kraken-js_func.log
# sh runTestClients.sh compression molstar 2>>Data/test_compression_molstar_func_error.log >> Data/test_compression_molstar_func.log
# sh runTestClients.sh compression router 2>>Data/test_compression_router_func_error.log >> Data/test_compression_router_func.log

# sh runTestClients.sh compression hexo-server 2>>Data/test_compression_hexo-server_file_error.log >> Data/test_compression_hexo-server_file.log
# sh runTestClients.sh compression koop-core 2>>Data/test_compression_koop-core_file_error.log >> Data/test_compression_koop-core_file.log
# sh runTestClients.sh compression kraken-js 2>>Data/test_compression_kraken-js_file_error.log >> Data/test_compression_kraken-js_file.log
# sh runTestClients.sh compression molstar 2>>Data/test_compression_molstar_file_error.log >> Data/test_compression_molstar_file.log
# sh runTestClients.sh compression router 2>>Data/test_compression_router_file_error.log >> Data/test_compression_router_file.log


sh runTestClients.sh fastify fastify-vhost 2>>Data/test_fastify_fastify-vhost_func_error.log >> Data/test_fastify_fastify-vhost_func.log
sh runTestClients.sh fastify pubsub-http-handler 2>>Data/test_fastify_pubsub-http-handler_func_error.log >> Data/test_fastify_pubsub-http-handler_func.log
sh runTestClients.sh yeoman-generator sfdx-plugin-generate 2>>Data/test_yeoman-generator_sfdx-plugin-generate_func_error.log >> Data/test_yeoman-generator_sfdx-plugin-generate_func.log