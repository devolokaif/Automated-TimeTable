import random
import psycopg2
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape,A3,A4,A2
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

# Define a custom page size (width x height in points)
custom_page_size = (650, 800)  # 650 points wide, 800 points tall
custom_page_size2 = (620, 1000)  # 650 points wide, 1000 points tall
custom_page_size3 = (1050, 1300)  # 1050 points wide, 1300 points tall

data_Master=[]

updated_Master_data = [
    ["PERIODS", "I", "II", "III", "IV", "V", "VI", "BREAK", "Laboratories(2:00 PM to 4:15 PM)","Laboratories(2:00 PM to 4:15 PM)"],
    ["DAYS", "8:00-8:50 AM", "8:50-9:40 AM", "9:40-10:30 AM", "10:30-11:20 AM", "11:20-12:10 PM", "12:10-1:00 PM", "1:00-2:00 PM", "Group I", "Group II"],

    ["MON", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E", "L1E" ], # Semester 2
    ["MON", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E", "L1E" ], # Semester 4
    ["MON", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E", "L1E" ], # Semester 6
    ["MON", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E", "L1E" ], # Semester 8

    ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E", "L2E"],
    ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E", "L2E"],
    ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E", "L2E"],
    ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E", "L2E"],

    ["WED", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E", "L3E"],
    ["WED", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E", "L3E"],
    ["WED", " ", "L3M1", "L3M1", "T7", "T9", "T8", "LUNCH", "L3E", "L3E"],
    ["WED", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E", "L3E"],

    ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E","L4E"],
    ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E","L4E"],
    ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E","L4E"],
    ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E","L4E"],

    ["FRI", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", "",""],
    ["FRI", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", "",""],
    ["FRI", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", "",""],
    ["FRI", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", "",""],

    ["SAT", "L6M1", "L6M1", "L6M1", "T4", "T6", "T5", "LUNCH", "L6E", "L6E"],
    ["SAT", "T9", "T9", "T8", "T4", "T6", "T5", "LUNCH", "L6E", "L6E"],
    ["SAT", "T9", "T9", "T8", "T4", "T6", "T5", "LUNCH", "L6E", "L6E"],
    ["SAT", "T9", "T9", "T8", "T4", "T6", "T5", "LUNCH", "L6E", "L6E"],

]

second_table_data2= [["Course No.", "Course Title", "Course Incharge"]]
d2=["COA1912","Computer Programming Lab","Dr. Nadeem Akhtar"]
second_table_data2.append(d2)


def decimal_to_roman(num):
    roman_numerals = [
        ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
        ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
        ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1)
    ]
    result = ""
    for roman, value in roman_numerals:
        while num >= value:
            result += roman
            num -= value
    return result

def generate_timetable_pdf(filename,timetable,semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name):
    # Create a document with landscape orientation
    pdf = SimpleDocTemplate(filename,leftMargin=20,rightMargin=20,topMargin=20,bottomMargin=20,pagesize=landscape(custom_page_size))

    # Create a stylesheet and custom styles
    styles = getSampleStyleSheet()
    centered_heading_style = ParagraphStyle(
        'CenteredHeading',
        parent=styles['Heading2'],
        alignment=1,  # 1 for center alignment
        fontSize=10,
        spaceAfter=8
    )

    paragraph_style = ParagraphStyle(
        'NormalParagraph',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8
    )
    left_aligned_style = ParagraphStyle(
        'LeftAligned',
        parent=styles['BodyText'],
        alignment=0,  # Left alignment
        fontSize=10,  # Smaller font to fit content
        spaceAfter=5,
        leftIndent=50  # Indent the paragraph by 30 points
    )

    paragraph_style_right = ParagraphStyle(
    'RightAlignedParagraph',
    parent=styles['BodyText'],
    fontSize=10,
    spaceAfter=8,
    alignment=2,  # 2 for right alignment
    rightIndent=30  # Indent the paragraph by 30 points
    )

    even_odd=None
    if(semester%2==0):
        year=semester/2
        even_odd="EVEN"
    else:
        year=int(semester/2)+1
        even_odd="ODD"
    year2=decimal_to_roman(year)
    sem = decimal_to_roman(semester)

    # Create the heading and paragraph
    heading = Paragraph(f"COMPUTER ENGINEERING DEPARTMENT<br/>Z.H.COLLEGE OF ENGINEERING AND TECHNOLOGY,A.M.U.,ALIGARH<br/><u>B.Tech {year2} Year {sem} Semester [{even_odd} SEMESTER]</u><br/>", centered_heading_style)
    paragraph = Paragraph(
        "<b>SESSION 2024-25</b>",
        left_aligned_style
    )

    # Add a space between the heading and the table
    space = Spacer(1, 8)
    space2 = Spacer(1, 18)
    # Adjusted sample data for the table (replace this with actual data)
    data = [
        ["Time", "8:00-8:50 AM", "8:50-9:40 AM", "9:40-10:30 AM", "10:30-11:20 AM", "11:20-12:10 PM", "12:10-1:00 PM", "1:00-2:00 PM", "2:00-2:50 PM", "2:50-3:40 PM", "3:40-4:30 PM"],
        ["Monday", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E", "L1E", "L1E" ],
        ["", "L1M1", "L1M1", "L1M1", "L1M2", "L1M2", "L1M2","LUNCH", "T10", "T11", "T12"],
        ["Tuesday", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E", "L2E", "L2E"],
        ["", "L2M1", "L2M1", "L2M1","L2M2", "L2M2", "L2M2","LUNCH", "T11", "T12", "T10"],
        ["Wednesday", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E", "L3E", "L3E"],
        ["", "L3M1", "L3M1", "L3M1", "L3M2", "L3M2", "L3M2","LUNCH", "T12", "T10", "T11"],
        ["Thursday", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E","L4E","L4E"],
        ["", "L4M1", "L4M1", "L4M1", "L4M2", "L4M2", "L4M2","LUNCH", "T10", "T11", "T12"],
        ["Friday", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", "","",""],
        ["", "L5M1", "L5M1", "L5M1", "", "", "","LUNCH", "","",""],
        ["Saturday", "T9", "T9", "T8", "T4", "T6", "T5", "LUNCH", "","",""],
        ["", "L6M1", "L6M1", "L6M1", "L6M2", "L6M2", "L6M2","LUNCH", "L6E", "L6E", "L6E"],

    ]

    # Create the table
    table = Table(data)
    
   # Apply style to the table
    style = TableStyle([
        # (1, 2) refers to the starting cell (column 1, row 2).
        # (3, 2) refers to the ending cell (column 3, row 2).
        ('SPAN', (1, 2), (3, 2),),  # Merge cells for "L1M" from 8:00-10:30 AM on Monday
        ('SPAN', (4, 2), (6, 2),),  
        ('SPAN', (8, 1), (10, 1),), 
        ('SPAN', (7, 1), (7, 12),), 

        ('SPAN', (1, 4), (3, 4),),
        ('SPAN', (4, 4), (6, 4),),  
        ('SPAN', (1, 6), (3, 6),),
        ('SPAN', (4, 6), (6, 6),),  
        ('SPAN', (1, 8), (3, 8),),
        ('SPAN', (4, 8), (6, 8),),  
        ('SPAN', (1, 10), (3, 10),),
        ('SPAN', (1, 12), (3, 12),),
        ('SPAN', (4, 12), (6, 12),),  

        ('SPAN', (0, 3), (0, 4),),
        ('SPAN', (0, 5), (0, 6),),
        ('SPAN', (0, 7), (0, 8),),
        ('SPAN', (0, 9), (0, 10),),
        ('SPAN', (0, 11), (0, 12),),

        ('SPAN', (8, 3), (10, 3),), 
        ('SPAN', (8, 5), (10, 5),), 
        ('SPAN', (8, 7), (10, 7),), 
        ('SPAN', (8, 12), (10, 12),), 

        ('SPAN', (4, 8), (6, 8),), 
        ('SPAN', (4, 12), (6, 12),), 


        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header row background
        ('BACKGROUND', (0, 1), (0, -1), colors.lightgrey),  # Day column background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertical alignment for all cells
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Day column font
        ('FONTSIZE', (0, 0), (-1, 0), 7),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),  # Padding for header row
        ('BACKGROUND', (1, 1), (-1, -1), colors.beige),  # Background color for table cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines
    ])
    table.setStyle(style)

    # Build the PDF
    pdf.build([table])
    print(f"Timetable PDF created: timetable.pdf")

    # Replace placeholders with actual timetable details
    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                # Look up the course and faculty for the slot from the timetable
                for course, timeslot, faculty in timetable:
                    if timeslot == slot:
                        # Match found, replace placeholder
                        course_info = ""
                        # print(semester_courses)
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                #print(course_info)
                                break
                        data[day_index][slot_index] = f"{course_info}\n[{faculty}]"
                        break

    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                data[day_index][slot_index]=""

    #print(data)
    #print(timetable)
    # Create the table
    table = Table(data)
    table.setStyle(style)

    # Second table data
    second_table_data = [["Course No.", "Course Title", "Course Incharge"]]
    for sem,course_no,_,title in semester_courses:
        incharge=""
        for course,_,_,course_incharge in faculties:
            if course==course_no:
                incharge=course_incharge
                for facultyID,Name in facultyID_Name:
                    if facultyID==incharge:
                        incharge=Name
                        break
        second_table_data.append([course_no, title, incharge])

    second_table = Table(second_table_data)

    second_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ])
    second_table.setStyle(second_table_style)


    paragraph2 = Paragraph(
        "[CHAIRMAN]",
        paragraph_style_right
    )
    pdf.build([heading,paragraph, space, table,space2,second_table,paragraph2])
    print(f"Timetable PDF created for {filename}")


def generate_timetable2_pdf(filename,timetable,semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name):
    # Create a document with landscape orientation
    pdf = SimpleDocTemplate(filename,leftMargin=20,rightMargin=20,topMargin=20,bottomMargin=20,pagesize=landscape(custom_page_size2))

    # Create a stylesheet and custom styles
    styles = getSampleStyleSheet()
    centered_heading_style = ParagraphStyle(
        'CenteredHeading',
        parent=styles['Heading2'],
        alignment=1,  # 1 for center alignment
        fontSize=10,
        spaceAfter=0,
        spaceBefore=0
    )

    paragraph_style = ParagraphStyle(
        'NormalParagraph',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8
    )
    left_aligned_style = ParagraphStyle(
        'LeftAligned',
        parent=styles['BodyText'],
        alignment=0,  # Left alignment
        fontSize=10,  # Smaller font to fit content
        spaceAfter=5,
        leftIndent=50  # Indent the paragraph by 30 points
    )

    paragraph_style_right = ParagraphStyle(
    'RightAlignedParagraph',
    parent=styles['BodyText'],
    fontSize=10,
    spaceAfter=8,
    alignment=2,  # 2 for right alignment
    rightIndent=30  # Indent the paragraph by 30 points
    )

    even_odd=None
    if(semester%2==0):
        year=semester/2
        even_odd="EVEN"
    else:
        year=int(semester/2)+1
        even_odd="ODD"
    year2=decimal_to_roman(year)
    sem = decimal_to_roman(semester)

    # Create the heading and paragraph
    heading = Paragraph(f" DEPARTMENT OF COMPUTER ENGINEERING<br/>Z.H.COLLEGE OF ENGINEERING AND TECHNOLOGY,A.M.U.,ALIGARH<br/><u>B.Tech {year2} Year {sem} Semester [{even_odd} SEMESTER TIMETABLE]</u><br/>", centered_heading_style)
    paragraph = Paragraph(
        "<b>SESSION 2024-25</b>",
        left_aligned_style
    )

    # Add a space between the heading and the table
    space = Spacer(1, 8)
    space2 = Spacer(1, 18)

    data = [
        ["PERIODS", "I", "II", "III", "IV", "V", "VI", "BREAK", "Laboratories(2:00 PM to 4:15 PM)","Laboratories(2:00 PM to 4:15 PM)"],
        ["DAYS", "8:00-8:50 AM", "8:50-9:40 AM", "9:40-10:30 AM", "10:30-11:20 AM", "11:20-12:10 PM", "12:10-1:00 PM", "1:00-2:00 PM", "Group I", "Group II"],
        ["MON", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E", "L1E" ],
        ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E", "L2E"], 
        ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E","L4E"],
        ["FRI", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", "",""],
        ["SAT", "T9", "T9", "T8", "T4", "T6", "T5", "LUNCH", "L6E", "L6E"],

    ]

    wed1=["WED", " ", "L3M1", "L3M1", "T7", "T9", "T8", "LUNCH", "L3E", "L3E"]
    wed2=["WED", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E", "L3E"]

    if semester==6:
        data.insert(4,wed1)
    else:
        data.insert(4,wed2)

    # Create the table
    table2= Table(data)

    dynamic_style=[
        # (1, 2) refers to the starting cell (column 1, row 2).
        # (3, 2) refers to the ending cell (column 3, row 2).
        # ('SPAN', (1, 2), (3, 2),),  # Merge cells for "L1M" from 8:00-10:30 AM on Monday
        # ('SPAN', (0, 1), (0, 2),), 
        ('SPAN', (8, 0), (9, 0),), 
        ('SPAN', (7, 2), (7, 7),), 
        ('SPAN', (6, 6), (9, 6),), 

        # ('SPAN', (1, 4), (3, 4),),


        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),  # Header row background
        ('BACKGROUND', (0, 2), (0, -1), colors.lightgrey),  # Day column background
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertical alignment for all cells
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),  # Header font
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Day column font
        ('FONTSIZE', (0, 0), (-1, 0), 10),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),  # Padding for header row
        ('BACKGROUND', (1, 2), (-1, -1), colors.white),  # Background color for table cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines

        ('BACKGROUND', (6, 6), (-1, 6), colors.lightgrey),  # FRIDAY row colour
        ('BACKGROUND', (7, 2), (7, -1), colors.lightgrey)  # LUNCH column colour
    ]
    
    for _,course_code,_,_ in semester_courses:
        if course_code == "COC3800":
            dynamic_style.append(('SPAN', (2, 4), (3, 4))) 
        elif course_code == "COC4990":
            dynamic_style.append(('SPAN', (8, 7), (9, 7))) 
    
    
    # Apply style to the table
    style2 = TableStyle(dynamic_style)
    table2.setStyle(style2)

    # Build the PDF
    pdf.build([table2])
    print(f"Timetable PDF created: timetable2.pdf")

    time2=['L1M1','L1M2','L1E','L2M1','L2M2','L2E','L3M1','L3M2','L3E','L4M1','L4M2','L4E','L5M1','L6M1','L6M2','L6E']

    # Replace placeholders with actual timetable details
    processed_slots = []  # To track replaced slots
    n=[]
    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                # Look up the course and faculty for the slot from the timetable
                for course, timeslot, faculty in timetable:

                    if (timeslot == slot) and (timeslot in time2) and (timeslot not in processed_slots):
                        # Match found, replace placeholder
                        count=0
                        k=slot_index
                        for day in data:
                            for slot in day:
                                if f"{course}\n[" in slot:  # Check if course appears in the formatted string
                                    if slot_index==8:
                                        k += 1
                                        n.append(data[day_index][slot_index])
                                        count+=1
                                        break  # Exit inner loop when found
                                    # else:
                                    #     continue  # Continue outer loop if no match in current day
                            # break  # Exit outer loop when a match is found

                        course_info = ""
                        # print(semester_courses)
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                #print(course_info)
                                break

                        data[day_index][k] = f"{course_info}\n[{faculty}]"
                        processed_slots.append(timeslot)  # Mark slot as processed
                        # if count==1:
                        #     slot_index -= 2
                        break
                         

                    elif (timeslot == slot) and (timeslot in time2):
                        count=0
                        k=slot_index
                        # for day in data:
                        #     for slot in day:
                        #         if day==day_index:
                        #             if f"{course}\n[" in slot:  # Check if course appears in the formatted string
                        #                 # slot_index += 1
                        #                 count+=1
                                        # break  # Exit inner loop when found
                                    # else:
                                    #     continue  # Continue outer loop if no match in current day
                                # break  # Exit outer loop when a match is found
                        
                        course_info = ""
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                break

                        if k==8:
                            
                            if (data[day_index][k] in processed_slots) and ((f"{course}\n[" not in data[day_index][k+1])):
                                data[day_index][k] = f"{course_info}\n[{faculty}]"
                                break
                            
                            elif (data[day_index][k+1] in processed_slots) and ((f"{course}\n[" not in data[day_index][k])):
                                data[day_index][k+1] = f"{course_info}\n[{faculty}]"
                                break
                            
                        elif k==9:

                            if (data[day_index][k-1] in processed_slots) and ((f"{course}\n[" not in data[day_index][k])):
                                data[day_index][k-1] = f"{course_info}\n[{faculty}]"
                                break
                        
                            elif (data[day_index][k] in processed_slots) and ((f"{course}\n[" not in data[day_index][k-1] )):
                                data[day_index][k] = f"{course_info}\n[{faculty}]"
                                break

                            
                            
                            # elif (data[day_index][k-2] in time2) and ((f"{course}\n[" not in data[day_index][k-1])):
                            #     data[day_index][k-2] = f"{course_info}\n[{faculty}]"
                            #     break

                            # elif (data[day_index][k+2] in time2) and ((f"{course}\n[" not in data[day_index][k+1])):
                            #     data[day_index][k+2] = f"{course_info}\n[{faculty}]"
                            #     break

                        # elif count==1:
                        #     if data[day_index][slot_index] in time2:
                        #         data[day_index][slot_index] = f"{course_info}\n[{faculty}]"
                        #         break
                            
                        #     elif data[day_index][slot_index+1] in time2:
                        #         data[day_index][slot_index+1] = f"{course_info}\n[{faculty}]"
                        #         break

                        #     elif data[day_index][slot_index-1] in time2:
                        #         data[day_index][slot_index-1] = f"{course_info}\n[{faculty}]"
                        #         break
                        # else:
                        #     break


                    elif (timeslot == slot) and (timeslot not in time2):
                        # Match found, replace placeholder
                        course_info = ""
                        # print(semester_courses)
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                #print(course_info)
                                break
                        data[day_index][slot_index] = f"{course_info}\n[{faculty}]"
                        break
            elif (data[day_index][slot_index-1] in timeslots):
                course_info = ""
                faculty1 = ""
                time1=""

                for course, timeslot, faculty in timetable:
                    count=0
                    for day in data:
                        for slot in day:
                            if f"{course}\n[" in slot:  # Check if course appears in the formatted string
                                count+=1
                                print(count)

                    if(timeslot in n) and (timeslot in time2) and (count ==1):
                        
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                faculty1 = faculty
                                time1=timeslot
                                print(course_info)
                                
                # if data[day_index][slot_index]==timeslot:
                #     data[day_index][slot_index] = f"{course_info}\n[{faculty1}]"
                    
                if data[day_index][slot_index-1]==time1:
                    data[day_index][slot_index-1] = f"{course_info}\n[{faculty1}]"
                            

    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                data[day_index][slot_index]=""

    for day_index in range(0, 3):
        for slot_index in range(0, 3):
            slot = data[day_index][slot_index]
            print(slot,"\n")
            if (slot == "AMS2622\n[ToD]"):
                data[day_index][slot_index]=""
            # if (day_index==2 and slot_index==2 and f"AMS2622" in slot):
            #     data[day_index][slot_index]=""
    print(n)

    data_Master=data
    #print(data)
    #print(timetable)
    # Create the table
    table2 = Table(data)
    table2.setStyle(style2)

    # Second table data
    second_table_data = [["Course No.", "Course Title", "Course Incharge"]]
    for sem,course_no,_,title in semester_courses:
        incharge=""
        for course,_,_,course_incharge in faculties:
            if course==course_no:
                incharge=course_incharge
                for facultyID,Name in facultyID_Name:
                    if facultyID==incharge:
                        incharge=Name
                        break
        second_table_data.append([course_no, title, incharge])


    # Sort the second_table_data by "Course No." in increasing order

    second_table_data_sorted=sorted(
        second_table_data[1:], 
        key=lambda x: x[0]  # Sort by the "Course No." column
    )

    second_table_data3=second_table_data_sorted
    if semester % 2 ==0:
        for i in range(len(second_table_data3)):
            second_table_data2.append(second_table_data3[i])

    second_table_data_sorted = [second_table_data[0]] + second_table_data_sorted

    second_table_data=second_table_data_sorted


    second_table = Table(second_table_data)

    second_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ])
    second_table.setStyle(second_table_style)


    paragraph2 = Paragraph(
        "[CHAIRMAN]",
        paragraph_style_right
    )
    pdf.build([heading,paragraph, space, table2,space2,second_table,paragraph2])
    print(f"Timetable2 PDF created for {filename}")
    return data_Master



def generate_all_timetables(timetable, courses,timeslots,faculties,facultyID,facultyID_Name):
    # Separate timetables for each semester
    semesters = set(sem for sem,a,b,c in courses)
    
    for semester in semesters:
        semester_courses = [course for course in courses if course[0] == semester]
        semester_timetable = [gene for gene in timetable if gene[0] in [course[1] for course in semester_courses]]
        oe=None
        if semester%2==0:
            oe="EVEN"
        else:
            oe="ODD"

        if semester==1 or semester==2:
            filename = f"{oe}_Semester_{semester}_Timetable.pdf"
            data_Master = generate_timetable_1Y_pdf(filename, semester_timetable, semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name)
            if semester%2==0:
                generate_master_timetable_pdf(data_Master,semester,second_table_data2)

        elif semester==0 or semester==13:
            if semester==0:
                filename="Courses offered to Electronics Dept.pdf"
            elif semester==13:
                filename="Open Elective Course.pdf"

            generate_timetable_oe_ee_pdf(filename, semester_timetable, semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name)

        else:
            filename = f"{oe}_Semester_{semester}_Timetable.pdf"
            generate_timetable_pdf(filename, semester_timetable, semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name)

            filename = f"{oe}_Semester_{semester}_Timetable2.pdf"
            data_Master = generate_timetable2_pdf(filename, semester_timetable, semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name)

            if semester%2==0:
                generate_master_timetable_pdf(data_Master,semester,second_table_data2)


def generate_timetable_1Y_pdf(filename,timetable,semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name):
    # Create a document with landscape orientation
    pdf = SimpleDocTemplate(filename,leftMargin=20,rightMargin=20,topMargin=20,bottomMargin=20,pagesize=landscape(custom_page_size2))

    # Create a stylesheet and custom styles
    styles = getSampleStyleSheet()
    centered_heading_style = ParagraphStyle(
        'CenteredHeading',
        parent=styles['Heading2'],
        alignment=1,  # 1 for center alignment
        fontSize=10,
        spaceAfter=0,
        spaceBefore=0
    )

    paragraph_style = ParagraphStyle(
        'NormalParagraph',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8
    )
    left_aligned_style = ParagraphStyle(
        'LeftAligned',
        parent=styles['BodyText'],
        alignment=0,  # Left alignment
        fontSize=10,  # Smaller font to fit content
        spaceAfter=8,
        leftIndent=80  # Indent the paragraph by 30 points
    )

    paragraph_style_right = ParagraphStyle(
    'RightAlignedParagraph',
    parent=styles['BodyText'],
    fontSize=10,
    spaceAfter=8,
    alignment=2,  # 2 for right alignment
    rightIndent=30  # Indent the paragraph by 30 points
    )

    even_odd=None
    if(semester%2==0):
        year=semester/2
        even_odd="EVEN"
    else:
        year=int(semester/2)+1
        even_odd="ODD"
    year2=decimal_to_roman(year)
    sem = decimal_to_roman(semester)

    # Create the heading and paragraph
    heading = Paragraph(f"DEPARTMENT OF COMPUTER ENGINEERING<br/>Z.H.COLLEGE OF ENGINEERING AND TECHNOLOGY,A.M.U.,ALIGARH<br/><u>B.Tech {year2} Year {sem} Semester (A1A,A1B,A1C)</u><br/>[{even_odd} SEMESTER TIMETABLE]<br/>", centered_heading_style)
    paragraph = Paragraph(
        "<b>SESSION 2024-25</b>",
        left_aligned_style
    )

    # Add a space between the heading and the table
    space = Spacer(1, 8)
    space2 = Spacer(1, 18)

    data = [
        ["PERIODS", "I", "II", "III", "IV", "V", "VI", "BREAK", "Laboratories(2:00 PM to 4:15 PM)"],
        ["DAYS", "8:00-8:50 AM", "8:50-9:40 AM", "9:40-10:30 AM", "10:30-11:20 AM", "11:20-12:10 PM", "12:10-1:00 PM", "1:00-2:00 PM", "Laboratories(2:00 PM to 4:15 PM)"],
        ["MON", "T1", "T2", "T3", "T6", "T5", "T4", "LUNCH", "L1E"],
        ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E"], 
        ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E"],
        ["FRI", "T5", "T6", "T4", "T7", "T8", "", "LUNCH", ""],
        ["SAT", "L6M1", "L6M1", "L6M1", "T4", "T6", "T5", "LUNCH", "L6E"],

    ]

    wed1=["WED", "L3M1", "L3M1", "L3M1", "T7", "T9", "T8", "LUNCH", "L3E"]
    wed2=["WED", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E"]

    if semester==6:
        data.insert(4,wed1)
    else:
        data.insert(4,wed2)

    # Create the table
    table2= Table(data)

    dynamic_style=[
        # (1, 2) refers to the starting cell (column 1, row 2).
        # (3, 2) refers to the ending cell (column 3, row 2).
        # ('SPAN', (1, 2), (3, 2),),  # Merge cells for "L1M" from 8:00-10:30 AM on Monday
        # ('SPAN', (0, 1), (0, 2),), 
        ('SPAN', (1, 7), (3, 7),),
        ('SPAN', (7, 2), (7, 7),), 
        ('SPAN', (8, 0), (8, 1),), 
        ('SPAN', (6, 6), (8, 6),), 
        
        # ('SPAN', (1, 4), (3, 4),),

        # Header rows background and text color
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),  # Background for first two rows
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.black),  # Text color for first two rows

        # Header rows font styles
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),  # Bold font for first two rows
        ('FONTSIZE', (0, 0), (-1, 1), 10),  # Font size for first two rows

        # Column-specific styles
        ('BACKGROUND', (0, 2), (0, -1), colors.lightgrey),  # Background for the "Day" column
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Bold font for the "Day" column

        # Alignment and padding
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertical alignment for all cells
        ('BOTTOMPADDING', (0, 0), (-1, 1), 5),  # Padding for header rows

        # Regular cell styles
        ('BACKGROUND', (1, 2), (-1, -1), colors.white),  # Background color for table cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines

        ('BACKGROUND', (6, 6), (-1, 6), colors.lightgrey),  # FRIDAY row colour
        ('BACKGROUND', (7, 2), (7, -1), colors.lightgrey),  # LUNCH column colour
    ]
    
    # Apply style to the table
    style2 = TableStyle(dynamic_style)
    table2.setStyle(style2)

    # Build the PDF
    pdf.build([table2])
    print(f"Timetable PDF created: timetable2.pdf")

    time2=['L1M1','L1M2','L1E','L2M1','L2M2','L2E','L3M1','L3M2','L3E','L4M1','L4M2','L4E','L5M1','L6M1','L6M2','L6E']

    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                # Look up the course and faculty for the slot from the timetable
                for course, timeslot, faculty in timetable:
                    if timeslot == slot:
                        # Match found, replace placeholder
                        course_info = ""
                        # print(semester_courses)
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                #print(course_info)
                                break
                        data[day_index][slot_index] = f"{course_info}\n[{faculty}]"
                        break

    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                if day_index==6:
                    data[day_index][slot_index]="\n"
                else:
                    data[day_index][slot_index]=""

    data_Master=data

    table = Table(data)
    table.setStyle(style2)

    # Second table data
    second_table_data = [["Course No.", "Course Title", "Course Incharge"]]
    d1=["COA1912","Computer Programming Lab","Dr. Nadeem Akhtar"]
    second_table_data.append(d1)

    second_table = Table(second_table_data)

    second_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ])
    second_table.setStyle(second_table_style)

    
    # Third table data
    third_table_data = [["Abbreviation", "Faculty"]]

    for sem,course_no,_,title in semester_courses:
        fac=[]
        fac3=""
        for course,fac1,_,course_incharge in faculties:
            if course==course_no:
                fac=fac1.split(',')
                for i in fac:
                    if i=="NA2*":
                        i="NA2"
                    for facultyID,Name in facultyID_Name:
                        if facultyID==i:
                            fac3=i
                            if [facultyID, Name] not in third_table_data:
                                third_table_data.append([facultyID, Name])


    preference = {'NA2': 1, 'MI': 2, 'MHK': 3, 'MS': 4,'HJ': 5,'SUA': 6,'MA': 7,'AI':8,'AH': 9}

    third_table_data_sorted = [third_table_data[0]] + sorted(
    third_table_data[1:], 
    key=lambda x: preference.get(x[0], float('inf'))  # Use inf for facultyIDs not in preference
    )

    third_table_data=third_table_data_sorted

    # Split the data into two halves
    mid_index = len(third_table_data) // 2
    first_table_data = third_table_data[:mid_index+1]
    second_table_data = third_table_data[mid_index+1:]
    second_table_data.insert(0,third_table_data[0])

    # Create the two tables
    first_table1 = Table(first_table_data)
    second_table1 = Table(second_table_data)


    third_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ])
    first_table1.setStyle(third_table_style)
    second_table1.setStyle(third_table_style)

    side_by_side_table = Table([
        [first_table1, second_table1]  # Place tables side by side
    ], colWidths=[3 * inch, 3 * inch])  # Adjust column widths as needed

    # Apply styles to the container table (optional)
    side_by_side_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for tables
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),    # Align both tables at the top
    ])

    side_by_side_table.setStyle(side_by_side_style)



    paragraph2 = Paragraph(
        "[CHAIRMAN]",
        paragraph_style_right
    )

    pdf.build([heading,paragraph, space, table,space2,second_table,space2,side_by_side_table,space2,paragraph2])
    print(f"Timetable1Y PDF created for {filename}")

    return data_Master


def generate_timetable_oe_ee_pdf(filename,timetable,semester_courses,timeslots,semester,faculties,facultyID,facultyID_Name):
    # Create a document with landscape orientation
    pdf = SimpleDocTemplate(filename,leftMargin=20,rightMargin=20,topMargin=20,bottomMargin=20,pagesize=landscape(custom_page_size2))

    # Create a stylesheet and custom styles
    styles = getSampleStyleSheet()
    centered_heading_style = ParagraphStyle(
        'CenteredHeading',
        parent=styles['Heading2'],
        alignment=1,  # 1 for center alignment
        fontSize=10,
        spaceAfter=0,
        spaceBefore=0
    )

    paragraph_style = ParagraphStyle(
        'NormalParagraph',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8
    )
    left_aligned_style = ParagraphStyle(
        'LeftAligned',
        parent=styles['BodyText'],
        alignment=0,  # Left alignment
        fontSize=10,  # Smaller font to fit content
        spaceAfter=8,
        leftIndent=80  # Indent the paragraph by 30 points
    )

    paragraph_style_right = ParagraphStyle(
    'RightAlignedParagraph',
    parent=styles['BodyText'],
    fontSize=10,
    spaceAfter=8,
    alignment=2,  # 2 for right alignment
    rightIndent=30  # Indent the paragraph by 30 points
    )

    even_odd=None
    if(semester%2==0):
        year=semester/2
        even_odd="EVEN"
    else:
        year=int(semester/2)+1
        even_odd="ODD"
    year2=decimal_to_roman(year)
    sem = decimal_to_roman(semester)

    # Create the heading and paragraph
    if semester==0:
        heading = Paragraph(f"DEPARTMENT OF COMPUTER ENGINEERING<br/>Z.H.COLLEGE OF ENGINEERING AND TECHNOLOGY,A.M.U.,ALIGARH<br/><u>Computer Engineering course for B.Tech Electonics Engineering Students</u><br/>", centered_heading_style)
    elif semester==13:
        heading = Paragraph(f"DEPARTMENT OF COMPUTER ENGINEERING<br/>Z.H.COLLEGE OF ENGINEERING AND TECHNOLOGY,A.M.U.,ALIGARH<br/><u>Open Elective : COO4470 </u><br/>", centered_heading_style)

    paragraph = Paragraph(
        "<b>SESSION 2024-25</b>",
        left_aligned_style
    )

    # Add a space between the heading and the table
    space = Spacer(1, 8)
    space2 = Spacer(1, 18)

    data = [
        ["PERIODS", "I", "II", "III", "IV", "V", "VI", "BREAK", "Laboratories(2:00 PM to 4:15 PM)"],
        ["DAYS", "8:00-8:50 AM", "8:50-9:40 AM", "9:40-10:30 AM", "10:30-11:20 AM", "11:20-12:10 PM", "12:10-1:00 PM", "1:00-2:00 PM", "Laboratories(2:00 PM to 4:15 PM)"],
        ["MON", "T1", "T1", "T3", "T6", "T5", "T4", "LUNCH", "L1E"],
        ["TUE", "T1", "T3", "T2", "T4", "T6", "T5","LUNCH", "L2E"], 
        ["THU", "T1", "T2", "T3", "T9", "T7", "T8", "LUNCH", "L4E"],
        ["FRI", "T6", "T6", "T4", "T7", "T8", "", "LUNCH", ""],
        ["SAT", "T7", "T9", "T8", "T4", "T6", "T5", "LUNCH", "L6E"]

    ]

    wed1=["WED", "L3M1", "L3M1", "L3M1", "T7", "T9", "T8", "LUNCH", "L3E"]
    wed2=["WED", "T1", "T2", "T3", "T7", "T9", "T8", "LUNCH", "L3E"]

    if semester==6:
        data.insert(4,wed1)
    else:
        data.insert(4,wed2)

    # Create the table
    table2= Table(data)

    dynamic_style=[
        # (1, 2) refers to the starting cell (column 1, row 2).
        # (3, 2) refers to the ending cell (column 3, row 2).
        # ('SPAN', (1, 2), (3, 2),),  # Merge cells for "L1M" from 8:00-10:30 AM on Monday
        # ('SPAN', (0, 1), (0, 2),), 
        # ('SPAN', (1, 7), (3, 7),),
        ('SPAN', (7, 2), (7, 7),), 
        ('SPAN', (8, 0), (8, 1),), 
        ('SPAN', (6, 6), (8, 6),), 
        
        # ('SPAN', (1, 4), (3, 4),),

        # Header rows background and text color
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),  # Background for first two rows
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.black),  # Text color for first two rows

        # Header rows font styles
        ('FONTNAME', (0, 0), (-1, 1), 'Helvetica-Bold'),  # Bold font for first two rows
        ('FONTSIZE', (0, 0), (-1, 1), 10),  # Font size for first two rows

        # Column-specific styles
        ('BACKGROUND', (0, 2), (0, -1), colors.lightgrey),  # Background for the "Day" column
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Bold font for the "Day" column

        # Alignment and padding
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertical alignment for all cells
        ('BOTTOMPADDING', (0, 0), (-1, 1), 5),  # Padding for header rows

        # Regular cell styles
        ('BACKGROUND', (1, 2), (-1, -1), colors.white),  # Background color for table cells
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines

        ('BACKGROUND', (6, 6), (-1, 6), colors.lightgrey),  # FRIDAY row colour
        ('BACKGROUND', (7, 2), (7, -1), colors.lightgrey),  # LUNCH column colour
    ]
    
    # Apply style to the table
    style2 = TableStyle(dynamic_style)
    table2.setStyle(style2)

    # Build the PDF
    pdf.build([table2])
    print(f"Timetable PDF created: timetable2.pdf")

    time2=['L1M1','L1M2','L1E','L2M1','L2M2','L2E','L3M1','L3M2','L3E','L4M1','L4M2','L4E','L5M1','L6M1','L6M2','L6E']

    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                # Look up the course and faculty for the slot from the timetable
                for course, timeslot, faculty in timetable:
                    if timeslot == slot:
                        # Match found, replace placeholder
                        course_info = ""
                        # print(semester_courses)
                        for _,course_code,_,_ in semester_courses:
                            if course_code == course:
                                course_info = course_code  # Get the course info if it matches
                                #print(course_info)
                                break
                        data[day_index][slot_index] = f"{course_info}\n[{faculty}]"
                        break

    for day_index in range(1, len(data)):
        for slot_index in range(1, len(data[day_index])):
            slot = data[day_index][slot_index]
            if slot in timeslots:
                data[day_index][slot_index]="\n"

    table2 = Table(data)
    table2.setStyle(style2)

    second_table_data=[]

    if semester==0:
    # Second table data
        second_table_data = [["Course Code", "Course Title","Class","Classroom/Laboratory","Course Incharge"]]

        class1=["B.Tech (A2EL) IV Semester","B.Tech (A3EL) VI Semester"]
        classroom=["NL-30","ML-09"]
        i=0

        for sem,course_no,_,title in semester_courses:
            incharge=""
            for course,_,_,course_incharge in faculties:
                if course==course_no:
                    incharge=course_incharge
                    for facultyID,Name in facultyID_Name:
                        if facultyID==incharge:
                            incharge=Name
                            break

            second_table_data.append([course_no, title,class1[i],classroom[i], incharge])
            i+=1


    elif semester==13:
        second_table_data = [["Course Code", "Course Title","Course Catogory","Course Incharge"]]
        i=0

        for sem,course_no,_,title in semester_courses:
            incharge=""
            for course,_,_,course_incharge in faculties:
                if course==course_no:
                    incharge=course_incharge
                    for facultyID,Name in facultyID_Name:
                        if facultyID==incharge:
                            incharge=Name
                            break

            second_table_data.append([course_no, title,"OE", incharge])
            i+=1

    second_table = Table(second_table_data)


    second_table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ])

    second_table.setStyle(second_table_style)

    paragraph2 = Paragraph(
        "[CHAIRMAN]",
        paragraph_style_right
    )

    space3=Spacer(1,80)
    pdf.build([heading,paragraph, space, table2,space2,second_table,space3,paragraph2])
    print(f"Timetable PDF created for {filename}")


