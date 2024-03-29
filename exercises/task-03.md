# **TASK-03** / Extract malware families for CTI

## Context

The CTI team needs to know the families of the malicious samples to retrieve them quickly and analyze them.

## Action

Only malicious samples should be used in this task. We want to easily access, for all the samples, the official name of the families associated to them. 

The list of existing families is stored in `MalwareFamily`. This table gives the official name of each family, and the unofficial aliases they may have.

The families are associated to the samples with the tags of types: `FAMILY`, `FAMILY_FROM_SCRAPER`, `FAMILY_FROM_ANALYSIS`. These tags match a `MalwareFamily` if they **contain** the alias of a malware family.


## Tips

1) You should re-use the maliciousness information about the samples you computed in [**TASK-01**](./task-01.md)
2) This task will require you to identify the best term-matching process of a large number of strings on a large number of categories
