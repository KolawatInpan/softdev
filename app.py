from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/')
def index():
    return "Index!"


@app.route('/getcode', methods=['GET'])
def get_code():
    return jsonify({'hello': 'world'})


@app.route('/plus/<num1>/<num2>', methods=['GET'])
def plus(num1, num2):
    try:
        num1 = float(num1)
        num2 = float(num2)
        return jsonify({'result': num1 + num2})
    except ValueError:
        return jsonify({'error_msg': 'inputs must be numbers'})

<<<<<<< HEAD
# testtestasdasddsadasd
=======
# testtestasdasd
>>>>>>> 27b8ec59bb2ce32aa82462e666d2829c0eb4f9bb


if __name__ == "__main__":
    app.run()
