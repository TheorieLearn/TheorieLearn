from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG


def get_describe_target_graph_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
        START -> "we build a" PROPERTY GRAPH "."

        PROPERTY -> WEIGHTED DIRECTED | DIRECTED WEIGHTED | DIRECTED | WEIGHTED | EPSILON
        WEIGHTED -> "weighted" | "unweighted"
        DIRECTED -> "directed" | "undirected"

        GRAPH -> "graph" DESCRIBE_VERTICES | "graph" EPSILON
        DESCRIBE_VERTICES -> "whose vertices are" OBJECT DESCRIBE_EDGES
        DESCRIBE_EDGES -> "and whose edges are" "between" OBJECT CONNECTED | EPSILON
        CONNECTED -> "connected by" OBJECT

        OBJECT -> "airports" | "flights" | "planes" | "cities" | "coordinates" | "starting times" | "ending times"
        EPSILON ->
        """)


def get_restate_problem_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
        START -> "We compute" ALGORITHM "."

        ALGORITHM -> "shortest path" IN_G SP | "connected components" IN_G | "reachability" IN_G RE
        SP -> "from" STARTING_NODE "to" ENDING_NODE
        RE -> "from" STARTING_NODE

        STARTING_NODE -> "s" | "ORD" | "SFO"
        ENDING_NODE -> "t" | "JFK" |"LHR"
        IN_G -> "in G" | EPSILON
        EPSILON ->
        """)


def get_solve_problem_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
        START -> "We run" ALGORITHM "."

        ALGORITHM -> "BFS" SSSP | "DFS" SSSP | "Kosaraju's" ON_G | "Prim's" ON_G | "Dijkstra's" SSSP | "Bellman Ford" SSSP | "Floyd-Warshall" APSP | "Ford-Fulkerson" ON_G
        SSSP -> ON_G "starting" START_NODE "and return the path" END_NODE
        APSP -> ON_G "and return the the path" START_NODE END_NODE
        ON_G -> "on G" | EPSILON

        START_NODE -> "from" NODE
        END_NODE -> "to" NODE
        NODE -> "s" | "t" | "ORD" | "SFO" | "JFK" | "LHR"
        EPSILON ->
        """)
