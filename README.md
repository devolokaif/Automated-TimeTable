# Automated Timetable Management System

## 📌 Overview
The **Automated Timetable Management System** is designed to generate clash-free master and individual timetables for students and faculty using a **Genetic Algorithm (GA)**.  
It ensures:
- No overlapping of classes for faculty or students.
- Optimized time slot allocation.
- Easy visualization of final timetables.

---

## 🚀 Features
✔ **Automatic Clash Detection** – Prevents overlapping of classes.  
✔ **Faculty & Student Timetables** – Generates individual schedules automatically.  
✔ **Customizable Input** – Works with course, faculty, and slot CSV files.  
✔ **PDF Timetables** – Pre-generated PDFs for quick reference.  

---

## 🛠️ Tech Stack
- **Language:** Python (Genetic Algorithm Implementation)  
- **Database/Files:** CSV & SQL (`project genetic.session.sql`)  
- **Additional:** C test files for quick logic validation.

---

## 📂 Project Structure
Automated-TimeTable/
│
├── ga.py, ga2.py, ga3.py        # Genetic Algorithm code files
├── course_structure.csv         # Course data
├── faculty_course.csv           # Faculty-course mapping
├── slots.csv, timeslots2.csv    # Available time slots
├── MasterTimeTable.pdf          # Generated master timetable
├── EVEN_Semester_*_Timetable.pdf# Semester-wise timetables
├── tt.py                        # Utility scripts
└── project genetic.session.sql  # Database session file

---

## 🧪 How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/devolokaif/Automated-TimeTable.git
   cd Automated-TimeTable
Run the Genetic Algorithm 
    python ga.py

   (Make sure you have Python 3 installed.)

	3.	Check Generated Timetables
PDFs and CSVs will be updated automatically.

🔮 Future Enhancements
	•	Web-based UI for easy timetable visualization.
	•	Integration with a proper database (PostgreSQL/MySQL).
	•	Improved optimization for minimizing free periods.

⸻

🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

⸻

👤 Author

Mohd Kaif
📧 Email: kaifamu03@gmail.com
🌐 GitHub: devolokaif



 
