"""
Project for Week 4 of "Python Data Representations".
Find differences in file contents.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""
#import os

IDENTICAL = -1

def singleline_diff(line1, line2):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
    Output:
      Returns the index where the first difference between
      line1 and line2 occurs.

      Returns IDENTICAL if the two lines are the same.
    """
    index = -1
    equal = 0
    if line1 > line2:
        length = len(line2)
    elif line1 < line2:
        length = len(line1)
    else:
        length = len(line1)
        equal = 1
    for index in range(length):
        if line1[index] != line2[index]:
            return index
    if equal == 0:
        return index + 1
    else:
        return IDENTICAL


def singleline_diff_format(line1, line2, idx):
    """
    Inputs:
      line1 - first single line string
      line2 - second single line string
      idx   - index at which to indicate difference
    Output:
      Returns a three line formatted string showing the location
      of the first difference between line1 and line2.

      If either input line contains a newline or carriage return,
      then returns an empty string.

      If idx is not a valid index, then returns an empty string.
    """
    string = ""
    for char in line1:
        if char == '\n':
            return string
    for char in line2:
        if char == '\n':
            return string
    if line1 >= line2:
        length = len(line2)
    else:
        length = len(line1)    
    if 0 <= idx < length + 1:
        string += line1 + '\n'
        for _ in range(idx):
            string += '='
        string += "^\n" + line2 + "\n"    
        return string
    
    return string
    


def multiline_diff(lines1, lines2):
    """
    Inputs:
      lines1 - list of single line strings
      lines2 - list of single line strings
    Output:
      Returns a tuple containing the line number (starting from 0) and
      the index in that line where the first difference between lines1
      and lines2 occurs.

      Returns (IDENTICAL, IDENTICAL) if the two lists are the same.
    """
    equal = 0
    index = -1
    if len(lines1) > len(lines2):
        length = len(lines2)
    elif len(lines1) < len(lines2):
        length = len(lines1)
    else:
        length = len(lines1)
        equal = 1
    for index in range(length):
        idx = singleline_diff(lines1[index], lines2[index])
        if idx != IDENTICAL:
            return (index, idx)
    if equal == 0:
        return (index + 1, 0)
    return (IDENTICAL, IDENTICAL)


def get_file_lines(filename):
    """
    Inputs:
      filename - name of file to read
    Output:
      Returns a list of lines from the file named filename.  Each
      line will be a single line string with no newline ('\n') or
      return ('\r') characters.

      If the file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    file = open(filename, "rt")
    content = []
    for line in file.readlines():
        if line.endswith('\n'):
            content.append(line[:len(line)-1])
        else:
            content.append(line)
    file.close()
    return content


def file_diff_format(filename1, filename2):
    """
    Inputs:
      filename1 - name of first file
      filename2 - name of second file
    Output:
      Returns a four line string showing the location of the first
      difference between the two files named by the inputs.

      If the files are identical, the function instead returns the
      string "No differences\n".

      If either file does not exist or is not readable, then the
      behavior of this function is undefined.
    """
    lines1 = get_file_lines(filename1)
    lines2 = get_file_lines(filename2)
    content = ""
    (line_no, index) = multiline_diff(lines1, lines2)
    if line_no != IDENTICAL:
        content += "Line " + str(line_no) + ":\n"
        if lines1 == []:
            lines1.append('')
        if lines2 == []:
            lines2.append('')    
        content += singleline_diff_format(lines1[line_no], lines2[line_no], index)
        return content
    else:
        return "No differences\n"

# print(os.getcwd())
#print(file_diff_format('isp_diff_files/file8.txt', 'isp_diff_files/file9.txt'))
