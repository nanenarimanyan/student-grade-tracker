import csv

file_path = "C:\\Users\\norga\\Downloads\\student-scores (2).csv"


with open(file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    # Extract the header and all rows
    rows = [row for row in csv_reader]
    
relevant_columns = [
    "id", "first_name", "last_name", "math_score", "history_score", "physics_score",
    "chemistry_score", "biology_score", "english_score", "geography_score"
]

# Prepare the data
header = rows[0] if rows else []  # First row is the header
data = rows[1:] if len(rows) > 1 else []  # Rest are the data rows



def technical_document():
    """Generates a technical document for the dataset."""
    doc = f"""
    ### Technical Document: Student Scores Dataset

    #### 1. Purpose
    This dataset contains academic performance data for students, including their scores in various subjects.
    It is designed for use in analysis, such as calculating averages, identifying top performers, and ensuring
    data integrity.

    #### 2. Dataset Structure
    - File Type: CSV (Comma-Separated Values)
    - Number of Columns: {len(header)}
    - Number of Rows: {len(data)}

    #### 3. Column Descriptions:
    Each row contains data for a single student. The columns represent the following attributes:
    """
    # Loop through relevant columns to describe them
    for col in relevant_columns:
        doc += f"- `{col}`: {col.replace('_', ' ').capitalize()}\n"
        if col in ['id', 'math_score', 'history_score', 'physics_score', 'chemistry_score', 'biology_score',
                   'english_score', 'geography_score']:
            doc += "  - Expected Data Type: Integer (0-100)\n"
        else:
            doc += "  - Expected Data Type: String\n"

    doc += f"""
    #### 4. Data Rules:
    - All scores must be integers between 0 and 100.
    - Rows must not contain missing values.
    - Each student must have a unique ID.

    #### 5. Example Data (First Row):
    - Header: {header}
    - Sample Row: {data[0] if data else 'N/A'}

    #### 6. Summary:
    - Total records: {len(data)}
    """
    return doc


# Generate the document as a string
doc_content = technical_document()
print(doc_content)

# Save the technical document to a file
output_doc_path = "C:\\Users\\norga\\Downloads\\technical_document.txt"
with open(output_doc_path, mode='w') as doc_file:
    doc_file.write(technical_document())
print(f"\nTechnical document saved to {output_doc_path}\n")
print("\n\n----------------------------------------------------------------------------------------------")

# 2-----------------------------------------------------------------------------------------------------------------------


# Getting the indices of relevant columns
relevant_indices = {col: header.index(col) for col in relevant_columns}

# Creating formatted output
def format_row(row):
    return {
        "Name": f"{row[relevant_indices['first_name']]} {row[relevant_indices['last_name']]}",
        "Student ID": f"S{row[relevant_indices['id']]}",
        "Math": row[relevant_indices["math_score"]],
        "History": row[relevant_indices["history_score"]],
        "Physics": row[relevant_indices["physics_score"]],
        "Chemistry": row[relevant_indices["chemistry_score"]],
        "Biology": row[relevant_indices["biology_score"]],
        "English": row[relevant_indices["english_score"]],
        "Geography": row[relevant_indices["geography_score"]],
    }


# Printing sample data
print("Sample Data (First 5 Rows):")
# Iterating over the first five rows
for row in data[:5]:  
    print(format_row(row))

print("\nSample Data (Last 5 Rows):")
# Iterating over the last five rows
for row in data[-5:]: 
    print(format_row(row))
print("\n\n----------------------------------------------------------------------------------------------")
# 3-----------------------------------------------------------------------------------------------------------------------

# Removing duplicate rows
unique_rows = []
seen = set()
for row in rows:
    row_tuple = tuple(row)  # Converting to tuple for immutability
    if row_tuple not in seen:  # Checking for uniqueness
        seen.add(row_tuple)
        unique_rows.append(row)

# Handling missing values by removing rows with missing data and keeping rows with no empty cells
cleaned_rows = [row for row in unique_rows if "" not in row] 

# Checking data consistency by getting valid numeric ranges for grades
valid_rows = []
grades_indices = [header.index(col) for col in [
    "math_score", "history_score", "physics_score", 
    "chemistry_score", "biology_score", "english_score", "geography_score"
]]

valid_rows = []
# Iterating over the cleaned rows
for row in cleaned_rows:
    valid = True
    for idx in grades_indices: #Iterating over indices
        grade = row[idx]
        # Checking if the grade is a digit and is in the valid range
        if not grade.isdigit() or not (0 <= int(grade) <= 100):
            valid = False
            break
    if valid:
        valid_rows.append(row)


# Printing statistics about the cleaned dataset
print("\n### Initial Dataset Statistics ###")
print(f"Total Records (Before Cleaning): {len(rows)}")

print("\n### Cleaned Dataset Statistics ###")
print(f"Total Records (After Removing Duplicates and Missing Values): {len(valid_rows)}")
print(f"Total Duplicates Removed: {len(rows) - len(unique_rows)}")
print(f"Total Records Removed Due to Missing Values: {len(unique_rows) - len(cleaned_rows)}")
print(f"Total Records Removed Due to Invalid Grades: {len(cleaned_rows) - len(valid_rows)}")

# Saving the cleaned dataset
output_file_path = "C:\\Users\\norga\\Downloads\\cleaned_student_scores.csv"
with open(output_file_path, mode='w', newline='') as file:
    # Writing the header
    file.write(','.join(header) + '\n')

    # Writing each row
    for row in valid_rows:
        file.write(','.join(row) + '\n')

# Showing the output file path
print("\nCleaned dataset saved to:", output_file_path)
print("\n\n----------------------------------------------------------------------------------------------")
# -----------------------------------------------------------------------------------------------------------------------


import matplotlib.pyplot as plt
import numpy as np


plt.style.use('_mpl-gallery')

#the dataset of first and last 5 students
selected_students = valid_rows[:5] + valid_rows[-5:]

#selecting dataset as student firs and last names
student_names = [
    f"{row[relevant_indices['first_name']]} {row[relevant_indices['last_name']]}" 
    for row in selected_students
]

#calculating average scores for each student 
average_scores = [
    sum(int(row[relevant_indices[subject]]) for subject in relevant_columns[3:]) / len(relevant_columns[3:])
    for row in selected_students
]

#visualising the average grades on bar charts
x = np.arange(len(student_names))  #locations for the bars
width = 0.5  #width of the bars

fig, ax = plt.subplots(figsize=(10, 5))

#creating the bar charts for grades 
average_bar = ax.bar(x, average_scores, width, color='skyblue', edgecolor='black')

#setting the titles for the bar charts
ax.set_xlabel('Students')
ax.set_ylabel('Average Score')
ax.set_title('Average Grade for Selected Students')
ax.set_xticks(x)
ax.set_xticklabels(student_names, rotation=45, ha="right")

#adding labels(average grades) on the bars
ax.bar_label(average_bar, padding=3)

#tight layout for better display and avoid label cutoffs
fig.tight_layout()

#displaying the plot
plt.show()


#calculating the average scores of the students
selected_student_averages = [
    (f"{row[relevant_indices['first_name']]} {row[relevant_indices['last_name']]}", 
     sum(int(row[relevant_indices[subject]]) for subject in relevant_columns[3:]) / len(relevant_columns[3:]))
    for row in selected_students
]

#sorting the selected students by average score (highest to lowest)
selected_student_averages_sorted = sorted(selected_student_averages, key=lambda x: x[1], reverse=True)

#top and bottom performers from the selected students
top_performers = selected_student_averages_sorted[:3]
bottom_performers = selected_student_averages_sorted[-3:]

#output of the high and low performers 
print("\nHigh Performers (from graph data):")
for name, avg in top_performers:
    print(f"{name}: {round(avg, 2)}")

print("\nLow Performers (from graph data):")
for name, avg in bottom_performers:
    print(f"{name}: {round(avg, 2)}")
print("\n\n----------------------------------------------------------------------------------------------")
# 5-----------------------------------------------------------------------------------------------------------------------

def get_student_info(student_id, valid_rows, relevant_indices, relevant_columns):
    # Iterating over the rows to find the matching student by ID
    for row in valid_rows:
        if row[relevant_indices['id']] == student_id:
            # If the student ID matches, it will retrieve the student's details
            student_name = f"{row[relevant_indices['first_name']]} {row[relevant_indices['last_name']]}"
            student_surname = row[relevant_indices['last_name']]
            
            # Extracting the grades and corresponding subjects 
            grades = [int(row[relevant_indices[subject]]) for subject in relevant_columns[3:]]
            # Splitting and Capitalizing the subject
            subjects = [subject.split('_')[0].capitalize() for subject in relevant_columns[3:]]  
            
            # Calculating the average score
            average_score = sum(grades) / len(grades)
            
            # Finding the highest and lowest grades and their corresponding subjects
            highest_grade = max(grades)
            lowest_grade = min(grades)
            highest_subject = subjects[grades.index(highest_grade)]
            lowest_subject = subjects[grades.index(lowest_grade)]
            
            # the student's information
            print(f"Student Name: {student_name}")
            print(f"Student ID: {student_id}")
            print(f"Average Grade: {round(average_score, 2)}")
            print(f"Highest Grade: {highest_grade} in {highest_subject}")
            print(f"Lowest Grade: {lowest_grade} in {lowest_subject}")
            return
    
    # The case when no student matches the ID
    print(f"\n\nNo student found with ID: {student_id}")


# Getting student info by calling the function
student_id_input = input("\n\nEnter the student ID: ")
get_student_info(student_id_input, valid_rows, relevant_indices, relevant_columns)



print("\n\n----------------------------------------------------------------------------------------------")
# 6-----------------------------------------------------------------------------------------------------------------------
# The file path for the summary text file
summary_file_path = "C:\\Users\\norga\\Downloads\\Student_Performance_Summary.txt"

# Selecting the first 5 and last 5 students for analysis
selected_students = valid_rows[:5] + valid_rows[-5:]

# Calculating the average score for each student
student_averages = [
    (f"{row[relevant_indices['first_name']]} {row[relevant_indices['last_name']]}", 
     sum(int(row[relevant_indices[subject]]) for subject in relevant_columns[3:]) / len(relevant_columns[3:]))
    for row in selected_students
]

# Sorting from highest to lowest students by the average score 
student_averages_sorted = sorted(student_averages, key=lambda x: x[1], reverse=True)

# Identifying the top and bottom 3 performers 
top_performers = student_averages_sorted[:3]

# Sorting the results to get the lowest average
bottom_performers = sorted(student_averages_sorted, key=lambda x: x[1])[0]  

# The content for the summary
summary_content = (
    "\n\n===========================================\n"
    "            STUDENT PERFORMANCE REPORT\n"
    "===========================================\n\n"
    "SUMMARY OF ANALYSIS\n"
    "- Total Students Analyzed: 10 (First 5 and Last 5)\n"
    "- Top Performer: " + top_performers[0][0] + 
    " (Average Score: " + str(round(top_performers[0][1], 2)) + ")\n"
    "- Bottom Performer: " + bottom_performers[0] + 
    " (Average Score: " + str(round(bottom_performers[1], 2)) + ")\n\n"
    "===========================================\n"
    "Prepared by: Nane, Nare, Norayr and David\n"
)

# Writing the content in the text file
with open(summary_file_path, "w") as file:
    file.write(summary_content)
    
# Printing the results of the summary
print(summary_content)
print("\nSummary report saved to", summary_file_path)
print("~ THE END ~")
