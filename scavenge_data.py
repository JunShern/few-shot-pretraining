from scavenger import PileReader

reader = PileReader("./data")
# for idx, doc in enumerate(reader):
#     print(doc)
#     if idx > 1:
#         break
print(next(reader))

# writer = Writer()

# for c in [DomainCriterion, RegexStructureCriterion]:
#     checker.add_criterion(c)

# for doc in reader:
#     passing_criteria = checker.check(doc)
#     writer.add(doc_id, passing_criteria)