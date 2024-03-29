# **TASK-02** / Create AI datasets

## Context

The AI team needs to build an algorithm to detect malicious executable files on windows. To build it, they need a dataset containing malicious and non-malicious files divided into two subsets, one used for training and the other for testing the algorithm.


## Action


Only samples with a magic containing `PE32` should be in this dataset. For each sample, we should know:
- it's sha256
- if it is malicious or not
- if it's a sample to use for training or testing


## Tips

1) You should re-use the maliciousness information about the samples you computed in [**TASK-01**](./task-01.md)