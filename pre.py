"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()
current_time = arrow.now('US/Pacific')
print (current_time)

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """
    field = None
    entry = { }
    cooked = [ ] 
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line
            continue
        if len(parts) == 2: 
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                #base = arrow.get(content)
                base = arrow.get(content, "M/D/YYYY")
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = ""
            entry['week'] = content
            first_date = base.replace(weeks=+(int (content) - 1)) #get new arrow obeject datetime for each week 
            entry['date'] = first_date.format("MM/DD/YY") # format to display on the html page 
            first_date_range = first_date.replace(days=+6)
            if first_date <= current_time and current_time <= first_date_range:
                entry['current_time'] = True
            else:
                entry['current_time'] = False


            #entry['date'] = first_date

        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    return cooked


def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
