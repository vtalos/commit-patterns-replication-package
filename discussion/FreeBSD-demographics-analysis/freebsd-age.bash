#!/usr/bin/env bash
#
# Calculate the average FreeBSD developer age
# in the end of 2007 (the year the developer list was added) and in the
# end of 2023.
#

set -eu

if [[ $# -ne 1 ]] ; then
  echo "Usage: $0 freebsd-bare-git-repo-path" 1>&2
  exit 1
fi

GIT_DIR="$1"

# Run git on the FreeBSD repo
freebsd-git()
{
  git --git-dir=$GIT_DIR "$@"
}

# Return a sorted list of each developer's birth year
birthyears()
{
   freebsd-git show origin/main:usr.bin/calendar/calendars/calendar.freebsd |
     # Separate into : fields
     sed -n 's/</:/;s/@/:/;s/, */:/g;/:/p' |
     # Output login-id and birth year
     awk -F: '{print $2, $NF}' |
     sort
}

# Report the number and average age of the input's second field
# The reference year is passed as the first argument
average()
{
  awk '{n++; s+= $2} END {print n, '$1' - s / n}'
}

# Report the FreeBSD developer age at a given reference year
developer-age()
{
  local year="$1"
  join \
    # Active developers at the given year
    <(freebsd-git show $(freebsd-git rev-list -1 --before="$year-12-31" origin/main):share/misc/committers-src.dot |
    # Split into fields
    sed -n 's/ /:/;s/\\n/:/g;/label=/p' |
    # Select developers with active commit bit
    awk -F: 'NF == 4 {print $1}' |
    sort) <(birthyears) |
    average $year
}

# Report the average age in 2007 and 2023
for year in 2007 2023 ; do
  echo $year $(developer-age $year)
done
