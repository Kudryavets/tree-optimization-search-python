import re
import collections
import ast


class Tree:
    def __init__(self, name):
        self.name = name
        self.branch_names = {name}
        self.children = []
        self.items = []

    def add_item(self, question):
        self.items.append(question)

    def grow_tree(self, parsed_tree):
        if parsed_tree:
            child = self.add_child(parsed_tree.pop(0))
            if parsed_tree:
                possible_child = parsed_tree[0]
                if isinstance(possible_child, list):
                    child.extend_branch_names(possible_child)
                    child.grow_tree(possible_child)
                    self.grow_tree(parsed_tree[1:])
                else:
                    self.grow_tree(parsed_tree)

    def add_child(self, name):
        self.branch_names.add(name)
        l = Tree(name)
        self.children.append(l)
        return l

    def extend_branch_names(self, parsed_tree):
        self.branch_names.update(set(flatten(parsed_tree)))

    def traverse(self, name):
        if self.name == name:
            return self
        else:
            return next((child for child in self.children if child.contains_name(name))).traverse(name)

    def contains_name(self, name):
        return name in self.branch_names

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
        name, parsed_children = self.parse_f_tree(flat_tree)
        Tree.__init__(self, name)
        self.grow_tree(parsed_children)

    @staticmethod
    def parse_f_tree(f_tree):
        f_tree = f_tree.rstrip()
        f_tree = re.sub("(?P<word>\w+)", "'\g<word>',", f_tree)
        f_tree = re.sub("\) ", "), ", f_tree)
        f_tree = re.sub("\)", "]", f_tree)
        f_tree = re.sub("\(", "[", f_tree)
        return list(ast.literal_eval(f_tree))

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
