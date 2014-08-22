#$ -S /bin/bash
#$ -N ameert_login
#$ -j y

nodeNumber=$*
nodeName="node${nodeNumber}"

ssh -Y $nodeName

