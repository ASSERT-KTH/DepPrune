# sh runTestClients.sh session routing-controllers 2>>Data/test_session_routing-controllers_func_error.log >> Data/test_session_routing-controllers_func.log
# sh runTestClients.sh session server 2>>Data/test_session_server_func_error.log >> Data/test_session_server_func.log
# sh runTestClients.sh session Lien 2>>Data/test_session_Lien_func_error.log >> Data/test_session_Lien_func.log
# sh runTestClients.sh session kraken-js 2>>Data/test_session_kraken-js_func_error.log >> Data/test_session_kraken-js_func.log
# sh runTestClients.sh session kettle 2>>Data/test_session_kettle_func_error.log >> Data/test_session_kettle_func.log

sh runTestClients.sh session routing-controllers 2>>Data/test_session_routing-controllers_file_error.log >> Data/test_session_routing-controllers_file.log
sh runTestClients.sh session server 2>>Data/test_session_server_file_error.log >> Data/test_session_server_file.log
sh runTestClients.sh session Lien 2>>Data/test_session_Lien_file_error.log >> Data/test_session_Lien_file.log
sh runTestClients.sh session kraken-js 2>>Data/test_session_kraken-js_file_error.log >> Data/test_session_kraken-js_file.log
sh runTestClients.sh session kettle 2>>Data/test_session_kettle_file_error.log >> Data/test_session_kettle_file.log