def generate_master_timetable_pdf(data_Master,semester,second_table_data2):
    # Create a document with landscape orientation
    pdf = SimpleDocTemplate("MasterTimeTable.pdf", pagesize=landscape(custom_page_size3))

    # Here’s a summary of some of the larger built-in page sizes in ReportLab:

    # A0 - pagesizes.A0: 2384 x 3370 points
    # A1 - pagesizes.A1: 1684 x 2384 points
    # A2 - pagesizes.A2: 1191 x 1684 points
    # A3 - pagesizes.A3: 842 x 1191 points

    # Create a stylesheet and custom styles
    styles = getSampleStyleSheet()
    centered_heading_style = ParagraphStyle(
        'CenteredHeading',
        parent=styles['Heading1'],
        alignment=1,  # 1 for center alignment
        fontSize=12,
        spaceAfter=0
    )
    paragraph_style = ParagraphStyle(
        'NormalParagraph',
        parent=styles['BodyText'],
        fontSize=10,
        spaceAfter=8
    )

    left_aligned_style = ParagraphStyle(
        'LeftAligned',
        parent=styles['BodyText'],
        alignment=0,  # Left alignment
        fontSize=10,  # Smaller font to fit content
        spaceAfter=8,
        leftIndent=50  # Indent the paragraph by 80 points
    )

    paragraph_style_right = ParagraphStyle(
        'RightAlignedParagraph',
        parent=styles['BodyText'],
        fontSize=12,
        spaceAfter=10,
        alignment=2  # 2 for right alignment
    )

    # Create the heading and paragraph
    heading = Paragraph(f"<b>DEPARTMENT OF COMPUTER ENGINEERING<br/>Z.H.COLLEGE OF ENGINEERING AND TECHNOLOGY,A.M.U.,ALIGARH<br/><u>MASTER TIMETABLE [EVEN SEMESTER]</u><br/></b>", centered_heading_style)

    paragraph = Paragraph(
        "<b>SESSION 2024-25</b><br/>",
        left_aligned_style
    )

    # Add a space between the heading and the table
    space = Spacer(1, 8)
    space2 = Spacer(1, 28)
    # Adjusted sample data for the table (replace this with actual data)

    # Create the table
    table = Table(updated_Master_data)

    style_data=[
        # # (1, 2) refers to the starting cell (column 1, row 2).
        # # (3, 2) refers to the ending cell (column 3, row 2).
        # ('SPAN', (1, 2), (3, 2),),  # Merge cells for "L1M" from 8:00-10:30 AM on Monday
        ('SPAN', (0, 2), (0, 5),),  
        ('SPAN', (0, 6), (0, 9),), 
        ('SPAN', (0, 10), (0, 13),), 
        ('SPAN', (0, 14), (0, 17),), 
        ('SPAN', (0, 18), (0, 21),), 
        ('SPAN', (0, 22), (0, 25),), 

        # ('SPAN', (1, 4), (3, 4),),
        # ('SPAN', (4, 4), (6, 4),),  
        # ('SPAN', (1, 6), (3, 6),),


        ('SPAN', (8, 0), (9, 0),), 
        ('SPAN', (7, 2), (7, -1),), 

        ('SPAN', (8, 2), (9, 2),),

        ('SPAN', (8, 6), (9, 6),),

        ('SPAN', (8, 10), (9, 10),),
        ('SPAN', (8, 14), (9, 14),),
        ('SPAN', (8, 22), (9, 22),),
        ('SPAN', (1, 22), (3, 22),),

        ('SPAN', (2, 12), (3, 12),),

        ('SPAN', (8, 25), (9, 25),),
        ('SPAN', (6, 18), (9, 21),),
        # ('SPAN', (6, 19), (9, 19),),
        # ('SPAN', (6, 20), (9, 20),),
        # ('SPAN', (6, 21), (9, 21),),



        # Header rows background and text color
        ('BACKGROUND', (0, 0), (-1, 1), colors.lightgrey),  # Background for first two rows
        ('TEXTCOLOR', (0, 0), (-1, 1), colors.black),  # Text color for first two rows

        # Header rows font styles
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),  # Bold font for first two rows
        ('FONTSIZE', (0, 0), (-1, 1), 10),  # Font size for first two rows

        # Column-specific styles
        ('BACKGROUND', (0, 2), (0, -1), colors.lightgrey),  # Background for the "Day" column
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),  # Bold font for the "Day" column

        # Alignment and padding
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for all cells
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Center vertical alignment for all cells
        ('BOTTOMPADDING', (0, 0), (-1, 1), 5),  # Padding for header rows

        # Regular cell styles
        ('BACKGROUND', (1, 2), (-1, -1), colors.white),  # Background color for table cells
        ('GRID', (0, 0), (-1, -1), 0.75, colors.black),  # Grid lines

        ('BACKGROUND', (6, 18), (-1, 21), colors.lightgrey),  # FRIDAY row colour
        ('BACKGROUND', (7, 2), (7, -1), colors.lightgrey),  # LUNCH column colour

        # Custom border line styles
        # Bolden a horizontal line (e.g., line below row 2)
        ('LINEABOVE', (0, 0), (-1, 2), 1.5, colors.black),  # Thickness 2, black color
        # Bolden a horizontal line (e.g., line below row 5)
        ('LINEBELOW', (0, 5), (-1, 5), 1.5, colors.black),  # Thickness 2, black color
        ('LINEBELOW', (0, 9), (-1, 9), 1.5, colors.black),  # Thickness 2, black color
        ('LINEBELOW', (0, 13), (-1, 13), 1.5, colors.black),  # Thickness 2, black color
        ('LINEBELOW', (0, 17), (-1, 17), 1.5, colors.black),  # Thickness 2, black color
        ('LINEBELOW', (0, 21), (-1, 21), 1.5, colors.black),  # Thickness 2, black color
        ('LINEBELOW', (0, 25), (-1, 25), 1.5, colors.black),  # Thickness 2, black color

        # Lighten a vertical line (e.g., column between column 0 and 1)
        ('LINEAFTER', (0, 0), (0, -1), 1.5, colors.black),  # Thickness 1, light grey color
        ('LINEAFTER', (6, 0), (6, -1), 1.5, colors.black),  # Thickness 1, light grey color
        ('LINEAFTER', (7, 0), (7, -1), 1.5, colors.black),  # Thickness 1, light grey color
        ('LINEAFTER', (9, 0), (9, -1), 1.5, colors.black),  # Thickness 1, light grey color

        ('LINEBEFORE', (0, 0), (0, -1), 1.5, colors.black),  # Thickness 1, light grey color
        ('LINEBEFORE', (6, 18), (6, 21), 1.5, colors.black),  # Thickness 1, light grey color
        # # Custom diagonal line for a specific cell (e.g., (2, 5))
        # ('LINEABOVE', (0, 10), (-1, 10), 0.5, colors.grey), 
    ]

    
    # Apply style to the table
    style = TableStyle(style_data)
    table.setStyle(style)

    # Build the PDF
    pdf.build([table])
    print(f"Timetable PDF created: timetable.pdf")

    day_index1=2
    for day_index in range(int(1+semester/2), len(updated_Master_data),4):
        for slot_index in range(1, len(updated_Master_data[day_index])):
            slot = updated_Master_data[day_index][slot_index]
            if (day_index1) < len (data_Master):
                if (semester==2):
                    if(slot_index<(len(updated_Master_data[day_index])-1)):
                        entry=data_Master[int(day_index/4)+2][slot_index]
                        entry=entry.replace("\n", " ")
                        updated_Master_data[day_index][slot_index]=entry

                    elif(slot_index==(len(updated_Master_data[day_index]))):
                        entry=data_Master[int(day_index/4)+2][slot_index-1]
                        entry=entry.replace("\n", " ")
                        updated_Master_data[day_index][slot_index]=entry

                else:
                    entry=data_Master[day_index1][slot_index]
                    if f"OE\n" in entry:
                        entry = "OE/COO4470\n[SUA]"
                    entry=entry.replace("\n", " ")
                    updated_Master_data[day_index][slot_index]=entry

        day_index1=day_index1+1


    # # Replace placeholders with actual timetable details
    # for day_index in range(1, len(data)):
    #     for slot_index in range(1, len(data[day_index])):
    #         slot = data[day_index][slot_index]
    #         if slot in timeslots:
    #             slot_data=[]
    #             # Look up the course and faculty for the slot from the timetable
    #             for course, timeslot, faculty in timetable:
    #                 if timeslot == slot:
    #                     # Match found, replace placeholder
    #                     course_info = ""
    #                     # print(semester_courses)
    #                     for sem,course_code,c,b in semester_courses:
    #                         if sem % 2 == 0:
    #                             if course_code == course:
    #                                 course_info = course_code  # Get the course info if it matches
    #                                 #print(course_info)
    #                                 slot_data.append(f"{course_info}[{faculty}]")
    #             # Join all the elements of slot_data with newline characters and assign it to the cell
    #             data[day_index][slot_index] = "\n".join(slot_data)

    # for day_index in range(:
    #     for slot_index in range(1, len(data[day_index])):
    #         slot = data[day_index][slot_index]
    #         if slot in timeslots:
    #             data[day_index][slot_index]=""

    #print(data)
    #print(timetable)
    # Create the table

    
    # Split the data into two halves
    mid_index = len(second_table_data2) // 2
    first_table_data = second_table_data2[:mid_index+1]
    second_table_data = second_table_data2[mid_index+1:]
    length=-1
    for i in second_table_data:
        length+=1
        if "OE" in i:
            second_table_data[length]=["OE/COO4470","Select.TopicsinComputerEngg.-II","Dr. Sayyed Usman Ahmed"]
    second_table_data.insert(0,second_table_data2[0])

    # Create the two tables
    first_table1 = Table(first_table_data)
    second_table1 = Table(second_table_data)


    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    ])

    first_table1.setStyle(table_style)
    second_table1.setStyle(table_style)

    side_by_side_table = Table([
        [first_table1, second_table1]  # Place tables side by side
    ], colWidths=[7 * inch, 7 * inch])  # Adjust column widths as needed

    # Apply styles to the container table (optional)
    side_by_side_style = TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Center alignment for tables
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),    # Align both tables at the top
    ])

    side_by_side_table.setStyle(side_by_side_style)


    table = Table(updated_Master_data)
    table.setStyle(style)

    
    # second_table = Table(second_table_data2)

    # second_table_style = TableStyle([
    #     ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
    #     ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
    #     ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    #     ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    #     ('GRID', (0, 0), (-1, -1), 1, colors.black),
    #     ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold')
    # ])
    # second_table.setStyle(second_table_style)


    paragraph2 = Paragraph(
        "[CHAIRMAN]",
        paragraph_style_right
    )

    pdf.build([heading,paragraph, space, table,space2,side_by_side_table,space2,paragraph2])
    print(f"Master Timetable PDF created.")





