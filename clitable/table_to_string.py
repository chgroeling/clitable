from collections import namedtuple

FormatterContext = namedtuple(
    "FormatterContext", ["col_idx", "row_idx", "active_col_name", "row"]
)


def dummy_formatter(inp, context):
    return inp


def create_formatter_context(col_idx, row_idx, active_col_name, headers, row):
    return FormatterContext(
        col_idx=col_idx,
        row_idx=row_idx,
        active_col_name=active_col_name,
        row={k: v for k, v in zip(headers, row)},
    )


def get_max_column_width(table, options):
    formatter = options.get("cell_formatter", dummy_formatter)
    noheader = options.get("noheader", False)

    data = [i for i in table]
    headers = table.get_headers()
    no_elements = len(headers)
    max_col_width = [0] * no_elements

    if not noheader:
        for idx, i in enumerate(headers):
            max_col_width[idx] = max(max_col_width[idx], len(str(i)))

    for row, i in enumerate(data):
        for col, v in enumerate(i):
            active_col_name = headers[col]
            fmt_context = create_formatter_context(
                col, row, active_col_name, headers, i
            )
            max_col_width[col] = max(
                max_col_width[col], len(formatter(str(v), fmt_context))
            )

    return max_col_width


def table_to_formatted_string(table, options):
    formatter = options.get("cell_formatter", dummy_formatter)
    headers = table.get_headers()
    noheader = options.get("noheader", False)
    separator = options.get("separator", "  ")

    data = [i for i in table]

    max_col_width = get_max_column_width(table, options)

    format_strs = []

    for i in max_col_width:
        format_strs.append("{:<%i}" % i)

    # build the format string
    str_format = separator.join(format_strs)

    lines = []

    if not noheader:
        # Add headers
        lines.append(str_format.format(*headers))

        # Add separators
        str_put = []
        for i in max_col_width:
            str_put.append("-" * i)
        lines.append(str_format.format(*str_put))

    # Add data
    for row, i in enumerate(data):
        str_put = []

        for col, v in enumerate(i):
            active_col_name = headers[col]
            fmt_context = create_formatter_context(
                col, row, active_col_name, headers, i
            )
            str_put.append(formatter(str(v), fmt_context))

        lines.append(str_format.format(*str_put))

    return "\n".join(lines)


def table_to_plain_string(table, options):
    headers = table.get_headers()
    noheader = options.get("noheader", False)
    separator = options.get("separator", " ")
    data = [i for i in table]
    lines = []
    no_elements = len(headers)
    format_strs = ["{}"] * no_elements
    str_format = separator.join(format_strs)

    if not noheader:
        # Add headers
        lines.append(str_format.format(*headers))

    # Add data
    for i in data:
        str_put = []
        for v in i:
            str_put.append(str(v))

        lines.append(str_format.format(*str_put))
    return "\n".join(lines)


def get_default_formatter():
    return "autoformat"


def get_available_formatters():
    return {"autoformat": table_to_formatted_string, "plain": table_to_plain_string}
