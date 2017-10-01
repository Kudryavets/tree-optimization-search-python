import unittest
from question_tree import QuestionRoot


class TestStringMethods(unittest.TestCase):
    flat_tree = "Animals ( Reptiles Birds ( Eagles Pigeons Crows ) Mammals ( Bears ( Grizzly White ) ) )"

    def test_parse_f_tree(self):
        self.assertEqual(QuestionRoot.parse_f_tree(self.flat_tree),
                         {'Animals': {'Birds': {'Crows': {}, 'Eagles': {}, 'Pigeons': {}},
                                      'Mammals': {'Bears': {'Grizzly': {}, 'White': {}}},
                                      'Reptiles': {}}})

    def test_grow_tree(self):
        tree = QuestionRoot(self.flat_tree)
        self.assertEqual(str(tree), self.flat_tree)

    def test_traverse(self):
        tree = QuestionRoot(self.flat_tree)
        self.assertEqual(str(tree.traverse("Birds")), "Birds ( Eagles Pigeons Crows )")
        self.assertEqual(str(tree.traverse("Bears")), "Bears ( Grizzly White )")

    def test_add_question(self):
        tree = QuestionRoot(self.flat_tree)
        tree.add_question("Bears", "Why bears are so big?")
        tree.add_question("Animals", "How many animals do you know?")
        self.assertEqual(tree.traverse("Bears").items, ["Why bears are so big?"])
        self.assertEqual(tree.items, ["How many animals do you know?"])

    def test_search_question(self):
        tree = QuestionRoot(self.flat_tree)
        tree.add_question("Bears", "Why bears are so big?")
        tree.add_question("White", "Why white bears are so white?")
        tree.add_question("Bears", "If any bear can fly?")
        self.assertEqual(tree.question_count("Bears", "Why"), 2)
        self.assertEqual(tree.question_count("Mammals", "If"), 1)
        self.assertEqual(tree.question_count("White", "Why"), 1)
        self.assertEqual(tree.question_count("Reptiles", "Why"), 0)

    def test_question_tree(self):
        tree = QuestionRoot("Animals ( Reptiles Birds ( Eagles Pigeons Crows ) )")
        tree.add_question("Reptiles", "Why are many reptiles green?")
        tree.add_question("Birds", "How do birds fly?")
        tree.add_question("Eagles", "How endangered are eagles?")
        tree.add_question("Pigeons", "Where in the world are pigeons most densely populated?")
        tree.add_question("Eagles", "Where do most eagles live?")


if __name__ == '__main__':
    unittest.main()