# Connect to PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="tt_project",
            user="postgres",
            password="ubaid"
        )
        return conn
    except Exception as e:
        print(f"Error: {e}")
        return None

# Fetch required data from the database
def fetch_data(conn):
    cur = conn.cursor()

    # Fetch course data
    cur.execute("SELECT Semester, Course_Number,Contact_Periods_LTP,Course_title FROM course_structure")
    # semesters=[row[0] for row in cur.fetchall()]
    courses = cur.fetchall()
    print(courses)

    # Fetch slot data
    cur.execute("SELECT slot FROM slots")
    timeslots = [row[0] for row in cur.fetchall()]
    unique_entries = []
    for item in timeslots:
        if item not in unique_entries:
            unique_entries.append(item)
    timeslots=unique_entries
    print(timeslots)

    # Fetch only faculty data
    cur.execute("SELECT Faculty_ID,Name FROM faculty_id")
    facultyID = [row[0] for row in cur.fetchall()]
    cur.execute("SELECT Faculty_ID,Name FROM faculty_id")
    facultyID_Name=cur.fetchall()
    print(facultyID_Name)
    print(facultyID)

    # Fetch faculty data
    cur.execute("SELECT Course_Number, Faculty, Available_Timeslots,Course_Incharge FROM faculty_course")
    # course_numbers=[row[0] for row in cur.fetchall()]
    faculties = cur.fetchall()
    # print(faculties)

    # Initialize an empty list to store the transformed data
    transformed_data = []

    # Iterate over the list of tuples
    for course, faculty, time,course_incharge in faculties:
        # Check if the third element (time) contains a comma
        if ',' in time:
            # Split the string by commas and append the tuple with the list
            transformed_data.append((course,faculty, time.split(','),course_incharge))
        else:
            # If no comma, just append the tuple with the single time as a list
            transformed_data.append((course,faculty, [time],course_incharge))

    # Print the transformed list of tuples
    faculties=transformed_data
    print(faculties)

    cur.close()
    return courses, timeslots, faculties, facultyID,facultyID_Name

