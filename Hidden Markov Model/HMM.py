
class HiddenMarkovModel(object):

    # Hidden state set
    Q = ['Hot', 'Cold']

    #Initial Probability
    Pi = [0.8, 0.2 ]

    # Transitional Probability Matrix
    A = [[ 0.7, 0.3 ],
         [ 0.4, 0.6 ]]

    # Observation Likelihood
    B = [ [ 0.2, 0.5],
          [ 0.4, 0.4],
          [ 0.4, 0.1] ]

    # Observation Set
    O = [1, 2, 3]

    #This method implements Viterbi Algorithm to decode the best hidden state sequence for given observation sequence.
    def decode(self, obs_seq):
        T = len(obs_seq)
        N = len(self.Q)
        # Veterbi Trellis
        V = []
        #Back Track
        BT = []

        #Initialization
        V.append([])
        BT.append([])
        for j in range (0, N):
            trellis = self.Pi[j] * self.B[obs_seq[0]][j]
            V[0].append(trellis)
            BT[0].append(0)

        #Recursion
        for t in range (1, T):
            V.append([])
            BT.append([])
            for j in range (0, N):
                max_trellis = 0
                back_track = 0
                for i in range (0, N):
                    trellis = V[t-1][i] * self.A[i][j] * self.B[obs_seq[t]][j]
                    if max_trellis < trellis:
                        max_trellis = trellis
                        back_track = i
                V[t].append(max_trellis)
                BT[t].append(back_track)

        #Termination
        max_prob, back_track = 0, 0
        for i in range (0, N):
            trellis = V[T-1][i]
            if max_prob < trellis:
                max_prob = trellis
                back_track = i

        #Back track seq
        print ("\nBest hidden sequence: "),
        prob_seq = [self.Q[back_track]]
        for i in range (T-1, 0, -1):
            back_track = BT[i][back_track]
            prob_seq.append(self.Q[back_track])
        print prob_seq[::-1]
        print "Prob ", max_prob, "\n"
        return V

    def checkSeq(self, sequence):
        arr = []
        for c in sequence:
            try:
                value = int(c)
                if value not in self.O:
                    return False
                else:
                    index = self.O.index(value)
                    arr.append(index)
            except ValueError:
                return False
        return arr

#Driver code
h = HiddenMarkovModel()
while True:
    print ("Enter the seq or type 'q' to exit")
    seq = raw_input()
    if seq == "q":
        break
    arr = h.checkSeq(seq)
    if arr:
        h.decode(arr)
    else:
        print ("Invalid sequence")
