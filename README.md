# PrairieLearn for TCS ("TheorieLearn") Public Repository

[![Slack](https://img.shields.io/badge/join%20slack-pl4tcs-orange)](https://pl4tcs.slack.com)

## Welcome to TheorieLearn!

This is a public PrairieLearn repository for CS 374, CS 225, and other courses that teach theoretical computer science.
Anyone with a Microsoft or Google email address can see a demo of these problems at <https://www.prairielearn.org/>.

You can see and edit the canonical live version of PrairieLearn at <https://www.prairielearn.org/>.

For more information on developers, publications, instructor usage, funding, and more, please see the project page at <https://theorielearn.github.io/>

For questions related to CS 374 and development specific to this repository, there is a separate [Slack](https://pl4tcs.slack.com).

## Using Elements & Questions

If you run your own PrairieLearn course, you can use elements, questions, and code from this repository.

### Copying Elements

To use an element, copy the elements you want from `elements/` into your own `elements/` folder. Each element is self contained and should work without external code.
### Copying Questions

To use a question, or series of questions, copy the question folders from our `questions/` into your own `questions/` folder.
Some questions have shared code and resources located in `serverFilesCourse/theorielearn/`. The easiest way would be to place this `theorielearn/` subdirectory into your own `serverFilesCourse`, which will automatically support any question you import from here. You can optionally delete subfolders in `theorielearn/` that aren't imported by the questions you use.

A select few questions have shared resources located in `clientFilesCourse/`. Please check if the questions you use utilize this directory and copy what you need.

### Automatic Script

TBA! We will provide a script in the future that will let you select questions and elements you want and package it for you to drop in your course, automatically.

## Licensing

All text in this repository is published under a <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution (CC-BY 4.0)</a> licence.
  
All code in this repository is published under <a href="https://opensource.org/license/mit">the MIT License</a>.
