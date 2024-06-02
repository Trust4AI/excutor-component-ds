import allure
import pytest
import json
import os
from pathlib import Path

current_directory = Path(os.path.dirname(__file__))
parent_directory = os.path.dirname(current_directory)
results_directory = Path(os.path.join(parent_directory, 'results'))
allure_report_directory = Path(os.path.join(results_directory, 'allure-report'))


def load_test_cases(filename):
    with open(filename, 'r') as file:
        return json.load(file)


def custom_test(expected_result):
    assert expected_result.strip().lower().replace('"', '') == "pass"


json_files = list(results_directory.glob("*.json"))

# Preparar los datos de las pruebas recogiendo todos los casos de cada archivo
test_cases = []
for file in json_files:
    cases = load_test_cases(str(file))
    test_cases.extend([(str(file), case) for case in cases])


# Parametrizar las pruebas con Pytest
@pytest.mark.parametrize("filename, test_case", test_cases)
def test_dynamic(filename, test_case):
    # Descripción completa del caso de prueba
    description = (
        f"Query: {test_case['query']}\n"
        f"Model: {test_case['model']}\n"
        f"Description: {test_case['description']}\n"
        f"Response: {test_case['response']}"
    )

    with allure.step("Setup and Load Test Case"):
        # Definir las etiquetas dinámicas de Allure para categorizar y describir mejor el caso de prueba
        allure.dynamic.suite(test_case["description"])
        allure.dynamic.sub_suite("Detailed Analysis")
        allure.dynamic.feature(test_case["values"][0])
        allure.dynamic.story(f"Handling {test_case['values'][0]}")
        allure.dynamic.title(test_case["query"])
        allure.dynamic.description(description)

    with allure.step("Verify Test Case"):
        # Verificar los resultados del caso de prueba utilizando una función personalizada
        expected_cleaned = test_case["result"].strip().lower().replace('"', '')
        actual_result = "pass"  # Deberías definir cómo obtienes este resultado real basado en tu contexto
        custom_test(expected_cleaned)


# Ejecutar Pytest y generar reportes de Allure
if __name__ == "__main__":
    pytest.main(['--alluredir', str(allure_report_directory)])