# Create the gene (individual course with timeslot and faculty)
def create_gene(course, timeslot, faculty):
    return (course, timeslot, faculty)

# Function to create a chromosome
def create_chromosome(courses,timeslots, faculties):
    chromosome = []
    t1=[]
    time2=['L1M1','L1M2','L1E','L2M1','L2M2','L2E','L3M1','L3M2','L3E','L4M1','L4M2','L4E','L5M1','L6M1','L6M2','L6E']
    t3=['T8']
    t4=['T7', 'T9']
    excluded_slots=time2+t3+t4
    for i in range(len(timeslots)):
        if timeslots[i] not in excluded_slots:
            t1.append(timeslots[i])
    
    default_timeslots=t1

    for course,faculty,time,_ in faculties:
        if time==['']:
            if 'OE' in course:
                timeslots = ['T8']
            elif 'HM' in course:
                timeslots = ['T7', 'T9']
            else:
                for sem,c,contact,_ in courses:
                    if course==c and (contact=='0-1-2' or contact=='0-2-0' or contact=='0-0-8' or contact=='0-0-12' or contact=='0-0-3'):
                        timeslots=time2
                    else:
                        timeslots=default_timeslots

            timeslot=random.choice(timeslots)
            gene=create_gene(course,timeslot,faculty)
            chromosome.append(gene)



        else:
            timeslots=time
            for sem,c,contact,_ in courses:
                if course==c and (contact=='0-1-2' or contact=='0-2-0' or contact=='0-0-8' or contact=='0-0-12' or contact=='0-0-3'):
                    group1_slot = random.choice(timeslots) 
                    timeslots2=[]
                    for i in range(len(timeslots)):
                        if timeslots[i] not in timeslots2:
                            if timeslots[i]!=group1_slot:
                                timeslots2.append(timeslots[i])
                    if timeslots2==[]:
                        timeslots2=timeslots

                    group2_slot = random.choice(timeslots2) 
                    gene1 = create_gene(course, group1_slot, faculty)
                    gene2 = create_gene(course, group2_slot, faculty)
                    chromosome.append(gene1)
                    chromosome.append(gene2)
            

            timeslot=random.choice(timeslots)
            if timeslot in time2:
                continue
            gene=create_gene(course,timeslot,faculty)
            chromosome.append(gene)
            
        timeslots=default_timeslots

    return chromosome


