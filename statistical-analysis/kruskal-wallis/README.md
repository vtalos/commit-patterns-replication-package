# Kruskal-Wallis

* [`kruskal.py`](kruskal.py) performs the Kruskal-Wallis test on commit data from a CSV file to determine if there are statistically significant differences between groups (days). If significant differences are found, it conducts post-hoc pairwise Mann-Whitney U tests with Bonferroni correction to identify which specific groups differ.  
  Run `python kruskal.py <filename.csv>`
