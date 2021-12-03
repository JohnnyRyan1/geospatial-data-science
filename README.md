# Geospatial Data Science #

Course materials for Geospatial Date Science (GEOG 4/590) taught at the Department of Geography, University of Oregon

## Schedule

| **Week**    |  **Date**  | **Lecture x 1 hour**  | **Lab x 2 hours**                     | **Project**      |
| ----------- |------------|-----------------------|---------------------------------------|------------------|
| 1           | Jan 3      |Introduction           |Getting started with Python and GitHub |                  | 
| 2           | Jan 10     |Tables + vector data   |Census data + city stats               |                  | 
| 3           | Jan 17     |Network data           |Walking distances                      |                  |
| 4           | Jan 24     |Gridded data           |Land cover classification              |Submit project idea and outline| 
| 5           | Jan 31     |Machine learning       |Predicting river discharge             |                  |
| 6           | Feb 7      |Accessing data + web scraping     |Wildfire + air quality        |Project milestone #1           |
| 7           | Feb 14     |Data management + version control |Pubic school redistricting    |                  |
| 8           | Feb 21     |Missing data + feature selection  |Wind farm placement           |Project milestone #2           |
| 9           | Feb 28     |Ethics and responsibility |No lab, work on project       |                               |
| 10          | Mar 7      |Project presentations  |Project presentations                  |Project submission             |


## Step 1: Download Anaconda

In order to execute the code in the notebooks, you will need to install a Python distribution with the necessary packages.

The recommended way to do this is to install the [Anaconda](https://www.anaconda.com/download/) which uses the the [conda package management utility](https://conda.io/docs/).

## Step 2: Clone this repository

The best way to interact with the materials is to use [git](https://git-scm.com/) to [clone this repository](https://git-scm.com/book/en/v2/Git-Basics-Getting-a-Git-Repository). If you don't have git already on you computer, it is easy to install on all platforms following [these instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

From the command line, navigate to your course folder and run in a terminal:

<code>git clone https://github.com/JohnnyRyan1/geospatial_data_science</code>

Once you have the repository cloned, you can update it by running:

<code>git pull origin master</code>

<!-- The links below will render the notebooks via the [nbviewer](http://nbviewer.jupyter.org/) service, which allows some of the fancy interactive graphics to be viewed online. If you browse directly to the notebooks on github, they may not show up properly. So please use these links.-->

<!--The lecture notes are in the form of interactive [Jupyter Notebooks](https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/What%20is%20the%20Jupyter%20Notebook.html).-->

## Step 3: Make a new environment

Each lab includes an environment file (e.g. <code>environment.yml</code>) which can be used to set up your Python environment. Foe example, to install the conda environment for Lab #1, type the following in a terminal:

<code>conda env create -f environment.yml</code>

This will create a new environment called **lab1**. To activate this environment, type

<code>conda activate lab1</code>

<!--For more depth, you can read my [detailed intstructions for installing python](https://rabernat.github.io/research_computing/python.html).-->

## Step 4: Viewing the assignments

The notebooks can be viewed and run using the [jupyter notebook](https://jupyter-notebook.readthedocs.io/en/stable/notebook.html) application. To launch the notebook interface, type:

<code>jupyter notebook</code>

When you are done working with the notebooks, close the notebook app and, if you wish, deactive the environment by typing:

<code>conda deactivate</code>

## Useful resources ##

* https://automating-gis-processes.github.io/site/course-info/course-info.html

<!--## Why Python ##

A great deal has been written on [this subject](http://cyrille.rossant.net/why-using-python-for-scientific-computing/).
My reasons are summarized as follows.

1. __Python is open source__. [Open source](https://en.wikipedia.org/wiki/Open_source)
means that the source code is available freely to the public and can be examined,
modified, and improved. The alternative to open source is closed, proprietary.
Proprietary tools, such as MATLAB, are ultimately controlled by corporations, and
those corporations decide what features they will include. I consider software
tools as a central part of scientific research---if we want to have transparent,
reproducible, scientific results, we should be using open source tools.
[Nature](http://www.nature.com/nature/journal/v482/n7386/full/nature10836.html)
agrees with me.

1. __Python is free__. It does not cost money to use python. If your scientific
code is written in MATLAB, it can only be run by others with access to MATLAB.
That means people outside the university world (e.g. high school students), in
economically disadvantaged communities, or in developing countries will be
unable to reproduce and build on your results.

1. __Python is easy to read__. This may seem like a superficial point, but it is
crucial for effective sharing of code. Even if you are the only one reading
your code, python is easy on the eyes.

1. __Python has a great library__. The [scipy ecosystem](http://scipy.org)
provides the tools to do almost anything you can imagine.

1. __Python is constantly evolving__. If you find something you _can't_ do with
python, chances are someone is working on it. The world is changing: data is
exploding, computers architecture is evolving, and new forms of analysis and
visualization are being invented. Python is evolving too, and it evolves based
on what the community needs.

1. __Python is at home on the web__. The [Jupyter project](https://jupyter.org/)
grew out of the python community and is revolutionizing the way we do science
and communicate it with others. With Jupyter, I never have to leave my browser.
[Nature agrees](http://www.nature.com/news/interactive-notebooks-sharing-the-code-1.16261)
that this is the future of scientific communication. -->