# Function to count conflicts in a chromosome
def count_conflicts(courses,chromosome,faculties):
    conflicts = 0
    num_genes = len(chromosome)
    time2=['L1M1','L1M2','L1E','L2M1','L2M2','L2E','L3M1','L3M2','L3E','L4M1','L4M2','L4E','L5M1','L6M1','L6M2','L6E']
    
    for i in range(num_genes):
        gene1 = chromosome[i]
        count=0
        z=gene1[0]
        sem1=0
        sem2=0
        for k in range(len(courses)):
            if z == courses[k][1]:
                sem1=courses[k][0]

        for j in range(i + 1, num_genes):
            gene2 = chromosome[j]
            w=gene2[0]
            for k in range(len(courses)):
                if w == courses[k][1]:
                    sem2=courses[k][0]
            
            if (sem1==sem2):
                # Same timeslot for two courses in same semester

                if(gene1[1] == gene2[1]):
                    if (gene1[1] not in time2):
                        conflicts+=1
                        if (gene1[2] == gene2[2] and gene1[2]=='ToD'):
                            conflicts-=1
                    if (gene1[1] in time2):
                        count+=1
                if count > 1:
                        conflicts=conflicts+(count-1)
                    
            
            else:
                # Conflict condition- Same Faculty, Different Courses, Same Timeslot
                if ((sem1%2==0 and sem2%2==0) or (sem1%2!=0 and sem2%2!=0)):
                    if ((gene1[0] != gene2[0] and gene1[1] == gene2[1] and gene1[2] == gene2[2])):
                        conflicts += 1
                        if (gene1[2] == gene2[2] and gene1[2]=='ToD'):
                            conflicts-=1

    # Define parallel slot groups
    parallel_groups = {
        'group1': {
            'lab': ['L1M1', 'L2M1', 'L3M1', 'L4M1'],
            'theory': ['T1', 'T2', 'T3']
        },
        'group2': {
            'lab': ['L1E', 'L2E', 'L3E', 'L4E'],
            'theory': ['T10', 'T11', 'T12']
        }
        # 'group3': {
        #     'lab': ['L5M', 'L6M'],
        #     'theory': ['T7', 'T8', 'T9']
        # },
        # 'group4': {
        #     'lab': ['L6M#'],
        #     'theory': ['T4', 'T5', 'T6']
        # }
    }
    
    for i in range(num_genes):
        gene1 = chromosome[i]
        course1 = gene1[0]
        slot1 = gene1[1]
        faculty1 = gene1[2]
        
        # Get semester for gene1
        sem1 = None
        for sem, c, _ ,_ in courses:
            if c == course1:
                sem1 = sem
                break
        
        # # Check slot restrictions
        # if 'OE' in course1 and slot1 != 'T8':
        #     conflicts += 1
        # if 'HM' in course1 and slot1 not in ['T7', 'T9']:
        #     conflicts += 1
        
        # Check parallel slot conflicts
        for group in parallel_groups.values():
            if slot1 in group['lab']:
                for t_slot in group['theory']:
                    for gene in chromosome:
                        # Get semester for current gene
                        gene_sem = None
                        for sem, c, _,_ in courses:
                            if c == gene[0]:
                                gene_sem = sem
                                break
                        
                        if gene[1] == t_slot and gene_sem == sem1:
                            conflicts += 1
                            break
                            
            elif slot1 in group['theory']:
                for l_slot in group['lab']:
                    for gene in chromosome:
                        # Get semester for current gene
                        gene_sem = None
                        for sem, c, _ ,_ in courses:
                            if c == gene[0]:
                                gene_sem = sem
                                break
                        
                        if gene[1] == l_slot and gene_sem == sem1:
                            conflicts += 1
                            break
    
    return conflicts

