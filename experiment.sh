#!/bin/bash
> log.txt
for LC in 1 2 3
do
  export LC_ENV=$LC
  t=$(expr 30 \* $LC_ENV)
  for EXP in 0 1 2 3
    do
      export EXP_ENV=$EXP

      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep $t
      sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
      sleep $t
      sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
      sleep $t
      sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
      sleep $t
      sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
      sleep $t
      sh workload/conflict0_load0.sh & sh workload/conflict0_load1.sh & sh workload/conflict0_load2.sh 
      sleep $t
      cp -r data/ lc$LC_ENV/data0_$EXP_ENV
      kill $P_PID
      sleep 45

      echo "Done lc" $LC_ENV " exp "$EXP_ENV " con " 0 >> log.txt

      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep $t
      sh workload/conflict2_load0.sh & sh workload/conflict2_load1.sh & sh workload/conflict2_load2.sh 
      sleep $t
      sh workload/conflict2_load0.sh & sh workload/conflict2_load1.sh & sh workload/conflict2_load2.sh 
      sleep $t
      sh workload/conflict2_load0.sh & sh workload/conflict2_load1.sh & sh workload/conflict2_load2.sh 
      sleep $t
      sh workload/conflict2_load0.sh & sh workload/conflict2_load1.sh & sh workload/conflict2_load2.sh 
      sleep $t
      sh workload/conflict2_load0.sh & sh workload/conflict2_load1.sh & sh workload/conflict2_load2.sh 
      sleep $t
      cp -r data/ lc$LC_ENV/data2_$EXP_ENV
      kill $P_PID
      sleep 45

      echo "Done lc" $LC_ENV " exp "$EXP_ENV " con " 2 >> log.txt

      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep $t
      sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
      sleep $t
      sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
      sleep $t
      sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
      sleep $t
      sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
      sleep $t
      sh workload/conflict10_load0.sh & sh workload/conflict10_load1.sh & sh workload/conflict10_load2.sh 
      sleep $t
      cp -r data/ lc$LC_ENV/data10_$EXP_ENV
      kill $P_PID
      sleep 45

      echo "Done lc" $LC_ENV " exp "$EXP_ENV " con " 10 >> log.txt

      for f in $(find data); do > $f; done
      make down
      make run &
      P_PID=$!
      sleep 60
      sh workload/base.sh
      sleep $t
      sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
      sleep $t
      sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
      sleep $t
      sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
      sleep $t
      sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
      sleep $t
      sh workload/conflict20_load0.sh & sh workload/conflict20_load1.sh & sh workload/conflict20_load2.sh 
      sleep $t
      cp -r data/ lc$LC_ENV/data20_$EXP_ENV
      kill $P_PID
      sleep 45

      echo "Done lc" $LC_ENV " exp "$EXP_ENV " con " 20 >> log.txt
    done
done

for f in $(find data); do > $f; done
make down

python reports/report_generator.py