from theorielearn.scaffolded_writing.cfg import ScaffoldedWritingCFG


def get_french_flag_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
       START -> STATEMENT_ABOUT_G "."\
              | STATEMENT_ABOUT_G_PRIME "."\
              | "If" STATEMENT_ABOUT_G "," "then" STATEMENT_ABOUT_G_PRIME "."\
              | "If" STATEMENT_ABOUT_G_PRIME "," "then" STATEMENT_ABOUT_G "."\
              | STATEMENT_ABOUT_G CONJUNCTION STATEMENT_ABOUT_G_PRIME "."\
              | STATEMENT_ABOUT_G_PRIME CONJUNCTION STATEMENT_ABOUT_G "."

       STATEMENT_ABOUT_G -> "the graph G has a" OBJECT
       STATEMENT_ABOUT_G_PRIME -> "the graph G' has a" OBJECT
       CONJUNCTION -> "and" | "or" | "if" | "if and only if"

       OBJECT -> "french flag walk" DESCRIPTION | "walk" DESCRIPTION | "path" DESCRIPTION | "cycle"
       DESCRIPTION -> "starting from" START_NODE "to" END_NODE | EPSILON

       START_NODE -> "s" | "(s, 0)" | "(s, 1)" | "(s, 2)" | S_GENERAL
       END_NODE ->   "t" | "(t, 0)" | "(t, 1)" | "(t, 2)" | T_GENERAL

       T_GENERAL -> "(t,i)" "where i is" I_CHARACTERISTIC
       S_GENERAL -> "(s,i)" "where i is" I_CHARACTERISTIC

       I_CHARACTERISTIC -> "an integer" NUMBER_CHARACTERISTIC | "a natural number" NUMBER_CHARACTERISTIC | "0" | "1" | "2"
       NUMBER_CHARACTERISTIC -> "between 0 and 2" | "less than |V|"

       EPSILON ->
    """)


def get_no_russian_flag_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
       START -> STATEMENT_ABOUT_G "."\
              | STATEMENT_ABOUT_G_PRIME "."\
              | "If" STATEMENT_ABOUT_G "," "then" STATEMENT_ABOUT_G_PRIME "."\
              | "If" STATEMENT_ABOUT_G_PRIME "," "then" STATEMENT_ABOUT_G "."\
              | STATEMENT_ABOUT_G CONJUNCTION STATEMENT_ABOUT_G_PRIME "."\
              | STATEMENT_ABOUT_G_PRIME CONJUNCTION STATEMENT_ABOUT_G "."

       STATEMENT_ABOUT_G -> "the graph G has a" OBJECT
       STATEMENT_ABOUT_G_PRIME -> "the graph G' has a" OBJECT
       CONJUNCTION -> "and" | "or" | "if" | "if and only if"

       OBJECT ->  "walk" RUSSIAN DESCRIPTION | "path" RUSSIAN DESCRIPTION | "cycle"
       RUSSIAN -> "with no Russian flags" | EPSILON
       DESCRIPTION -> "starting from" START_NODE "to" END_NODE | EPSILON

       START_NODE -> "s" | "(s, None)" | "(s, W)" | "(s, WB)" | S_GENERAL
       END_NODE ->   "t" | "(t, None)" | "(t, W)" | "(t, WB)" | T_GENERAL

       S_GENERAL -> "(s, q) for some q in {None, W, WB}" | "(s, q) for all q in {None, W, WB}"
       T_GENERAL -> "(t, q) for some q in {None, W, WB}" | "(t, q) for all q in {None, W, WB}"

       EPSILON ->
    """)


def get_ham_path_cycle_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
       START -> STATEMENT_ABOUT_G "."\
              | STATEMENT_ABOUT_G_PRIME "."\
              | "If" STATEMENT_ABOUT_G "," "then" STATEMENT_ABOUT_G_PRIME ADDITIONAL_RESTRICTION "." \
              | "If" STATEMENT_ABOUT_G_PRIME "," "then" STATEMENT_ABOUT_G ADDITIONAL_RESTRICTION "." \
              | STATEMENT_ABOUT_G CONJUNCTION STATEMENT_ABOUT_G_PRIME ADDITIONAL_RESTRICTION "." \
              | STATEMENT_ABOUT_G_PRIME CONJUNCTION STATEMENT_ABOUT_G ADDITIONAL_RESTRICTION "."

       STATEMENT_ABOUT_G -> "the input G has a" OBJECT
       STATEMENT_ABOUT_G_PRIME -> "the output G' has a" OBJECT
       OBJECT -> "path" | "cycle" | "Hamiltonian path" | "Hamiltonian cycle"

       ADDITIONAL_RESTRICTION -> EPSILON | "of the same length" | "containing the same vertices" | "containing the same edges"
       CONJUNCTION -> "and" | "or" | "if and only if"
       EPSILON ->
    """)


def get_dag_path_anden_cfg() -> ScaffoldedWritingCFG:
    return ScaffoldedWritingCFG.fromstring("""
      START -> STATEMENT_ABOUT_G "."\
            | STATEMENT_ABOUT_ARRAY_A "."\
            | "If" STATEMENT_ABOUT_G "," "then" STATEMENT_ABOUT_ARRAY_A "." \
            | "If" STATEMENT_ABOUT_ARRAY_A "," "then" STATEMENT_ABOUT_G "." \
            | STATEMENT_ABOUT_G CONJUNCTION STATEMENT_ABOUT_ARRAY_A "." \
            | STATEMENT_ABOUT_ARRAY_A CONJUNCTION STATEMENT_ABOUT_G "."

      STATEMENT_ABOUT_G -> "there exists a" OBJECT "from" SOURCE "to" TARGET G_LENGTH_RESTRICTION
      STATEMENT_ABOUT_ARRAY_A -> "there exists a" OBJECT "in the array A" ARRAY_LENGTH_RESTRICTION
      OBJECT -> "path" | "cycle" | "walk" | "delta-andén"
      SOURCE -> "t" | "s" | "an arbitrary vertex in G"
      TARGET -> "t" | "s" | "an arbitrary vertex in G"

      G_LENGTH_RESTRICTION -> EPSILON | "of length k" | "of length k + 2" | "of length k - 2"
      ARRAY_LENGTH_RESTRICTION -> EPSILON | "of length k"
      CONJUNCTION -> "and" | "or" | "if and only if"
      EPSILON ->
   """)
