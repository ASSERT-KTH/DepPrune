# sh runTestClients.sh memdown pouchdb 2>>Data/test_memdown_pouchdb_func_error.log >> Data/test_memdown_pouchdb_func.log
# sh runTestClients.sh memdown mem 2>>Data/test_memdown_mem_func_error.log >> Data/test_memdown_mem_func.log
# sh runTestClients.sh memdown dynalite 2>>Data/test_memdown_dynalite_func_error.log >> Data/test_memdown_dynalite_func.log
# sh runTestClients.sh memdown level-test 2>>Data/test_memdown_level-test_func_error.log >> Data/test_memdown_level-test_func.log
# sh runTestClients.sh memdown pico-framework 2>>Data/test_memdown_pico-framework_func_error.log >> Data/test_memdown_pico-framework_func.log

sh runTestClients.sh memdown pouchdb 2>>Data/test_memdown_pouchdb_file_error.log >> Data/test_memdown_pouchdb_file.log
sh runTestClients.sh memdown mem 2>>Data/test_memdown_mem_file_error.log >> Data/test_memdown_mem_file.log
sh runTestClients.sh memdown dynalite 2>>Data/test_memdown_dynalite_file_error.log >> Data/test_memdown_dynalite_file.log
sh runTestClients.sh memdown level-test 2>>Data/test_memdown_level-test_file_error.log >> Data/test_memdown_level-test_file.log
sh runTestClients.sh memdown pico-framework 2>>Data/test_memdown_pico-framework_file_error.log >> Data/test_memdown_pico-framework_file.log
