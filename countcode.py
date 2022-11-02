import os
def countlines(start,lines=0, header=True, begin_start=None):
    print(start)
    if header:
        print('{:>10} |{:>10} | {:<20}'.format('ADDED', 'TOTAL', 'FILE'))
        print('{:->11}|{:->11}|{:->20}'.format('', '', ''))
    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isfile(thing):
            if thing.endswith('.cs'):
                with open(thing, 'r') as f:
                    newlines = [line.rstrip('\n') for line in f.readlines() if line.strip() != '' ]
                    lineArray =[]
                    for line in newlines:
                        if  line.strip().startswith("//"):
                            continue
                        elif line.strip().startswith('/*') & line.strip().endswith('*/'): #single line comment
                            continue
                        lineArray.append(line)
                    commentStart = False
                    commentEnd = True
                    for i,l in enumerate(lineArray):
                        if l.strip().startswith('/*') and commentEnd == True : #multi line comment run until we find the end sequence
                            commentStart = True
                            commentEnd = False
                        if l.strip().endswith('*/') and commentStart == True :
                            commentEnd = True
                            commentStart = False
                            lineArray[i]=''
                        if commentStart == True and commentEnd == False:
                            lineArray[i] = ''
                            #continue until we find sthe closing line
                    newlines = filter(None, lineArray)
                    length = len(lineArray)
                    lines += length
                    if begin_start is not None:
                        reldir_of_thing = '.' + thing.replace(begin_start, '')
                    else:
                        reldir_of_thing = '.' + thing.replace(start, '')
                    print('{:>10} |{:>10} | {:<20}'.format(
                            length, lines, reldir_of_thing))
    for thing in os.listdir(start):
        if thing=='Migrations' or thing == 'bin' or thing =='debug' or thing=='obj' :
            continue
        thing = os.path.join(start, thing)
        if os.path.isdir(thing):
            lines = countlines(thing, lines, header=False, begin_start=start)
    return lines
def main():
    import argparse
    descr = """Scan project for C# files"""
    parser = argparse.ArgumentParser(usage=descr)
    parser.add_argument('--folderPath',  metavar='PATH', help='folder path')
    args = parser.parse_args()
    try:
        countlines(args.folderPath)
    except (KeyboardInterrupt, StopIteration):
        pass
    except Exception:
        print("Exception has been raised")
if __name__ == '__main__':
    main()