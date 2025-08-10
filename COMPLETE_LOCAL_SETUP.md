# Complete Local Setup Guide
## Multi-Clinic Doctor Appointment System

This guide will walk you through **every single step** to get your appointment system running on your local computer.

---

## 📋 **STEP 1: Download and Install Required Software**

### 1.1 Install Python
1. Go to [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Download Python 3.8 or newer (3.11+ recommended)
3. **Important**: During installation, check "Add Python to PATH"
4. Complete the installation
5. Test by opening Command Prompt/Terminal and typing: `python --version`

### 1.2 Install VS Code (Optional but Recommended)
1. Go to [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. Download and install VS Code
3. Open VS Code and install the "Python" extension by Microsoft

---

## 📁 **STEP 2: Create Your Project Folder**

### 2.1 Create Project Directory
```bash
# Open Command Prompt (Windows) or Terminal (Mac/Linux)
# Navigate to where you want your project (e.g., Desktop)
cd Desktop

# Create project folder
mkdir my-clinic-app
cd my-clinic-app
```

### 2.2 Copy All Project Files
Copy **ALL** of these files from Replit to your `my-clinic-app` folder:

**Main Files:**
- `local_main.py` (your startup file)
- `local_app.py` (Flask app configuration)
- `local_db.py` (database configuration - IMPORTANT!)
- `local_requirements.txt` (dependencies list)
- `models.py` (database models)
- `.env.example` (configuration template)

**Folders and Their Contents:**
- `routes/` folder with all .py files inside
- `templates/` folder with all .html files inside  
- `static/` folder with css/, js/, and any image files

**Optional Files:**
- `README.md`
- `simple_local_setup.md`
- `.vscode/` folder (VS Code configuration)

Your folder should look like:
```
my-clinic-app/
├── local_main.py
├── local_app.py
├── local_db.py          ← IMPORTANT: New file that fixes import issues
├── local_requirements.txt
├── models.py
├── .env.example
├── routes/
│   ├── auth.py
│   ├── booking.py
│   ├── admin.py
│   └── doctor.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── auth/
│   ├── booking/
│   ├── admin/
│   └── doctor/
└── static/
    ├── css/
    ├── js/
    └── images/
```

---

## 🐍 **STEP 3: Set Up Python Virtual Environment**

### 3.1 Create Virtual Environment
```bash
# Make sure you're in your project folder
cd my-clinic-app

# Create virtual environment
python -m venv venv
```

### 3.2 Activate Virtual Environment
**Windows:**
```bash
venv\Scripts\activate
```

**Mac/Linux:**
```bash
source venv/bin/activate
```

**Success Check:** You should see `(venv)` at the beginning of your command prompt

### 3.3 Install Dependencies
```bash
# Install all required packages
pip install -r local_requirements.txt
```

This will install:
- Flask (web framework)
- SQLAlchemy (database)
- Email validator
- Other required packages

---

## ⚙️ **STEP 4: Configuration (Optional)**

### 4.1 Environment Variables (Optional)
If you want custom settings:
```bash
# Copy the example file
copy .env.example .env    # Windows
# cp .env.example .env    # Mac/Linux

# Edit .env file if needed (optional)
```

**Note:** The app works perfectly with default settings, so this step is optional.

---

## 🚀 **STEP 5: Run the Application**

### 5.1 Start the Server
```bash
# Make sure virtual environment is activated (you see (venv))
# Make sure you're in the project folder
python local_main.py
```

### 5.2 What You Should See
```
🏥 Multi-Clinic Appointment System
========================================
Server running at: http://127.0.0.1:5000
Database: SQLite (clinic_appointments.db)
Default Admin: admin@clinic.com / admin123
Sample Doctor: doctor@clinic.com / doctor123
========================================
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

### 5.3 Open Your Browser
1. Open your web browser
2. Go to: `http://localhost:5000` or `http://127.0.0.1:5000`
3. You should see the appointment system homepage

---

## 🏥 **STEP 6: Test the Application**

### 6.1 Login as Admin
- Email: `admin@clinic.com`
- Password: `admin123`
- Test: Create clinics, manage doctors, view appointments

### 6.2 Login as Doctor  
- Email: `doctor@clinic.com`
- Password: `doctor123`
- Test: View schedule, manage appointments, set availability

### 6.3 Register as Patient
- Click "Sign Up" 
- Create a patient account
- Test: Book appointments, view history

### 6.4 Test Booking Flow
1. Login as patient
2. Select "General Medical Center" clinic
3. Choose "Dr. Sarah Johnson"
4. Pick an available time slot
5. Confirm booking

---

## 📊 **STEP 7: VS Code Setup (Optional)**

### 7.1 Open Project in VS Code
```bash
# From your project folder
code .
```

### 7.2 Select Python Interpreter
1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (Mac)
2. Type "Python: Select Interpreter"
3. Choose the one from your `venv` folder

### 7.3 Run with Debugger
1. Press `F5` or go to Run → Start Debugging
2. Choose "Flask Development Server" if prompted

---

## 🗃️ **Understanding Your Local Database**

### What Gets Created Automatically:
- **Database file**: `clinic_appointments.db` in your project folder
- **Admin account**: admin@clinic.com / admin123
- **Sample clinic**: General Medical Center
- **Sample doctor**: Dr. Sarah Johnson (doctor@clinic.com / doctor123)
- **Time slots**: 7 days of available appointments (9 AM-12 PM, 2 PM-5 PM)

### Database File Location:
```
my-clinic-app/
├── clinic_appointments.db  ← Your database file (created automatically)
├── local_main.py
└── ... other files
```

---

## 🔧 **Troubleshooting Common Issues**

### Issue: "Python not found"
**Solution:** Reinstall Python and check "Add to PATH" during installation

### Issue: "Port 5000 already in use"
**Solution:** 
```bash
# Change port in local_main.py, line 11:
port = int(os.environ.get('PORT', 8000))  # Changed from 5000 to 8000
```

### Issue: "Module not found" 
**Solution:**
```bash
# Make sure virtual environment is activated
venv\Scripts\activate    # Windows
# source venv/bin/activate   # Mac/Linux

# Reinstall packages
pip install -r local_requirements.txt
```

### Issue: "(venv) doesn't appear"
**Solution:** Virtual environment not activated
```bash
# Windows
venv\Scripts\activate

# Mac/Linux  
source venv/bin/activate
```

### Issue: "Permission denied"
**Solution:** Run Command Prompt as Administrator (Windows) or use `sudo` (Mac/Linux)

---

## 🎯 **Quick Commands Summary**

```bash
# Navigate to project
cd my-clinic-app

# Activate virtual environment
venv\Scripts\activate           # Windows
source venv/bin/activate        # Mac/Linux

# Install dependencies (first time only)
pip install -r local_requirements.txt

# Run application
python local_main.py

# Open in browser
# http://localhost:5000
```

---

## ✅ **Success Checklist**

- [ ] Python installed and working (`python --version`)
- [ ] Project folder created with all files
- [ ] Virtual environment created and activated (see `(venv)`)
- [ ] Dependencies installed successfully
- [ ] Application starts without errors
- [ ] Can access http://localhost:5000 in browser
- [ ] Can login as admin (admin@clinic.com / admin123)
- [ ] Can register new patient account
- [ ] Can book appointment as patient
- [ ] Database file `clinic_appointments.db` created

**If all items are checked, your local setup is complete and working!**

---

## 🔄 **Daily Usage**

After initial setup, to use the app daily:

1. **Open Command Prompt/Terminal**
2. **Navigate to project**: `cd my-clinic-app`
3. **Activate virtual environment**: `venv\Scripts\activate`
4. **Start app**: `python local_main.py`
5. **Open browser**: `http://localhost:5000`

To stop the app: Press `Ctrl+C` in the terminal

---

## 📞 **Need Help?**

If you encounter issues:
1. Check the troubleshooting section above
2. Make sure all files are copied correctly
3. Verify virtual environment is activated
4. Ensure Python and pip are working
5. Check that port 5000 isn't used by another application

The setup should work smoothly if you follow each step carefully!