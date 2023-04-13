import clitable.table
import clitable.table_to_string as tof
import clitable.table_filter as tabfil
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

    if args.rowfilter != None and args.rowfilter != "":
        filtered_table = tabfil.filter_table_rows(table, args.rowfilter)
    else:
        filtered_table = table

    if args.tablesort != None and args.tablesort != "":
        sorted_table = tabfil.sort_table_rows(filtered_table, args.tablesort)
    else:
        sorted_table = filtered_table

    if args.deletecol != None and len(args.deletecol) > 0:
        spliced_table = tabfil.remove_table_cols(sorted_table, args.deletecol)
    else:
        spliced_table = sorted_table

    out_str = table_formatters[args.formatter](spliced_table, options)

    print(out_str)


if __name__ == "__main__":
    main()
