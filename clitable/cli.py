import clitable.table
import clitable.clitable
import clitable.table_to_string as tof
import clitable.table_ops as tabfil
from argparse import ArgumentParser


def setup_sample_table():
    data = [
        [1, "1_test1", 1],
        [2, "1_test2--", 1],
        [3, "1_test3", 1],
        [4, "2_test4-", 2],
        [5, "1_test5", 1],
        [6, "3_test6----", 3],
    ]
    table = clitable.table.Table(data=data, headers=["id", "name", "class"])
    return table


def cell_formatter(col, row, col_name, inp):
    """Example cell formatter"""
    if col_name == "class":
        return f'"  {inp}  "'
    return inp


def main():
    parser = ArgumentParser(prog="cli")

    table_formatters = tof.get_available_formatters()
    formatters = [k for k, _ in table_formatters.items()]
    parser.add_argument(
        "-f",
        "--formatter",
        default=tof.get_default_formatter(),
        choices=formatters,
        help="Table formatter selection.",
    )

    parser.add_argument(
        "-n",
        "--noheader",
        default=False,
        action="store_true",
        help="If set, print no header",
    )

    parser.add_argument(
        "-s",
        "--separator",
        default=None,
        help="Set separator",
    )

    parser.add_argument(
        "-r",
        "--rowfilter",
        default="",
        help="Filter each row by the specified expression",
    )

    parser.add_argument(
        "-t",
        "--tablesort",
        default="",
        help="Sort each row by the specified expression",
    )
    parser.add_argument(
        "-d",
        "--deletecol",
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

    out_str = clitable.clitable.clitable(
        table,
        args.formatter,
        options,
        rowfilter_expr=args.rowfilter,
        tablesort_expr=args.tablesort,
        deletecol=args.deletecol,
    )

    print(out_str)


if __name__ == "__main__":
    main()
