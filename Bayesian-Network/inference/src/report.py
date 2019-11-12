"""This module is created to build the report."""
from inference import Inference
from alarmNetwork import AlarmNetwork
from alarmNetwork import psuedorandom

inputQueries = []
inputQueries.append("[<A,f>][B]")
inputQueries.append("[<A,f>][J]")
inputQueries.append("[<J,t> <E,f>][B]")
inputQueries.append("[<J,t> <E,f>][M]")
inputQueries.append("[<M,t> <J,f>][B]")
inputQueries.append("[<M,t> <J,f>][E]")

net = AlarmNetwork()
random = psuedorandom()
sample_size = [1, 10, 50, 100, 200, 500, 1000, 10000]
inference_types = [1, 2, 3]

for input in inputQueries:
    for sample in sample_size:
        print("sample size: ", sample)
        for type in inference_types:
            ans = 0.0
            print ("Query: ", input, " type: ", type, " : ")
            for i in range(10):
                str, prob = Inference(net, type, sample, random ).infer(input)
                ans += prob
            print(ans/10.0)
