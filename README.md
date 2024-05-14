# CFG Assignments

### About me

#### Background
My name is Dr. Bronte Mckeown and I have a background in Psychology and Neuroscience. I completed my PhD in Neuroscience at the University of York in September 2022, and then carried on my research programme in Canada for 18 months! Having returned to the UK, I have recently started a new freelance role back at the National Institute of Teaching, which I absolutely love. I am *super* excited to complete the CFGdegree as I hope it will improve both my technical skills and my confidence.

#### Links to find out more
- [LinkedIn](www.linkedin.com/in/bronte-mckeown)
- [Google Scholar](https://scholar.google.com/citations?user=5HWZCp0AAAAJ&hl=en)
- [Latest study](https://www.researchsquare.com/article/rs-4131471/v1)

### Assignment 1

#### Part 1
Part 1 is worth **14 marks**. These 14 marks are awarded for: "Demonstration of setting up GitHub and use of README."

Specifically, I need to:
- [x] Create a GitHub account.
- [x] Create a private repository.
- [x] Create a README.md file that contains information about me and what I'll be using GitHub for in this assignment.
    
- This README.md needs to contain *at least* 6 different markdown text formatting features. I have decided to use:
  - [x] Headings
  - [x] Bold
  - [x] Italic
  - [x] Quoting code 
  - [x] Links to URLs
  - [x] Lists
  - [x] Task lists
  - [ ] Images

#### Part 2

Part 2 is also worth **14 marks**. These 14 marks are awarded for: "Knowledge and demonstrated use of GitHub commands."

Specifically, I need to demonstrate:
- [] Checking the status
- [] Create a branch
- [] Adding files to a branch
- [] Adding commits with meaningful messages
- [] Opening a pull request
- [] Merging and deploying to main branch

##### The project to demonstrate Part 2 steps

I have used Python to run a correlation analysis on some made-up data and visualise the correlation with a scatter plot. I've broken this down below, with screenshots.

1. After creating this remote repository on GitHub, I created a local copy on my machine using `git clone`.
3. I then created a Python script that reads in data I collected during my PhD (two continuous variables) and stores them in a [pandas](https://pandas.pydata.org/) data frame.
4. I then used `git add` and `git commit` to document this step. I also used `git status` to check this worked.
5. I then correlated the two columns of interest using [panda's](https://pandas.pydata.org/) [.corr()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.corr.html) function.
    - The result is printed out to the console using `print()` statement.
8. I then used `git add` and `git commit` once more, and used `git push` to push all of the commits so far to the remote repository.
9. I then created a new branch called 'plot-dev'. In this branch, I created a new Python script that plots a scatter plot showing the association between the two variables using [seaborn's](https://seaborn.pydata.org/index.html) [.scatterplot()](https://seaborn.pydata.org/generated/seaborn.scatterplot.html) function.
10. I then used `git add`, `git commit` and `git push` once more to publish 'plot-dev' branch to the remote repository.
11. On GitHub, I then opened a pull request and merged the changes on 'plot-dev' branch to the main branch.
12. Finally, I used `git fetch` and `git pull` on my local machine to reflect this merging.
