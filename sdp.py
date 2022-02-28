import scispacy
import spacy
from spacy import displacy
from nltk import Tree
from IPython.core.display import display, HTML
import re

nlp = spacy.load("en_core_sci_sm")
# text=u'Convulsions that occur after DTaP are caused by a fever, and fever may cause headache.'
# text='Paul Allen started a company and named Vern Raburn its President.'
# text2='The company to be called Paul Allen Group will be based in Bellevue Washington. '


# text1="The ocular myasthenia associated with combination therapy of IFN and ribavirin for CHC is very rarely reported; therefore, we present this case with a review of the various eye complications of IFN therapy."
#
# text2="Ophthalmologic examinations showed ptosis on the right upper lid and restricted right eye movement without any other neurological signs."
# text='To determine mitochondrial events from HAART in vivo, 8-week-old hemizygous transgenic @Disease@ mice (NL4-3Delta gag/pol; TG) and wild-type FVB/n littermates were treated with the HAART combination of @OTHER_C@, @Chemical@, and @OTHER_C@ or vehicle control for 10 days or 35 days.'
# (4,7,6,8)
# ('ribavirin', 'ocular myasthenia')
# def get_tokens(text):
#    doc = nlp(text)
#    token_list=[]
#    dep_list=[]
#    for token in doc:
#        token_list.append(token)
#        dep_list.append(token.dep_)
#    return token_list,dep_list
#
#
# token_list1,dep_list1=get_tokens(text1)
# token_list2,dep_list2=get_tokens(text2)

import networkx as nx


def get_parsed(text, a):
    # MERGING THE MULTI ENTITIES
    doc = nlp(text)
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(doc[ent.start:ent.end])

    edges = []
    for token in doc:
        for child in token.children:
            edges.append(('{0}'.format(token.lower_), '{0}'.format(child.lower_)))

    graph = nx.Graph(edges)  # Get the length and path

    tok = []
    dep = []
    for token in doc:
        tok.append(token)
        dep.append(token.dep_)
    # entity1 = '@Chemical@'
    # entity2 = '@Disease@'

    for i, t in enumerate(dep):
        if t == 'ROOT':
            term = tok[i]
    print(term)
    entity1 = a
    entity2 = str(term)
    e1 = entity1.split()[0]
    e2 = entity2.split()[0]
    #
    # print('???',e1,e2)
    entity1 = e1
    entity2 = e2

    #    print(entity1,entity2)
    # e1=entity1.split()
    # e2=entity2.split()

    for token in tok:

        if entity1 in str(token):
            entity1 = str(token).lower()

        if entity2 in str(token):
            entity2 = str(token).lower()

        #    print('##',entity1,entity2)
    try:
        n = nx.shortest_path_length(graph, source=entity1, target=entity2)

        m = nx.shortest_path(graph, source=entity1, target=entity2)
        m = [re.sub(r'[\.]', '', x) for x in m]
    #        print(m)
    except Exception:
        #        print('Caught this error: ' + repr(error))
        # print(label,text)
        return 100000, ['nil'], 'nil', entity1, entity2
    deps1 = []

    r = []

    for token in doc:
        # print((token.head.text, token.text, token.dep_))
        dep_rel = (token.head.text.lower(), token.text.lower(), token.dep_.lower())
        dep_rel1 = (re.sub(r'[\.]', '', dep_rel[0]), re.sub(r'[\.]', '', dep_rel[1]), dep_rel[2])

        for i, item in enumerate(m):
            if i < len(m) - 1:
                if m[i] in dep_rel1:
                    if m[i + 1] in dep_rel1:
                        #                        print(dep_rel1)
                        j = (m[i], m[i + 1])

                        # print(m[i],m[i+1],dep_rel1[-1])
                        if j not in r:
                            deps1.append(dep_rel1[-1])
                            r.append(j)

    #    print(deps1)
    if len(deps1) > 0:
        g = []
        s = ''

        for k, item in enumerate(m):
            if k != len(m) - 1:
                g.append(item)
                s += item + '--' + deps1[k] + '-->'
            else:
                g.append(item)
                s += item

        s1 = []
        for k, item in enumerate(m):
            if k == 0:
                s1.append(['start' + ' ' + item + ' ' + deps1[k]])
            elif k != len(m) - 1:
                s1.append([deps1[k - 1] + ' ' + item + ' ' + deps1[k]])
            else:
                s1.append([deps1[k - 1] + ' ' + item + ' ' + 'end'])

    else:
        s = m[0]
        s1 = [m]

    return n, m, s1, entity1, entity2


