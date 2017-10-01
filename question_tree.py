import re
import collections
import json


class Tree:
    """
    The base class for optimizing search via trees.

    It represents one node (topic) and contains all items (questions) which are belong to this particular node.
    It also contains links to all it's children as well as information (names) about all children in the branch.
    Several methods to traverse tree, count items matching a pattern, and represent branch are implemented in the class.
    """

    def __init__(self, name, json_tree):
        """
        Creates a new node.
        :param name: str. Topic name.
        :param json_tree: json parsed to python dict. Represents children in current branch.
        """
        self.name = name
        self.children = [Tree(child_name, child_json) for child_name, child_json in json_tree.items()]
        self.all_children_names = {name}
        self.extract_all_names(json_tree)
        self.items = []

    def extract_all_names(self, json_tree):
        """
        Recursively extracts child names.
        :param json_tree: json parsed to python dict. Represents childs in current branch.
        """
        self.all_children_names.update(json_tree.keys())
        [self.extract_all_names(value) for value in json_tree.values()]

    def add_item(self, question):
        self.items.append(question)

    def traverse(self, name):
        """
        Traverses a tree.
        Recursively checks if current node is target one. If it is not, checks which of it's
        children contains branch with target node.
        :param name: str. target node name.
        :return: target node.
        """
        if self.name == name:
            return self
        else:
            return next((child for child in self.children if child.branch_contains_child(name))).traverse(name)

    def branch_contains_child(self, name):
        return name in self.all_children_names

    def count_items(self, pattern):
        """
        Recursively counts items matching for the pattern.
        :param pattern: str. Beginning of the item (question).
        :return: int. Number of items in the branch which match for the pattern.
        """
        return sum([1 for q in self.items if q.startswith(pattern)]) + \
               sum([child.count_items(pattern) for child in self.children])

    def __repr__(self):
        # String representation of the current branch
        if self.is_leaf():
            return self.name
        else:
            return "%s ( %s )" % (self.name, " ".join([ child.__repr__() for child in self.children ]))

    def __str__(self):
        return self.__repr__()

    def is_leaf(self):
        return not bool(self.children)


class QuestionRoot(Tree):
    """
    The class provides tree functionality for the solving question search optimization problem.
    Methods for building tree and counting questions are implemented here.
    """

    def __init__(self, flat_tree):
        """
        Builds a tree from it's flat string representation.
        :param flat_tree: str. Like "Animals ( Reptiles Birds ( Eagles Pigeons Crows ) )".
        """
        json_tree = self.parse_f_tree(flat_tree)
        name = list(json_tree.keys())[0]
        Tree.__init__(self, name, json_tree[name])

    @staticmethod
    def parse_f_tree(f_tree):
        # Coerces flat string representation of the tree to json and parses it via json library.
        f_tree = re.sub("(?P<word>\w+)", '"\g<word>"', f_tree)
        f_tree = re.sub('" "', '": {}, "', f_tree)
        f_tree = re.sub('" \)', '": {} )', f_tree)
        f_tree = re.sub(' \(', ': {', f_tree)
        f_tree = re.sub(' \) "', ' }, "', f_tree)
        f_tree = re.sub(' \)', ' }', f_tree)
        return json.loads("{ %s }" % f_tree)

    def add_question(self, name, question):
        # entry point for adding a question to this tree
        self.traverse(name).add_item(question)

    def question_count(self, name, pattern):
        # entry point for counting questions matching a pattern.
        return self.traverse(name).count_items(pattern)


def flatten(l):
    # coerces nested iterable to a flat one.
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el


if __name__ == "__main__":
    # Script for submission

    count_categories = input()

    flat_tree = input()
    tree = QuestionRoot(flat_tree)

    questions_count = int(input())
    [tree.add_question(*input().split(": ", 1)) for i in range(questions_count)]

    patterns_count = int(input())
    answer_acc = [tree.question_count(*input().split(" ", 1)) for i in range(patterns_count)]

    print("\n".join([str(answ) for answ in answer_acc]))
