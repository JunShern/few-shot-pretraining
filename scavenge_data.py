import scavenger

writer = Writer()

for c in [DomainCriterion, RegexStructureCriterion]:
    checker.add_criterion(c)

for doc in reader:
    passing_criteria = checker.check(doc)
    writer.add(doc_id, passing_criteria)