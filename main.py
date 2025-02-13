from flask import Flask, request, jsonify
import inspect

app = Flask(__name__)

@app.route('/getupvalues', methods=['POST'])
def get_upvalues():
    data = request.json
    func_name = data.get("func_name")

    if func_name not in globals():
        return jsonify({"error": "Function not found"}), 400

    func = globals()[func_name]
    upvalues = {k: v for k, v in inspect.getclosurevars(func).nonlocals.items()}

    return jsonify(upvalues)

@app.route('/setupvalue', methods=['POST'])
def set_upvalue():
    data = request.json
    func_name = data.get("func_name")
    var_name = data.get("var_name")
    new_value = data.get("new_value")

    if func_name not in globals():
        return jsonify({"error": "Function not found"}), 400

    func = globals()[func_name]
    closure = inspect.getclosurevars(func)

    if var_name not in closure.nonlocals:
        return jsonify({"error": "Upvalue not found"}), 400

    closure.nonlocals[var_name] = new_value

    return jsonify({"success": True})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
