import hashlib
import json
import random
from time import time

from collections import OrderedDict
from math import exp


# https://stackoverflow.com/questions/19472530/representing-graphs-data-structure-in-python
# https://www.python-course.eu/graphs_python.php
# https://github.com/davebshow/structures

# TODO: Visualizing the graph: probably best as tree structure
# TODO: Solving the chain problem with several full nodes
# TODO: User registration
class DAG(object):
    """ Graph data structure, undirected by default. """

    def __init__(self):
        self.graph = OrderedDict()
        self.graph[0] = {'edges': [], 'transaction': 'genesis', 'proof': 100}
        self.genesis_amount = 100

    def genesis(self, init_distribution):
        for i in range(1, init_distribution + 1):
            self.graph[i] = {'edges': [0, 0],
                             'transaction': {
                                 "sender": 'genesis',
                                 "receiver": 'initial_TX ' + str(i),
                                 "amount": self.genesis_amount / init_distribution
                             },
                             'proof': self.proof_of_work(self.graph[0], self.graph[0])
                             }

    def new_transaction(self, content):
        """ Adds node(transaction) to graph """

        index = max(self.graph.keys()) + 1
        # edges = self.tip_selection(list(self.graph.keys()))

        edge1 = self.MCMC()
        edge2 = self.MCMC()
        edges = [edge1, edge2]

        for e in edges:
            tips = self.graph[e]['edges']
            new_edge = []
            checking = e
            while not (self.valid_proof(self.graph[tips[0]]['proof'], self.graph[tips[1]]['proof'],
                                        self.graph[checking]['proof']) and
                       self.check_balance()):
                # print(str(self.valid_proof(self.graph[tips[0]]['proof'], self.graph[tips[1]]['proof'], self.graph[checking]['proof'])) + " " +
                # str(self.check_balance(checking)))
                print(checking)
                print(self.get_balance())
                del self.graph[checking]  # Delete from graph <-- radical maybe not necessary step
                new_edge = self.MCMC()
                checking = new_edge
                tips = self.graph[new_edge]['edges']
            if edges.count(edges[0]) == len(edges) and new_edge:  # if list elements are the same
                edges = [new_edge, new_edge]
                break
            elif new_edge:
                edges[edges.index(e)] = new_edge

        data = {'edges': edges,
                'timestamp': time(),
                'transaction': content,
                'proof': self.proof_of_work(self.graph[edges[0]], self.graph[edges[1]]),
                'previous_hash_1': self.hash(self.graph[edges[0]]),
                # TODO: Eigentlich unnötig die previous hashs. Raus?
                'previous_hash_2': self.hash(self.graph[edges[1]])
                }
        self.graph[index] = data

    def get_tips(self):
        """ List all tips with no vertex pointing to them """
        keys = self.graph.keys()
        values = [v['edges'] for v in self.graph.values()]
        vertex = []
        for v in values:
            vertex.extend(v)
        tips = []
        for k in keys:
            if k not in vertex:
                tips.append(k)
        return tips

    def cum_weight(self):
        """
        1. Select vertex
        2. Give vertex weight = vertex
        3. Look at edges in vertex: give edges weight = node.weight
        """
        tips = self.get_tips()
        cw_list = {}
        for node in self.graph.keys():
            fill = {}
            fill['weight'] = set()
            fill['cd_edges'] = set()  # counter-directed
            fill['edges'] = set(self.graph.get(node)['edges'])  # Kann ich auch rausnehmn und 3 Zeilen später einfügen
            cw_list[node] = fill
        for tip in tips:
            edges = cw_list[tip]['edges']
            cw_list[tip]['weight'].update([tip])
            if edges:
                for e in edges:
                    cw_list[e]['weight'] |= cw_list[tip]['weight']  # |= union of two sets
                    cw_list[e]['cd_edges'].update([tip])
                tips.extend(
                    edges)  # important so that also indirect connections are in weight (not just iteration through nodes)
        return cw_list

    def tip_selection(self, tip_list):
        """ Select randomly two tips """
        # https://iota.stackexchange.com/questions/1329/what-is-the-actual-iota-algorithm-for-tip-selection
        selection = [random.choice(tip_list)]
        if len(tip_list) >= 2:
            tip_list.remove(selection[0])
            selection.append(random.choice(tip_list))  # Assumption always two tips available
        return selection

    def MCMC(self):
        alpha = 0.5
        weights = self.cum_weight()
        start = [0]  # this is genesis
        for vertex in start:
            edges = weights[vertex]['cd_edges']  # TODO: Warum so komliziert mit den cd_edges wenn ich mir einfach die keys geben könnte vom ganzen Graphen?
            if edges:
                Hx = len(weights[vertex]['weight'])
                sum_Hz = 0
                for e in edges:
                    sum_Hz += exp(-alpha * (Hx - len(weights[e]['weight'])))
                prob = [exp(-alpha * (Hx - len(weights[e]['weight']))) / sum_Hz for e in edges]
                next_vertex = random.choices(list(edges), prob)
                start.extend(next_vertex)
            else:
                final_tip = vertex
        return final_tip

    def extract_balance(self, tip):
        current_transaction = self.graph[tip]['transaction']
        sender = current_transaction['sender']
        receiver = current_transaction['receiver']
        amount = current_transaction['amount']
        return [sender, receiver, amount]

    # def get_balance(self, tip):  # maybe change to get balance
    #     balance = {'genesis': [self.genesis_amount]}
    #     tip = {tip}
    #     iterator = list(tip)
    #     for t in iterator:
    #         if t != 0:
    #             sender, receiver, amount = self.extract_balance(t)
    #             balance[sender] = balance.get(sender, []) + [-amount]
    #             balance[receiver] = balance.get(receiver, []) + [amount]
    #             tip.update(self.graph[t]['edges'])
    #             appender = list(tip - set(iterator))
    #             iterator.extend(appender)
    #     total = {key: sum(balance[key]) for key in balance}
    #     return total

    def get_balance(self):  # maybe change to get balance
        balance = {'genesis': [self.genesis_amount]}
        vertices = self.graph.keys()
        for vertex in vertices:
            if vertex != 0:
                sender, receiver, amount = self.extract_balance(vertex)
                balance[sender] = balance.get(sender, []) + [-amount]
                balance[receiver] = balance.get(receiver, []) + [amount]
        total = {key: sum(balance[key]) for key in balance}
        return total

    def check_balance(self):
        total = self.get_balance()
        sums = [total[key] for key in total]
        return all(s >= 0 for s in sums)


    @staticmethod
    def hash(vertex):
        """
        Creates a SHA-256 hash of a vertex which is converted as String

        :param vertex: <dict> vertex in graph
        """

        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        vertex_string = json.dumps(vertex, sort_keys=True).encode()
        return hashlib.sha256(vertex_string).hexdigest()

    def proof_of_work(self, edge_1, edge_2):
        """
        Simple Proof of Work Algorithm:
         - Find a number p' such that hash(pp') contains leading 4 zeroes
         - Where p is the previous proof, and p' is the new proof
         - Content of the block is converted to string (incl. the previous_hash)
           and proof variable is iterated until hash ends with '0000'

        :param last_block: <dict> last Block
        :return: <int>
        """

        edge_1_proof = edge_1['proof']
        edge_2_proof = edge_2['proof']

        proof = 0
        while self.valid_proof(edge_1_proof, edge_2_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(edge_1_proof, edge_2_proof, proof):
        """
        Validates the Proof: Does hash(last_proof, proof, last_hash) contain 4 leading zeroes?
        :param edge_1_proof: <int> Proof of the previous edge 1
        :param edge_2_proof: <int> Proof of the previous edge 2
        :param proof: <int> Current Proof
        :return: <bool> True if correct, False if not.
        """

        guess = f'{edge_1_proof}{edge_2_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def get_graph(self):
        return dict(self.graph)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.graph))

    def __repr__(self):
        return repr(dict(self.graph))
