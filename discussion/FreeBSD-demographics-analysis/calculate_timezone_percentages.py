with open('discussion-about-the-changes\FreeBSD-demographics-analysis\commits_by_timezone_2023.txt', 'r') as file:
    lines = file.readlines()
    commits = []
    for line in lines:
        commits.append(int(line.split(':')[1].strip()))
    summary= sum(commits)
    for i in range(len(commits)): 
        print(f'{i-12}: {commits[i]/summary}')
    
