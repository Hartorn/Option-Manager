This code test arises from a practical idea, that can be summarized as follows.

You have an application for renting cars. One of the steps in the process is choosing the color, extras, etc. you want. Some options required some other option to be included. For example, you can't have the GPS system if you dont also have a USB plug. (But you can have the U5B without having the GPS system.) So, when the user clicks on the GPS checkbox, the USB checkbox is automatically checked, and if the USB checkbox is unchecked, the US checkbox gets unchecked too.

Now, say you have another system that uses the U5B plug, for example a music device or whatever. The USB plug is unique, so you cant have both the GPS and the music thing. When the user checks the GPS checkbox,the music checkbox is disabled, and the other way around. 

# Rule Sets

Let's say we  set of optons which the user can select. Options can be related between them in two ways: one can depend on another, and two options can be mutually exclusive. That means that these equalities must always hold true (note: this is not code,those are logical equations): 
- "A depends on B", or "for A to be selected, B needs to be selected"
ruleSet.addDep(A, B) =>
if isSelected(A) than isSelected(B) 
- "A and B are exclusive" or "B and A are exclusive" or "for A to be selected, B needs to be unselected"; and for B to be selected. A needs to be unselected."
ruleset.addConflict(A, B) <=> ruleSet.add[ontlict(B. A) =>
if isSelected(A) then !isselected(B) && if isselected(B) then !isselected(A) 


We say that a set of relations are coherent if the laws above are valid for that set. For example, this set of relations is coherent: 
addDep(A,B) // "A depends de B"
addDep(B,C) // "B depends de C"
addContlict(C, D) // "C and D are exclusive" 

And these sets are not coherent :
addDep(A,B)
addContlict(B,C)

A depends on B, so it's a contradiction that they are exclusive. If A is selected, then B would need to be selected, but that's impossible because, by the exclusion rule, both can't selected at the same time.
addDep(A,B)
addDep(B,C)
addContlict(C, D)

The dependency relation is transitive; it's easy to see, from the rules above, that if A depends on B, and B depends on C, then A also depends on C. So this is a contradiction for the same reason as the previous case.

# Questions 

## A.
Write a data structum (RuleSet) for expressing these rules betweem options, ie. for defining a rule set. You also need to define a constructor and 2 methods :
- NewRuleSet(): Returns an empty rule set.
- RuleSet.addDep(A,B): a method for rule sets that adds a new dependency A.
- RuleSet.addConflict(A,B): a method for rule sets that adds a new conflict between A and B.

## B.
Implement the algorithm that checks that an instance of that data structure is coherent, that is, that no option can depend, directly or indirectly, on another option and also mutually exclusive with it.

- RuleSet.isCoherent(): a method for rule sets that returns true if it is a coherent rule set, false otherwise.

## C.
Implement the algontim that, given the rules between options, an option, and a collection of selected options coherent with the rules, adds the option to a collection of selected options, or removes it from the collection if it is already there, selecting and deselecting options automatically based on dependencies and exclusions. 
- New(rs): returns a new (empty) collection of selected options (Opts)for the rule set rs. 
- Opts.toggle(o): a method for a collection of selected options, to set or unset option o. 
- Opts.stringSlice(): returns a slice of string with the current list of selected options.

The algorithm for when a checkbox is selected is asked to you in section C, based on the data structures you define in section A. In section B you should provide an algorithm that 'tests' that sections A and C give a good solution.

## Evaluation

We encourage you to take all the time allowed to write a code you are proud of.