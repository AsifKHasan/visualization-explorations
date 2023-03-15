> *ganttchart-from-yml* is for generating ganttchart image (SVG, PNG etc.) via GraphViz .dot documents from yml data

# pre-requisites
1. Git (https://git-scm.com/downloads). *Make sure Git executables are in the PATH*
2. GitHub account (https://github.com/)
3. GraphViz (dot) latest version (https://graphviz.org/download/). *Make sure dot executables are in the PATH*
4. Python (3.8+ or latest) (https://www.python.org/downloads/). *Make sure Python executables are in the PATH*

# installation
1. open command prompt or shell terminal
2. go to a directory (create it if needed) where you want to download to and run the project from
3. clone GitHub repository ```AsifKHasan/visualization-explorations``` from https://github.com/AsifKHasan/visualization-explorations

       git clone https://github.com/AsifKHasan/visualization-explorations.git

4. this should get you all required source in a subdirectory named ```visualization-explorations```
5. cd to **mindmap** code

        cd visualization-explorations/ganttchart
6. get required Python libraries

        pip install -r requirements.txt

You should be done with installations now

# generating mindmaps
ganttchart images are geneated by running a script which takes the name of an ```yml``` file. What we want in the mindmap we describe in the yml.

```yml``` files must under ```data``` directory and must have ```*.yml``` extension. You can create subdirectories under ```data``` directory to create and keep your ```yml``` files

For example if you have a ganttchart ```yml``` under ```data/spectrum``` directory named ```my-test.yml```, this is how you run the tool and generate the ganttchart as an SVG

    ganttchart-from-yml.bat spectrum/my-test

>   note we do not need to indicate that the file is under ```data``` directory (it is assumed) and we do not need to provide the ```*.yml``` extension (it is assumed)

If everything goes well you should be able to get two files under ```out``` directory

- my-test.gv
- my-test.svg

The best way to open the ```svg``` is through a browser.

# ganttchart yml notes
