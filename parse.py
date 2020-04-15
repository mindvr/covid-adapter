import sys
import re

dateFormat = re.compile('\d\d\.\d\d\.\d\d')
regionFormat = re.compile('🔸.*-')


def readfile(name):
    file = open(name, 'r')
    lines = file.readlines()
    file.close()
    return lines


def clean(lines):
    return [line for line in lines if regionFormat.search(line) or dateFormat.search(line)]


def parse_lines(lines):
    parse_result = {}
    current_date = '00.00'
    for line in lines:
        if dateFormat.search(line):
            date_tokens = dateFormat.findall(line)[0].split('.')
            current_date = date_tokens[2]+'-'+date_tokens[1]+'-'+date_tokens[0]
            parse_result[current_date] = {}
        else:
            tokens = line.split()
            region = regionFormat.findall(line)[0][1:-1].strip()
            parse_result[current_date][region] = tokens[-1]
    return parse_result


def get_dates(parse_result):
    dates = list(parse_result.keys())
    dates.sort()
    return dates

def get_header(dates):
    return '\t' + '\t'.join(dates)

def group_by_region(parse_result):
    transformation = {}
    for date in parse_result:
        for city in parse_result[date]:
            if(not city in transformation):
                transformation[city] = {}
            transformation[city][date] = parse_result[date][city]
    return transformation

def write_lines(name, lines):
    file = open(name, 'w')
    file.write('\n'.join(lines))
    file.close()


if __name__ == '__main__':
    filename = sys.argv[1]
    lines = clean(readfile(filename))
    parse_result = parse_lines(lines)
    dates = get_dates(parse_result)
    result = []
    result.append(get_header(dates))
    byRegions = group_by_region(parse_result)
    regionsSorted = list(byRegions.keys())
    regionsSorted.sort()
    for region in regionsSorted:
        row = region
        for date in dates:
            row += '\t'
            if date in byRegions[region]:
                row += byRegions[region][date]
            else:
                row += '0'
        result.append(row)
    write_lines(sys.argv[2], result)
