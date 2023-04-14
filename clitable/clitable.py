import clitable.table_to_string as tof
import clitable.table_ops as tabfil
import clitable.table_to_string as tts


def post_process_table(
    input_table, rowfilter_expr=None, sort_expr=None, removecollist=None
):
    if rowfilter_expr != None and rowfilter_expr.strip() != "":
        filtered_table = tabfil.filter_table_rows(input_table, rowfilter_expr)
    else:
        filtered_table = input_table

    if sort_expr != None and sort_expr.strip() != "":
        sorted_table = tabfil.sort_table_rows(filtered_table, sort_expr)
    else:
        sorted_table = filtered_table

    if removecollist != None and len(removecollist) > 0:
        sliced_table = tabfil.remove_table_cols(sorted_table, removecollist)
    else:
        sliced_table = sorted_table

    return sliced_table


def table_to_string(
    input_table,
    formatter=tts.get_default_formatter(),
    output_options={},
    rowfilter_expr=None,
    sort_expr=None,
    removecollist=None,
):
    processed_table = post_process_table(
        input_table,
        rowfilter_expr=rowfilter_expr,
        sort_expr=sort_expr,
        removecollist=removecollist,
    )
    table_formatters = tof.get_available_formatters()
    out_str = table_formatters[formatter](processed_table, output_options)
    return out_str
