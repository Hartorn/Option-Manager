from dataclasses import dataclass, field

# Python code​​​​​​‌​‌​​‌​‌​​​​​‌​‌​‌​‌‌‌​​​ below
@dataclass
class OGraph:
    # start = None
    dict_node: dict = field(init=False, repr=True, default_factory=dict)

    def add_dependencies(self, A, B):
        """
        Check if the node is not already in the list node.
        Add a dependencies in the list dependencies of the node A.

        Arguments:
            A : one node.
            B : one node.
        """
        if A not in self.dict_node:
            self.dict_node[A] = Node(A)
        if B not in self.dict_node:
            self.dict_node[B] = Node(B)
        self.dict_node[A].dependencies.append(self.dict_node[B])
        self.dict_node[B].dependents.append(self.dict_node[A])

    def add_conflict(self, A, B):
        """
        Check if the node is not already in the list node.
        Add a conflict in the list conflicts of the node A and B.

        Arguments:
            A : one node.
            B : one node.
        """
        if A not in self.dict_node:
            self.dict_node[A] = Node(A)
        if B not in self.dict_node:
            self.dict_node[B] = Node(B)
        self.dict_node[A].conflicts.append(self.dict_node[B])
        self.dict_node[B].conflicts.append(self.dict_node[A])

    def dfs_dependencies(self, start: "Node", visited=None):
        """Depth First Search for dependencies.

        Arguments:
            start : The started node.
            visited : The list of visited Nodes. None if it is empty.

        Returns:
            The list of visited Nodes.
        """
        if visited is None:
            visited = []
        visited.append(start)

        for node in start.dependencies:
            if node not in visited:
                self.dfs_dependencies(node, visited)

        return visited

    def dfs_dependents(self, start: "Node", visited=None):
        """Depth First Search for dependencies.

        Arguments:
            start : The started node.
            visited : The list of visited Nodes. None if it is empty.

        Returns:
            The list of visited Nodes.
        """
        if visited is None:
            visited = []
        visited.append(start)

        for node in start.dependents:
            if node not in visited:
                self.dfs_dependents(node, visited)

        return visited


@dataclass
class Node:
    name: str
    dependencies: list = field(init=False, repr=True, default_factory=list)
    dependents: list = field(init=False, repr=True, default_factory=list)
    conflicts: list = field(init=False, repr=True, default_factory=list)


@dataclass
class RuleSet:
    o_graph: OGraph = field(init=False, repr=True, default_factory=OGraph)

    def get_option(self, option):
        return self.o_graph.dict_node[option]

    def NewRuleSet(self):
        """
        Create a new rule set with an empty graph.
        """
        self.o_graph = OGraph()
        return self

    def addDep(self, A: str, B: str):
        """
        Add a dependencies in the graph and in the list dependencies of the node A.

        Arguments:
            A : one node.
            B : one node.
        """
        self.o_graph.add_dependencies(A, B)

    def addConflict(self, A: str, B: str):
        """
        Add a conflict in the graph and in the list conflicts of the node A and B.

        Arguments:
            A : one node.
            B : one node.
        """
        self.o_graph.add_conflict(A, B)

    def getDep(self, A):
        return self.o_graph.dict_node[A.name].dependencies

    def getConf(self, A):
        return self.o_graph.dict_node[A.name].conflicts

    def isCoherent(self):
        """
        Check if the graph is coherent. If all the dependencies are respected.
        If there is no conflict between option.

        Returns:
            A boolean if is coherent or not.
        """
        checked = []
        for node_name, node in self.o_graph.dict_node.items():
            if node in checked:
                # to optimize the algo, don't check twice
                continue
            # check if there is a combinaison from node to node with one conflict
            # DFS with dependencies
            final_dependencies = self.o_graph.dfs_dependencies(node)

            checked += final_dependencies
            # check conflict
            for index_first, dependent_node in enumerate(final_dependencies):
                for conflicted_node in (
                    final_dependencies[index_first:] + final_dependencies[:index_first]
                ):
                    # check with itself if there is a mutual conflict
                    if conflicted_node in dependent_node.conflicts:
                        return False
        return True


# NOTE: Other possibilities
# Dependencies : Dictionnary with the key = the name of the node, value = list of name dependent node
# In the value, we put only the direct dependent node.

# Conflicts = List[List[Tuple]], list of list with tuple of conflict
# or Same thing between conflicts and dependencies
# Conflicts : Dictionnary withe the key : name of the node, value list of name node

# For more understanding, I implemented with classes.


@dataclass
class Options:
    rule_set: RuleSet
    options_collection: list = field(init=True, repr=True, default_factory=list)

    def New(self, rule_set):
        """
        Create a new empty collection with its rule set.
        """
        self.options_collection = []
        self.rule_set = rule_set
        return self

    def toggle(self, option):
        """
        Add or remove selected option in the collection, and modify logically
        with dependences and conflicts rule set.

        Arguments:
            option : The option to add or remove.

        Returns:
            The collection updated with respected rules.
        """
        if option not in self.rule_set.o_graph.dict_node:
            return f"{option} doesn't exist"
        # selection = add option + dependencies
        # enleve conflict + conflict dependencies
        node_option = self.rule_set.get_option(option)

        if option not in self.options_collection:
            # in case the option is unticked
            # add the option in the collection
            self.options_collection.append(option)
            # get its direct and indirect dependencies
            dependencies = [node_option] + self.rule_set.o_graph.dfs_dependencies(node_option)
            conflicts = []
            for dependence in dependencies:
                if dependence.name not in self.options_collection:
                    # if not already in the collection add it
                    self.options_collection.append(dependence.name)
                # for each dependence and the selected option add its conflicts
                conflicts += self.rule_set.getConf(dependence)

            for conflict in conflicts:
                # for each conflict
                if conflict.name in self.options_collection:
                    # if it is in the option collection, remove it
                    self.options_collection.remove(conflict.name)
                    dependents = self.rule_set.o_graph.dfs_dependents(conflict)
                    # same with all its dependents
                    for dependent in dependents:
                        if dependent.name in self.options_collection:
                            self.options_collection.remove(dependent.name)

        else:
            # in case the option is ticked, remove it
            self.options_collection.remove(option)
            dependents = self.rule_set.o_graph.dfs_dependents(node_option)
            # with all its dependents
            for dependent in dependents:
                if dependent.name in self.options_collection:
                    self.options_collection.remove(dependent.name)

        return self.options_collection

    def stringSlice(self):
        """
        Return the option collection as concatenated string.
        """
        return "".join(self.options_collection)

    def selection(self):
        """
        Return the option collection as set.
        """
        return set(self.options_collection)
