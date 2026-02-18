# TheorieLearn Public Repository

[![Slack](https://img.shields.io/badge/join%20slack-pl4tcs-orange)](https://pl4tcs.slack.com)

<img src="NewTLlogo.png" width="66%" alt="TheorieLearn logo">

## Welcome to TheorieLearn!

This is a public repository of scaffolding exercises for theoretical computer science, implemented on the on the [PrairieLearn](https://www.prairielearn.org) platform.  These exercises were designed for [CS 374](https://courses.grainger.illinois.edu/cs374al1/) and other courses that teach theoretical computer science at the University of Illinois Urbana-Champaign.

A public practice course containing all our available exercises is available on [PrairieLearn](https://www.prairielearn.org) to anyone with a Microsoft account, Google account, or login credentials at a university with a PrarieLearn license.

For more information about the TheorieLearn project, including developers, publications, instructor usage, and funding information, please see the project page at <https://theorielearn.github.io/>.

For questions specific to this repository, feel free to join the TheorieLearn [Slack](https://pl4tcs.slack.com) or email the project director [Jeff Erickson](https://jeffe.cs.illinois.edu) (jeffe@illinois.edu).  For more general PrairieLearn questions, we recommend joining the [PrairieLearn Slack](prairielearn.slack.com); Jeff and other members of the TheorieLearn team are active on this Slack space.

## Copyright and License Information

**Copyright &copy; 2026 [TheorieLearn](https://theorielearn.github.io/)**

* All text in this repository is released under a [Creative Commons Attribution 4.0 International (CC-BY) License](https://creativecommons.org/licenses/by/4.0/deed.en).

* All code in this repository is released under [The MIT License](LICENSE).

You may freely free to use, copy, adapt, remix, and/or redistribure any questions, assessments, elements, or other code from this repository, subject to the terms of these licenses.  In particular, if you redistribute any code, please include a link either to this repository <https://github.com/TheorieLearn/TheorieLearnPublic> or to the main TheorieLearn page <https://theorielearn.github.io/>

These resources are based in part on [Jeff Erickson's _Algorithms_ textbook and other course materials](https://jeffe.cs.illinois.edu/teaching/algorithms/), which are also freely available.

## How to Use Our Resources in Your Own PrairieLearn Course

### Copying Questions

To use a question or series of questions, copy the question folders from our `questions/` into your own `questions/` folder.
Some questions have shared code and resources located in `serverFilesCourse/theorielearn/`. The easiest way would be to place this `theorielearn/` subdirectory into your own `serverFilesCourse`, which will automatically support any question you import from here. You can optionally delete subfolders in `theorielearn/` that aren't imported by the questions you use.

A select few questions have shared resources located in `clientFilesCourse/`. Please check if the questions you use utilize this directory and copy what you need.

### Copying Elements

To use an element, copy the elements you want from `elements/` into your own `elements/` folder. Each element is self contained and should work without external code.

### Automatic Script

TBA! We will provide a script in the future that will let you select questions and elements you want and package it for you to drop in your course, automatically.

