# Instance Creator POC
This is a proof-of-concept helper tool for the creation of CIG instances within the TMR model.
As a POC it is not meant to be used as a go-to solution for creating new instances within the TMR model, but as a demonstration of its possibility.

For ease-of-use the TKinter library is used to create a window from which a new guideline and all its dependencies are added.

## General instructions:
To run the code one should run the python file: "GuidelineAddingTool.py".

The values between point 6-10 and 15-16 are not mandatory but they do help with connecting the drugs used with external sources.
The helper tool requires a few bits of information to properly function:
1.  Guideline name - The name of the guideline in which the rest of the data is used
2.  Causation Belief name - The name of the belief relating to the drug used (i.e. AspirinPain)
3.  Should or should not pursue drug?
4.  Is this guideline merged? - This is only to separate the combined guidelines from the singular guidelines
5.  Drug name
6.  Is this drug a category of drugs or a singular drug? - An example: NSAID is a drug category which Aspirin belongs to
7.  DrugBankID - The id of the specific drug can be found on go.drugbank.com/drugs/
8.  DrugBankpedia name - The name of the drug as classified by dbpedia.org/page/
9.  PUBchem id - The id of the drug w.r.t. the SIDER side effect database sideeffects.embl.de/drugs
10.  Drug UMLS code - can be found within the sider database
11.  Drug Side Effect - The name of the side effect (i.e. Pain)
12.  Drug Side Effect causes transition - What transition does this drug-side effect combination cause? (i.e. Heal pain)
13.  Pre-situation - the situation before the drug (i.e. HasPain)
14.  Post-situation - the situation after the drug (i.e. NoPain)
15.  Pre-situation Code - can be found within the sider database
16.  Post-sitution Code - can be found within the sider database


Below are two examples of new instances being added. Both of the instances belong within the same Guideline, but are reffering to two different drugs which cause opposite transitions.

![alt text](https://github.com/jgrguric96/instance_creator_POC/blob/main/images/Example_drug_1.png?raw=true) ![alt text](https://github.com/jgrguric96/instance_creator_POC/blob/main/images/Example_drug_2.png?raw=true)
