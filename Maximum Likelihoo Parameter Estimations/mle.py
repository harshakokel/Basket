import sampling
import numpy as np
import LBP
import logging
import argparse
import json
import itertools

log = logging.getLogger("MLE")

def colorem(A, L, samples, its=50):
    log.info(" colorem called")

    #Converting L to np array
    L = np.array(L)

    # missing vertices
    V_m = np.nonzero(L)[0]

    # observed vertices
    V_o = np.nonzero(L<1)[0]

    # Number of nodes
    V = A.__len__()

    # Number of samples
    if A.__len__() != samples.__len__(): # Handling the case where sample is mxn
        samples = np.transpose(samples)
    M = samples[0].__len__()

    # Maximum color assignment
    max_color = np.max(samples)

    # subtract 1 from all sample assignments if color starts from  1.
    if min(np.min(samples), 1):  # if start from zero do not subtract
        samples = samples - 1

    min_color = 0
    log.info(" colors starting from " + str(min_color))
    domain_size = max_color + (1 - min_color)

    # step size
    learning_rate = max(2e-1/M, 2e-4)

    # Initial weight vector: all colors have uniform weights
    w = np.ones(domain_size)

    # Count color assignments in observed variables
    # obs is vector of domain size with number of counts for each domain
    unique, counts = np.unique(samples[V_o,:], return_counts=True)
    obs = np.array([])
    for color in range(min_color,max_color+1):
        if len(np.where(unique==color)[0]) == 0:
            obs = np.append(obs, 0)
        else:
            obs = np.append(obs, counts[np.where(unique==color)[0][0]])

    # Count color assignments in domain of missing variables
    X_m = [range(w.__len__())] * V_m.__len__()
    X_m = list(itertools.product(*X_m))
    m_obs = np.empty([domain_size,X_m.__len__()])
    i = 0
    for color in range(min_color, max_color + 1):
        j = 0
        for x in X_m:
            m_obs[i,j]=x.count(color)
            j = j+1
        i = i + 1


    while its:
        # E step: Calculate expected values of missing variables
        q = np.empty([M,X_m.__len__()])
        for i in range(M):
            evidence = dict(zip(V_o, samples[V_o, i]))
            q[i] = LBP.conditional_marginals(A, w, 100, evidence, V_m, X_m)

        # M step: Calculate updated values of w
        e_obs_m = np.zeros(domain_size)
        j = 0
        for color in range(min_color,max_color+1):
            for i in range(M):
                e_obs_m[j] = e_obs_m[j] + np.dot(q[i], m_obs[j])
            j = j +1

        # gradient formula derived in the attached pdf
        gradient = obs + e_obs_m - M * LBP.sum_of_marginals(A, w, 100)

        # Check convergence
        if max(learning_rate*gradient) <= 0.05:
            log.info(" converged: ")
            log.info(w)
            break

        # Gradient Ascent
        w = w + learning_rate * gradient
        log.info(w)
        its = its-1

    # scaling weights to positive number to make it pleasant
    w = w - np.min(w) + 1
    return w


def colormle(A, samples, its=50):
    log.info(" colormle called")

    # Number of nodes
    V = A.__len__()

    # Number of samples
    if A.__len__() != samples.__len__(): # Handling the case where sample is mxn
        samples = np.transpose(samples)
    M = samples[0].__len__()

    # Maximum color assignment
    max_color = np.max(samples)

    # Min color assignment (Default is 1) but to handle samples with color 0
    min_color = min(np.min(samples), 1)
    log.info(" colors starting from " + str(min_color))
    domain_size = max_color + (1 - min_color)

    # step size
    learning_rate = min(2e-1/M, 2e-5)

    # Initial weight vector: all colors have uniform weights
    w = np.ones(domain_size)

    # Count color assignments in samples
    # obs is vector of domain size with number of counts for each domain
    unique, counts = np.unique(samples, return_counts=True)
    obs = np.array([])
    for color in range(min_color,max_color+1):
        obs = np.append(obs, counts[np.where(unique==color)[0][0]])

    while its:
        # Gradient derived in the attached pdf
        gradient = obs - M*LBP.sum_of_marginals(A, w, 100)
        log.info(sum(abs(gradient)) )
        # Check convergence
        if max(learning_rate*gradient) <= 0.05:
            log.info(" converged: ")
            log.info(w)
            break

        # Gradient Ascent
        w = w + learning_rate*gradient
        log.info(w)
        its = its-1
    # scaling weights to positive number to make it pleasant
    w = w - np.min(w) + 1
    return w



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action="count",
                        help="increase output verbosity (e.g., -vv is more than -v)")
    parser.add_argument('-A', '--adjacency_matrix', help='<Required> Adjacency Matrix', required=True)
    parser.add_argument('-w', '--weights', help='<Required> weights', required=True)
    parser.add_argument('-L', '--latent', help='Latent variables', required=False)
    parser.add_argument('-b', '--burnin', help='<Required> number of burn-in samples', required=True)
    parser.add_argument('-s', '--samples', help='<Required> number of samples after burn-in', type=int,
                        required=True)
    parser.add_argument('-its', '--iterations', help='number of iterations', required=False)
    parser.add_argument('--em', dest='mle', action='store_const',
                        const=colorem, default=None,
                        help='Get Max assignments (default: find the bethe free energy)')
    args = parser.parse_args()
    if args.verbose:
        logging.getLogger("MLE").setLevel(logging.DEBUG)
        logging.getLogger("MLE").info("Verbose output.")
    else:
        logging.getLogger("MLE").setLevel(logging.INFO)
        logging.getLogger("MLE").info("Verbose output.")
        pass
    A = np.array(json.loads(args.adjacency_matrix))
    w = np.array(json.loads(args.weights))
    b = int(args.burnin)
    s = int(args.samples)
    samples_transpose = sampling.gibbs_samples(A, w,b,s )
    samples = np.transpose(samples_transpose)
    if args.mle:
        L = np.array(json.loads(args.latent))
        print(colorem(A, L, samples_transpose))
    else:
        print(colormle(A, samples))