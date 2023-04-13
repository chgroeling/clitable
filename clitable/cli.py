import clitable.table
import clitable.table_output_formatted as tof
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
        help="Table formatter selection.",
    )

    parser.add_argument(
        "-s",
        "--separator",
        default=None,
        help="set separator",
    )

    args = parser.parse_args()
    table = setup_sample_table()

    options = {"noheader": args.noheader, "separator": args.separator}
    out_str = table_formatters[args.formatter](table, options)

    print(out_str)


if __name__ == "__main__":
    main()