# Function to calculate the fitness of an individual
def calculate_fitness(num_conflicts):
    return 1 / (1 + num_conflicts)


def create_individual(courses, timeslots, faculties, generation):
    chromosome = create_chromosome(courses, timeslots, faculties)
    num_conflicts = count_conflicts(courses,chromosome,faculties)
    fitness = calculate_fitness(num_conflicts)
    return {
        "chromosome": chromosome,
        "fitness": fitness,
        "num_conflicts": num_conflicts,
        "generation": generation
    }

# Function to create an initial population
def create_population(pop_size, courses, timeslots, faculties):
    population = []
    for i in range(pop_size):
        individual = create_individual(courses, timeslots, faculties, generation=0)
        population.append(individual)
    return population

def order_population(population):
    # Loop over the entire population
    for i in range(len(population)):
        # Assume the current element is the largest
        max_index = i
        for j in range(i + 1, len(population)):
            # If any element has a higher fitness, update max_index
            if population[j]["fitness"] > population[max_index]["fitness"]:
                max_index = j
        # Swap the fittest found element with the current element
        population[i], population[max_index] = population[max_index], population[i]
    return population

def sum_evaluations(population):
    sum=0
    for individual in population:
        sum+=individual["fitness"]
    return sum

# Function to perform selection (roulette wheel selection)
def select_individuals(population):
    max_fitness = sum_evaluations(population)
    # The uniform() method returns a random floating number between the two specified numbers (both included).
    pick = random.uniform(0, max_fitness)
    current = 0
    for individual in population:
        current += individual["fitness"]
        if current > pick:
            return individual

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1['chromosome']) - 1)
    
    # Create offspring by combining genes from both parents
    offspring1_chromosome = parent1['chromosome'][:crossover_point] + parent2['chromosome'][crossover_point:]
    offspring2_chromosome = parent2['chromosome'][:crossover_point] + parent1['chromosome'][crossover_point:]
    
    return offspring1_chromosome, offspring2_chromosome

