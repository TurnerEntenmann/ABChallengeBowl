import json, os, matplotlib, zipfile, shutil, platform
import numpy as np
import pandas as pd
from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot, Figure, Package, Itemize, Command, Hyperref, Package
from pylatex.utils import NoEscape, escape_latex
from matplotlib.ticker import MaxNLocator
from zipfile import ZipFile
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from pandas import Series, DataFrame
import matplotlib.pyplot as plt


# makes dict to hold answers when entering a student response
AD={}
# makes list to hold answer sets for refrence when showing available ans sets
ansSets=[]

# make answer set dir if it doesn't exist
dirList=os.listdir()
if "Answer_Sets" not in dirList:
    os.mkdir("Answer_Sets")

# home window basics
root=Tk()
root.configure(bg="WhiteSmoke")
root.iconbitmap("abIcon.ico")
root.title("Asset Builders Quiz Bowl")
quitButton=Button(root, text="Exit", command=root.quit, bg="coral")
quitButton.grid(column=3, row=0)

# text editor window
def textEditor():
    # window basics
    window=Toplevel()
    window.configure(bg="WhiteSmoke")
    window.iconbitmap("abIcon.ico")
    window.title=("Answer Editor")
    window.rowconfigure(0, minsize=800, weight=1)
    window.columnconfigure(1, minsize=800, weight=1)

    # allow editing of already created answers
    def openFile():
        # open a file for editing
        filepath = askopenfilename(filetypes=[("All Files", "*.*")])
        if not filepath:
            return
        txt_edit.delete(1.0, END)
        with open(filepath, "r") as input_file:
            text = input_file.read()
            txt_edit.insert(END, text)

    # allows saving of edited answers
    def saveFile():
        # save the current file as a new file
        filepath = asksaveasfilename(
            defaultextension="txt",
            filetypes=[("All Files", "*.*")])
        if not filepath:
            return
        with open(filepath, "w") as output_file:
            text = txt_edit.get(1.0, END)
            output_file.write(text)

    # makes and places the editor
    txt_edit=Text(window)
    txt_edit.grid(row=0, column=1, sticky="nsew")
    
    # makes button frame and places buttons in the frame
    buttonFrame = Frame(window, bd=2, bg="ghost white")
    openButton=Button(buttonFrame, text="Open a File", command=openFile, bg="DeepSkyBlue2")
    openButton.grid(column=0, row=0, sticky="ew")

    saveButton=Button(buttonFrame, text="Save As ...", command=saveFile, bg="DarkSeaGreen")
    saveButton.grid(column=0, row=1, sticky="ew")
    
    doneButton=Button(buttonFrame, text="Done", command=window.destroy, bg="coral")
    doneButton.grid(column=0, row=2, sticky="ew")
    
    buttonFrame.grid(column=0, row=0, sticky="ns")

# button to open answer editor
editButton=Button(root, text="Edit An Answer", command=textEditor, bg="orchid1")
editButton.grid(column=1, row=1)

# frame for list of answer sets
ansFrame=LabelFrame(root, text="Answer Sets", padx=25, pady=5, bg="ghost white")
ansFrame.grid(column=0, row=0, padx=10, pady=2)

# fxn to populate a file frame
def frameSetUp(frameName):
    global ansSets
    os.chdir("Answer_Sets")
    ansSets=os.listdir()
    for set in ansSets:
        Label(frameName, text=set, bg="ghost white").pack(anchor=W)
    os.chdir("..")
frameSetUp(ansFrame)

# refreshes the file frame
def refresh():
    global ansSets
    # destroy all widgets from frame
    for widget in ansFrame.winfo_children():
       widget.destroy()
    os.chdir("Answer_Sets")
    ansSets=os.listdir()
    for set in ansSets:
        Label(ansFrame, text=set, bg="ghost white").pack(anchor=W)
    os.chdir("..")

# fxn to create new ans sets
# must start in highest dir, ends in highest dir
def newSet(name):
    os.chdir("Answer_Sets")
    os.mkdir(name)
    os.chdir("..")
    refresh()

# makes frame, entry slot and button to make new ans sets
nsFrame=LabelFrame(root, text="Create New Set", padx=25, pady=5, bg="ghost white")
nsFrame.grid(column=0, row=2)
nsEntry=Entry(nsFrame, width=20)
nsEntry.grid(column=0,row=0)
nsEntry.insert(0,"Set Name")
nsButton=Button(root, text="Create", command=lambda: newSet(nsEntry.get()), bg="ghost white")
nsButton.grid(column=0, row=3, sticky="ns")

# vars path stuff
savingDirString=""

