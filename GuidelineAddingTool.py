import tkinter as tk


# Aspirin,T,DB00945,Aspirin,2244,C0004057,GIB,IncreaseRiskGIB,LowRiskGIB,HighRiskGIB,RiskUMLSCODE1, RiskUMLSCODE2
def add_all_values(guideline, action, shouldPursue, isMerged, drugID, drugType, DBid, DBpedia, PubchemCID, DrugUMLS, SideEffect, Transition, PreSituation, PostSituation, PreCode, PostCode):
    # Care actioons and LOD mapping
    careAction = open("CareAction&DrugTypes.ttl", "r")
    if drugID not in careAction.read():
        careAction.close()
        careAction = open("CareAction&DrugTypes.ttl", "a")
        careAction.write(f"\n:ActAdminister{drugID} rdf:type vocab:DrugAdministrationType, owl:NamedIndividual ;\n\t rdfs:label \"Administer {drugID}\"@en ;\n\t vocab:administrationOf :Drug{drugType}{drugID} .\n")
        careAction.write(f"\n:Drug{drugType}{drugID} rdf:type vocab:DrugType, owl:NamedIndividual ;\n\t rdfs:label \"{drugID}\"@en .\n")
        careAction.close()
        lodMap = open("LODmapping.ttl", "a")
        lodMap.write(f"\n:Drug{drugType}{drugID} owl:sameAs drug:{DBid};\n\t owl:sameAs dbpedia:{DBpedia};\n\t vocab:pubchemCID \"{PubchemCID}\"^^xsd:string ;\n\t vocab:umlsCode \"{DrugUMLS}\"^^xsd:string .\n")

    else:
        careAction.close()
        print("Skipping CareAction/LOD additions - Drug found")

    #Causation Beliefs
    CBs = open("CausationBeliefs-Nanopub.trig", "r")
    if f"{drugID}{SideEffect}" not in CBs.read():
        CBs.close()
        CBs = open("CausationBeliefs-Nanopub.trig", "a")
        text = f"""\n##############################################################\n
data:CB{drugID}{SideEffect}_head {{
      \tdata:CB{drugID}{SideEffect}_nanopub
      \t  a                             nanopub:Nanopublication ;
      \t  nanopub:hasAssertion          data:CB{drugID}{SideEffect} ; 
      \t  nanopub:hasProvenance         data:CB{drugID}{SideEffect}_provenance ; 
      \t  nanopub:hasPublicationInfo    data:CB{drugID}{SideEffect}_publicationinfo . 
}}\n

data:CB{drugID}{SideEffect} {{
    \tdata:ActAdminister{drugID}
    \t\t    vocab:causes                  data:Tr{Transition} . 
    \tdata:CB{drugID}{SideEffect}\n
    \t\t    a                             vocab:CausationBelief ; 
    \t\t    vocab:strength                "L1"^^xsd:string; 
    \t\t   vocab:frequency               "always"^^xsd:string. 
}}\n

data:CB{drugID}{SideEffect}_provenance {{ 
    \tdata:CB{drugID}{SideEffect}_provenance
    \t\t    a                             oa:Annotation ;
    \t\t    oa:hasBody                    data:CB{drugID}{SideEffect} ;
    \t\t    oa:hasTarget                  [ oa:hasSource <https://pubmed.ncbi.nlm.nih.gov/22195153/> ] .
    \tdata:CB{drugID}{SideEffect}
    \t\t    prov:wasDerivedFrom           <https://pubmed.ncbi.nlm.nih.gov/22195153/> .\n
}}\n

data:CB{drugID}{SideEffect}_publicationinfo {{
    \tdata:CB{drugID}{SideEffect}_nanopub
        \t\tprov:generatedAtTime          "2015-10-01"^^xsd:dateTime ;
            \t\t\tprov:wasAttributedTo          data:Veruska.
}}"""
        CBs.write(text)
        CBs.close()

    else:
        CBs.close()
        print("Skipping CBs")

    #Transitions
    transitions = open("Transition&SituationTypes.ttl", "r")
    if Transition not in transitions.read():
        transitions.close()
        transitions = open("Transition&SituationTypes.ttl", "a")
        transitions.write(f"\n:Tr{Transition} rdf:type vocab:TransitionType, owl:NamedIndividual ;\n"
                          f"\tvocab:hasTransformableSituation :Sit{PreSituation} ;\n"
                          f"\tvocab:hasExpectedSituation :Sit{PostSituation} .\n")
        if PreCode:
            transitions.write(f"\n:Sit{PreSituation} rdf:type vocab:SituationType, owl:NamedIndividual ;\n"
                          f"\tvocab:umlsCode	\"{PreCode}\"^^xsd:string ;\n"
                          f"\trdfs:label \"Situation is {PreSituation}\"@en .\n")
        else:
            transitions.write(f"\n:Sit{PreSituation} rdf:type vocab:SituationType, owl:NamedIndividual ;\n"
                              f"\trdfs:label \"Situation is {PreSituation}\"@en .\n")

        if PostCode:
            transitions.write(f"\n:Sit{PostSituation} rdf:type vocab:SituationType, owl:NamedIndividual ;\n"
                          f"\tvocab:umlsCode	\"{PostCode}\"^^xsd:string ;\n"
                          f"\trdfs:label \"Situation is {PostSituation}\"@en .\n")
        else:
            transitions.write(f"\n:Sit{PostSituation} rdf:type vocab:SituationType, owl:NamedIndividual ;\n"
                              f"\trdfs:label \"Situation is {PostSituation}\"@en .\n")
        transitions.close()
    else:
        transitions.close()
        print("Skipping transitions as it already exists")

    #Regs and Norms


    guidelineReader = open("MergedReg&Norms-Nanopub.trig", "r") if isMerged else open("Reg&Norms-Nanopub.trig", "r")
    if guideline not in guidelineReader.read():
        guidelineReader.close()
        guidelineReader = open("MergedReg&Norms-Nanopub.trig", "a") if isMerged else open("Reg&Norms-Nanopub.trig", "a")
        guideText = f"\n:CIG-{guideline}\n" \
                    "\trdf:type vocab:ClinicalGuideline ;\n" \
                    f"\trdfs:label \"CIG for {guideline}\"@en .\n"
        guidelineReader.write(guideText)
        guidelineReader.close()
    else:
        print("Guideline Found")
        guidelineReader.close()

    regReader = open("MergedReg&Norms-Nanopub.trig", "r") if isMerged else open("Reg&Norms-Nanopub.trig", "r")

    if f"{guideline}-{action}" not in regReader.read():
        regReader.close()
        regReader = open("MergedReg&Norms-Nanopub.trig", "a") if isMerged else open("Reg&Norms-Nanopub.trig", "a")
        textRec = f"""\n##############################################################\n
:Rec{guideline}-{action}_head {{
    \t:Rec{guideline}-{action}_nanopub
        \t\ta                             nanopub:Nanopublication ;
        \t\tnanopub:hasAssertion          :Rec{guideline}-{action} ;
        \t\tnanopub:hasProvenance         :Rec{guideline}-{action}_provenance ;
            \t\t\tnanopub:hasPublicationInfo    :Rec{guideline}-{action}_publicationinfo .
}}\n

:Rec{guideline}-{action} {{
    \t:Rec{guideline}-{action}
        \t\ta                             vocab:ClinicalRecommendation ;
        \t\trdfs:label "{shouldPursue} {action}"@en ;
        \t\tvocab:strength "{shouldPursue}"^^xsd:string ;
        \t\tvocab:partOf :CIG-{guideline} ;
        \t\tvocab:aboutExecutionOf :ActAdminister{drugID};
        \t\tvocab:basedOn :CB{drugID}{SideEffect} .
}}\n

:Rec{guideline}-{action}_provenance {{
    \t:Rec{guideline}-{action}_provenance
        \t\ta                             oa:Annotation ;
        \t\toa:hasBody                    :Rec{guideline}-{action} ;
        \t\toa:hasTarget                  [ oa:hasSource <http://hdl.handle.net/10222/43703> ] .
    \t:Rec{guideline}-{action}
        \tprov:wasDerivedFrom           <http://hdl.handle.net/10222/43703> .
}}\n

:Rec{guideline}-{action}_publicationinfo {{
    \t:Rec{guideline}-{action}_nanopub
        \t\tprov:generatedAtTime          "2015-10-01"^^xsd:dateTime ;
            \t\t\tprov:wasAttributedTo          :Veruska.
}}"""

        regReader.write(textRec)
    else:
        regReader.close()
        print("Regulation was found")



