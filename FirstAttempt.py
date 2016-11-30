filename="Collins English rule.txt"
file=open(filename)

from nltk import Production,Nonterminal

def preprocess_line(line):
    tmp=line.split("\t")
    return (tmp[0],tmp[2],tmp[-1].strip().split(" "))

def file2rule(file_name):
    file=open(file_name)
    rules=[]
    first_line=file.readline()

    while first_line:
        if first_line=="\t" or first_line=="\n" :
            continue
        rules.append(preprocess_line(first_line))
        first_line=file.readline()

    return rules

collins_rules=file2rule(filename)

from nltk.corpus import treebank

def prod2str(production):
    lhs=production.lhs().symbol()
    # if isinstance(lhs,Nonterminal):
    #     lhs
    rhs_non=production.rhs()
    rhs=[]
    for i in list(rhs_non):
        rhs.append(str(i))
    return lhs,rhs

sub_parsed_corpus=treebank.parsed_sents()[:100]

# First attempt: try to finding most important word ( called head) in list of children according to one specific head-finding rule
# (Will try to expand later with list of head-finding rules)
def head_(grammar_production,head_finding_rule):
    lhs,rhs=prod2str(grammar_production)

    # Check if this rule is appropriate for grammar
    if lhs!=head_finding_rule[0]:
        return (None,None)

    if head_finding_rule[1]=="l":
        for j in head_finding_rule[2]:
            for iter,i in enumerate(rhs):
                if i==j:
                    return (iter,j)
                    # break
    if head_finding_rule[1]=="r":
        for j in head_finding_rule[2]:
            for iter,i in enumerate(reversed(rhs)):
                if i==j:
                    return (len(rhs)-1-iter,j)
                    # break
    return (None,None)
#Expand head_ function: try find most important word with list of head-finding rules
def __head__(grammar_production,head_finding_rules):
    lhs,rhs=prod2str(grammar_production)

    for rule in head_finding_rules:
        location,name=head_(grammar_production,rule)
        if location!=None and name!=None:
            return location,name
    return (None,None)

# However, __head__ function only working with list of collins rules in file.
# There are some special cases: 1/NP 2/Coordinate Phrase
def head_NP(grammar_production):
    lhs,rhs=prod2str(grammar_production)

    # if lhs not in ["NP","NP-SBJ","NP-PRD","NP-1","NP-SBJ-1","NP-SBJ-4",
    #                "NP-LGS","NP-SBJ-6","NP-SBJ-7","NP-TMP",]:
    #     return None
    if lhs!="NP" and "NP-" not in lhs:
        return None,None

    if rhs[-1]=="POS":
        return len(rhs)-1,rhs[-1]
    else:
        find_flag=False

        for iter,i in enumerate(reversed(rhs)):
            if find_flag == True:
                break
            if i in ["NN","NNPS","NNP","NNS","NX","POS","JJR"]:
                find_flag=True
                return len(rhs)-1-iter,i

        for iter,i in enumerate(rhs):
            if find_flag == True:
                break
            if i == "NP":
                find_flag=True
                return iter,i

        for iter,i in enumerate(reversed(rhs)):
            if find_flag==True:
                break
            if i in ["$","ADJP","PRN"]:
                find_flag=True
                return len(rhs)-1-iter,i

        for iter,i in enumerate(reversed(rhs)):
            if find_flag == True:
                break
            if i =="CD" :
                find_flag=True
                return len(rhs)-1-iter,i

        for iter,i in enumerate(reversed(rhs)):
            if find_flag==True:
                break
            if i in ["JJ","JJS","RB","QP"] :
                find_flag=True
                return len(rhs)-1-iter,i

        if find_flag==False:
            return len(rhs)-1,rhs[-1]


result=[]
for sent in sub_parsed_corpus:
    for prod in sent.productions():
        lhs,rhs= prod2str(prod)
        if lhs=="NP" or "NP-" in lhs:
            loc,head=head_NP(prod)
        else:
            loc,head=__head__(prod,collins_rules)
        result.append((prod,loc,head))

# for a,b,c in result:
#     print(a,end=" \\")
#     print("location :",b,end=" ")
#     print("head_name :",c)