# fxn to enter new answer
def openAnswerCreator():
    # window set up
    top=Toplevel()
    top.iconbitmap("abIcon.ico")
    top.configure(bg="WhiteSmoke")
    top.state("zoomed")
    top.title("Answer Entry")
    # make scroll bar
    def makeScrollBar():
        global mainFrame, secondFrame, canvas
        mainFrame=Frame(top)
        mainFrame.pack(fill=BOTH, expand=1)
        # create canvas
        canvas=Canvas(mainFrame)
        canvas.pack(side=LEFT, fill=BOTH, expand=1)
        # scroll bar
        sb=Scrollbar(mainFrame, orient=VERTICAL, command=canvas.yview)
        sb.pack(side=RIGHT, fill=Y)
        # configure the canvas
        canvas.configure(yscrollcommand=sb.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        # create another frame in the canvas
        secondFrame=Frame(canvas)
        canvas.create_window((0,0), window=secondFrame, anchor="nw")
    def resetScrollBar():
        global mainFrame, canvas
        mainFrame.update()
        canvas.configure(scrollregion=canvas.bbox("all"))
    makeScrollBar()
    # mouse wheel    
    def mouseWheel(event):
        global canvas
        # windows
        if platform.system()=="Windows":
            canvas.yview_scroll(-1*int(event.delta/120), "units")
        # linux
        if platform.system()=="Linux":
            if event.num==5:
                canvas.yview_scroll(1, "units")
            if event.num==4:
                canvas.yview_scroll(-1, "units")
        # mac
        if platform.system()=="Darwin":
            canvas.yview_scroll(event.delta, "units")
    top.bind("<MouseWheel>", mouseWheel)

    # global vars
    global a1, a2, a3, a3LB, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, a18LB, ansSets, savingDirString, setName
    # makes frame to select which set to save into
    setFrame=LabelFrame(secondFrame, text="Answer Sets", height=500, width=100, padx=5, pady=2, bg="WhiteSmoke")
    setFrame.grid(column=1, row=0, padx=10, pady=2, rowspan=18)
    # makes variables for the saving set as a string var
    setName=StringVar()
    setName.set(None)
    # fxn which takes the selected set to save into and makes the global savingDirString var that set
    # must start in highest dir, ends in highest dir
    def click(value):
        global savingDirString, fnameEntry, mainFrame, canvas
        # sets target dir as a string
        savingDirString=str(value)
        # goes to the selected dir and counts how many responses are in it
        dirPath=os.path.join("Answer_Sets", savingDirString)
        os.chdir(dirPath)
        stuCount=0
        for file in os.listdir():
            if file[-4:]=="json":
                stuCount+=1
        os.chdir("..")
        os.chdir("..")
        # makes file name entry box
        fnameEntry=Entry(secondFrame, width=50)
        fnameEntry.grid(column=2, row=4)
        fnameEntry.insert(0,"Student"+str(stuCount))
        # makes entry frame
        eSetUp()
        # makes save button
        saveButton=Button(secondFrame, text="Save Answers", command=lambda: saveEntries(fnameEntry.get()), bg="DarkSeaGreen")
        saveButton.grid(column=2, row=5)
        resetScrollBar()
    # saves text from entries in AD as a json
    # must start in highest dir, ends in highest dir
    # TODO:
    #     declutter / get rid of old code / vars
    def saveEntries(name):
        global a1, a2, a3, a3LB, a4, a5, a6, a7, a8, a8LB, a9, a9LB, a10, a10LB, a11, a11LB, a12, a13, a14, a14LB, a15, a16, a16LB, a17, q17entry, a18, a18LB, AD, savingDirString, setName, fnameEntry, LBDict
        targetDir=os.path.join("Answer_Sets", savingDirString)
        os.chdir(targetDir)
        # gets answers into strings
        a1=a1.get()
        a2=a2.get()
        List=[]
        for idx in a3LB.curselection():
            List.append(a3LB.get(idx))
        a3=", ".join(List)
        a4=a4.get()
        a5=a5.get()
        a6=a6.get()
        a7=a7.get()
        List=[]
        for idx in a8LB.curselection():
            List.append(a8LB.get(idx))
        a8=", ".join(List)
        List=[]
        for idx in a9LB.curselection():
            List.append(a9LB.get(idx))
        a9=", ".join(List)
        List=[]
        for idx in a10LB.curselection():
            List.append(a10LB.get(idx))
        a10=", ".join(List)
        List=[]
        for idx in a11LB.curselection():
            List.append(a11LB.get(idx))
        a11=", ".join(List)
        a12=a12.get()
        a13=a13.get()
        List=[]
        for idx in a14LB.curselection():
            List.append(a14LB.get(idx))
        a14=", ".join(List)
        a15=a15.get()
        List=[]
        for idx in a16LB.curselection():
            List.append(a16LB.get(idx))
        a16=", ".join(List)
        a17=q17entry.get()
        List=[]
        for idx in a18LB.curselection():
            List.append(a18LB.get(idx))
        a18=", ".join(List)
        answerDict={"Q1":a1, "Q2":a2, "Q3":a3, "Q4":a4, "Q5":a5, "Q6":a6, "Q7":a7, "Q8":a8, "Q9":a9,"Q10":a10, "Q11":a11, "Q12":a12, "Q13":a13, "Q14":a14, "Q15":a15, "Q16":a16, "Q17":a17, "Q18":a18}
        fileName=fnameEntry.get()
        with open(name+".json", "w") as outfile:
            json.dump(answerDict, outfile)
        # updates the name of the file that the answers are saved as
        stuCount=0
        for file in os.listdir():
            if file[-4:]=="json":
                stuCount+=1
        os.chdir("..")
        os.chdir("..")
        # reset entries
        eSetUp()
        # makes file name entry box
        fnameEntry=Entry(secondFrame, width=50)
        fnameEntry.grid(column=2, row=4)
        fnameEntry.insert(0,"Student"+str(stuCount))
    # gets answers from multiple selection questions
    def makeAnsList(LB):
        retList=[]
        for i in LB.curselection():
            retList.append(LB.get(i))
        return retList
    # makes the answer set radio buttons
    rowNum=0
    for aset in ansSets:
        Radiobutton(setFrame, text=aset, variable=setName, value=aset, command=lambda: click(setName.get()), bg="ghost white").grid(column=0, row=rowNum, sticky="W")
        rowNum+=1
    # fxn that sets up entries
    # TODO:
    #     changing dir stacks frames on top of eachother
    #     delete old widgets when updating LBs, entering in new group, entering new student
    #     declutter / get rid of old code / vars
    def eSetUp():
        global a1, a2, a3, a3LB, a4, a5, a6, a7, a8, a8LB, a9, a9LB, a10, a10LB, a11, a11LB, a12, a13, a14, a14LB, a15, a16, a16LB, a17, q17entry, a18, a18LB, savingDirString, mainFrame, canvas, LBDict
        # allows for fast selections
        # makes buttons for free response questions
        def FRQbutton(question, frame, var):
            colNum=0
            rowNum=1
            for ans in ansListDict[question]:
                Radiobutton(frame, text=ans, variable=var, value=ans, bg="ghost white").grid(column=colNum, row=rowNum, sticky="w")
                colNum+=1
                if colNum==2:
                    colNum=0
                    rowNum+=1
        # returns "No Answer" if value==""
        def blankFxn(value):
            if value=="":
                ans="No Answer"
            else:
                ans=value
            return ans
        # dict of lists of free response options
        def makeAnsLists():
            global savingDirString
            # makes a dict of lists for each question
            aListDict={"Q1":[], "Q3":[], "Q8":[], "Q9":[], "Q10":[], "Q11":[], "Q14":[], "Q16":[], "Q17":[], "Q18":[]}
            # goes thu ansFiles, populates aListDict with all answers
            dirPath=os.path.join("Answer_Sets", savingDirString)
            os.chdir(dirPath)
            for file in os.listdir():
                if file[-4:]=="json":
                    with open(file) as json_file:
                        data = json.load(json_file)
                        aListDict["Q1"].append(blankFxn(data["Q1"]))
                        aListDict["Q3"].append(blankFxn(data["Q3"]))
                        aListDict["Q8"].append(blankFxn(data["Q8"]))
                        aListDict["Q9"].append(blankFxn(data["Q9"]))
                        aListDict["Q10"].append(blankFxn(data["Q10"]))
                        aListDict["Q11"].append(blankFxn(data["Q11"]))
                        aListDict["Q14"].append(blankFxn(data["Q14"]))
                        aListDict["Q16"].append(blankFxn(data["Q16"]))
                        aListDict["Q17"].append(blankFxn(data["Q17"]))
                        aListDict["Q18"].append(blankFxn(data["Q18"]))

            for key in aListDict:
                realList=[]
                for answer in aListDict[key]:
                    if ", " in answer:
                        for word in answer.split(", "):
                            realList.append(word)
                    else:
                        realList.append(answer)
                aListDict[key]=list(set(realList))
            resetScrollBar()

            #for key in aListDict:
            #    aListDict[key]=list(set(aListDict[key]))
            # aListDict["Q3"]=list(set(realQ3List))
            os.chdir("..")
            os.chdir("..")
            return aListDict
        ansListDict=makeAnsLists()
        # updates a list of previous answers with newAns
        def updateAnsList(newAns, question, frame, var):
            global mainFrame, canvas
            if len(newAns)>0:
                if newAns not in ansListDict[question]:
                    # updates list
                    ansListDict[question].append(newAns)
                    # makes buttons
                    FRQbutton(question, frame, var)
                    # updates scrollbar
                    resetScrollBar()
        # clears entry boxes
        def clearE(question, frame, hsize=50):
            entryDict[question]=Entry(frame, width=hsize)
            entryDict[question].grid(column=0, row=0)
        # frame for q1
        q1Frame=LabelFrame(secondFrame, text="Q1: what school did you attend?", bg="ghost white")
        q1Frame.grid(column=0, row=0, sticky=W)
        # var and buttons for a1
        a1=StringVar()
        a1.set(None)
        FRQbutton("Q1", q1Frame, a1)
        # entry box for q1
        q1entry=Entry(q1Frame, width=50)
        q1entry.grid(column=0,row=0)
        q1AddButton=Button(q1Frame, text="Add", command=lambda: updateAnsList(q1entry.get(), "Q1", q1Frame, a1), bg="ghost white").grid(column=1, row=0)
        # frame and buttons for q2
        a2=StringVar()
        a2.set(None)
        q2Frame=LabelFrame(secondFrame, text="Q2: what is your grade level?", bg="ghost white")
        q2Frame.grid(column=0, row=1, sticky=W)
        fButton=Radiobutton(q2Frame, text="Freshman", variable=a2, value="Freshman", bg="ghost white").grid(column=0, row=0)
        soButton=Radiobutton(q2Frame, text="Sophomore", variable=a2, value="Sophomer", bg="ghost white").grid(column=1, row=0)
        jButton=Radiobutton(q2Frame, text="Junior", variable=a2, value="Junior", bg="ghost white").grid(column=2, row=0)
        srButton=Radiobutton(q2Frame, text="Senior", variable=a2, value="Senior", bg="ghost white").grid(column=3, row=0)
        # frame for q3
        q3Frame=LabelFrame(secondFrame, text="Q3: What classes are/have you take(n)", bg="ghost white")
        q3Frame.grid(column=0, row=2, sticky=W)
        List=ansListDict["Q3"]
        a3LB=Listbox(q3Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a3LB.grid(column=0, row=1)
        for item in List:
            a3LB.insert(END, item)
        # updates q3LB
        def q3Updater(newAns):
            global a3LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q3"]:
                    ansListDict["Q3"]=[newAns]+ansListDict["Q3"]
                    a3LB=Listbox(q3Frame, selectmode="multiple", width=40, height=len(ansListDict["Q3"]), exportselection=False)
                    for ans in ansListDict["Q3"]:
                        a3LB.insert(END, ans)
                    a3LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q3entry.delete(0, END)
            resetScrollBar()
        # entry box for q3
        q3entry=Entry(q3Frame, width=50)
        q3entry.grid(column=0,row=0)
        q3AddButton=Button(q3Frame, text="Add", command=lambda: q3Updater(q3entry.get()), bg="ghost white").grid(column=7, row=0)        
        # frame and buttons for q4
        a4=StringVar()
        a4.set(None)
        q4Frame=LabelFrame(secondFrame, text="Q4: How well prepared were you for the questions?", bg="ghost white")
        q4Frame.grid(column=0, row=3, sticky=W)
        button41=Radiobutton(q4Frame, text="1", variable=a4, value="1", bg="ghost white").grid(column=0, row=0)
        button42=Radiobutton(q4Frame, text="2", variable=a4, value="2", bg="ghost white").grid(column=1, row=0)
        button43=Radiobutton(q4Frame, text="3", variable=a4, value="3", bg="ghost white").grid(column=2, row=0)
        button44=Radiobutton(q4Frame, text="4", variable=a4, value="4", bg="ghost white").grid(column=3, row=0)
        button45=Radiobutton(q4Frame, text="5", variable=a4, value="5", bg="ghost white").grid(column=4, row=0)
        # frame and buttons for q5
        a5=StringVar()
        a5.set(None)
        q5Frame=LabelFrame(secondFrame, text="Q5: Does FICB content mirror what you learned in school?", bg="ghost white")
        q5Frame.grid(column=0, row=4, sticky=W)
        button51=Radiobutton(q5Frame, text="1", variable=a5, value="1", bg="ghost white").grid(column=0, row=0)
        button52=Radiobutton(q5Frame, text="2", variable=a5, value="2", bg="ghost white").grid(column=1, row=0)
        button53=Radiobutton(q5Frame, text="3", variable=a5, value="3", bg="ghost white").grid(column=2, row=0)
        button54=Radiobutton(q5Frame, text="4", variable=a5, value="4", bg="ghost white").grid(column=3, row=0)
        button55=Radiobutton(q5Frame, text="5", variable=a5, value="5", bg="ghost white").grid(column=4, row=0)
        # frame and buttons for q6
        a6=StringVar()
        a6.set(None)
        q6Frame=LabelFrame(secondFrame, text="Q6: Was the competition format easy to understand?", bg="ghost white")
        q6Frame.grid(column=0, row=5, sticky=W)
        button61=Radiobutton(q6Frame, text="1", variable=a6, value="1", bg="ghost white").grid(column=0, row=0)
        button62=Radiobutton(q6Frame, text="2", variable=a6, value="2", bg="ghost white").grid(column=1, row=0)
        button63=Radiobutton(q6Frame, text="3", variable=a6, value="3", bg="ghost white").grid(column=2, row=0)
        button64=Radiobutton(q6Frame, text="4", variable=a6, value="4", bg="ghost white").grid(column=3, row=0)
        button65=Radiobutton(q6Frame, text="5", variable=a6, value="5", bg="ghost white").grid(column=4, row=0)
        # frame and buttons for q7
        a7=StringVar()
        a7.set(None)
        q7Frame=LabelFrame(secondFrame, text="Q7: I studied the content at www.ficbonline.org", bg="ghost white")
        q7Frame.grid(column=0, row=6, sticky=W)
        button71=Radiobutton(q7Frame, text="1", variable=a7, value="1", bg="ghost white").grid(column=0, row=0)
        button72=Radiobutton(q7Frame, text="2", variable=a7, value="2", bg="ghost white").grid(column=1, row=0)
        button73=Radiobutton(q7Frame, text="3", variable=a7, value="3", bg="ghost white").grid(column=2, row=0)
        button74=Radiobutton(q7Frame, text="4", variable=a7, value="4", bg="ghost white").grid(column=3, row=0)
        button75=Radiobutton(q7Frame, text="5", variable=a7, value="5", bg="ghost white").grid(column=4, row=0)
        # frame for q8
        q8Frame=LabelFrame(secondFrame, text="Q8: How did you prepare for the competition?", bg="ghost white")
        q8Frame.grid(column=0, row=7, sticky=W)
        # var and buttons for a8
        a8=StringVar()
        a8.set(None)
        List=ansListDict["Q8"]
        a8LB=Listbox(q8Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a8LB.grid(column=0, row=1)
        for item in List:
            a8LB.insert(END, item)
        # updates a8LB
        def q8Updater(newAns):
            global a8LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q8"]:
                    ansListDict["Q8"]=[newAns]+ansListDict["Q8"]
                    a8LB=Listbox(q8Frame, selectmode="multiple", width=40, height=len(ansListDict["Q8"]), exportselection=False)
                    for ans in ansListDict["Q8"]:
                        a8LB.insert(END, ans)
                    a8LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q8entry.delete(0, END)
        # entry box for q8
        q8entry=Entry(q8Frame, width=50)
        q8entry.grid(column=0,row=0)
        q8AddButton=Button(q8Frame, text="Add", command=lambda: q8Updater(q8entry.get()), bg="ghost white").grid(column=7, row=0)
        # frame for q9
        q9Frame=LabelFrame(secondFrame, text="Q9: What did you enjoy most about the competition?", bg="ghost white")
        q9Frame.grid(column=0, row=8, sticky=W)
        # var and buttons for a9
        a9=StringVar()
        a9.set(None)
        List=ansListDict["Q9"]
        a9LB=Listbox(q9Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a9LB.grid(column=0, row=1)
        for item in List:
            a9LB.insert(END, item)
        # updates a9LB
        def q9Updater(newAns):
            global a9LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q9"]:
                    ansListDict["Q9"]=[newAns]+ansListDict["Q9"]
                    a9LB=Listbox(q9Frame, selectmode="multiple", width=40, height=len(ansListDict["Q9"]), exportselection=False)
                    for ans in ansListDict["Q9"]:
                        a9LB.insert(END, ans)
                    a9LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q9entry.delete(0, END)
        # entry box for q9
        q9entry=Entry(q9Frame, width=50)
        q9entry.grid(column=0,row=0)
        q9AddButton=Button(q9Frame, text="Add", command=lambda: q9Updater(q9entry.get()), bg="ghost white").grid(column=7, row=0)
        # frame for q10
        q10Frame=LabelFrame(secondFrame, text="Q10: What did you enjoy least about the competition?", bg="ghost white")
        q10Frame.grid(column=0, row=9, sticky=W)
        # var and buttons for a10
        a10=StringVar()
        a10.set(None)
        List=ansListDict["Q10"]
        a10LB=Listbox(q10Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a10LB.grid(column=0, row=1)
        for item in List:
            a10LB.insert(END, item)
        # updates a10LB
        def q10Updater(newAns):
            global a10LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q10"]:
                    ansListDict["Q10"]=[newAns]+ansListDict["Q10"]
                    a10LB=Listbox(q10Frame, selectmode="multiple", width=40, height=len(ansListDict["Q10"]), exportselection=False)
                    for ans in ansListDict["Q10"]:
                        a10LB.insert(END, ans)
                    a10LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q10entry.delete(0, END)
        # entry box for q10
        q10entry=Entry(q10Frame, width=50)
        q10entry.grid(column=0,row=0)
        q10AddButton=Button(q10Frame, text="Add", command=lambda: q10Updater(q10entry.get()), bg="ghost white").grid(column=7, row=0)
        # frame for q11
        q11Frame=LabelFrame(secondFrame, text="Q11: What did you learn as a result of being involved with FCIB?", bg="ghost white")
        q11Frame.grid(column=0, row=10, sticky=W)
        # var and buttons for a11
        a11=StringVar()
        a11.set(None)
        List=ansListDict["Q11"]
        a11LB=Listbox(q11Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a11LB.grid(column=0, row=1)
        for item in List:
            a11LB.insert(END, item)
        # updates a11LB
        def q11Updater(newAns):
            global a11LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q11"]:
                    ansListDict["Q11"]=[newAns]+ansListDict["Q11"]
                    a11LB=Listbox(q11Frame, selectmode="multiple", width=40, height=len(ansListDict["Q11"]), exportselection=False)
                    for ans in ansListDict["Q11"]:
                        a11LB.insert(END, ans)
                    a11LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q11entry.delete(0, END)
        # entry box for q11
        q11entry=Entry(q11Frame, width=50)
        q11entry.grid(column=0,row=0)
        q11AddButton=Button(q11Frame, text="Add", command=lambda: q11Updater(q11entry.get()), bg="ghost white").grid(column=7, row=0)
        # frame and buttons for q12
        a12=StringVar()
        a12.set(None)
        q12Frame=LabelFrame(secondFrame, text="Q12: Did you increase your knowlage about personal finance?", bg="ghost white")
        q12Frame.grid(column=0, row=11, sticky=W)
        yButton12=Radiobutton(q12Frame, text="Yes", variable=a12, value="Yes", bg="ghost white").grid(column=0, row=0)
        nButton12=Radiobutton(q12Frame, text="No", variable=a12, value="No", bg="ghost white").grid(column=1, row=0)
        # frame and buttons for q13
        a13=StringVar()
        a13.set(None)
        q13Frame=LabelFrame(secondFrame, text="Q13: Do you plan to go on to college or higher education?", bg="ghost white")
        q13Frame.grid(column=0, row=12, sticky=W)
        yButton13=Radiobutton(q13Frame, text="Yes", variable=a13, value="Yes", bg="ghost white").grid(column=0, row=0)
        nButton13=Radiobutton(q13Frame, text="No", variable=a13, value="No", bg="ghost white").grid(column=1, row=0)
        # frame for q14
        q14Frame=LabelFrame(secondFrame, text="Q14: How would you improve FICB?", bg="ghost white")
        q14Frame.grid(column=0, row=13, sticky=W)
        # var and buttons for a14
        a14=StringVar()
        a14.set(None)
        List=ansListDict["Q14"]
        a14LB=Listbox(q14Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a14LB.grid(column=0, row=1)
        for item in List:
            a14LB.insert(END, item)
        # updates a14LB
        def q14Updater(newAns):
            global a14LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q14"]:
                    ansListDict["Q14"]=[newAns]+ansListDict["Q14"]
                    a14LB=Listbox(q14Frame, selectmode="multiple", width=40, height=len(ansListDict["Q14"]), exportselection=False)
                    for ans in ansListDict["Q14"]:
                        a14LB.insert(END, ans)
                    a14LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q14entry.delete(0, END)
        # entry box for q14
        q14entry=Entry(q14Frame, width=50)
        q14entry.grid(column=0,row=0)
        q14AddButton=Button(q14Frame, text="Add", command=lambda: q14Updater(q14entry.get()), bg="ghost white").grid(column=7, row=0)
        # frame and buttons for q15
        a15=StringVar()
        a15.set(None)
        q15Frame=LabelFrame(secondFrame, text="Q15: Do you have an account at a bank", bg="ghost white")
        q15Frame.grid(column=0, row=14, sticky=W)
        yButton15=Radiobutton(q15Frame, text="Yes", variable=a15, value="Yes", bg="ghost white").grid(column=0, row=0)
        nButton15=Radiobutton(q15Frame, text="No", variable=a15, value="No", bg="ghost white").grid(column=1, row=0)
        # frame for q16
        q16Frame=LabelFrame(secondFrame, text="Q16: Please describe how others in the community are aware ...", bg="ghost white")
        q16Frame.grid(column=0, row=15, sticky=W)
        # var and buttons for a16
        a16=StringVar()
        a16.set(None)
        List=ansListDict["Q16"]
        a16LB=Listbox(q16Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a16LB.grid(column=0, row=1)
        for item in List:
            a16LB.insert(END, item)
        # updates a16LB
        def q16Updater(newAns):
            global a16LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q16"]:
                    ansListDict["Q16"]=[newAns]+ansListDict["Q16"]
                    a16LB=Listbox(q16Frame, selectmode="multiple", width=40, height=len(ansListDict["Q16"]), exportselection=False)
                    for ans in ansListDict["Q16"]:
                        a16LB.insert(END, ans)
                    a16LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q16entry.delete(0, END)
        # entry box for q16
        q16entry=Entry(q16Frame, width=50)
        q16entry.grid(column=0,row=0)
        q16AddButton=Button(q16Frame, text="Add", command=lambda: q16Updater(q16entry.get()), bg="ghost white").grid(column=7, row=0)
        # frame for q17
        q17Frame=LabelFrame(secondFrame, text="Q17: Share your email if you want", bg="ghost white")
        q17Frame.grid(column=0, row=16, sticky=W)
        # var and buttons for a17
        a17=StringVar()
        a17.set(None)        
        # entry box for q17
        q17entry=Entry(q17Frame, width=50)
        q17entry.grid(column=0,row=0)
        # frame for q18
        q18Frame=LabelFrame(secondFrame, text="Q18: Bonus: what stock would you recommend to invest in for the next year?", bg="ghost white")
        q18Frame.grid(column=0, row=17, sticky=W)
        # var and buttons for a18
        a18=StringVar()
        a18.set(None)
        List=ansListDict["Q18"]
        a18LB=Listbox(q18Frame, selectmode="multiple", width=40, height=len(List), exportselection=False)
        a18LB.grid(column=0, row=1)
        for item in List:
            a18LB.insert(END, item)
        # updates a18LB
        def q18Updater(newAns):
            global a18LB
            if len(newAns)>0:
                if newAns not in ansListDict["Q18"]:
                    ansListDict["Q18"]=[newAns]+ansListDict["Q18"]
                    a18LB=Listbox(q18Frame, selectmode="multiple", width=40, height=len(ansListDict["Q18"]), exportselection=False)
                    for ans in ansListDict["Q18"]:
                        a18LB.insert(END, ans)
                    a18LB.grid(column=0, row=1)
                else:
                    messagebox.showerror("Error", f"{newAns} is already an option")
                q18entry.delete(0, END)
        # entry box for q18
        q18entry=Entry(q18Frame, width=50)
        q18entry.grid(column=0,row=0)
        q18AddButton=Button(q18Frame, text="Add", command=lambda: q18Updater(q18entry.get()), bg="ghost white").grid(column=7, row=0)

        LBDict={"Q3":a3LB, "Q8":a8LB, "Q9":a9LB, "Q10":a10LB, "Q11":a11LB, "Q14":a14LB, "Q16":a16LB, "Q18":a18LB}
        entryDict={"Q1": q1entry, "Q3":q3entry, "Q8":q8entry, "Q9":q9entry, "Q10":q10entry, "Q11":q11entry, "Q14":a14LB, "Q16":a16LB, "Q18":a18LB}

    # makes done button
    doneButton=Button(secondFrame, text="Done", command=top.destroy, bg="coral")
    doneButton.grid(column=2, row=7)

    # makes help page
    def openAddHelp():
        aHelp=Toplevel()
        aHelp.iconbitmap("abIcon.ico")
        aHelp.configure(bg="WhiteSmoke")
        aHelp.title("Help")
        aHelpDoneButton=Button(aHelp, text="Done", command=aHelp.destroy, bg="coral").grid(column=1, row=0)
        
        stepFrame=LabelFrame(aHelp, text="Adding a new answer sheet", padx=5, pady=5, bg="ghost white")
        stepFrame.grid(column=0, row=0)
        Label(stepFrame, text="1) Click the button corresponding to the group that the answer sheet belongs to", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="Question 1:", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -If the school is not on the screen, type it into the entry box and press 'Add'", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -IF the school is on the screen, press the button corresponding to it", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="Question 2, 4, 5, 6, 7, 12, 13, 15:", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -Press the button corresponding to the answer", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="Question 3, 8, 9, 10, 11, 14, 16, 18:", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -If the answer is not on the screen, type it into the entry box and press 'Add', repeat as necessary", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -eg) If the student puts Accounting and Personal Finance as their answer to question 3:", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="        -Type in 'Accounting' then press 'Add' then type in 'Personal Finance' then press add", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="        -Then click both of them", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -After all answers are on the screen, click them so that they are highlighted", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="Question 17:", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="    -Type the email address into the enty box", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="Note: If no answer is provided for any question, leave it blank", bg="ghost white").pack(anchor=W)
        Label(stepFrame, text="2) When all answers are entered, press 'Save Anwers'", bg="ghost white").pack(anchor=W)
    # button to open help page
    addHelpButton=Button(secondFrame, text="Help", command=openAddHelp, bg="LightGoldenRod").grid(column=2, row=8)

# makes button to open answer creator
ACButton=Button(root, text="Add New Student", command=openAnswerCreator, bg="DarkSeaGreen")
ACButton.grid(column=1, row=0)

# summary window
def openSummaryCreator():
    global ansSets, savingDirString, setName
    # set up
    top=Toplevel()
    top.iconbitmap("abIcon.ico")
    top.configure(bg="WhiteSmoke")
    top.title("Summary Creator")
    doneButton=Button(top, text="Done", command=top.destroy, bg="coral")
    doneButton.grid(column=0, row=0)

    # makes variables for the set as a string var and a string
    setName=StringVar()
    setName.set(None)

     # makes frame and buttons to select which set to summarize
    setFrame=LabelFrame(top, text="Choose An Answer Set", padx=5, pady=2, bg="ghost white")
    setFrame.grid(column=1, row=0, padx=10, pady=2, rowspan=2)
    rowNum=0
    for aset in ansSets:
        Radiobutton(setFrame, text=aset, variable=setName, value=aset, command=lambda: sumClick(setName.get()), bg="ghost white").grid(column=0, row=rowNum, sticky="W")
        rowNum+=1
    # makes tournament title entry box
    TNFrame=LabelFrame(top, text="Tournament Name", padx=25, pady=5, bg="ghost white")
    TNFrame.grid(column=1, row=1)
    TNEntry=Entry(TNFrame, width=20)
    TNEntry.grid(column=0,row=0)
    TNEntry.insert(0,"Tournament Name")

    # makes date entry box
    dateFrame=LabelFrame(top, text="Date", padx=25, pady=5, bg="ghost white")
    dateFrame.grid(column=1, row=2)
    dateEntry=Entry(dateFrame, width=20)
    dateEntry.grid(column=0,row=0)

    # make or dont make zipfile
    zipFrame=LabelFrame(top, text="Make a ZipFile of Answer Files", padx=5, pady=2, bg="ghost white")
    zipFrame.grid(column=2, row=0, padx=10, pady=2)
    makeZip=BooleanVar()
    makeZip.set(False)
    Radiobutton(zipFrame, text="Yes", variable=makeZip, value=True, bg="ghost white").grid(column=0, row=0, sticky="W")
    Radiobutton(zipFrame, text="No", variable=makeZip, value=False, bg="ghost white").grid(column=0, row=1, sticky="W")
    # fxn to make default options
    def defaultOptions():
        with open("SummaryOptions.json", "w") as outfile:
            optDict={"width":"11 cm", "topXclasses":7, "cutoffNumber":1}
            json.dump(optDict, outfile)
    # make default options if they don't exist
    if "SummaryOptions.json" not in os.listdir():
        defaultOptions()
    
    # create the summary of the selected set
    def summarize(name):
        logoPath=os.path.abspath("ABLogo.pdf")
        currentOptions={}
        with open("SummaryOptions.json", "r") as infile:
            currentOptions=json.load(infile)
        plt.style.use('tableau-colorblind10')
        dirName=name
        dirPath=os.path.join("Answer_Sets", dirName)
        # make a dir for the summary and its files
        os.chdir(dirPath)
        if not "Summary" in os.listdir():
            os.mkdir("Summary")
        os.chdir("..")
        os.chdir("..")
        # copy logo into summary folder
        shutil.copy("ABLogo.pdf", os.path.join(dirPath, "Summary"))
        # fxn to make nice axies and a list of colorblind-friendly colors
        def get_ax(figsize=(8, 6)):
            fig, ax = plt.subplots(figsize=figsize)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            return ax
        # fxn to make DF from jsons and gets # of jsons
        def makeDF(dirName):
            RN=0
            dirPath=os.path.join("Answer_Sets", name)
            os.chdir(dirPath)
            # DF is horizontal
            DF=DataFrame({"Q1":[], "Q2":[], "Q3":[], "Q4":[], "Q5":[], "Q6":[], "Q7":[], "Q8":[], "Q9":[], "Q10":[], "Q11":[], "Q12":[], "Q13":[], "Q14":[], "Q15":[], "Q16":[], "Q17":[], "Q18":[]})
            for file in os.listdir():
                if file[-4:]=="json":
                    RN+=1
                    with open(file) as json_file:
                        data = json.load(json_file)
                        # dataDF is horizontal
                        dataDF=DataFrame.from_dict(data, orient='index').transpose()
                        DF.loc[len(DF.index)] = list(dataDF.iloc[0])
            return [DF, RN]
        # make DF from jsons and list of schools
        DFRN=makeDF(name)
        bigDF=DFRN[0]
        RN=DFRN[1]
        schools=list(set(bigDF["Q1"])) 
        # make plot of grade distribution in schools in the set
        def gradeSummary(plotFile=os.path.join("Summary","AgeDistributionPlot.pdf"), dataFrame=schools, figSize=(10,8), fsize=20):
            # gets a list of unique schools from bigDF
            # returns dict with schools as keys, list of # of fresh, ... as vals
            def schoolGather(dataFrame):
                schoolDict={}
                for school in dataFrame:
                    schoolDict[school]=[]
                    schoolDF=bigDF[bigDF["Q1"]==school]
                    tempDict={"Freshman":0, "Sophomore":0, "Junior":0, "Senior":0}
                    for ans in schoolDF["Q2"]:
                        if ans == "Freshman":
                            tempDict["Freshman"]+=1
                        if ans == "Sophomore":
                            tempDict["Sophomore"]+=1
                        if ans == "Junior":
                            tempDict["Junior"]+=1
                        if ans == "Senior":
                            tempDict["Senior"]+=1
                    schoolDict[school]=[tempDict["Freshman"], tempDict["Sophomore"], tempDict["Junior"], tempDict["Senior"]]
                return schoolDict
            # makes the plot
            def gradePlotter(plotFile=os.path.join("Summary","AgeDistributionPlot.pdf"), dataFrame=schools, figSize=(10,8), fsize=20):
                ax=get_ax(figSize)
                # makes the lists for #'s of freshman, ...
                schoolDict=schoolGather(dataFrame)
                fList=[]
                soList=[]
                jList=[]
                srList=[]
                for school in schools:
                    fList.append(schoolDict[school][0])
                    soList.append(schoolDict[school][1])
                    jList.append(schoolDict[school][2])
                    srList.append(schoolDict[school][3])
                # makes df with school name as idx, # of freshman, ... as bar lengths
                gradesDF=DataFrame({"School":schools, "Freshman":fList, "Sophomore":soList, "Junior":jList, "Senior":srList})
                gradesDF=gradesDF.set_index("School")
                maxX=max(max(gradesDF["Freshman"]), max(gradesDF["Sophomore"]), max(gradesDF["Junior"]), max(gradesDF["Senior"]))
                gradesDF.plot.barh(ax=ax)
                # graph settings
                handles, labels = ax.get_legend_handles_labels()
                ax.legend(handles[::-1], labels[::-1], fontsize=fsize-2, loc="upper left", bbox_to_anchor=(-0.4, 1), ncol=4)
                plt.xticks(np.arange(0, maxX+1, 1), size=fsize)
                plt.yticks(size=fsize)
                ax.set_xlabel("")
                ax.set_ylabel("")
                ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                plt.tight_layout()
                plt.savefig(plotFile)
            gradePlotter()
        gradeSummary()
        # make plot of top (classNumber) of classes taken
        # makes (bar| x=class, y=Freq) what classes ppl are taking
        def classesSummary(plotFile=os.path.join("Summary", "ClassesTakenPlot.pdf"), classNumber=currentOptions["topXclasses"], dataFrame=schools, figSize=(10,8), fsize=20, DF=bigDF):
            # makes a list of classes taken
            classesNonsep=list(DF["Q3"])
            classes=[]
            for course in classesNonsep:
                classList=course.split(", ")
                for course2 in classList:
                    if course2=="":
                        courseVal="None"
                    else:
                        courseVal=course2
                    classes.append(courseVal)
            # makes a list of unique classes
            uClasses=list(set(classes))
            # make dict with class names as keys, number of times taken as values
            classDict={}
            for course in uClasses:
                classDict[course]=0
                for course2 in classes:
                    if course2==course:
                        classDict[course]+=1
            # makes the plot
            def plotter(plotFile=os.path.join("Summary", "ClassesTakenPlot.pdf"), classNumber=7, dataFrame=schools, figSize=(10,8), fsize=20):
                    ax=get_ax(figSize)
                    # makes and sorts df with class name as idx, # of times taken as bar lengths
                    classesDF=DataFrame.from_dict(classDict, columns=["Times Taken"], orient="index").sort_values(by='Times Taken', ascending=False)
                    classesDF.head(classNumber).plot.barh(ax=ax, color="0")
                    maxX=0
                    for (columnName, columnData) in classesDF.iteritems():
                        if max(classesDF[columnName])>=maxX:
                            maxX=max(classesDF[columnName])
                    # graph settings
                    ax.legend().remove()
                    plt.xticks(np.arange(0, maxX+1, 1), size=fsize)
                    plt.yticks(size=fsize)
                    ax.set_xlabel("")
                    ax.set_ylabel("")
                    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
                    plt.tight_layout()
                    plt.savefig(plotFile)
            plotter()
        classesSummary()
        # make plot of numerical questions
        def numSummary(plotFile=os.path.join("Summary", "NumbersPlot.pdf"), fsize=20):
            # preparation question
            prep=bigDF["Q4"]
            # content question
            cont=bigDF["Q5"]
            # rules question
            rule=bigDF["Q6"]
            # study question
            stud=bigDF["Q7"]
            # list of number of scores
            # prep, cont, rule, stud
            lst1=[0,0,0,0]
            lst2=[0,0,0,0]
            lst3=[0,0,0,0]
            lst4=[0,0,0,0]
            lst5=[0,0,0,0]
            for score in prep:
                if score=="1":
                    lst1[0]+=1
                if score=="2":
                    lst2[0]+=1
                if score=="3":
                    lst3[0]+=1
                if score=="4":
                    lst4[0]+=1
                if score=="5":
                    lst5[0]+=1
            for score in cont:
                if score=="1":
                    lst1[1]+=1
                if score=="2":
                    lst2[1]+=1
                if score=="3":
                    lst3[1]+=1
                if score=="4":
                    lst4[1]+=1
                if score=="5":
                    lst5[1]+=1  
            for score in rule:
                if score=="1":
                    lst1[2]+=1
                if score=="2":
                    lst2[2]+=1
                if score=="3":
                    lst3[2]+=1
                if score=="4":
                    lst4[2]+=1
                if score=="5":
                    lst5[2]+=1       
            for score in stud:
                if score=="1":
                    lst1[3]+=1
                if score=="2":
                    lst2[3]+=1
                if score=="3":
                    lst3[3]+=1
                if score=="4":
                    lst4[3]+=1
                if score=="5":
                    lst5[3]+=1        
            qList=["I Was Well Prepared\nto Compete", "FICB Content Mirrors\nSchool Content", "The Competition Rules Were\nEasy to Understand", "I Studied Content at\nwww.ficbonline.org"]
            numsDF=DataFrame({"Question":qList, "1-Disagree":lst1, "2":lst2, "3":lst3, "4":lst4, "5-Strongly Agree":lst5})
            numsDF=numsDF.set_index("Question")
            maxX=0
            for (columnName, columnData) in numsDF.iteritems():
                if max(numsDF[columnName])>=maxX:
                    maxX=max(numsDF[columnName])
            ax=get_ax((12,9))
            numsDF.plot.barh(ax=ax)
            # graph settings
            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles[::-1], labels[::-1], fontsize=fsize-2, loc="upper left", bbox_to_anchor=(-0.3, 1), ncol=5)
            plt.xticks(np.arange(0, maxX+1, 1), size=fsize)
            plt.yticks(size=fsize)
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout()
            plt.savefig(plotFile)
        numSummary()
        # gets free response data and returns a dict {response, int(times), ...}
        # data is bigDF["QX"]
        def freqList(data):
            def addToDict(name):
                if name not in dataDict:
                    dataDict[name]=1
                else:
                    dataDict[name]+=1
            # list of all responses
            dataList=list(data)
            dataDict={}
            # get count of each response
            for item in dataList:
                if ", " in item:
                    answers=item.split(", ")
                    for ans in answers:
                        if ans=="":
                            name="No Answer"
                        else:
                            name=ans
                        addToDict(name)
                else:
                    if item=="":
                        name="No Answer"
                    else:
                        name=item
                    addToDict(name)
            # sort highest count -> lowest
            dataDict=dict(sorted(dataDict.items(), key=lambda item: item[1], reverse=True))            
            return dataDict
        # make plot for y/n questions
        def ynSummary(plotFile=os.path.join("Summary", "YesNoPlot.pdf"), fsize=20):
            # increase knowlage question
            know=bigDF["Q12"]
            # college question
            coll=bigDF["Q13"]
            # bank account question
            bank=bigDF["Q15"]
            # list of number of scores
            # know, coll, bank
            lstY=[0,0,0]
            lstN=[0,0,0]
            for ans in know:
                if ans=="Yes":
                    lstY[0]+=1
                if ans=="No":
                    lstN[0]+=1
            for ans in coll:
                if ans=="Yes":
                    lstY[1]+=1
                if ans=="No":
                    lstN[1]+=1
            for ans in bank:
                if ans=="Yes":
                    lstY[2]+=1
                if ans=="No":
                    lstN[2]+=1
            qList=["Did you increase your knowledge\nof personal finance?", "Do you plan to attend\ncollege or other higher education?", "Do You have an\naccount at a bank or credit union?"]
            ynDF=DataFrame({"Question":qList, "Yes":lstY, "No":lstN})
            ynDF=ynDF.set_index("Question")
            maxX=0
            for (columnName, columnData) in ynDF.iteritems():
                if max(ynDF[columnName])>=maxX:
                    maxX=max(ynDF[columnName])
            ax=get_ax((12,9))
            ynDF.plot.barh(ax=ax)
            # graph settings
            ax.legend(fontsize=fsize-2, loc="upper left", ncol=2)
            plt.xticks(np.arange(0, maxX+1, 1), size=fsize)
            plt.yticks(size=fsize)
            ax.set_xlabel("")
            ax.set_ylabel("")
            ax.xaxis.set_major_locator(MaxNLocator(integer=True))
            plt.tight_layout()
            plt.savefig(plotFile)
        ynSummary()
        # get emails into a .txt
        def getEmails(textFile=os.path.join("Summary", "Emails.txt")):
            emails=bigDF["Q17"]
            with open(textFile, "w") as file:
                for email in emails:
                    if email!="None":
                        if len(email)>1:
                            file.write(email+"\n")
        getEmails()
        # makes the latex pdf
        # needs MiKTeX
        #   needs to be updated after installatiion
        #   needs to add float package
        # TODO:
        #     refactor / make functions instead of copy paste
        def pdfMaker(name):
            # makes hyperlinks
            def hyperlink(url, text):
                text=escape_latex(text)
                return NoEscape(r'\href{' + url + '}{' + text + '}')
            cutoff=currentOptions["cutoffNumber"]
            plotWidth=currentOptions["width"]
            os.chdir("Summary")
            # LaTeX options
            geometry_options = {"right": "2cm", "left": "2cm"}
            # make LaTeX doc, packages
            doc=Document(geometry_options=geometry_options)
            doc.packages.append(Package("float"))
            doc.packages.append(Package("multicol"))
            doc.packages.append(Package("graphicx"))
            doc.packages.append(Package("hyperref", options="colorlinks=true, urlcolor=blue"))

            # title stuff
            ts0=r'\title{%'+'\n'
            ts1=r'\includegraphics[width=0.25\textwidth]{ABLogo.pdf}~'+'\n'
            ts2=r'\\'+'\n'+r'Finance and Investment Challenge Bowl}'+'\n'
            ts3=r'\author{'+str(TNEntry.get())+" ("+str(RN)+" "+"Responses)}"
            if len(dateEntry.get())>0:
                doc.preamble.append(Command('date', dateEntry.get()))
            else:
                doc.preamble.append(Command('date', NoEscape(r'\today')))

            doc.preamble.append(NoEscape(ts0+ts1+ts2+ts3))
            if len(dateEntry.get())>0:
                doc.preamble.append(Command('date', dateEntry.get()))
            else:
                doc.preamble.append(Command('date', NoEscape(r'\today')))
            doc.append(NoEscape(r'\maketitle'))

            # insert age/school plot
            with doc.create(Section("Distribution of ages in participating schools")):
                with doc.create(Figure(position="H")) as plot1:
                    plot1.add_image("AgeDistributionPlot.pdf", width=plotWidth)
            # insert classes taken plot
            with doc.create(Section("Classes taken by participants")):
                with doc.create(Figure(position="H")) as plot2:
                    plot2.add_image("ClassesTakenPlot.pdf", width=plotWidth)
            # insert number response plot
            with doc.create(Section("Student Preparation")):
                with doc.create(Figure(position="H")) as plot3:
                    plot3.add_image("NumbersPlot.pdf", width=plotWidth)
            # insert y/n response plot
            with doc.create(Section("Yes / No Questions")):
                with doc.create(Figure(position="H")) as plot4:
                    plot4.add_image("YesNoPlot.pdf", width=plotWidth)
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert how ppl studided list
            with doc.create(Section("How Students Prepared")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q8"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            # two columns and a horizontal line sepparating sections
            doc.append(NoEscape(r'\end{multicols}'))
            doc.append(NoEscape(r'\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}'))
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert what ppl enjoyed list
            with doc.create(Section("What Students Enjoyed The Most")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q9"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            doc.append(NoEscape(r'\end{multicols}'))
            doc.append(NoEscape(r'\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}'))
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert what ppl enjoyed least list
            with doc.create(Section("What Students Enjoyed The Least")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q10"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            doc.append(NoEscape(r'\end{multicols}'))
            doc.append(NoEscape(r'\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}'))
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert what ppl learned list
            with doc.create(Section("What Students Learned")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q11"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            doc.append(NoEscape(r'\end{multicols}'))
            doc.append(NoEscape(r'\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}'))
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert how ppl would improve list
            with doc.create(Section("How Students Would Improve FICB")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q14"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            doc.append(NoEscape(r'\end{multicols}'))
            doc.append(NoEscape(r'\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}'))
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert what ppl are aware of list
            with doc.create(Section("How Others in the Students' Communities are Aware of their Participation")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q16"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            doc.append(NoEscape(r'\end{multicols}'))
            doc.append(NoEscape(r'\noindent\makebox[\linewidth]{\rule{\paperwidth}{0.4pt}}'))
            doc.append(NoEscape(r'\begin{multicols}{2}'))
            # insert stock list
            with doc.create(Section("What Stock Students Suggest to Buy")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q18"])
                    for key in Dict:
                        if Dict[key]>=cutoff:
                            if key[-1]==" ":
                                ans=key[:-1]
                            else:
                                ans=key
                            itemize.add_item(ans+": (x"+str(Dict[key])+")")
            doc.append(NoEscape(r'\end{multicols}'))
            # thank you page
            doc.append(NoEscape(r'\pagebreak'))
            with doc.create(Section("Follow Up")):
                doc.append("If you have any questions or would like to learn about how you could be more involved with the FICB please:")
                with doc.create(Itemize()) as itemize:
                    itemize.add_item("Call Richard Entenmann of Asset Builders at (608) 663-6332")
                    itemize.add_item(NoEscape("Visit "+r'\href{www.assetbuilders.org}{www.assetbuilders.org}'))
                    itemize.add_item(NoEscape("Send us an email at "+r'\href{info@assetbuilders.org}{info@assetbuilders.org}'))
                doc.append("Thank you!")
            # generate pdf
            doc.generate_pdf("Summary_of_"+name, clean=True, clean_tex=True, compiler="pdfLatex")
            # delete extra logo file
            os.remove("ABLogo.pdf")
            # return to set dir i.e. "testSet1"
            os.chdir("..")
        pdfMaker(name)

        # get jsons into a zipfile
        if makeZip.get():
            with ZipFile("CompressedAnswers.zip", "w") as studentZip:
                for thing in os.listdir():
                    if thing[-4:]=="json":
                        studentZip.write(thing)

        # return to highest dir
        os.chdir("..")
        os.chdir("..")
        
    # makes the buttons work
    # must start in highest dir, ends in highest dir
    def sumClick(value):
        global savingDirString
        savingDirString=str(value)
        # create the button to execute the summary
        sumButton=Button(top, text="Summarize", command=lambda: summarize(name=value), bg="DarkSeaGreen")
        sumButton.grid(column=3, row=0)
        # sets t name
        TNEntry.delete(0, END)
        TNEntry.insert(0, value)
    # opens page to change options
    def openOptions():
        optWindow=Toplevel()
        optWindow.iconbitmap("abIcon.ico")
        optWindow.configure(bg="WhiteSmoke")
        optWindow.title("Options")
        doneButton=Button(optWindow, text="Done", command=optWindow.destroy, bg="coral")
        doneButton.grid(column=1, row=0)
        # get current options
        currentOptions={}
        with open("SummaryOptions.json", "r") as infile:
            currentOptions=json.load(infile)
        # figsize
        sizeFrame=LabelFrame(optWindow, text="Figure Width", padx=5, pady=5, bg="ghost white")
        sizeFrame.grid(column=0, row=0, sticky=W)
        sizeEntry=Entry(sizeFrame, width=25)
        sizeEntry.insert(0, currentOptions["width"])
        sizeEntry.pack(anchor=W)
        # number of classes shown in fig 2
        numFrame=LabelFrame(optWindow, text="Top __ Classes Shown", padx=5, pady=5, bg="ghost white")
        numFrame.grid(column=0, row=1, sticky=W)
        numEntry=Entry(numFrame, width=25)
        numEntry.insert(0, currentOptions["topXclasses"])
        numEntry.pack(anchor=W)
        # cutoff number for sections 5-11
        cutFrame=LabelFrame(optWindow, text="Cutoff for Free Responses", padx=5, pady=5, bg="ghost white")
        cutFrame.grid(column=0, row=2, sticky=W)
        cutEntry=Entry(cutFrame, width=25)
        cutEntry.insert(0, currentOptions["cutoffNumber"])
        cutEntry.pack(anchor=W)
        # save button
        def saveOptions():
            # ensure good entries
            if "cm" in sizeEntry.get() or "in" in sizeEntry.get():
                # good entry 1
                try:
                    int(numEntry.get())
                    if int(numEntry.get())>0:
                        # good entry 2
                        try:
                            int(cutEntry.get())
                            if int(cutEntry.get())>0:
                                # good entry 3
                                # save the settings
                                with open("SummaryOptions.json", "w") as outfile:
                                    optDict={"width":sizeEntry.get(), "topXclasses":int(numEntry.get()), "cutoffNumber":int(cutEntry.get())}
                                    json.dump(optDict, outfile)
                            else:
                                # cutoff number is not > 0
                                messagebox.showerror("Error", "Cutoff Number must be >=1")
                        except:
                            # cutoff number is not an int
                            messagebox.showerror("Error", "Cutoff Number must be an integer (1,2,3,...) without spaces")
                    else:
                        messagebox.showerror("Error", "Top __ Classes must be >=1")
                except:
                    messagebox.showerror("Error", "Top __ Classes must be an integer (1,2,3,...) without spaces")
            else:
                messagebox.showerror("Error", "Figure width must have either ' in' or ' cm' i.e.\n7 cm")
        saveOpButton=Button(optWindow, text="Save", command=saveOptions, bg="DarkSeaGreen")
        saveOpButton.grid(column=1, row=1)
        # help button
        def helpOptions():
            helpOpWindow=Toplevel()
            helpOpWindow.iconbitmap("abIcon.ico")
            helpOpWindow.configure(bg="WhiteSmoke")
            helpOpWindow.title("Help")
            doneButton=Button(helpOpWindow, text="Done", command=helpOpWindow.destroy, bg="coral")
            doneButton.grid(column=2, row=0, sticky=W)

            sizeLF=LabelFrame(helpOpWindow, text="Changing Figure Width", padx=5, pady=5, bg="ghost white")
            sizeLF.grid(column=0, row=0, sticky=W)
            Label(sizeLF, text="Enter the desired width of the figures", bg="ghost white").pack(anchor=W)
            Label(sizeLF, text="IMPORTANT: You must include either 'cm' or 'in' (without quotation marks)", bg="ghost white").pack(anchor=W)

            numLF=LabelFrame(helpOpWindow, text="Changing the number of classes shown", padx=5, pady=5, bg="ghost white")
            numLF.grid(column=0, row=1, sticky=W)
            Label(numLF, text="This sets the number of classes shown in the plot", bg="ghost white").pack(anchor=W)
            Label(numLF, text="For example, the default setting is 7 so the 7 most popular classes are shown", bg="ghost white").pack(anchor=W)

            cutLF=LabelFrame(helpOpWindow, text="Free Response Cutoff Number", padx=5, pady=5, bg="ghost white")
            cutLF.grid(column=0, row=2, sticky=W)
            Label(cutLF, text="This sets the number of times an answer must be chosen for it to appear in the summary", bg="ghost white").pack(anchor=W)
            Label(cutLF, text="For example, if this is 2, then only answers which have been chosen twice or more will be on the summary", bg="ghost white").pack(anchor=W)
        helpOpButton=Button(optWindow, text="Help", command=helpOptions, bg="LightGoldenrod")
        helpOpButton.grid(column=1, row=2)
        # reset button
        resetButton=Button(optWindow, text="Reset to Defaults", command=defaultOptions, bg="orchid1")
        resetButton.grid(column=1, row=3)
    optButton=Button(top, text="Options", command=openOptions, bg="orchid1")
    optButton.grid(column=0, row=1)



# button to open summary creator
SCButton=Button(root, text="Create Summary", command=openSummaryCreator, bg="DeepSkyBlue2")
SCButton.grid(column=2, row=0)

# home help window
def openHomeHelp():
    top=Toplevel()
    top.iconbitmap("abIcon.ico")
    top.configure(bg="WhiteSmoke")
    top.title("Help")
    doneButton=Button(top, text="Done", command=top.destroy, bg="coral")
    doneButton.grid(column=1, row=0, sticky=W)
    
    groupFrame=LabelFrame(top, text="How to make a new GROUP for answer sheets", padx=5, pady=5, bg="ghost white")
    groupFrame.grid(column=0, row=0 ,sticky=W)
    groupLabel1=Label(groupFrame, text="1) Type in the name of the group into the 'Set Name' field", bg="ghost white").pack(anchor=W)
    groupLabel2=Label(groupFrame, text="2) Press the 'Create' button", bg="ghost white").pack(anchor=W)
    
    ansFrame=LabelFrame(top, text="How to enter a new ANSWER SHEET", padx=5, pady=5, bg="ghost white")
    ansFrame.grid(column=0, row=1, sticky=W)
    ansLabel1=Label(ansFrame, text="1) Press the 'Add New Student' button", bg="ghost white").pack(anchor=W)
    ansLabel2=Label(ansFrame, text="2) Press the button corresponding to the group that the answer sheet belongs to", bg="ghost white").pack(anchor=W)
    ansLabel2a=Label(ansFrame, text="    a) If the correct group does not appear, make a new group by following the steps above", bg="ghost white").pack(anchor=W)
    ansLabel3=Label(ansFrame, text="3) Fill in the answers (see the help page in the Answer Entry window for details)", bg="ghost white").pack(anchor=W)

    sumFrame=LabelFrame(top, text="How to make a SUMMARY", padx=5, pady=5, bg="ghost white")
    sumFrame.grid(column=0, row=2, sticky=W)
    sumLabel1=Label(sumFrame, text="1) Press the 'Create Summary' button", bg="ghost white").pack(anchor=W)
    sumLabel2=Label(sumFrame, text="2) Press the button corresponding to the group that you want to summarize", bg="ghost white").pack(anchor=W)
    sumLabel3=Label(sumFrame, text="3) Press the 'Summarize' button", bg="ghost white").pack(anchor=W)
    sumLabel3a=Label(sumFrame, text="    a) This may take a couple of seconds and may resize the windows, don't worry :)", bg="ghost white").pack(anchor=W)

# button to open home help
HHButton=Button(root, text="Help", command=openHomeHelp, bg="LightGoldenRod")
HHButton.grid(column=2, row=1)


root.mainloop()