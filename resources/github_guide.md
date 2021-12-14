# Github Guide

Here are some notes about Git and Github from the labs in one place. 

## Install git

Instructions for installing `git` on different operating systems can be found [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

## Clone a repository

We can clone the forked course repository from the command line by running:

<code>git clone https://github.com/your_username/geospatial_data_science</code>

Where <code>your_username</code> is your GitHub username. *Note that you should navigate to your coursework folder before running this command*

In GitHub Desktop, click **Clone a repository from the Internet**, enter <code>https://github.com/your_username/geospatial_data_science</code> as the **URL**, choose a **local path** where you keep your coursework (e.g. `C:\Users\your_name\Documents`) and click **Clone**.

## Submit an assignment via command line

In **command line**, we first check to see which files were added/edited.

<code>git status</code>

Which should show what changes have occurred compared to the previous commit. We can add these files to the staging environment using the <code>git add</code> command. 

<code>git add labX_submission.ipynb</code>

Where <code>labX_submission.ipynb</code> is your assignment to be submitted. 

Now if you rerun the <code>git status</code>, you'll see that `git` has added the file to the staging environment (notice the "Changes to be committed" line). 

**NB: only push your answer notebooks (and other relevant files) to your GitHub repository**

If you make changes to the *assignment notebooks*, command line users can run <code>git checkout filename.ipynb</code> to discard unstaged changes to the file. If the changes were accidently staged, run <code>git reset</code>. 

We can commit these new/edited files by running:

<code>git commit -m "uploaded first assignment"</code>

The message at the end of the commit should be something related to what the commit contains - could be a new feature, a bug fix, or just fixing a typo. 

Finally, we can send these file to our GitHub repository by typing:

<code>git push</code>

## First time login

At this stage, git will probably ask for your username and email which you can configure using:

<code>git config --global user.name "your name"</code>\
<code>git config --global user.email "your_email@uoregon.edu"</code>

In addition, GitHub no longer supports username/password authentication from the command line so users must switch to "personal access tokens" which can be configured using the following instructions [here](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) or [here](https://swcarpentry.github.io/git-novice/07-github/index.html#ssh-background-and-setup).

## Submit an assignment via GitHub Desktop

To upload the files to GitHub using **GitHub Desktop**, simply click **Commit to master** in the lower left pane and then **Push to origin**. 

Again, only push your answers notebooks (and any other new files such as images) to your GitHub repository. If you made changes to the assignment notebooks you can discard these changes by right-clicking on the file in GitHub Desktop and selecting **Discard changes** before clicking **Commit to master**.

## Check for any updates in the course materials

Before we start an assignment, we need to check whether there are any updates to the original course repository. We can do this by adding the original repository (the one we forked) as a *remote*. Command line users can do this by running:

<code>git remote add upstream https://github.com/JohnnyRyan1/geospatial-data-science</code>

Then fetch and merge the updated course content by running:

<code>git fetch upstream</code>

<code>git merge upstream/master master</code>

GitHub Desktop users should first click the **Fetch origin** button to check for new changes. Then click the triangle symbol next to **Current branch: master**, click **Choose a branch to merge into master**, click **upstream/master** from **Other branches** and click **Create a merge commit**. 

Any new updates to the course repository will now be available in your local repository. 

## Basic branching 
```
git checkout -b newbranch
git add .
git commit -m 'Made some changes'
git checkout main
git merge newbranch
git checkout -d newbranch
```

## Improved git log formatting
`git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit`