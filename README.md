# Lexicalized_PennTreeBank


PCFG (Probabilistic Context-Free Grammars) is an extremely useful concept for CFG parsing. Using PCFG, we can deal with ambigious problem which is very common with phrase parsing task.

However, PCFG has some weakness that why people have to lexicalized PCFG before parsing.

This is a very useful paper for Lexicalized PCFG by Michael Collins: http://www.cs.columbia.edu/~mcollins/courses/nlp2011/notes/lexpcfgs.pdf

He explained very clearly about weakness of PCFG, and also showed how to lexicalize PCFG in practice (www.cs.columbia.edu/~mcollins/papers/thesis.ps (Appendix A part))

According to his thesis, we can lexicalize a standard Treebank (in this code, I will try to use PennTreebank in nltk) with head-finding rules in Table A.1 in Appendix A. Besides, there are some special cases, like NPs, Coordinated Phrases,... which are more complex than rules in the table. However, author also showed pseudocode for these cases.

Note: The main attempt of this project is to examine and understand the idea behind of lexicalizing treebank.

1/First attempt will be:

  -Input: productions. Ex: S->NP VP
  
  -Output: location and head. Ex: (1,VP) because VP is head of S
  

2/Second attempt: 

Try to rebuild a parsed Tree with lexicalized feature
  
  -Input: parsed tree. Ex: 
  
    (S
      (NP (NN I))
      (VP (VB hit)
          (NP (DT a) (NN ball))
      )
      (. .)
    )
  
  
  -Output: lexicalized tree. Ex:
    
    (S(hit)
      (NP(I) (NN(I) I))
      (VP(hit) (VB(hit) hit)
               (NP(ball) (DT(a) a) (NN(ball) ball) )
      )
      (.(.) .)
    )
