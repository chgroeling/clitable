def get_max_column_width(table):
    data = [i for i in table]
    headers = table.get_headers()
    no_elements = len(data[0])
    max_col_width = [0] * no_elements

    for idx, i in enumerate(headers):
        max_col_width[idx] = max(max_col_width[idx], len(str(i)))

    for i in data:
        for idx, v in enumerate(i):
            max_col_width[idx] = max(max_col_width[idx], len(str(v)))

    return max_col_width


def table_to_formatted_string(table, options):
    headers = table.get_headers()
    noheader = options['noheader']
    separator = options['separator'] if options['separator'] else "  "
    data = [i for i in table]

    max_col_width = get_max_column_width(table)

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
    for i in data:
        str_put = []
        for v in i:
            str_put.append(str(v))

        lines.append(str_format.format(*str_put))

    return "\n".join(lines)


def table_to_plain_string(table, options):
    headers = table.get_headers()
    noheader = options['noheader']
    separator = options['separator'] if options['separator'] else " "
    data = [i for i in table]
    lines = []
    no_elements = len(data[0])
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
