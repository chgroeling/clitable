import clitable
from argparse import ArgumentParser

def setup_sample_table():
    data = [
        [1, "1_test1", 1],
        [2, "1_test2--", 1],
        [3, "1_test3", 1],
        [4, "2_test4-", 2],
        [5, "1_test5", 1],
        [6, "3_test6----", 3],
        [7, "abc", 3],
    ]
    table = clitable.Table(data=data, headers=["id", "name", "class"])
    return table


def cell_formatter(col, row, col_name, inp):
    """Example cell formatter"""
    if col_name == "class":
        return f'"  {inp}  "'
    return inp


def main():
    parser = ArgumentParser(prog="cli")

    table_formatters = clitable.get_available_formatters()
    formatters = [k for k, _ in table_formatters.items()]
    parser.add_argument(
        "-fo",
        "--formatter",
        default=clitable.get_default_formatter(),
        choices=formatters,
        help="Table formatter selection.",
    )

    parser.add_argument(
        "-nh",
        "--noheader",
        default=False,
        action="store_true",
        help="If set, print no header",
    )

    parser.add_argument(
        "-sep",
        "--separator",
        default=" ",
        help="Set separator",
    )

    parser.add_argument(
        "-f",
        "--rowfilter",
        default="",
        help="Filter each row by the specified expression",
    )

    parser.add_argument(
        "-s",
        "--sort",
        default="",
        help="Sort each row by the specified expression",
    )
    parser.add_argument(
        "-r",
        "--removecol",
        action="append",
        help="Removes the col given by header name. Can be used multiple times.",
    )
    args = parser.parse_args()
    table = setup_sample_table()

    options = {
        "noheader": args.noheader,
        "separator": args.separator,
        "cell_formatter": cell_formatter,
    }

    out_str = clitable.clitable(
        table,
        args.formatter,
        options,
        rowfilter_expr=args.rowfilter,
        sort_expr=args.sort,
        removecollist=args.removecol,
    )

    print(out_str)


if __name__ == "__main__":
    main()
