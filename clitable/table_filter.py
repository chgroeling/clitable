import clitable.table
from lark import Lark, Transformer, v_args

comparison_grammar = r"""
?expression: comparison
    | expression AND expression -> and_op
    | expression OR expression -> or_op

?comparison: additive_expression 
    | additive_expression  "==" comparison -> equal
    | additive_expression  "!=" comparison -> not_equal
    | additive_expression  "<" comparison -> less_than
    | additive_expression  ">" comparison -> more_than
    | additive_expression  "<=" comparison -> less_or_equal
    | additive_expression  ">=" comparison -> more_or_equal

?additive_expression: multiplicative_expression
    | multiplicative_expression  "+"  additive_expression -> add
    | multiplicative_expression  "-"  additive_expression -> sub

?multiplicative_expression:  primary_expression 
    | primary_expression  "*"  multiplicative_expression -> mul
    | primary_expression  "/"  multiplicative_expression -> div
                           
?primary_expression:  "(" expression ")"
    | SIGNED_FLOAT -> float
    | SIGNED_INT -> integer
    | IDENTIFIER -> id
    | "-" IDENTIFIER -> neg_id
    | ESCAPED_STRING -> string

AND: "and" | "AND"
OR: "or" | "OR"
INTEGER: SIGNED_INT
IDENTIFIER: ("a" .. "z" | "A" .. "Z")("a" .. "z" | "A" .. "Z" | "0" .."9")*
WHITESPACE: (" " | "\n" | "\t" | "\r" )+
%import common.ESCAPED_STRING
%import common.SIGNED_FLOAT
%import common.SIGNED_INT

%ignore WHITESPACE
"""
# STRING: " ~[\"]* "
# IDENTIFIER: ["a"-"z""A"-"Z"_][a-zA-Z0-9_]*


class CompareExpressionTree(Transformer):
    """
    Basic Interperter to parse the grammar from above
    """

    def __init__(self, symbol_table):
        self.__symbol_table = symbol_table

    def or_op(self, items):
        # items[0] OR items[2]
        return items[0] or items[2]

    def and_op(self, items):
        # items[0] AND items[2]
        return items[0] and items[2]

    def add(self, items):
        return items[0] + items[1]

    def sub(self, items):
        return items[0] - items[1]

    def mul(self, items):
        return items[0] * items[1]

    def div(self, items):
        return items[0] / items[1]

    def more_than(self, items):
        return items[0] > items[1]

    def less_than(self, items):
        return items[0] < items[1]

    def less_or_equal(self, items):
        return items[0] <= items[1]

    def more_or_equal(self, items):
        return items[0] >= items[1]

    def equal(self, items):
        return items[0] == items[1]

    def not_equal(self, items):
        return items[0] != items[1]

    def integer(self, items):
        (s,) = items
        return int(s)

    def float(self, items):
        (s,) = items
        return float(s)

    def id(self, items):
        (id_,) = items
        return self.__symbol_table[id_]
    
    def neg_id(self, items):
        (id_,) = items
        return -self.__symbol_table[id_]

def filter_table_rows(table, string_predicate):
    compare_parser = Lark(comparison_grammar, start="expression")
    tree = compare_parser.parse(string_predicate)

    header = table.get_headers()
    data = []

    for row in table:
        symbol_table = {k: v for k, v in zip(header, row)}
        out = CompareExpressionTree(symbol_table).transform(tree)
        if type(out) != bool:
            raise Exception("String predicate doesn't evaluate to bool")
        if out:
            data.append(row)

    return clitable.table.Table(headers=header, data=data)


def sort_table_rows(table, string_key):
    compare_parser = Lark(comparison_grammar, start="expression")
    tree = compare_parser.parse(string_key)

    header = table.get_headers()
    data = [row for row in table]

    def string_key_parser(row):
        symbol_table = {k: v for k, v in zip(header, row)}
        out = CompareExpressionTree(symbol_table).transform(tree)
        return out

    data = sorted(data, key=lambda i: string_key_parser(i))

    return clitable.table.Table(headers=header, data=data)

def remove_table_cols(table, remove_list):
   

    header = []
    for pos in table.get_headers():
        if pos not in remove_list:
            header.append(pos)

    data = []

    for i in table:
        row = []
        for head, c in zip(table.get_headers(), i):
            if head not in remove_list:
                row.append(c)
        data.append(row)


    return clitable.table.Table(headers=header, data=data)