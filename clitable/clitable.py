import clitable.table
import clitable.table_to_string as tof
import clitable.table_ops as tabfil


def clitable(
    table, formatter, options, rowfilter_expr=None, tablesort_expr=None, deletecol=None
):

    table_formatters = tof.get_available_formatters()
    if rowfilter_expr != None and rowfilter_expr != "":
        filtered_table = tabfil.filter_table_rows(table, rowfilter_expr)
    else:
        filtered_table = table

    if tablesort_expr != None and tablesort_expr != "":
        sorted_table = tabfil.sort_table_rows(filtered_table, tablesort_expr)
    else:
        sorted_table = filtered_table

    if deletecol != None and len(deletecol) > 0:
        spliced_table = tabfil.remove_table_cols(sorted_table, deletecol)
    else:
        spliced_table = sorted_table

    out_str = table_formatters[formatter](spliced_table, options)
    return out_str
