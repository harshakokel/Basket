from copy import copy, deepcopy
import math
import random
import numpy as np
import logging as log
import json
import argparse

class GibbsSampling:

    def __init__(self, adj_matrix, domain_size, psi, phi):
        self.adj_matrix = adj_matrix
        self.domain_size = domain_size
        self.N = len(adj_matrix)
        self.psi_function = psi
        self.phi_function = phi
        self.sum = sum
        self.unnormalized_prob={}
        self.initial_sample = np.random.choice(self.domain_size, self.N)
        # self.initial_sample = np.array([1,2,2,3])
        log.info("Initial sample "+str(self.initial_sample))

    def generate_next_sample(self, current_sample=None):
        if current_sample is None:
            current_sample = self.initial_sample
        next_sample = copy(current_sample)
        for i in range(self.N):
            next_sample[i] = self.sample_variable(i,next_sample)
        self.initial_sample = next_sample
        return next_sample

    def sample_variable(self, i, sample):
        p_i = self.get_unnormalized_prob(i, sample)
        assert (np.sum(p_i) > 0), "Irreducible Graph"
        return random.choices(list(range(self.domain_size)), p_i)[0]

    def get_unnormalized_prob(self, i, sample ):
        adjacent_vertices = np.nonzero(self.adj_matrix[i])[0]
        key = (i, tuple(sample[adjacent_vertices].tolist()))
        if key not in self.unnormalized_prob:
            p_i = np.ones(self.domain_size)
            for x_i in range(self.domain_size):
                p_i[x_i] = p_i[x_i]*self.phi_function(i,x_i)
                for j in adjacent_vertices:
                    p_i[x_i] = p_i[x_i]*self.psi_function(i,j,x_i,sample[j])
            self.unnormalized_prob[key] = p_i
        return self.unnormalized_prob[key]

    def generate_samples(self, its, current_sample=None):
        if current_sample is None:
            current_sample = self.initial_sample
        samples = np.array([current_sample])
        for n in range(its):
            current_sample = self.generate_next_sample(current_sample)
            samples = np.append(samples, [current_sample], axis=0)
            # log.info("sample generated: "+ str(n))
        return samples

    def compute_marginals(self, samples):
        marginal_matrix = np.zeros((self.N, self.domain_size))
        sample_size = len(samples)
        for i in range(self.N):
            for x_i in range(self.domain_size):
                marginal_matrix[i,x_i] = np.sum(samples[:,i]==x_i)/sample_size
        return marginal_matrix

def gibbs_samples(A, w, burnin, its):
    __w = deepcopy(w)

    def psi_function(i, j, x_i, x_j):
        return int(x_i != x_j)

    def phi_function(i, x_i):
        return math.exp(__w[x_i])

    sampler = GibbsSampling(A, len(w), psi=psi_function, phi=phi_function)
    samples = sampler.generate_samples(its+burnin)
    return np.delete(samples, list(range(burnin)),axis=0)


def gibbs(A, w, burnin, its):
    __w = deepcopy(w)

    def psi_function(i, j, x_i, x_j):
        return int(x_i != x_j)

    def phi_function(i, x_i):
        return math.exp(__w[x_i])

    sampler = GibbsSampling(A, len(w), psi=psi_function, phi=phi_function)
    samples = sampler.generate_samples(its+burnin)
    marg_matrix = sampler.compute_marginals(np.delete(samples, list(range(burnin)), axis=0))
    # log.info("MARGINAL MATRIX \n"+ str(marg_matrix))
    return marg_matrix


def construct_table(A,w,vertex = 0,color = 3):
    its_set = [2**6, 2**10, 2**14, 2**18]
    burnin_set = [2**6, 2**10, 2**14, 2**18]
    print(["burnin","its","marginal"])

    for its in its_set:
        for burnin in burnin_set:
            marg_matrix = gibbs(A,w,burnin,its)
            print([burnin, its, marg_matrix[vertex,color]])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="count",
                        help="increase output verbosity (e.g., -vv is more than -v)")
    parser.add_argument('-A', '--adjacency_matrix',  help='<Required> Adjacency Matrix', required=True)
    parser.add_argument('-w', '--weights', help='<Required> weights',  required=True)
    parser.add_argument('-b', '--burnin', help='<Required> number of burn-in samples', required=False)
    parser.add_argument('-its', '--iteration', help='<Required> number of samples after burn-in', type= int, required=False)
    parser.add_argument('--table', dest='sampling', action='store_const',
                        const=construct_table, default=gibbs,
                        help='Construct Table for vertex a & color 4 (default: marginal matrix using gibbs sampling)')

    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")
    if args.sampling == construct_table:
        args.sampling(np.array(json.loads(args.adjacency_matrix)), np.array(json.loads(args.weights)))
    else:
        v = args.sampling(np.array(json.loads(args.adjacency_matrix)), np.array(json.loads(args.weights)), int(args.burnin), int(args.iteration))
        print(v)
