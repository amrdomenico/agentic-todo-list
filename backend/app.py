from flask import Flask, request, jsonify

import database

app = Flask(__name__)


@app.route("/api/todos", methods=["GET"])
def api_list_todos():
    return jsonify(database.list_todos())


@app.route("/api/todos/<int:todo_id>", methods=["GET"])
def api_get_todo(todo_id):
    todo = database.get_todo(todo_id)
    if todo is None:
        return jsonify({"error": "Todo não encontrado"}), 404
    return jsonify(todo)


@app.route("/api/todos", methods=["POST"])
def api_create_todo():
    data = request.get_json(silent=True) or {}
    description = (data.get("description") or "").strip()
    if not description:
        return jsonify({"error": "description é obrigatório"}), 400
    new_id = database.create_todo(description)
    return jsonify(database.get_todo(new_id)), 201


@app.route("/api/todos/<int:todo_id>", methods=["PATCH"])
def api_update_todo(todo_id):
    if database.get_todo(todo_id) is None:
        return jsonify({"error": "Todo não encontrado"}), 404

    data = request.get_json(silent=True) or {}
    description = data.get("description")
    done = data.get("done")

    if description is not None:
        description = description.strip()
        if not description:
            return jsonify({"error": "description não pode ser vazio"}), 400

    if description is None and done is None:
        return jsonify({"error": "Envie description e/ou done"}), 400

    database.update_todo(todo_id, description=description, done=done)
    return jsonify(database.get_todo(todo_id))


@app.route("/api/todos/<int:todo_id>", methods=["DELETE"])
def api_delete_todo(todo_id):
    if not database.delete_todo(todo_id):
        return jsonify({"error": "Todo não encontrado"}), 404
    return "", 204


if __name__ == "__main__":
    database.init_db()
    app.run(debug=True)
