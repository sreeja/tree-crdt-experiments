#!/bin/bash
for LC in 2
do
  export LC_ENV=$LC
  for EXP in 0 1 2 3
    do
      export EXP_ENV=$EXP
      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep 40
      sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
      sleep 40
      cp -r data/ lc$LC_ENV/data0_$EXP_ENV
      kill $P_PID
      sleep 30

      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep 40
      sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
      sleep 40
      cp -r data/ lc$LC_ENV/data10_$EXP_ENV
      kill $P_PID
      sleep 30

      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep 40
      sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
      sleep 40
      cp -r data/ lc$LC_ENV/data20_$EXP_ENV
      kill $P_PID
      sleep 30
    done
done
