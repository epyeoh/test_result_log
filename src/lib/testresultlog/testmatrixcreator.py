import os
import sys
import unittest

scripts_path = os.path.dirname(os.path.realpath(__file__))
lib_path = scripts_path + '/lib'
sys.path = sys.path + [lib_path]
import scriptpath
scriptpath.add_oe_lib_path()
scriptpath.add_bitbake_lib_path()
from testresultlog.testmatrixjsonencoder import TestEnvMatrixJsonEncoder
import subprocess

class TestEnvMatrixCreator(object):

    def _generate_flat_list_of_test_module_function(self, test_suite):
        for test in test_suite:
            if unittest.suite._isnotsuite(test):
                yield test
            else:
                for subtest in self._generate_flat_list_of_test_module_function(test):
                    yield subtest

    def _get_test_module_name(self, test):
        test_module_name = test[test.find("(")+1:test.find(")")]
        print('DEBUG: %s : module : %s' % (test, test_module_name))
        return test_module_name

    def _get_test_function_name(self, test):
        test_function_name = test[0:test.find("(")-1]
        print('DEBUG: %s : function : %s' % (test, test_function_name))
        return test_function_name

    def _get_test_module_name_from_key(self, key):
        test_module_name = key[0:key.find(".")]
        return test_module_name

    def _get_test_class_name_from_key(self, key):
        test_class_name = key[key.find(".")+1:]
        return test_class_name

    def _create_testsuite_testcase_list(self, testsuite_list, test_module_func_dict):
        #print('DEBUG: creating testsuite testcase for testsuite list: %s' % testsuite_list)
        json_object = {'testsuite':[]}
        for testsuite in testsuite_list:
            #print('DEBUG: creating testsuite: %s' % testsuite)
            testsuite_dict = {}
            testsuite_dict['testsuitename'] = testsuite
            testcase_list = test_module_func_dict[testsuite]
            #print('DEBUG: creating testcase list: %s' % testcase_list)
            testsuite_dict['testcase']=self._create_testcase_list(testcase_list, testsuite)
            json_object['testsuite'].append(testsuite_dict)
        return json_object

    def _create_testcase_list(self, testcase_list, testsuite_name):
        testcaselist = []
        for testcase in testcase_list:
            testcase_dict = {}
            testcase_dict['testcasename'] = '%s.%s' % (testsuite_name, testcase)
            testcase_dict['testresult'] = ""
            testcase_dict['testlog'] = ""
            #testcase_dict['testprocedures'] = ""
            testcaselist.append(testcase_dict)
        #print('DEBUG: testcase_list: %s' % testcaselist)
        return testcaselist

    def load_test_module_and_test_function(self, test_dir):
        loader = unittest.TestLoader()
        test_suite = loader.discover(start_dir=test_dir, pattern='*.py')
        return self._generate_flat_list_of_test_module_function(test_suite)

    def generate_test_moduleclass_key_test_function_value_dictionary(self, test_module_function_list):
        test_module_func_dict = {}
        print('DEBUG: start generate matrix')
        for test in test_module_function_list:
            key = self._get_test_module_name(str(test))
            value = self._get_test_function_name(str(test))
            if key in test_module_func_dict:
                test_module_func_dict[key].append(value)
            else:
                test_module_func_dict[key] = [value]
        return test_module_func_dict

    def generate_test_module_key_test_moduleclass_value_dictionary(self, module_class_list):
        test_module_class_dict = {}
        for module_class in module_class_list:
            module_name = self._get_test_module_name_from_key(module_class)
            class_name = '%s.%s' % (module_name, self._get_test_class_name_from_key(module_class))
            if module_name in test_module_class_dict:
                test_module_class_dict[module_name].append(class_name)
            else:
                test_module_class_dict[module_name] = [class_name]
        return test_module_class_dict

    def generate_testsuite_testcase_json_data_structure(self, testsuites_list, test_module_func_dict):
        testsuite_testcase_list = self._create_testsuite_testcase_list(testsuites_list, test_module_func_dict)
        encoder = TestEnvMatrixJsonEncoder()
        return encoder.start_encode(testsuite_testcase_list)

    def write_testsuite_testcase_json_data_structure_to_file(self, file_path, file_content):
        with open(file_path, 'a') as the_file:
            the_file.write(file_content)

    def push_testsuite_testcase_json_file_to_git_repo(self, file_dir, git_repo):
        return subprocess.run(["oe-git-archive", file_dir, "-g", git_repo])




