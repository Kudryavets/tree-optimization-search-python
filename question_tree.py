import re
import collections
import json


class Tree:
    def __init__(self, name, json_tree):
        self.name = name
        self.children = [Tree(child_name, child_json) for child_name, child_json in json_tree.items()]
        self.all_children_names = {name}
        self.extract_all_names(json_tree)
        self.items = []

    def extract_all_names(self, json_tree):
        self.all_children_names.update(json_tree.keys())
        [self.extract_all_names(value) for value in json_tree.values()]

    def add_item(self, question):
        self.items.append(question)

    def traverse(self, name):
        if self.name == name:
            return self
        else:
            return next((child for child in self.children if child.contains_name(name))).traverse(name)

    def contains_name(self, name):
        return name in self.all_children_names

    def count_questions(self, pattern):
        return sum([1 for q in self.items if q.startswith(pattern)]) + \
               sum([child.count_questions(pattern) for child in self.children])

    def __repr__(self):
        if self.is_leaf():
            return self.name
        else:
            return "%s ( %s )" % (self.name, " ".join([ child.__repr__() for child in self.children ]))

    def __str__(self):
        return self.__repr__()

    def is_leaf(self):
        return not bool(self.children)


class QuestionRoot(Tree):
    def __init__(self, flat_tree):
        json_tree = self.parse_f_tree(flat_tree)
        name = list(json_tree.keys())[0]
        Tree.__init__(self, name, json_tree[name])

    @staticmethod
    def parse_f_tree(f_tree):
        f_tree = re.sub("(?P<word>\w+)", '"\g<word>"', f_tree)
        f_tree = re.sub('" "', '": {}, "', f_tree)
        f_tree = re.sub('" \)', '": {} )', f_tree)
        f_tree = re.sub(' \(', ': {', f_tree)
        f_tree = re.sub(' \) "', ' }, "', f_tree)
        f_tree = re.sub(' \)', ' }', f_tree)
        return json.loads("{ %s }" % f_tree)

    def add_question(self, name, question):
        if name == self.name:
            Tree.add_item(self, question)
        else:
            self.traverse(name).add_item(question)

    def question_search(self, name, pattern):
        return self.traverse(name).count_questions(pattern)


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
    answer_acc = [ tree.question_search(*input().split(" ", 1)) for i in range(patterns_count) ]

    print("\n".join([str(answ) for answ in answer_acc]))