def main():
    # Aspirin,T,DB00945,Aspirin,2244,C0004057,GIB,IncreaseRiskGIB,LowRiskGIB,HighRiskGIB,RiskUMLSCODE1, RiskUMLSCODE2
    pursue = tk.StringVar()
    var = tk.IntVar()
    drugType = tk.StringVar()
    
    GuidelineLabel = tk.Label(master=window, text="Guideline name (DU)")
    GuidelineLabel.pack()

    GuidelineText = tk.Entry(master=window, text="")
    GuidelineText.pack()

    ActionLabel = tk.Label(master=window, text="Action name (AspirinGIB)")
    ActionLabel.pack()

    ActionText = tk.Entry(master=window, text="")
    ActionText.pack()

    shouldPursueR1 = tk.Radiobutton(window, text="should", variable=pursue, value="should")
    shouldPursueR1.pack()

    shouldPursueR2 = tk.Radiobutton(window, text="should-not", variable=pursue, value="should-not")
    shouldPursueR2.pack()

    labeltype = tk.Label(master=window, text="Is Guideline Merged or Singular?")
    labeltype.pack()

    R1 = tk.Radiobutton(window, text="Singular", variable=var, value=0)
    R1.pack()

    R2 = tk.Radiobutton(window, text="Merged", variable=var, value=1)
    R2.pack()

    labeldrug = tk.Label(master=window, text="Drug name (Aspirin)")
    labeldrug.pack()

    textdrug = tk.Entry(master=window, text="")
    textdrug.pack()


    drugTr = tk.Radiobutton(window, text="T", variable=drugType, value="T")
    drugTr.pack()

    drugTr2 = tk.Radiobutton(window, text="Cat", variable=drugType, value="Cat")
    drugTr2.pack()

    #
    labelDBval = tk.Label(master=window, text="DrugBank ID (DB002424) (see go.drugbank.com/drugs/)")
    labelDBval.pack()

    textDBval = tk.Entry(master=window, text="")
    textDBval.pack()


    labelDBped = tk.Label(master=window, text="DrugBankpedia name (Aspirin) (see dbpedia.org/page/)")
    labelDBped.pack()

    textDBped = tk.Entry(master=window, text="")
    textDBped.pack()

    labelPUBchem = tk.Label(master=window, text="PUBchem id (2424) (see sideeffects.embl.de/drugs)" )
    labelPUBchem.pack()

    textPUBchem = tk.Entry(master=window, text="")
    textPUBchem.pack()
    
    labelDrugUMLS = tk.Label(master=window, text="Drug UMLS code (C0004057)" )
    labelDrugUMLS.pack()

    textDrugUMLS = tk.Entry(master=window, text="")
    textDrugUMLS.pack()

    labelSE = tk.Label(master=window, text="Drug Side Effect (GIB)")
    labelSE.pack()

    textSE = tk.Entry(master=window, text="")
    textSE.pack()

    labelSEtrans = tk.Label(master=window, text="Drug Side Effect causes transition (IncreaseRiskGIB)")
    labelSEtrans.pack()

    textSEtrans = tk.Entry(master=window, text="")
    textSEtrans.pack()

    labelPreSit = tk.Label(master=window, text="Pre-situation (LowRiskGIB)")
    labelPreSit.pack()

    textPreSit = tk.Entry(master=window, text="")
    textPreSit.pack()

    labelPostSit = tk.Label(master=window, text="Post-situation (HighRiskGIB)")
    labelPostSit.pack()

    textPostSit = tk.Entry(master=window, text="")
    textPostSit.pack()

    labelPreSitCode = tk.Label(master=window, text="Pre-situation Code (C0020538)")
    labelPreSitCode.pack()

    textPreSitCode = tk.Entry(master=window, text="")
    textPreSitCode.pack()

    labelPostSitCode = tk.Label(master=window, text="Post-situation Code (C0020538)")
    labelPostSitCode.pack()

    textPostSitCode = tk.Entry(master=window, text="")
    textPostSitCode.pack()

    def read_and_add():
        
        add_all_values(guideline=GuidelineText.get(), action=ActionText.get(), shouldPursue=pursue.get(), isMerged=var.get(), drugID=textdrug.get(), drugType=drugType.get(),
                       DBid=textDBval.get(), DBpedia=textDBped.get(), PubchemCID=textPUBchem.get(), DrugUMLS=textDrugUMLS.get(), SideEffect=textSE.get(), Transition=textSEtrans.get(),
                       PreSituation=textPreSit.get(), PostSituation=textPostSit.get(), PreCode=textPreSitCode.get(), PostCode=textPostSitCode.get())




    def destroy():
        window.destroy()

    button = tk.Button(master=window, text="Add", command=read_and_add)
    button.pack()

    button = tk.Button(master=window, text="Close", command=destroy)
    button.pack()

    window.mainloop()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Helper Tool: Add Guideline")
    main()
