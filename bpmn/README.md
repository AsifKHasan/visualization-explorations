> *bpmn-from-yml* is for generating bpmn image (SVG, PNG etc.) via GraphViz .dot documents from yml data

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

        cd visualization-explorations/bpmn
6. get required Python libraries

        pip install -r requirements.txt

You should be done with installations now

# generating mindmaps
bpmn images are geneated by running a script which takes the name of an ```yml``` file. What we want in the mindmap we describe in the yml.

```yml``` files must under ```data``` directory and must have ```*.yml``` extension. You can create subdirectories under ```data``` directory to create and keep your ```yml``` files

For example if you have a bpmn ```yml``` under ```data/spectrum``` directory named ```my-test.yml```, this is how you run the tool and generate the bpmn as an SVG

    bpmn-from-yml.bat spectrum/my-test

>   note we do not need to indicate that the file is under ```data``` directory (it is assumed) and we do not need to provide the ```*.yml``` extension (it is assumed)

If everything goes well you should be able to get two files under ```out``` directory

- my-test.gv
- my-test.svg

The best way to open the ```svg``` is through a browser.

# bpmn yml notes
## allowed items 
### start events
start
start-compensation
start-conditional
start-conditional-non
start-error
start-escalation
start-escalation-non
start-message
start-message-non
start-multiple
start-multiple-non
start-parallel-multiple
start-parallel-multiple-non
start-signal
start-signal-non
start-timer
start-timer-non

### end events
end
end-cancel
end-compensation
end-error
end-escalation
end-message
end-multiple
end-signal
end-terminate

### intermediate events
intermediate
catch-cancel
catch-compensation
throw-compensation
catch-error
catch-escalation
catch-escalation-non
throw-escalation
catch-link
throw-link
catch-message
catch-message-non
throw-message
catch-multiple
catch-multiple-non
throw-multiple
catch-parallel-multiple
catch-parallel-multiple-non
catch-signal
catch-signal-non
throw-signal
conditional
conditional-non
timer
timer-non

### task activities
task
business-rule-task
manual-task
receive-task
script-task
send-task
service-task
user-task

### call activities
call
business-rule-call
manual-call
script-call
user-call

### subprocess activities
process
adhoc
transaction

### event subprocess activities
event
event-compensation
event-conditional
event-conditional-non
event-error
event-escalation
event-escalation-non
event-message
event-message-non
event-multiple
event-multiple-non
event-parallel-multiple
event-parallel-multiple-non
event-signal
event-signal-non
event-timer
event-timer-non

### gateways
exclusive
inclusive
parallel
complex
event-based
event-based-start
event-based-parallel-start

### data
data
data-collection
data-input
data-input-collection
data-output
data-output-collection
data-store

## allowed edges
sequence
message
association
directed-association
bidirectional-association
