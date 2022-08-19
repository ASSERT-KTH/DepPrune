# sh runTestClients.sh fastify fastify-micro 2>>Data/test_fastify_fastify-micro_func_error.log >> Data/test_fastify_fastify-micro_func.log
# sh runTestClients.sh fastify fastify-helpers 2>>Data/test_fastify_fastify-helpers_func_error.log >> Data/test_fastify_fastify-helpers_func.log
# sh runTestClients.sh fastify tydb 2>>Data/test_fastify_tydb_func_error.log >> Data/test_fastify_tydb_func.log
# sh runTestClients.sh fastify fastify-vhost 2>>Data/test_fastify_fastify-vhost_func_error.log >> Data/test_fastify_fastify-vhost_func.log
# sh runTestClients.sh fastify pubsub-http-handler 2>>Data/test_fastify_pubsub-http-handler_func_error.log >> Data/test_fastify_pubsub-http-handler_func.log

# sh runTestClients.sh fastify fastify-micro 2>>Data/test_fastify_fastify-micro_file_error.log >> Data/test_fastify_fastify-micro_file.log
# sh runTestClients.sh fastify fastify-helpers 2>>Data/test_fastify_fastify-helpers_file_error.log >> Data/test_fastify_fastify-helpers_file.log
# sh runTestClients.sh fastify tydb 2>>Data/test_fastify_tydb_file_error.log >> Data/test_fastify_tydb_file.log
# sh runTestClients.sh fastify fastify-vhost 2>>Data/test_fastify_fastify-vhost_file_error.log >> Data/test_fastify_fastify-vhost_file.log
# sh runTestClients.sh fastify pubsub-http-handler 2>>Data/test_fastify_pubsub-http-handler_file_error.log >> Data/test_fastify_pubsub-http-handler_file.log

sh runTestClients.sh deep-equal react-mapbox-gl 2>>Data/test_error.log >> Data/test_file.log
# sh runTestClients.sh deep-equal react-mapbox-gl >> Data/test_fastify_react-mapbox-gl_file.log 2>&1 
# sh runTestClients.sh deep-equal kbpgp 2>>Data/test_fastify_kbpgp_file_error.log >> Data/test_fastify_kbpgp_file.log