import yaml
from app import app


def generate_openapi_yaml():
    with app.test_client() as client:
        response = client.get("/apispec_1.json")

        if response.status_code == 200 and response.is_json:
            openapi_spec = response.get_json()

            with open("docs/openapi.yaml", "w", encoding="utf-8") as file:
                yaml.dump(openapi_spec, file, allow_unicode=True)

            print("Спецификация OpenAPI сохранена в docs/openapi.yaml")
        else:
            print("Ошибка: не удалось получить спецификацию OpenAPI.")


if __name__ == "__main__":
    generate_openapi_yaml()
