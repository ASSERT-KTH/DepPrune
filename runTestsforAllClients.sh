sh runTestClients.sh express firebase-functions 2>>Data/test_firebase-functions_express_func_error.log >> Data/test_firebase-functions_express_func.log
sh runTestClients.sh express hubot 2>>Data/test_hubot_express_func_error.log >> Data/test_hubot_express_func.log
sh runTestClients.sh express loopback 2>>Data/test_loopback_express_func_error.log >> Data/test_loopback_express_func.log
sh runTestClients.sh express probot 2>>Data/test_probot_express_func_error.log >> Data/test_probot_express_func.log
sh runTestClients.sh express routing-controllers 2>>Data/test_routing-controllers_express_func_error.log >> Data/test_routing-controllers_express_func.log