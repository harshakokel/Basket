class Inference:
    """Module represents Inference for Bays Net."""

    def __init__(self, net, type, noOfSamples, random):
        """Type 0: enum, 1: prior samp, 2: rej samp, 3: liklihood weighting."""
        self.net = net
        self.type_ = type
        self.noOfSamples = noOfSamples
        self.random = random

    def infer(self, query):
        """Runs the inference on the query and returns the.

        Args:
            query (string) String with List of evidence and the query nodes
                           Example: [<E,t> <J,t>][M, A]
        """
        strings = query.strip("[").strip("]").split("][")
        process = self.processStr(strings[0], strings[1])
        prior = process[0]
        postList = process[1]
        inferred_prob = []
        for posterior in postList:
            prob = self.doInference[self.type_](self, posterior, prior)
            inferred_prob.append("<" + posterior + ", " + str(prob) + ">")
        return inferred_prob, prob

    def processStr(self, strE, strQ):
        """Return the evidence list and query list for given strings."""
        eList = {}
        e = strE.replace("<", "").replace(">", "").split(" ")
        for x_ in e:
            x = x_.split(",")
            truthValue = 0
            if(x[1] == "t"):
                truthValue = 1
            eList[x[0]] = truthValue
        qList = [y.strip() for y in strQ.split(",")]
        return(eList, qList)

    def enumeration(self, query, evidence):
        """Infer the exact probability of the query by enumeration."""
        variables = self.net.nodes()
        evidence_ = evidence.copy()
        joint_distribution = []
        # for post = True and False
        for p_truth_value in [1, 0]:
            evidence_[query] = p_truth_value
            joint_distribution.append(self.enumerateAll(variables, evidence_))
        return self.normalize(joint_distribution)[0]

    def normalize(self, joint_distribution):
        """Return normalized probability."""
        return [x/sum(joint_distribution) for x in joint_distribution]

    def enumerateAll(self, variables, evidence):
        """Enumerate full joint_distribution for the given evidence."""
        if not variables:
            return 1
        sum_ = 0
        if variables[0] in evidence.keys():
            prior_ = [evidence[parent] for parent in self.net.parent(variables[0])]
            prob_ = self.net.probOf((variables[0], evidence[variables[0]]), prior_)
            sum_ = prob_ * self.enumerateAll(variables[1:], evidence)
        else:
            for val_ in [1, 0]:
                new_evidence = evidence.copy()
                new_evidence[variables[0]] = val_
                prior__ = [new_evidence[parent] for parent in self.net.parent(variables[0])]
                prob_ = self.net.probOf((variables[0], val_), prior__)
                sum_ = sum_ + (prob_ * self.enumerateAll(variables[1:], new_evidence))
        return sum_

    def priorSampling(self, query, evidence):
        """Wrapper method for prior sampling."""
        evidence_ = [(k, v) for k, v in evidence.items()]
        return self.count(self.genNSamples(self.noOfSamples), evidence_, query)

    def rejectionSampling(self, query, evidence):
        """Calculate the probability of query using rejection sampling.

           Find the probability of query being true given the evidence
           values using rejection sampling algo and the no of Samples mentioned.

           Args:
            noOfSamples (int)   No of samples
            evidence (dict)     Evidence dictionary with nodes as key and respective
                                truthvalues as value.
            query (string)      Name of node queried
        """
        samples = []
        for k in range(self.noOfSamples):
            s = self.generateRejectionSample(evidence)
            samples.append(s)
        positiveQueryCount = 0
        for sample in samples:
            if sample[query]:
                positiveQueryCount = positiveQueryCount + 1
        prob = float(positiveQueryCount)/self.noOfSamples
        return prob

    def generateRejectionSample(self, evidence):
        """Generate a sample that agrees with the evidence.

        Args:
            evidence (dict) Evidence dictionary with nodes as key and respective
                            truthvalues as value.
        """
        sample = {}
        sampleNotFound = True
        while sampleNotFound:
            sample = {}
            for node in self.net.nodes():
                parents = self.net.parent(node)
                probabilityOfNode = 0
                # calc the probability of current variable
                if len(parents) < 1:
                    # no parent so just get distr
                    probabilityOfNode = self.net.probOf((node, 1), [])
                else:
                    prior = [sample[x] for x in parents]
                    probabilityOfNode = self.net.probOf((node, 1), prior)
                randomValue = self.random.uniform()
                if randomValue <= (probabilityOfNode):
                    if node in evidence:
                        if evidence[node] == 0:
                            break
                    sample[node] = 1
                else:
                    if node in evidence:
                        if evidence[node] == 1:
                            break
                    sample[node] = 0
            if len(sample) == len(self.net.nodes()):
                    sampleNotFound = False
        return sample

    def likelihoodWeighting(self, query, evidence):
        """Wrapper method for likelihood weightage sampling."""
        # evidence_ = [ (k,v) for k,v in evidence.items()]
        pos = 0.0
        neg = 0.0
        ix = self.net.nodes().index(query)

        for i in range(self.noOfSamples):
            w, x = self.genWeightedSample(evidence)
            if x[ix] == 1:
                pos += w
            else:
                neg += w
        tot = pos+neg
        if tot > 0.0:
            # print(" < ", pos/tot, ",", neg/tot, ">")
            return pos/tot
        return 0.0

    def count(self, samples, evidence, query):
        # list [(a,1), (b,0) , .. ]
        evidences = {}
        vix = self.net.nodes().index(query)
        pos = 0.0
        neg = 0.0
        for e_ in evidence:
            ix = self.net.nodes().index(e_[0])
            evidences[ix] = e_[1]
        for s in samples:
            ignore = 0
            for ix, t in evidences.items():
                if s[ix] != t:
                    ignore = 1
                    break
            if not ignore == 0:
                if s[vix] == 1:
                    pos += 1
                else:
                    neg += 1

        t = pos + neg
        if t != 0:
            # print ("<", pos/t, ",", neg/t, ">")
            return float(pos)/float(t)
        else:
            return 0.0

    def genSample(self):
        # map to record value of parent
        parVal = {}

        for c in self.net.nodes():
            pars = self.net.parent(c)
            probDist = 0.0
            # calc the probability distribution of current variable
            if len(pars) < 1:
                # no parent so just get distr
                probDist = self.net.probOf((c, 1), [])
            else:
                post = [parVal[x] for x in pars]
                probDist = self.net.probOf((c, 1), post)
            r = self.random.uniform()
            if r <= (probDist):
                parVal[c] = 1
            else:
                parVal[c] = 0
        return list(parVal.values())

    def genNSamples(self, n):
        samples = []
        for k in range(n):
            s = self.genSample()
            samples.append(s)
            # print(s)
        return samples

    def genWeightedSample(self, e):
        w = 1  # intially weight is 1
        parVal = {}  # record the sample in top order
        for c in self.net.nodes():
            pars = self.net.parent(c)  # parents of current node
            probDist = 0.0
            #  calc the probability distribution of current variable
            if len(pars) < 1:   # no parent so just get distr
                probDist = self.net.probOf((c, 1), [])
            else:
                post = [parVal[x] for x in pars]
                probDist = self.net.probOf((c, 1), post)

            # if evidence variable update weight, sample has truth value of evidence
            if c in e.keys():
                if e[c] == 1:
                    w = w * probDist
                    parVal[c] = 1
                else:
                    w = w * (1. - probDist)
                    parVal[c] = 0
            # else randomly sample
            else:
                r = self.random.uniform()
                if r <= (probDist):
                    parVal[c] = 1
                else:
                    parVal[c] = 0
        return w, list(parVal.values())

    # map the inference to the function blocks
    doInference = {0: enumeration,
                   1: priorSampling,
                   2: rejectionSampling,
                   3: likelihoodWeighting
                  }  # replace 2 with rejection sampling
