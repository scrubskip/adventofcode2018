#!/usr/bin/env python
#

from parse import compile
import string


def main():
    step_lines = open("day7input.txt", "r")

    nodes = parse_lines(step_lines.readlines())

    print get_sequence(nodes)


def parse_lines(lines):
    p = compile(
        "Step {prereq} must be finished before step {label} can begin.")
    nodes = {}
    for line in lines:
        data = p.parse(line)
        if (data is not None):
            label = data['label']
            prereq = data['prereq']

            if (label in nodes):
                node = nodes[label]
            else:
                node = Node(label)
                nodes[label] = node

            if (prereq not in nodes):
                prereq_node = Node(prereq)
                nodes[prereq] = prereq_node

            node.add_prereq(prereq)

    return nodes


def find_root(nodes):
    root_list = filter(lambda x: not x.has_prereqs(),
                  map(nodes.get, nodes))
    root_list.sort(key = (lambda x: x.label))
    return root_list[0] if len(root_list) > 0 else None

def get_sequence(nodes):
    return_list = []
    while (len(nodes) > 0):
        root = find_root(nodes)
        if (root is None):
            break
        
        # Now remove the root as prereqs
        for node in nodes:
            nodes[node].remove_prereq(root.label)
        
        return_list.append(root.label)
        nodes.pop(root.label)

    return ''.join(return_list)

class Node:

    def __init__(self, label):
        self.label = label
        self.prereqs = []

    def add_prereq(self, prereq_label):
        self.prereqs.append(prereq_label)

    def remove_prereq(self, prereq_label):
        # print "Removing {0} from {1}".format(prereq_label, self.label)
        if (prereq_label in self.prereqs):
            self.prereqs.remove(prereq_label)

    def has_prereqs(self):
        return len(self.prereqs) > 0

    def has_prereq(self, prereq):
        return prereq in self.prereqs

class Worker:
    def __init__(self):
        self.current_job = None
        self.current_time = 0
        self.start_time = -1
        self.completed_job = None

    def start_job(self, label):
        self.start_time = self.current_time
        self.end_time = self.current_time + (61 + string.ascii_uppercase.index(label))
        self.current_job = label

    def do_work(self):
        self.current_time += 1
        if (self.current_job):
            if (self.current_time >= self.end_time):
                self.completed_job = self.current_job
                self.start_time = -1
                self.current_job = None

    def is_working(self):
        return self.current_job is not None


if __name__ == '__main__':
    main()
