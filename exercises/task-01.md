# **TASK-01** / Identify sample maliciousness

## Context

It is crucial for the AI and CTI teams to know if a sample is a malware or not.

## Action

Each sample is analyzed by different analyzers. The results of the analyses are recorded in the table `Analysis`

⚠️ The same analyzer might have analyzed the same sample multiple times. In this case, we only consider the analysis with the latest version of the analyzer made on the sample.

ℹ️ The reliable automatic analyzers are `AUTO_A`, `AUTO_B`, `AUTO_C`, `AUTO_D`, `AUTO_E` and `AUTO_F`.

A sample:
- is a malware if the analysis made by an automatic analyzer on the sample found it as `is_malware`
- is a goodware if all three automatic analyzers analyzed the sample and none of them found it as `is_malware`
- maliciousness cannot be decided if the sample does not fulfill the malware nor goodware conditions


## Tips
