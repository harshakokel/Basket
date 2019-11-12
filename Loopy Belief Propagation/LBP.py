from copy import copy, deepcopy
import math
import numpy as np
import logging as log
import json
import argparse

class LBP:
    def __init__(self, adj_matrix, domain_size, psi, phi, sum):
        self.adj_matrix = adj_matrix
        self.domain_size = domain_size
        self.N = len(adj_matrix)
        self.psi_function = psi
        self.phi_function = phi
        self.sum = sum
        # self.partition_function = partition_function
        # initialize messages uniformly, message from vertex i to clique ij for variable assignment x_i is stored at [x_i][i,j]
        self.message_vertex_to_clique =  np.array([deepcopy(self.adj_matrix) for j in range(self.domain_size)])

        # initialize messages uniformly, message from clique ij to vertex i for variable assignment x_i is stored at [x_i][j,i]
        self.message_clique_to_vertex = np.array([deepcopy(self.adj_matrix) for j in range(self.domain_size)])

        log.info("Initialized: "+ ("sum product" if sum else "max product" ))


    def max_marginal_assignment(self,i):
        adjacent_vertices = np.nonzero(self.adj_matrix[i])[0]
        tmp = list()
        for x in range(self.domain_size):
            tmp.append(self.phi_function(i,x)*np.prod( self.message_clique_to_vertex[x,adjacent_vertices,i]))
        tmp = (tmp/np.sum(tmp))
        if len(tmp[tmp==np.max(tmp)])>1:
            log.warning(" more than one maximizing assignment for: "+str(i) )
            return 0
        return np.argmax(tmp)

    def marginal_node(self, i,x_i): #i = 1, x_i =0
        adjacent_vertices = np.nonzero(self.adj_matrix[i])[0]
        tmp = list()
        for x in range(self.domain_size):
            tmp.append(self.phi_function(i,x)*np.prod( self.message_clique_to_vertex[x,adjacent_vertices,i]))
        # print(tmp/np.sum(tmp))
        return (tmp/np.sum(tmp))[x_i]



    def marginal_edge(self, i,j, x_i,x_j):
        tmp = self.psi_function(i,j,x_i,x_j) * self.message_vertex_to_clique[x_i,i,j]* self.message_vertex_to_clique[x_j,j,i]
        if tmp == 0:
            return 0
        tmp_sum = 0
        for xi in range(self.domain_size):
            for xj in range(self.domain_size):
                tmp_sum = tmp_sum + self.psi_function(i,j,xi,xj)*self.message_vertex_to_clique[xi,i,j]* self.message_vertex_to_clique[xj,j,i]
        return tmp/tmp_sum

    def belief_propoagation(self, its):
        iteration = 0
        while(iteration<its):
            iteration = iteration + 1
            # log.info("Iteration:"+ str(iteration))
            old_mvc = deepcopy(self.message_vertex_to_clique)
            old_mcv = deepcopy(self.message_clique_to_vertex)
            tmp_mvc = np.zeros((self.domain_size,self.N,self.N))
            tmp_mcv = np.zeros((self.domain_size, self.N,self.N ))
            # Code to compute messages for each vertex
            for i in range(self.N):
                # print ("i", i)
                adjacent_vertices = np.nonzero(self.adj_matrix[i])[0]
                # for each adjacent vertex
                for j in adjacent_vertices:
                    # print ("j", j)
                    # for each assignment of i
                    for x_i in range(self.domain_size):
                        # print ("x_i", x_i)
                        # Update tmp_mvc
                        # neighbours of i not including j.
                        n_i = adjacent_vertices[adjacent_vertices!=j]
                        tmp_mvc[x_i,i,j] = self.phi_function(i,x_i)*np.prod(old_mcv[x_i,n_i,i])
                        # Update tmp_mcv
                        tmp_vector = list()
                        for x_j in range(self.domain_size):
                            # print ("x_j", x_j)
                            tmp_vector.append(self.psi_function(i,j,x_i,x_j) * old_mvc[x_j,j,i])
                        if(self.sum):
                            tmp_mcv[x_i, j, i] = np.sum(tmp_vector)
                        else:
                            tmp_mcv[x_i, j, i] = np.max(tmp_vector)
                    # Scaling
                    # if(np.gcd.reduce(tmp_mvc[:,i,j].astype(int))):
                    #     tmp_mvc[:,i,j] = tmp_mvc[:,i,j]/np.gcd.reduce(tmp_mvc[:,i,j].astype(int))
                    # if(np.gcd.reduce(tmp_mcv[:,j,i].astype(int))):
                    #     tmp_mcv[:,j,i] = tmp_mcv[:,j,i]/np.gcd.reduce(tmp_mcv[:,j,i].astype(int))
                    # Normalizing
                    if (np.sum(tmp_mvc[:, i, j])):
                        tmp_mvc[:, i, j] = tmp_mvc[:, i, j] / np.sum(tmp_mvc[:, i, j])
                    if (np.sum(tmp_mcv[:, j, i])):
                        tmp_mcv[:, j, i] = tmp_mcv[:, j, i] / np.sum(tmp_mcv[:, j, i])
            # print("clique to vertex")
            # print(tmp_mcv)
            # print("vertex to clique")
            # print(tmp_mvc)
            # Check Convergence
            if(np.array_equal(tmp_mvc, self.message_vertex_to_clique) and np.array_equal(tmp_mcv, self.message_clique_to_vertex)):
                log.info("Converged at iteration: "+ str(iteration))
                break
            self.message_vertex_to_clique = copy(tmp_mvc)
            self.message_clique_to_vertex = copy(tmp_mcv)
        log.info(self.message_vertex_to_clique)
        log.info(self.message_clique_to_vertex)

    def entropy(self):
        tmp_sum = 0
        for i in range(self.N):
            adjacent_vertices = np.nonzero(self.adj_matrix[i])[0]
            for x_i in range(self.domain_size):
                tau_i = self.marginal_node(i, x_i)
                if tau_i:
                    tmp_sum = tmp_sum + tau_i*math.log(tau_i)
                for j in adjacent_vertices[adjacent_vertices>i]:
                    for x_j in range(self.domain_size):
                        tau_ij = self.marginal_edge(i,j,x_i,x_j)
                        if tau_ij == 0:
                            continue
                        tau_j = self.marginal_node(j,x_j)
                        tmp_sum = tmp_sum + tau_ij*math.log(tau_ij/(tau_i*tau_j))
        return (-1*tmp_sum)


    def bethe_free_energy(self):
        tmp_entropy = 0
        tmp_sum = 0
        for i in range(self.N):
            adjacent_vertices = np.nonzero(self.adj_matrix[i])[0]
            for x_i in range(self.domain_size):
                tau_i = self.marginal_node(i, x_i)
                if tau_i:
                    tmp_entropy = tmp_entropy + tau_i*math.log(tau_i)
                    tmp_sum = tmp_sum + tau_i*math.log(self.phi_function(i,x_i))
                for j in adjacent_vertices[adjacent_vertices>i]:
                    for x_j in range(self.domain_size):
                        tau_ij = self.marginal_edge(i,j,x_i,x_j)
                        if tau_ij == 0:
                            continue
                        tau_j = self.marginal_node(j,x_j)
                        if tau_j == 0:
                            continue
                        tmp_entropy = tmp_entropy + tau_ij*math.log(tau_ij/(tau_i*tau_j))
                        tmp_sum = tmp_sum + (tau_ij*math.log(self.psi_function(i,j,x_i,x_j)))
        return (-1*tmp_entropy)+tmp_sum



