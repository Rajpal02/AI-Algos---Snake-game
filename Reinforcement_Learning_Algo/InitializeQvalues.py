import itertools
import json

from sympy import sequence

sequence = [''.join(s) for s in list(itertools.product(*[['0','1']] * 4))]
left_right = ['0','1','NA']
up_down = ['2','3','NA']

states = {}
for i in left_right:
	for j in up_down:
		for k in sequence:
			states[str((i,j,k))] = [0,0,0,0]
 
with open("Reinforcement Learning/qvalues.json", "w") as f:
	json.dump(states, f)