def mutate(chromosome, timeslots, faculties,courses, mutation_rate=0.01):
    for i in range(len(chromosome)):
        t1=[]
        time2=['L1M1','L1M2','L1E','L2M1','L2M2','L2E','L3M1','L3M2','L3E','L4M1','L4M2','L4E','L5M1','L6M1','L6M2','L6E']
        t3=['T8']
        t4=['T7', 'T9']
        excluded_slots=time2+t3+t4
        for i in range(len(timeslots)):
            if timeslots[i] not in excluded_slots:
                t1.append(timeslots[i])
        
        default_timeslots=t1

        for course,faculty,time,_ in faculties:
            if time==['']:
                if 'OE' in course:
                    timeslots = ['T8']
                elif 'HM' in course:
                    timeslots = ['T7', 'T9']
                else:
                    for sem,c,contact,_ in courses:
                        if course==c and (contact=='0-1-2' or contact=='0-2-0' or contact=='0-0-8' or contact=='0-0-12' or contact=='0-0-3'):
                            timeslots=time2
                        else:
                            timeslots=default_timeslots
                
                
                if random.random() < mutation_rate:
                # Mutate by randomly assigning a new timeslot or faculty
                    chromosome[i] = (
                        chromosome[i][0],  # Course remains the same
                        random.choice(timeslots),  # Random timeslot mutation
                        # random.choice(faculties[i][1])  # Random faculty mutation
                        chromosome[i][2]  # Faculty remains the same
                    )

            # else:

            #     if random.random() < mutation_rate:
            #         timeslots=time
            #         # Mutate by randomly assigning a new timeslot or faculty
            #         chromosome[i] = (
            #             chromosome[i][0],  # Course remains the same
            #             random.choice(timeslots),  # Random timeslot mutation
            #             # random.choice(faculties[i][1])  # Random faculty mutation
            #             chromosome[i][2]  # Faculty remains the same
            #         )
            
            timeslots=default_timeslots


        # for course,faculty in faculties:
        #     if 'OE' in course:
        #         timeslots = ['T8']
        #     elif 'HM' in course:
        #         timeslots = ['T7', 'T9']
        #     else:
        #         for sem,c,contact in courses:
        #             if course==c and (contact=='0-1-2' or contact=='0-0-3'):
        #                 timeslots=time2


        #     if random.random() < mutation_rate:
        #         # Mutate by randomly assigning a new timeslot or faculty
        #         chromosome[i] = (
        #             chromosome[i][0],  # Course remains the same
        #             random.choice(timeslots),  # Random timeslot mutation
        #             random.choice(faculties[i][1])  # Random faculty mutation
        #         )
        #     timeslots=t1
    return chromosome

