from flask import Flask, request, jsonify
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

contacts = {}
current_id = 1


@app.route("/contacts", methods=["POST"])
@swag_from({
    "tags": ["Contacts"],
    "summary": "Создание нового контакта",
    "description": "Создает контакт с именем и телефоном",
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "properties": {
                    "name": {"type": "string"},
                    "phone": {"type": "string"}
                },
                "required": ["name", "phone"]
            }
        }
    ],
    "responses": {
        201: {
            "description": "Контакт создан"
        }
    }
})
def create_contact():
    global current_id
    data = request.get_json()

    contact = {
        "id": current_id,
        "name": data["name"],
        "phone": data["phone"]
    }

    contacts[current_id] = contact
    current_id += 1

    return jsonify(contact), 201


@app.route("/contacts/<int:contact_id>", methods=["GET"])
@swag_from({
    "tags": ["Contacts"],
    "summary": "Получение контакта",
    "description": "Возвращает контакт по ID",
    "parameters": [
        {
            "name": "contact_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Контакт найден"},
        404: {"description": "Контакт не найден"}
    }
})
def get_contact(contact_id):
    contact = contacts.get(contact_id)

    if not contact:
        return jsonify({"error": "Contact not found"}), 404

    return jsonify(contact)


@app.route("/contacts/<int:contact_id>", methods=["DELETE"])
@swag_from({
    "tags": ["Contacts"],
    "summary": "Удаление контакта",
    "description": "Удаляет контакт по ID",
    "parameters": [
        {
            "name": "contact_id",
            "in": "path",
            "type": "integer",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Контакт удалён"},
        404: {"description": "Контакт не найден"}
    }
})
def delete_contact(contact_id):
    if contact_id not in contacts:
        return jsonify({"error": "Contact not found"}), 404

    deleted = contacts.pop(contact_id)
    return jsonify(deleted)



if __name__ == "__main__":
    app.run(debug=True)
