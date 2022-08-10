# sh runTestClients.sh send serve-static 2>>Data/test_send_serve-static_func_error.log >> Data/test_send_serve-static_func.log
# sh runTestClients.sh send node-restify 2>>Data/test_send_node-restify_func_error.log >> Data/test_send_node-restify_func.log
# sh runTestClients.sh send gulp-connect 2>>Data/test_send_gulp-connect_func_error.log >> Data/test_send_gulp-connect_func.log
# sh runTestClients.sh send fastify-static 2>>Data/test_send_fastify-static_func_error.log >> Data/test_send_fastify-static_func.log
# sh runTestClients.sh send connect-gzip-static 2>>Data/test_send_connect-gzip-static_func_error.log >> Data/test_send_connect-gzip-static_func.log

sh runTestClients.sh send serve-static 2>>Data/test_send_serve-static_file_error.log >> Data/test_send_serve-static_file.log
sh runTestClients.sh send node-restify 2>>Data/test_send_node-restify_file_error.log >> Data/test_send_node-restify_file.log
sh runTestClients.sh send gulp-connect 2>>Data/test_send_gulp-connect_file_error.log >> Data/test_send_gulp-connect_file.log
sh runTestClients.sh send fastify-static 2>>Data/test_send_fastify-static_file_error.log >> Data/test_send_fastify-static_file.log
sh runTestClients.sh send connect-gzip-static 2>>Data/test_send_connect-gzip-static_file_error.log >> Data/test_send_connect-gzip-static_file.log