def visualize_generation(best_individual, generation,courses):
    print(f"Best individual in generation {generation}:")
    print(f"Fitness: {best_individual['fitness']}")
    print(f"Number of conflicts: {best_individual['num_conflicts']}")
    print("Timetable:")
    for gene in best_individual['chromosome']:
        for sem,course,contact,title in courses:
            if gene[0]==course:
                semester=sem

        print(f"Semester: {semester}, Course: {gene[0]}, Timeslot: {gene[1]}, Faculty: {gene[2]}")
    print("-" * 40)

def genetic_algorithm(pop_size, generations, courses, timeslots, faculties):
    # Create initial population
    population = create_population(pop_size, courses, timeslots, faculties)
    
    for generation in range(generations):
        # Order population by fitness (best first)
        population = order_population(population)
        
        # Visualize the best individual in this generation
        visualize_generation(population[0], generation,courses)
        
        # Select the top half of the population (elitism)
        next_population = population[:pop_size // 2]
        
        # Create offspring through crossover and mutation
        while len(next_population) < pop_size:
            parent1 = random.choice(population[:pop_size // 2])
            parent2 = random.choice(population[:pop_size // 2])
            
            # Crossover
            offspring1_chromosome, offspring2_chromosome = crossover(parent1, parent2)
            
            # Mutate offspring
            offspring1_chromosome = mutate(offspring1_chromosome, timeslots, faculties,courses)
            offspring2_chromosome = mutate(offspring2_chromosome, timeslots, faculties,courses)
            num_conflicts1=count_conflicts(courses, offspring1_chromosome,faculties)
            num_conflicts2=count_conflicts(courses, offspring2_chromosome,faculties)
            
            # Create offspring individuals
            offspring1 = {
                "chromosome": offspring1_chromosome,
                "fitness": calculate_fitness(num_conflicts1),
                "num_conflicts": num_conflicts1,
                "generation": generation + 1
            }
            offspring2 = {
                "chromosome": offspring2_chromosome,
                "fitness": calculate_fitness(num_conflicts2),
                "num_conflicts": num_conflicts2,
                "generation": generation + 1
            }
            
            # Add offspring to next generation
            next_population.append(offspring1)
            next_population.append(offspring2)
        
        # Update population with next generation
        population = next_population
    
    # Return the best individual after all generations
    return population[0]

# # Display the best timetable

# def display_best_timetable(best_timetable):
#     print("\nBest Timetable:")
#     for course, timeslot, faculty in best_timetable:
#         print(f"Course: {course}, Timeslot: {timeslot}, Faculty: {faculty}")

def main():
    conn = connect_db()
    if conn is None:
        return
    
    courses, timeslots, faculties, facultyID,facultyID_Name = fetch_data(conn)

    best_timetable = genetic_algorithm(pop_size=50, generations=30, courses=courses, timeslots=timeslots, faculties=faculties)
    print("\nBest timetable found:")
    visualize_generation(best_timetable, "Final",courses)


    # Run the genetic algorithm
    # best_timetable = genetic_algorithm(conn)

    # Display the best timetable
    # display_best_timetable(best_timetable)
    generate_all_timetables(best_timetable['chromosome'], courses,timeslots,faculties,facultyID,facultyID_Name)
    # generate_master_timetable_pdf(best_timetable['chromosome'], courses,timeslots)
    conflict=count_conflicts(courses,best_timetable['chromosome'],faculties)
    print(conflict)

    # Close the connection
    conn.close()

if __name__ == "__main__":
    main()
