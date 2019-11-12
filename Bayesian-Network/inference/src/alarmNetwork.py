import random

class AlarmNetwork:
    """Structure of Alarm Bayesian Network."""

    def __init__(self):
        """Initialize structure and the CPT of the network"""
        self.parents = dict()
        self.parents["A"] = ["B", "E"]
        self.parents["J"] = ["A"]
        self.parents["M"] = ["A"]
        self.parents["B"] = []
        self.parents["E"] = []
        self.table = dict()
        self.table["B"] = 0.001
        self.table["E"] = 0.002
        cptA = dict()  # P(A/B,E)
        cptA[(0, 0)] = 0.001
        cptA[(0, 1)] = 0.29
        cptA[(1, 0)] = 0.94
        cptA[(1, 1)] = 0.95
        self.table["A"] = cptA
        cptJ = dict()  # P(J/A)
        cptJ[0] = 0.05
        cptJ[1] = 0.90
        cptM = dict()  # P(M/A)
        cptM[0] = 0.01
        cptM[1] = 0.70
        self.table["J"] = cptJ
        self.table["M"] = cptM

    def parent(self, var_):
        """Get parent nodes."""
        return self.parents[var_]

    def nodes(self):
        """Return topological list of all the nodes in the bays net."""
        return  ["B", "E", "A", "J", "M"]


    def probOf(self, post, prior):
        """Return the conditional probability of post given prior.

        returns P(post=value|prior). Assumes prior contains the truth values of parents
        in correct order.

        Attributes:
        post    (node, truthvalue), Tuple with the posterior variable and
                the truth value. The posterior variable for which the
                probability is to be returned.
        prior   list of truth values of the parents.

        """
        if len(prior) < 1:
            # marginal prob
            prob = self.table[post[0]]
            if post[1] == 0:
                return (1. - prob)
            else:
                return prob
        else:
            # condn prob (post | prior)
            var_ = post[0]
            prob = 0.0
            if(len(prior)) > 1:
                prob = self.table[var_][(prior[0], prior[1])]
            else:
                prob = self.table[var_][prior[0]]
            if post[1] == 0:
                return (1. - prob)
            else:
                return prob


class psuedorandom:
    """Use this random function for sampling"""

    def __init__(self,seed=100):
        random.seed(seed)

    def uniform(self):
        """refer documentation of random"""
        return random.uniform(0.0, 1.0)