def maxprod(A, w, its):
    __w = deepcopy(w)
    def psi_function(i,j, x_i, x_j):
        return int(x_i != x_j)

    def phi_function(i,x_i):
        return math.exp(__w[x_i])
    algo = LBP(A, len(w), psi=psi_function, phi=phi_function, sum=False)
    algo.belief_propoagation(its)
    max_assignments = list()
    for i in range(algo.N):
        max_assignments.append(algo.max_marginal_assignment(i))
    return max_assignments


def sumprod(A, w, its):
    __w = deepcopy(w)
    def psi_function(i,j, x_i, x_j):
        return int(x_i != x_j)

    def phi_function(i,x_i):
        return math.exp(__w[x_i])
    algo = LBP(A, len(w), psi=psi_function, phi=phi_function, sum=True)
    algo.belief_propoagation(its)
    bfe = algo.bethe_free_energy()
    log.info("bethe free energy: "+ str(bfe))
    return math.exp(bfe)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="count",
                        help="increase output verbosity (e.g., -vv is more than -v)")
    parser.add_argument('-A', '--adjacency_matrix',  help='<Required> Adjacency Matrix', required=True)
    parser.add_argument('-w', '--weights', help='<Required> weights',  required=True)
    parser.add_argument('-its', '--iteration', help='<Required> Iterations', type= int, required=True)
    parser.add_argument('--maxprod', dest='bp', action='store_const',
                        const=maxprod, default=sumprod,
                        help='Get Max assignments (default: find the bethe free energy)')

    args = parser.parse_args()
    if args.verbose:
        log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
        log.info("Verbose output.")
    else:
        log.basicConfig(format="%(levelname)s: %(message)s")
    print(args.bp(np.array(json.loads(args.adjacency_matrix)), np.array(json.loads(args.weights)), args.iteration))
