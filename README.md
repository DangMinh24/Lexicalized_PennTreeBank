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
    
In First Attempt, try to apply Collins head-rules for NP, and others( I still don't understand clearly enough to apply Collins head-rules for coordinated phrases ). The __head__ function in FirstAttempt is used to do that job, however, still doesn't have ability to apply for productions having rhs is Terminal (Ex: NN -> 'eggs') . That why I created __head__v2


In Second Attempt, you can use nltk.tree.Tree as a standard tree. However, nltk Tree don't have variable for _label. So I think it is be a perfect change for you to pratice to create your own tree for NLP parsing. I use nltk.tree.Tree as my reference for class Tree (especially function __fromstring__) with a little different from the orginal.

Futher Attempt: 

   a/ My function only use for each sentence. Not be able to process with file have a lot of sentences. I will try to interact with file rather than speciffic sentence.

  b/ Binarize and Lexicalized tree are important skills for NLP parsers. I will try to combine Binarize and Lexicalized data before experiment with parsing methods
  
  
