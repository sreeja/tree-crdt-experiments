# tree-crdt-experiments

3 replicas, with FIFO connection. each replica has one log for self and one each per replica. 
each link has a network latency.
each operation has a vector timestamp associated with it.
log entry : {op, ts}
consistency levels determined during reading.
