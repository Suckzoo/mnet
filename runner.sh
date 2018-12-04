# for runner in traditional/traditional.py mnet/mnet_bd_sum.py mnet_bd_wg_sum.py mnet/mnet
# for var in 9 12
# do
#   for deepness in 5 20
#     filename=manual_$(var)_$(deepness).txt
#     run.sh manual

get_runner()
{
  if [ "$1" = "traditional.py" ]; then
    actual_runner="traditional/traditional.py"
  else
    actual_runner="mnet/$1"
  fi
}

get_testfile()
{
  testfile="manual_$1_$2.txt"
}

for runner in traditional.py $(ls mnet/)
do
  get_runner $runner
  echo "\n\nRunning $actual_runner..."
  for numvar in 9 12
  do
    for deepness in 5 20
    do
      get_testfile $numvar $deepness
      runner_directory=$(echo $runner | cut -d'.' -f 1)
      log_directory="log/$runner_directory/$testfile"
      mkdir -p $log_directory
      echo "[$actual_runner] Running on $testfile..."
      echo "./run.sh $actual_runner $testfile"
      ./run.sh $actual_runner "testcodes/results/$testfile" > $log_directory/stdout 2> $log_directory/stderr
    done
  done
done
