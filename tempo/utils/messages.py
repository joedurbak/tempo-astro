from io import StringIO
import collections

from pandas import read_csv


def is_blank_dict(test_dict):
    for value in test_dict.values():
        if value != "":
            return False
    return True


def format_markdown_table(markdown_table_str):
    # print(markdown_table_str)
    df = read_csv(StringIO(markdown_table_str), delimiter='|')
    df.dropna(axis=1, how='all')
    df2 = df[df.columns[1:-1]]
    df3 = df2.iloc[1:]
    df_str = str(df3.to_markdown(index=False))
    # df_str = str(df3.to_string(line_width=80, index=False))
    return_table_str = '```\n' + df_str + '\n```\n'
    # print(return_table_str)
    return return_table_str


def markdown_to_slack_post(markdown):
    markdown_lines = StringIO(markdown).readlines()
    # removing comments
    no_comment_lines = [l for l in markdown_lines if not l.startswith('[comment]: <>')]

    # removing multiple blank lines
    output_lines = []
    previous_blank = False
    for l in no_comment_lines:
        blank_line = l.strip() == ''
        if not previous_blank or not blank_line:
            output_lines.append(l)
        if blank_line:
            previous_blank = True
        else:
            previous_blank = False
    output_message = ''.join(output_lines)
    table_str = ''
    previous_pipe = False
    for l in output_lines:
        start_pipe = l.startswith('|')
        if not start_pipe and previous_pipe:
            new_table = format_markdown_table(table_str)
            output_message = output_message.replace(table_str, new_table)
            table_str = ''
            previous_pipe = False
        if start_pipe:
            table_str += l
            previous_pipe = True
    return output_message


def format_decimal_places(number, decimal_places):
    integers, decimals = str(number).split('.')
    current_dec_place = len(decimals)
    if current_dec_place > decimal_places:
        decimals = decimals[0:decimal_places]
    else:
        for i in range(decimal_places-current_dec_place):
            decimals += '0'
    return '.'.join((integers, decimals))


def count_decimal_places(number):
    try:
        decimals = str(number).split('.')[1]
        return len(decimals)
    except IndexError:
        return 0


def list_plus(possible_list):
    if (type(possible_list) is not list) and (type(possible_list) is not tuple):
        if isinstance(possible_list, collections.abc.Mapping):
            return [possible_list]
        else:
            return []
    return possible_list


def format_html(string, input_dict):
    if is_blank_dict(input_dict):
        return ""
    for key, value in input_dict.items():
        string = string.replace(r"{" + str(key) + r"}", str(value))
    return string


def xml_tag_loader(xml_dictionary, key_tuple):
    try:
        value = xml_dictionary.copy()
    except AttributeError:
        value = xml_dictionary
    for key in key_tuple:
        try:
            value = value[key]
        except KeyError:
            return ""
        except TypeError:
            if type(value) is list:
                try:
                    value = value[0][key]
                except KeyError or TypeError:
                    return ""
            else:
                return ""
    return value