def sdp(text, entity):
    doc = nlp(text)
    #    print(entity)
    #    print(text)
    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(doc[ent.start:ent.end])

    edges = []
    for token in doc:
        for child in token.children:
            edges.append(('{0}'.format(token.lower_), '{0}'.format(child.lower_)))

    graph = nx.Graph(edges)  # Get the length and path

    entity1 = str(entity[0])
    entity2 = str(entity[1])

    e1 = entity1.split()[0]
    e2 = entity2.split()[0]

    entity1 = e1
    entity2 = e2

    token_list = []
    dep_list = []
    for token in doc:
        token_list.append(token)
        dep_list.append(token.dep_)
    for i, j in enumerate(dep_list):
        if j == 'ROOT':
            predicate = str(token_list[i])

    for token in token_list:

        if entity1 in str(token):
            entity1 = str(token).lower()

        if entity2 in str(token):
            entity2 = str(token).lower()

    triple = [entity1, predicate, entity2]

    try:
        n = nx.shortest_path_length(graph, source=entity1, target=entity2)
        #        print(n)
        m = nx.shortest_path(graph, source=entity1, target=entity2)
        m = [re.sub(r'[\.]', '', x) for x in m]
    #        print(m)
    #        print('success:',entity)
    #    except:
    #        pass
    #        try:
    #            n=nx.shortest_path_length(graph, source=entity2, target=entity1)
    #            m=nx.shortest_path(graph, source=entity2, target=entity1)
    #            m=[re.sub(r'[\.]','',x) for x in m]
    ##            print('success:',entity)

    except Exception:
        #        print('Caught this error: ', (entity1,entity2))
        #        print(text)
        # print(label,text)
        return -1, ['nil'], 'nil', entity1, entity2, predicate

    #    for token in doc:
    #        dep_rel=(token.head.text.lower(), token.text.lower(), token.dep_.lower())
    #        print((re.sub(r'[\.]','',dep_rel[0]),re.sub(r'[\.]','',dep_rel[1]),dep_rel[2]))

    deps1 = []

    r = []

    for token in doc:
        # print((token.head.text, token.text, token.dep_))
        dep_rel = (token.head.text.lower(), token.text.lower(), token.dep_.lower())
        dep_rel1 = (re.sub(r'[\.]', '', dep_rel[0]), re.sub(r'[\.]', '', dep_rel[1]), dep_rel[2])

        for i, item in enumerate(m):
            if i < len(m) - 1:
                if m[i] in dep_rel1:
                    if m[i + 1] in dep_rel1:
                        #                        print(dep_rel1)
                        j = (m[i], m[i + 1])

                        # print(m[i],m[i+1],dep_rel1[-1])
                        if j not in r:
                            deps1.append(dep_rel1[-1])
                            r.append(j)

    #    print(deps1)
    if len(deps1) > 0:

        s = ''

        for k, item in enumerate(m):
            if k != len(m) - 1:
                s += item + '--' + deps1[k] + '-->'
            else:
                s += item

        s1 = []
        for k, item in enumerate(m):
            if k == 0:
                s1.append(['start' + ' ' + item + ' ' + deps1[k]])
            elif k != len(m) - 1:
                s1.append([deps1[k - 1] + ' ' + item + ' ' + deps1[k]])
            else:
                s1.append([deps1[k - 1] + ' ' + item + ' ' + 'end'])

    else:
        s = m[0]
        s1 = [m]
    #    print('triple',triple)
    return n, m, s1, entity1, entity2, predicate

text = r"Type 2 diabetes is an increasingly common, serious metabolic disorder\
 with a substantial inherited component. It is characterised by defects in both\
  insulin secretion and action. Progress in identification of specific genetic \
  variants predisposing to the disease has been limited. To complement ongoing \
  positional cloning efforts, we have undertaken a large-scale candidate gene \
  association study. We examined 152 SNPs in 71 candidate genes for association \
  with diabetes status and related phenotypes in 2,134 Caucasians in a case-control \
  study and an independent quantitative trait (QT) cohort in the United Kingdom. \
  Polymorphisms in five of 15 genes (33%) encoding molecules known to primarily \
  influence pancreatic \u03b2-cell function\u2014 ABCC8 (sulphonylurea receptor), \
  KCNJ11 (KIR6.2), SLC2A2 (GLUT2), HNF4A (HNF4\u03b1), and INS (insulin)\u2014significantly \
  altered disease risk, and in three genes, the risk allele, haplotype, or both had a biologically \
  consistent effect on a relevant physiological trait in the QT study. We examined 35 genes predicted \
  to have their major influence on insulin action, and three (9%)\u2014 INSR , PIK3R1 , and \
  SOS1 \u2014showed significant associations with diabetes. These results confirm the genetic \
  complexity of Type 2 diabetes and provide evidence that common variants in genes influencing \
  pancreatic \u03b2-cell function may make a significant contribution to the inherited component \
  of this disease. This study additionally demonstrates that the systematic examination of panels \
  of biological candidate genes in large, well-characterised populations can be an effective complement \
  to positional cloning approaches. The absence of large single-gene effects and the detection of multiple \
  small effects accentuate the need for the study of larger populations in order to reliably identify the size \
  of effect we now expect for complex diseases. The absence of large single gene effects and the detection of \
  multiple small effects confirms the genetic complexity of type 2 diabetes and the need for even larger studies".replace(r"\u2014", r"-")
a = "INS"
n,m,s,e1,e2,p = sdp(text,["INS","INSR"])
n_,m_,s_,e1_,p_ = get_parsed(text, a)
print("n is {0}, m is {1}, s is {2}, e1 is {3}, e2 is {4}, p is {5}".format(n,m,s,e1,e2,p))
print("n is {0}, m is {1}, s is {2}, e1 is {3}, p is {4}".format(n_,m_,s_,e1_,p_))