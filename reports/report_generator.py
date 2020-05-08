'''
for each set of experimental results, calculate response time and stabilisation time per operation, also average

response time = time when done - time when registered

stabilization time = 
for each op:
  if needs total order:
    time when last conflict logged - time when logged at origin

'''