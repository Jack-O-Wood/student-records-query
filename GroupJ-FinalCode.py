# GROUP J FINAL CODE

# -------------Defining Functions----------------------

# reading the file
def readRecords(inFile):
  header_line = inFile.readline().rstrip('\n')

  # Handle empty file or missing header
  if header_line == '':
      print("Error: file appears to be empty or missing a header row.")
      return {}

  keys = header_line.split("\t")
  records = {} #Dict of Dict

  line_num = 2   # because header is line 1

  for line in inFile:
    line = line.rstrip('\n').strip()

    # Skip empty lines using a flag
    has_content = (line != '')
    if not has_content:
        line_num += 1
        continue_processing = False
    else:
        continue_processing = True

    # Split fields only if we have content
    if continue_processing:
        fields = line.split("\t")

        # Check field count
        if len(fields) != len(keys):
            print("Warning: skipping malformed line", line_num,
                  "(expected", len(keys), "fields, got", len(fields), ").")
            continue_processing = False
    # Only build the inner dictionary if everything is okay
    if continue_processing:
        innerDict = {}
        i = 0
        while i < len(keys):
            key = keys[i]
            value = fields[i]
            innerDict[key] = value
            i += 1

        record_id = innerDict.get(keys[0])

        if record_id is None or record_id == '':
            print("Warning: skipping line", line_num,
                  "because it has no valid ID.")
        else:
            if record_id in records:
                print("Warning: duplicate ID", record_id,
                      "on line", line_num, "- overwriting previous record.")
            records[record_id] = innerDict

    line_num += 1

  if len(records) == 0:
    print("Warning: no valid records were loaded from the file.")

  return records

# Prints the table header with column names aligned in fixed-width columns
def printHeader():
    print('{:<12} {:<12} {:<12} {:<12} {:<12} {:<12}'.format(
        'ID', 'Last', 'First', 'Year', 'Term', 'Degree'))
    print('-' * 70)

# Prints one student record in a formatted row
def printStudentRow(student):
    print('{:<12} {:<12} {:<12} {:<12} {:<12} {:<12}'.format(
        student['ID'],
        student['Last'],
        student['First'],
        student['GradYear'],
        student['GradTerm'],
        student['DegreeProgram']
    ))
# display all the students
def displayStudents(masterDict):
    printHeader()
    for student in masterDict.values():
        printStudentRow(student)

# Search for students by last name
def filterStudentsWithLastnameBegins(masterDict, name):
  if name == '':
        print("Please enter at least one character for the last name search.")
        return
      
  found = False
  name = name.lower()
  for student in masterDict.values():
    search = student['Last'].lower()
    if search.startswith(name):
      if not found:
                printHeader()
                found = True
      printStudentRow(student)
  if not found:
      print('Name not found')

# Search for records by year
def filterStudentsYear(masterDict, year):
    found = False

    for student in masterDict.values():
        grad_text = student.get('GradYear', '')

        try:
            grad_year = int(grad_text)
        except ValueError:
            # Bad data in file; skip this record by simply not matching
            grad_year = None

        if grad_year == year:
            if not found:
                printHeader()
                found = True
            printStudentRow(student)

    if not found:
        print("Year", year, "not found")


# Summary Report
def summaryReport(masterDict, year):
    countYear = 0
    degrees = {}

    for student in masterDict.values():
        grad_text = student.get('GradYear', '')

        try:
            grad_year = int(grad_text)
        except ValueError:
            grad_year = None

        if grad_year == year:
            countYear = countYear + 1

            degree = student.get('DegreeProgram', 'Unknown')
            if degree in degrees:
                degrees[degree] = degrees[degree] + 1
            else:
                degrees[degree] = 1

    if countYear == 0:
        print("Year", year, "not found")
    else:
        print("Summary for graduating class", year)
        print("Total students:", countYear)
        print()
        print("{:<10} {:<10} {:<10}".format("Degree", "Count", "Percent"))
        print("----------------------------------")

        for degree, count in degrees.items():
            percent = (count / countYear) * 100
            print("{:<10} {:<10} {:>6.2f}%".format(degree, count, percent))
            
def getYearFromUser(prompt_text):
    year_str = input(prompt_text)
    try:
        year_value = int(year_str)
        return year_value
    except ValueError:
        print("Invalid year. Please enter a 4-digit number like 2020.")
        return None
    


# -----------------------User Input/Menu---------------------
def runMenu(masterDict):
  userinput = ''

  while userinput != 'quit':
      print('\nMenu:')
      print('1 - Display ALL students')
      print('2 - Search by last name prefix')
      print('3 - Search by graduation year')
      print('4 - Program Summary by graduation year')
      print('quit - Exit program')

      try:
          userinput = input('Enter choice: ').lower()
      except EOFError:
          # Input stream closed; exit cleanly
          print("\nInput closed. Exiting program.")
          userinput = 'quit'

      if userinput == '1':
          displayStudents(masterDict)

      elif userinput == '2':
          prefix = input('Enter beginning of last name: ')
          filterStudentsWithLastnameBegins(masterDict, prefix)

      elif userinput == '3':
        year = getYearFromUser('Enter graduation year: ')
        if year is not None:
          filterStudentsYear(masterDict, year)

      elif userinput == '4':
        year = getYearFromUser('Enter graduation year: ')
        if year is not None:
          summaryReport(masterDict, year)
          
      elif userinput == 'quit':
          print('Exiting...')

      else:
          print('Invalid choice.')


# ----- FILE LOADING WITH ERROR HANDLING -----

filename = input('Enter filename:').strip()
if filename == '':
    filename = 'students.txt'

masterDict = {}

try:
    with open(filename, 'r') as f:
        masterDict = readRecords(f)

    if len(masterDict) > 0:
        print('File loaded successfully.\n')
    else:
        print('No valid records found in the file.\n')

except FileNotFoundError:
    print("Error: File '", filename, "' not found. "
          "Please make sure the file is in the same folder as this program.", sep='')

except OSError as e:
    # Other file-related errors (permissions, etc.)
    print("Error opening file '", filename, "': ", e, sep='')

# Decide whether to run the menu
if len(masterDict) == 0:
    print("No records available. Program will exit.")
else:
    # call menu loop
    runMenu(masterDict)



