
\appendix

# Appendix


## Structuring a Scientific Project

The below are important highlights from [*A Quick Guide to Organizing Computational Biology Projects*](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424#pcbi-1000424-g001) by William Noble.

> It is generally a good idea to store all of the files relevant to one project under a common root directory.

> use a top-level organization that is logical, with chronological organization at the next level, and logical organization below that


\begin{figure}
\fbox{\includegraphics[width=1\linewidth]{assets/graphics/journal-pcbi-1000424-g001.png}}
\caption{Structuring a Scientific Project}
\end{figure}

> In parallel with this chronological directory structure, I find it useful to maintain a chronologically organized lab notebook. This is a document that resides in the root of the results directory and that records your progress in detail. Entries in the notebook should be dated, and they should be relatively verbose, with links or embedded images or tables displaying the results of the experiments that you performed.

### Carrying Out a Single Experiment
> record every operation that you perform

> create either a README file, in which I store every command line that I used while performing the experi- ment, or a driver script (I usually call this runall) that carries out the entire exper- iment automatically

> I work in a combination of shell scripts, Python, and C

> Whatever you decide, you should end up with a file that is parallel to the lab notebook entry

> Here are some rules of thumb that I try to follow when developing the driver script:

> 1. Record every operation that you per- form.

> 2. Comment generously.

> 3. Avoid editing intermediate files by hand.

> Many simple editing opera- tions can be performed using standard Unix utilities such as sed, awk, grep, head, tail, sort, cut, and paste.

> 4. Store all file and directory names in this script.

> 5. Use relative pathnames to access other files within the same project.

> 6. Make the script restartable.

> For experiments that take a long time to run, I find it useful to be able to obtain a summary of the experiment’s progress thus far.

### Command Lines versus Scripts versus Programs

> 1. Driver Script

> 2. Single-use Script

> 3. Project-specific script

> 4. Multi-project script.

> Regardless of how general a script is supposed to be, it should have a clearly documented interface.

### The Value of Version Control
> provides a form of backup

> version control provides a historical record that can be useful for tracking down bugs or understanding old results.

> invaluable for collaborative projects

> changes should be checked in at least once a day

> it is possible to check in your changes on a ‘‘branch’’ of the project

> should only be used for files that you edit by hand



```python

```
