from simpleDAG_2 import DAG
from flask import Flask, jsonify, request


# Instantiate the Main Node
app = Flask(__name__)

# Generate a globally unique address for this node --> recipient address for transaction sender and receivers
# node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
dag = DAG()


@app.route('/genesis', methods=['POST'])
def genesis():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['initial_distribution']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    dag.genesis(values['initial_distribution'])

    response = {'message': f'Genesis transactions will be added to DAG'}
    return jsonify(response), 201


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'receiver', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    dag.new_transaction(values)

    response = {'message': f'Transaction will be added to DAG'}
    return jsonify(response), 201


@app.route('/my_balance', methods=['POST'])
def my_balance():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['user_id']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Get all balances
    all_balances = dag.get_balance()
    balance = all_balances[values['user_id']]

    response = {values['user_id']: balance}
    return jsonify(response), 201


@app.route('/all_balance', methods=['GET'])
def all_balance():
    return jsonify(dag.get_balance())


@app.route('/dag', methods=['GET'])
def full_dag():
    response = {
        'DAG': dict(dag.graph),
        'length': len(dag.graph),
    }
    return jsonify(response), 200


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('-p', '--port', default=5000, type=int, help='port to listen on')
    args = parser.parse_args()
    port = args.port

    app.run(host='0.0.0.0', port=port)
