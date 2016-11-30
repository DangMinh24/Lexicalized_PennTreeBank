from FirstAttempt import prod2str,head_NP,head_,collins_rules
#######################################

def __head__v2(grammar_production,head_finding_rules,terminal_list):
    lhs,rhs=prod2str(grammar_production)

    if len(rhs)==1 and rhs[0] in terminal_list:
        return (0,rhs[0])

    for rule in head_finding_rules:
        location, name = head_(grammar_production, rule)
        if location != None and name != None:
            return location, name
    return (None, None)



#########Create a new tree:

import re
from nltk.grammar import Production,Nonterminal

class Leaf(object):
    def __init__(self,label=None):
        if not isinstance(label,str):
            raise TypeError()
        self._label=label
        self._father=None

class Tree(object):
    def __init__(self, node=None, child=None, parent=None):
        if child == None:
            raise TypeError()

        self._label = node

        self._child = child
        self._father = parent
        self._root = False
        self._head=None

    def set_root(self):
        self._root = True

    def set_head(self, head):
        self._head = head

    @classmethod
    def from_string(cls, sent):
        open_b = "("
        close_b = ")"
        open_pattern, close_pattern = (re.escape(open_b), re.escape(close_b))

        node_pattern = "[^%s%s\s]+" % (open_pattern, close_pattern)
        leaf_pattern = "[^%s%s\s]+" % (open_pattern, close_pattern)
        compile = re.compile(r"%s\s*(%s)?|(%s)|%s" % (open_pattern, node_pattern, leaf_pattern, close_pattern))

        stack = [Tree(None, [])]

        for i in compile.finditer(sent):
            token = i.group()
            if token[0] == "(":
                label = token[1:].lstrip()
                tmp_tree = cls(node=label, child=[])
                stack.append(tmp_tree)
            elif token[0] == ")":
                tmp_tree = stack.pop()
                tmp_tree._father = stack[-1]
                stack[-1]._child.append(tmp_tree)
            else:
                label = token
                label_ = Leaf(token)
                stack[-1]._child.append(label_)

        tree = stack[0]._child[0]
        tree._father = None
        return tree

    def children_name(self):
        result = []
        for i in self._child:
            result.append(i._label)
        return result

    def first_production(self):
        return Production(Nonterminal(self._label), self.children_name())

    def productions(self):
        prod = []
        prod.append(Production(Nonterminal(self._label), self.children_name()))
        for i in self._child:
            if isinstance(i, Tree):
                prod.extend(i.productions())
        return prod

    def leaves(self):
        leaves = []
        for child in self._child:
            if isinstance(child, Tree):
                leaves.extend(child.leaves())
            else:
                leaves.append(child._label)
        return leaves

    def print(self):
        print("("+str(self._label)+"/"+str(self._head),end=" ")
        for child in self._child:
            if isinstance(child,Tree):
                child.print()
            elif isinstance(child,Leaf):
                print(" "+child._label+")")
############################

# Now we need to find head!!!
# Remind that in FIRST_ATTEMPT, we already know how to create a list of tuple which contains instruction which word is the most important word
# Ex: (S->'NP' 'VP',1,'VP') which mean that S's head will depend on VP's head, 1 is iteration of VP in list of rhs of production

# Now, I create a function that only do each step:
# Using the example above (S->'NP' 'VP',1,'VP'):
# I try to assign S's head = VP's head if VP is Nonterminal/Tree, or S's head= VP if VP is Terminal/Leaf
def find_head_each_node(node,head_rules):
    consider_prod=node.first_production()
    for (prod,loc,name) in head_rules:
        if consider_prod==prod and loc!=None:
            if isinstance(node._child[0],Leaf) and node._head==None:
                node.set_head(node._child[0]._label)
            elif isinstance(node._child[0],Tree) and node._head==None:
                node.set_head(node._child[loc]._head)

# After done with one step, I try to traverse all the tree, each subtree I use the above function
def find_head_all_tree(tree,head_rules):

    for child in tree._child:
        if isinstance(child,Tree):
            find_head_all_tree(child,head_rules)
        elif isinstance(child,Leaf):
            continue
    find_head_each_node(tree,head_rules)

####All done! Now run example to see our result

# This is a standard parsed sentence in Penn Treebank
tmp_sent="""
( (S
    (NP-SBJ (NNP Mr.) (NNP Vinken) )
    (VP (VBZ is)
      (NP-PRD
        (NP (NN chairman) )
        (PP (IN of)
          (NP
            (NP (NNP Elsevier) (NNP N.V.) )
            (, ,)
            (NP (DT the) (NNP Dutch) (VBG publishing) (NN group) )))))
    (. .) ))
"""
# However, the first bracket use for segmentation. I skip it for now, which mean that
# our tmp_sent should be like this:
tmp_sent="""
(S
    (NP-SBJ (NNP Mr.) (NNP Vinken) )
    (VP (VBZ is)
      (NP-PRD
        (NP (NN chairman) )
        (PP (IN of)
          (NP
            (NP (NNP Elsevier) (NNP N.V.) )
            (, ,)
            (NP (DT the) (NNP Dutch) (VBG publishing) (NN group) )))))
    (. .) )
"""
tree=Tree.from_string(tmp_sent)

# The tree should have following format ( label/head <child>) where each child can be another tree
# The function print of Tree just for checking result, I still don't know how to make it easier to see
tree.print()


# To find head-rule for tree, we need a list of tree productions, a head-rules can be founded by collins rules

productions=tree.productions()
headrules=[]
for prod in productions:
    lhs,rhs =prod2str(prod)
    if lhs=="NP" or "NP-"in lhs:
        loc,head=head_NP(prod)
    else:
        loc,head=__head__v2(prod,collins_rules,tree.leaves())
    headrules.append((prod,loc,head))

print()
for i in headrules:
    print(i)

find_head_all_tree(tree,headrules)

print()
tree.print()

# We can compare tree before finding head and after finding head