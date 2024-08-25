#!/bin/bash
#A huge volume of commits is obesrved for maria db
#in 2013 during 23:57--00:03:00 for 16-17 April.
#As they are for sure automated, we count them,
#so they can be removed from the sample
#and not be considered as a spike.

cd /home/repos/github/mariadb/server || exit 1

commits=$(git log --grep="git-svn-id" --since="2013-01-01" --until="2013-12-31" --pretty=format:"%b %ad" | grep 'Tue Apr 16' | grep -E "23:5[7-9]:.." | wc -l)
echo "Reject $commits commits for 23:00-23:59 during 23:57-23:59" 

commits=$(git log --grep="git-svn-id" --since="2013-01-01" --until="2013-12-31" --pretty=format:"%b %ad" | grep 'Wed Apr 17' | grep -E "00:0[0-2]:.." | wc -l)
echo "Reject $commits commits for 00:00-00:59 during 00:00-:00:02" 
