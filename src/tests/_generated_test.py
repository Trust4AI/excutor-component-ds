# import allure
# import pytest
# import json
#
#
# def load_test_cases(filename):
#     with open(filename, 'r') as file:
#         return json.load(file)
#
#
# def custom_test(expected_result):
#     assert expected_result.strip().lower().replace('"', '') == "pass"
#
#
# test_cases = load_test_cases("results/2024-05-07_01-44-12_gemma_2b_wh_question.json")
#
#
# @pytest.mark.parametrize("test_case", test_cases)
# def test_dynamic(test_case):
#     allure.dynamic.suite(test_case["description"])
#     allure.dynamic.sub_suite("wh_question")
#     allure.dynamic.title(test_case["query"])
#     allure.dynamic.description('Type: ' + test_case["description"] + '\nExpected result: ' + test_case["result"] + '\nResponse: ' + test_case["response"])
#
#     for value in test_case["values"]:
#         allure.dynamic.feature(value)
#     allure.dynamic.label("query", test_case["query"])
#     allure.dynamic.label("response", test_case["response"])
#     allure.dynamic.label("expected_result", test_case["result"])
#
#     custom_test(test_case["result"])
