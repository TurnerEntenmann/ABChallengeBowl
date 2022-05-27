# TODO
# help screen
# tutorial screen
# graph options
# make scrollbar always work



import json, os, matplotlib
import numpy as np
from pylatex import Document, Section, Subsection, Table, Math, TikZ, Axis, \
    Plot, Figure, Package, Itemize
from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import pandas as pd
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

# starting window basics
root=Tk()
root.title("Asset Builders Quiz Bowl")
quitButton=Button(root, text="Exit", command=root.quit)
quitButton.grid(column=3, row=0)

# text editor window
def textEditor():
    # window basics
    window=Toplevel()
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
    buttonFrame = Frame(window, bd=2)
    openButton=Button(buttonFrame, text="Open a File", command=openFile)
    openButton.grid(column=0, row=0, sticky="ew")

    saveButton=Button(buttonFrame, text="Save As ...", command=saveFile)
    saveButton.grid(column=0, row=1, sticky="ew")
    
    doneButton=Button(buttonFrame, text="Done", command=window.destroy)
    doneButton.grid(column=0, row=2, sticky="ew")
    
    buttonFrame.grid(column=0, row=0, sticky="ns")

# button to open answer editor
editButton=Button(root, text="Edit An Answer", command=textEditor)
editButton.grid(column=1, row=1)

# frame for list of answer sets
ansFrame=LabelFrame(root, text="Answer Sets", padx=25, pady=5)
ansFrame.grid(column=0, row=0, padx=10, pady=2)

# fxn to populate a file frame
def frameSetUp(frameName):
    global ansSets
    os.chdir("Answer_Sets")
    ansSets=os.listdir()
    for set in ansSets:
        Label(frameName, text=set).pack()
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
        Label(ansFrame, text=set).pack()
    os.chdir("..")

# make refresh button
# ?? might not need ??
refButton=Button(root, text="Refresh", command=refresh)
refButton.grid(column=0, row=1)

# fxn to create new ans sets
# must start in highest dir, ends in highest dir
def newSet(name):
    os.chdir("Answer_Sets")
    os.mkdir(name)
    os.chdir("..")
    refresh()

# makes frame, entry slot and button to make new ans sets
nsFrame=LabelFrame(root, text="Create New Set", padx=25, pady=5)
nsFrame.grid(column=0, row=2)
nsEntry=Entry(nsFrame, width=20)
nsEntry.grid(column=0,row=0)
nsEntry.insert(0,"Set Name")
nsButton=Button(nsFrame, text="Create", command=lambda: newSet(nsEntry.get()))
nsButton.grid(column=0, row=1, sticky="ns")

# vars path stuff
savingDirString=""

# fxn to enter new answer
def openAnswerCreator():
    # window set up
    # TODO: make scrollbar work without dragging the window to the top
    top=Toplevel()
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
        #canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.config(scrollregion=mainFrame.bbox())
    makeScrollBar()
    # global vars
    global a1, a2, a3, a3LB, a4, a5, a6, a7, a8, a9, a10, a11, a12, a13, a14, a15, a16, a17, a18, ansSets, savingDirString, setName
    # makes frame to select which set to save into
    setFrame=LabelFrame(secondFrame, text="Answer Sets", height=500, width=100, padx=5, pady=2)
    setFrame.grid(column=1, row=0, padx=10, pady=2, rowspan=18)
    # makes variables for the saving set as a string var
    setName=StringVar()
    setName.set(None)
    # fxn which takes the selected set to save into and makes the global savingDirString var that set
    # must start in highest dir, ends in highest dir
    def click(value):
        global savingDirString, fnameEntry
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
        saveButton=Button(secondFrame, text="Save Answers", command=lambda: saveEntries(fnameEntry.get()))
        saveButton.grid(column=2, row=5)
    # saves text from entries in AD as a json
    # must start in highest dir, ends in highest dir
    def saveEntries(name):
        global a1, a2, a3, a3LB, a4, a5, a6, a7, a8, a8LB, a9, a9LB, a10, a10LB, a11, a11LB, a12, a13, a14, a14LB, a15, a16, a16LB, a17, a18, AD, savingDirString, setName, fnameEntry
        targetDir=os.path.join("Answer_Sets", savingDirString)
        os.chdir(targetDir)
        # gets answers into strings
        a1=a1.get()
        a2=a2.get()
        # TODO: fix a3 (multi select)
        # must be string with entries sep by ", "
        # e.g. merp, derp
        a3List=makeAnsList(a3LB)
        a3=", ".join(a3List)
        a4=a4.get()
        a5=a5.get()
        a6=a6.get()
        a7=a7.get()
        a8List=makeAnsList(a8LB)
        a8=", ".join(a8List)
        a9List=makeAnsList(a9LB)
        a9=", ".join(a9List)
        a10List=makeAnsList(a10LB)
        a10=", ".join(a10List)
        a11List=makeAnsList(a11LB)
        a11=", ".join(a11List)
        a12=a12.get()
        a13=a13.get()
        a14List=makeAnsList(a14LB)
        a14=", ".join(a14List)
        a15=a15.get()
        a16List=makeAnsList(a16LB)
        a16=", ".join(a16List)
        a17=a17.get()
        a18=a18.get()
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
        Radiobutton(setFrame, text=aset, variable=setName, value=aset, command=lambda: click(setName.get())).grid(column=0, row=rowNum)
        rowNum+=1
    # fxn that sets up entries
    # TODO: changing dir stacks frames on top of eachother
    def eSetUp():
        global a1, a2, a3, a3LB, a4, a5, a6, a7, a8, a8LB, a9, a9LB, a10, a10LB, a11, a11LB, a12, a13, a14, a14LB, a15, a16, a16LB, a17, a18, savingDirString, mainFrame, canvas
        # allows for fast selections
        # makes buttons for free response questions
        def FRQbutton(question, frame, var):
            colNum=0
            rowNum=1
            if question!="Q3":
                for ans in ansListDict[question]:
                    Radiobutton(frame, text=ans, variable=var, value=ans).grid(column=colNum, row=rowNum, sticky="w")
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
            # if it is a mult choice, we want each ans to be a button
            #TODO; fix a3
            realQ3List=[]
            for answer in aListDict["Q3"]:
                answerList=answer.split(", ")
                if len(answerList)>1:
                    for ans in answerList:
                        realQ3List.append(ans)
                else:
                    realQ3List.append(answer)
            aListDict["Q3"]=realQ3List
            for key in aListDict:
                aListDict[key]=list(set(aListDict[key]))
            # aListDict["Q3"]=list(set(realQ3List))
            os.chdir("..")
            os.chdir("..")
            return aListDict
        ansListDict=makeAnsLists()
        # updates a list of previous answers with newAns
        def updateAnsList(newAns, question, frame, var):
            global mainFrame, canvas
            # updates list
            ansListDict[question].append(newAns)
            # makes buttons
            FRQbutton(question, frame, var)
            # updates scrollbar
            resetScrollBar()
        # frame for q1
        q1Frame=LabelFrame(secondFrame, text="Q1: what school did you attend?")
        q1Frame.grid(column=0, row=0)
        # var and buttons for a1
        a1=StringVar()
        a1.set(None)
        FRQbutton("Q1", q1Frame, a1)
        # entry box for q1
        q1entry=Entry(q1Frame, width=50)
        q1entry.grid(column=0,row=0)
        q1AddButton=Button(q1Frame, text="Add", command=lambda: updateAnsList(q1entry.get(), "Q1", q1Frame, a1)).grid(column=1, row=0)
        
        # frame and buttons for q2
        a2=StringVar()
        a2.set(None)
        q2Frame=LabelFrame(secondFrame, text="Q2: what is your grade level?")
        q2Frame.grid(column=0, row=1)
        fButton=Radiobutton(q2Frame, text="Freshman", variable=a2, value="Freshman").grid(column=0, row=0)
        soButton=Radiobutton(q2Frame, text="Sophomore", variable=a2, value="Sophomer").grid(column=1, row=0)
        jButton=Radiobutton(q2Frame, text="Junior", variable=a2, value="Junior").grid(column=2, row=0)
        srButton=Radiobutton(q2Frame, text="Senior", variable=a2, value="Senior").grid(column=3, row=0)
        
        
        # frame for q3
        q3Frame=LabelFrame(secondFrame, text="Q3: What classes are/have you take(n)")
        q3Frame.grid(column=0, row=2)
        # var and buttons for a3
        a3=StringVar()
        a3.set(None)
        List=ansListDict["Q3"]
        a3LB=Listbox(q3Frame, selectmode="multiple")
        a3LB.grid(column=0, row=1)
        for item in List:
            a3LB.insert(END, item)
        # updates a3LB
        def q3Updater(newAns):
            ansListDict["Q3"].append(newAns)
            a3LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q3
        q3entry=Entry(q3Frame, width=50)
        q3entry.grid(column=0,row=0)
        q3AddButton=Button(q3Frame, text="Add", command=lambda: q3Updater(q3entry.get())).grid(column=7, row=0)
        # frame and buttons for q4
        a4=StringVar()
        a4.set(None)
        q4Frame=LabelFrame(secondFrame, text="Q4: How well prepared were you for the questions?")
        q4Frame.grid(column=0, row=3)
        button41=Radiobutton(q4Frame, text="1", variable=a4, value="1").grid(column=0, row=0)
        button42=Radiobutton(q4Frame, text="2", variable=a4, value="2").grid(column=1, row=0)
        button43=Radiobutton(q4Frame, text="3", variable=a4, value="3").grid(column=2, row=0)
        button44=Radiobutton(q4Frame, text="4", variable=a4, value="4").grid(column=3, row=0)
        button45=Radiobutton(q4Frame, text="5", variable=a4, value="5").grid(column=4, row=0)
        # frame and buttons for q5
        a5=StringVar()
        a5.set(None)
        q5Frame=LabelFrame(secondFrame, text="Q5: Does FICB content mirror what you learned in school?")
        q5Frame.grid(column=0, row=4)
        button51=Radiobutton(q5Frame, text="1", variable=a5, value="1").grid(column=0, row=0)
        button52=Radiobutton(q5Frame, text="2", variable=a5, value="2").grid(column=1, row=0)
        button53=Radiobutton(q5Frame, text="3", variable=a5, value="3").grid(column=2, row=0)
        button54=Radiobutton(q5Frame, text="4", variable=a5, value="4").grid(column=3, row=0)
        button55=Radiobutton(q5Frame, text="5", variable=a5, value="5").grid(column=4, row=0)
        # frame and buttons for q6
        a6=StringVar()
        a6.set(None)
        q6Frame=LabelFrame(secondFrame, text="Q6: Was the competition format easy to understand?")
        q6Frame.grid(column=0, row=5)
        button61=Radiobutton(q6Frame, text="1", variable=a6, value="1").grid(column=0, row=0)
        button62=Radiobutton(q6Frame, text="2", variable=a6, value="2").grid(column=1, row=0)
        button63=Radiobutton(q6Frame, text="3", variable=a6, value="3").grid(column=2, row=0)
        button64=Radiobutton(q6Frame, text="4", variable=a6, value="4").grid(column=3, row=0)
        button65=Radiobutton(q6Frame, text="5", variable=a6, value="5").grid(column=4, row=0)
        # frame and buttons for q7
        a7=StringVar()
        a7.set(None)
        q7Frame=LabelFrame(secondFrame, text="Q7: I studied the content at www.ficbonline.org")
        q7Frame.grid(column=0, row=6)
        button71=Radiobutton(q7Frame, text="1", variable=a7, value="1").grid(column=0, row=0)
        button72=Radiobutton(q7Frame, text="2", variable=a7, value="2").grid(column=1, row=0)
        button73=Radiobutton(q7Frame, text="3", variable=a7, value="3").grid(column=2, row=0)
        button74=Radiobutton(q7Frame, text="4", variable=a7, value="4").grid(column=3, row=0)
        button75=Radiobutton(q7Frame, text="5", variable=a7, value="5").grid(column=4, row=0)
        # frame for q8
        q8Frame=LabelFrame(secondFrame, text="Q8: How did you prepare for the competition?")
        q8Frame.grid(column=0, row=7)
        # var and buttons for a8
        a8=StringVar()
        a8.set(None)
        List=ansListDict["Q8"]
        a8LB=Listbox(q8Frame, selectmode="multiple")
        a8LB.grid(column=0, row=1)
        for item in List:
            a8LB.insert(END, item)
        # updates a8LB
        def q8Updater(newAns):
            ansListDict["Q8"].append(newAns)
            a8LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q8
        q8entry=Entry(q8Frame, width=50)
        q8entry.grid(column=0,row=0)
        q8AddButton=Button(q8Frame, text="Add", command=lambda: q8Updater(q8entry.get())).grid(column=7, row=0)
        
        # frame for q9
        q9Frame=LabelFrame(secondFrame, text="Q9: What did you enjoy most about the competition?")
        q9Frame.grid(column=0, row=8)
        # var and buttons for a9
        a9=StringVar()
        a9.set(None)
        List=ansListDict["Q9"]
        a9LB=Listbox(q9Frame, selectmode="multiple")
        a9LB.grid(column=0, row=1)
        for item in List:
            a9LB.insert(END, item)
        # updates a9LB
        def q9Updater(newAns):
            ansListDict["Q9"].append(newAns)
            a9LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q9
        q9entry=Entry(q9Frame, width=50)
        q9entry.grid(column=0,row=0)
        q9AddButton=Button(q9Frame, text="Add", command=lambda: q9Updater(q9entry.get())).grid(column=7, row=0)
        # frame for q10
        q10Frame=LabelFrame(secondFrame, text="Q10: What did you enjoy least about the competition?")
        q10Frame.grid(column=0, row=9)
        # var and buttons for a10
        a10=StringVar()
        a10.set(None)
        List=ansListDict["Q10"]
        a10LB=Listbox(q10Frame, selectmode="multiple")
        a10LB.grid(column=0, row=1)
        for item in List:
            a10LB.insert(END, item)
        # updates a9LB
        def q10Updater(newAns):
            ansListDict["Q10"].append(newAns)
            a10LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q10
        q10entry=Entry(q10Frame, width=50)
        q10entry.grid(column=0,row=0)
        q10AddButton=Button(q10Frame, text="Add", command=lambda: q10Updater(q10entry.get())).grid(column=7, row=0)
        # frame for q11
        q11Frame=LabelFrame(secondFrame, text="Q11: What did you learn as a result of being involved with FCIB?")
        q11Frame.grid(column=0, row=10)
        # var and buttons for a11
        a11=StringVar()
        a11.set(None)
        List=ansListDict["Q11"]
        a11LB=Listbox(q11Frame, selectmode="multiple")
        a11LB.grid(column=0, row=1)
        for item in List:
            a11LB.insert(END, item)
        # updates a9LB
        def q11Updater(newAns):
            ansListDict["Q11"].append(newAns)
            a11LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q11
        q11entry=Entry(q11Frame, width=50)
        q11entry.grid(column=0,row=0)
        q11AddButton=Button(q11Frame, text="Add", command=lambda: q11Updater(q11entry.get())).grid(column=7, row=0)
        # frame and buttons for q12
        a12=StringVar()
        a12.set(None)
        q12Frame=LabelFrame(secondFrame, text="Q12: Did you increase your knowlage about personal finance?")
        q12Frame.grid(column=0, row=11)
        yButton12=Radiobutton(q12Frame, text="Yes", variable=a12, value="Yes").grid(column=0, row=0)
        nButton12=Radiobutton(q12Frame, text="No", variable=a12, value="No").grid(column=1, row=0)
        # frame and buttons for q13
        a13=StringVar()
        a13.set(None)
        q13Frame=LabelFrame(secondFrame, text="Q13: Do you plan to go on to college or higher education?")
        q13Frame.grid(column=0, row=12)
        yButton13=Radiobutton(q13Frame, text="Yes", variable=a13, value="Yes").grid(column=0, row=0)
        nButton13=Radiobutton(q13Frame, text="Yes", variable=a13, value="No").grid(column=1, row=0)
        # frame for q14
        q14Frame=LabelFrame(secondFrame, text="Q14: How would you improve FICB?")
        q14Frame.grid(column=0, row=13)
        # var and buttons for a14
        a14=StringVar()
        a14.set(None)
        List=ansListDict["Q14"]
        a14LB=Listbox(q14Frame, selectmode="multiple")
        a14LB.grid(column=0, row=1)
        for item in List:
            a14LB.insert(END, item)
        # updates a14LB
        def q14Updater(newAns):
            ansListDict["Q14"].append(newAns)
            a14LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q14
        q14entry=Entry(q14Frame, width=50)
        q14entry.grid(column=0,row=0)
        q14AddButton=Button(q14Frame, text="Add", command=lambda: q14Updater(q14entry.get())).grid(column=7, row=0)
        # frame and buttons for q15
        a15=StringVar()
        a15.set(None)
        q15Frame=LabelFrame(secondFrame, text="Q15: Do you have an account at a bank")
        q15Frame.grid(column=0, row=14)
        yButton15=Radiobutton(q15Frame, text="Yes", variable=a15, value="Yes").grid(column=0, row=0)
        nButton15=Radiobutton(q15Frame, text="No", variable=a15, value="No").grid(column=1, row=0)
        # frame for q16
        # TODO:
        #     write out whole question
        q16Frame=LabelFrame(secondFrame, text="Q16: Please describe how others in the community are aware ...")
        q16Frame.grid(column=0, row=15)
        # var and buttons for a16
        a16=StringVar()
        a16.set(None)
        List=ansListDict["Q16"]
        a16LB=Listbox(q16Frame, selectmode="multiple")
        a16LB.grid(column=0, row=1)
        for item in List:
            a16LB.insert(END, item)
        # updates a16LB
        def q14Updater(newAns):
            ansListDict["Q16"].append(newAns)
            a16LB.insert(END, newAns)
            resetScrollBar()
        # entry box for q16
        q16entry=Entry(q16Frame, width=50)
        q16entry.grid(column=0,row=0)
        q16AddButton=Button(q16Frame, text="Add", command=lambda: q16Updater(q16entry.get())).grid(column=7, row=0)
        # frame for q17
        q17Frame=LabelFrame(secondFrame, text="Q17: Share your email if you want")
        q17Frame.grid(column=0, row=16)
        # var and buttons for a17
        a17=StringVar()
        a17.set(None)
        FRQbutton("Q17", q17Frame, a17)
        # entry box for q17
        q17entry=Entry(q17Frame, width=50)
        q17entry.grid(column=0,row=0)
        q17AddButton=Button(q17Frame, text="Add", command=lambda: updateAnsList(q17entry.get(), "Q17", q17Frame, a17)).grid(column=7, row=0)
        # frame for q18
        q18Frame=LabelFrame(secondFrame, text="Q18: Bonus: what stock would you recommend to invest in for the next year?")
        q18Frame.grid(column=0, row=17)
        # var and buttons for a18
        a18=StringVar()
        a18.set(None)
        FRQbutton("Q18", q18Frame, a18)
        # entry box for q18
        q18entry=Entry(q18Frame, width=50)
        q18entry.grid(column=0,row=0)
        q18AddButton=Button(q18Frame, text="Add", command=lambda: updateAnsList(q18entry.get(), "Q18", q18Frame, a18)).grid(column=7, row=0)
    # makes done button
    doneButton=Button(secondFrame, text="Done", command=top.destroy)
    doneButton.grid(column=2, row=7)

# makes button to open answer creator
ACButton=Button(root, text="Add New Student", command=openAnswerCreator)
ACButton.grid(column=1, row=0)

# summary window
# TODO:
#    make email saving fxn
#    make options page
#    limit number of free responses shown
def openSummaryCreator():
    global ansSets, savingDirString, setName
    # set up
    top=Toplevel()
    top.title("Summary Creator")
    doneButton=Button(top, text="Done", command=top.destroy)
    doneButton.grid(column=0, row=0)

    # makes variables for the set as a string var and a string
    setName=StringVar()
    setName.set(None)

     # makes frame and buttons to select which set to summarize
    setFrame=LabelFrame(top, text="Choose An Answer Set", padx=5, pady=2)
    setFrame.grid(column=1, row=0, padx=10, pady=2, rowspan=18)
    rowNum=0
    for aset in ansSets:
        Radiobutton(setFrame, text=aset, variable=setName, value=aset, command=lambda: sumClick(setName.get())).grid(column=0, row=rowNum)
        rowNum+=1

    # create the summary of the selected set
    # TODO:
    #   stich together plots and texts
    def summarize(name):
        dirName=name
        dirPath=os.path.join("Answer_Sets", dirName)
        # make a dir for the summary and its files
        os.chdir(dirPath)
        if not "Summary" in os.listdir():
            os.mkdir("Summary")
        os.chdir("..")
        os.chdir("..")
        # fxn to make nice axies and a list of colorblind-friendly colors
        def get_ax(figsize=(8, 6)):
            fig, ax = plt.subplots(figsize=figsize)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            return ax
        CB_color_cycle = ['#377eb8', '#ff7f00', '#4daf4a', '#f781bf', '#a65628', '#984ea3', '#999999', '#e41a1c', '#dede00']
        # fxn to make DF from jsons
        def makeDF(dirName):
            dirPath=os.path.join("Answer_Sets", name)
            os.chdir(dirPath)
            # DF is horizontal
            DF=DataFrame({"Q1":[], "Q2":[], "Q3":[], "Q4":[], "Q5":[], "Q6":[], "Q7":[], "Q8":[], "Q9":[], "Q10":[], "Q11":[], "Q12":[], "Q13":[], "Q14":[], "Q15":[], "Q16":[], "Q17":[], "Q18":[]})
            for file in os.listdir():
                if file[-4:]=="json":
                    with open(file) as json_file:
                        data = json.load(json_file)
                        # dataDF is horizontal
                        dataDF=DataFrame.from_dict(data, orient='index').transpose()


                        DF.loc[len(DF.index)] = list(dataDF.iloc[0])
            return DF    
        # make DF from jsons and list of schools
        bigDF=makeDF("testSet1")
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
                # gets correct number of colorblind-friendly colors
                colors=[]
                i=0
                while i<4:
                    colors.append(CB_color_cycle[i])
                    i+=1
                gradesDF.plot.barh(ax=ax, color=colors)
                # graph settings
                ax.legend(fontsize=fsize-5, loc="upper center", ncol=4)
                plt.xticks(size=fsize)
                plt.yticks(size=fsize)
                ax.set_xlabel("")
                ax.set_ylabel("")
                plt.tight_layout()
                plt.savefig(plotFile)
            gradePlotter()
        gradeSummary()
        # make plot of top (classNumber) of classes taken
        # makes (bar| x=class, y=Freq) what classes ppl are taking
        def classesSummary(plotFile=os.path.join("Summary", "ClassesTakenPlot.pdf"), classNumber=7, dataFrame=schools, figSize=(10,8), fsize=20, DF=bigDF):
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
                    # graph settings
                    ax.legend().remove()
                    plt.xticks(size=fsize)
                    plt.yticks(size=fsize)
                    ax.set_xlabel("")
                    ax.set_ylabel("")
                    plt.tight_layout()
                    plt.savefig(plotFile)
            plotter()
        classesSummary()
        # make plot of numerical questions
        # TODO: fix colors
        def numSummary(plotFile=os.path.join("Summary", "NumbersPlot.pdf"), fsize=15):
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
            qList=["I Was Well Prepared to Compete", "FICB Content Mirrors School Content", "The Competition Rules Were Easy to Understand", "I Studieded Content at www.ficbonline.org"]
            numsDF=DataFrame({"Question":qList, "1-Disagree":lst1, "2":lst2, "3":lst3, "4":lst4, "5-Strongly Agree":lst5})
            numsDF=numsDF.set_index("Question")
            # good colors
            colors=[]
            i=0
            while i<5:
                colors.append(CB_color_cycle[i])
                i+=1
            ax=get_ax((12,9))
            numsDF.plot.barh(ax=ax, color=colors)
            # graph settings
            ax.legend(fontsize=fsize-3, loc="upper left", ncol=5)
            plt.xticks(size=fsize)
            plt.yticks(size=fsize)
            ax.set_xlabel("")
            ax.set_ylabel("")
            plt.tight_layout()
            plt.savefig(plotFile)
        numSummary()
        # gets free response data and returns a dict {response, int(times), ...}
        # data is bigDF["QX"]
        def freqList(data):
            # list of all responses
            dataList=list(data)
            dataDict={}
            # get count of each response
            for item in dataList:
                if item=="":
                    name="None"
                else:
                    name=item
                if name not in dataDict:
                    dataDict[name]=1
                else:
                    dataDict[name]+=1
            # sort highest count -> lowest
            dataDict=dict(sorted(dataDict.items(), key=lambda item: item[1], reverse=True))            
            return dataDict
        # make plot for y/n questions
        def ynSummary(plotFile=os.path.join("Summary", "YesNoPlot.pdf"), fsize=15):
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
            qList=["Did you increase your knowledge of personal finance?", "Do you plan to attend college or other higher education?", "Do You have an account at a bank or credit union?"]
            ynDF=DataFrame({"Question":qList, "Yes":lstY, "No":lstN})
            ynDF=ynDF.set_index("Question")
            # good colors
            colors=[]
            i=0
            while i<2:
                colors.append(CB_color_cycle[i])
                i+=1
            ax=get_ax((12,9))
            ynDF.plot.barh(ax=ax, color=colors)
            # graph settings
            ax.legend(fontsize=fsize, loc="upper left", ncol=2)
            plt.xticks(size=fsize)
            plt.yticks(size=fsize)
            ax.set_xlabel("")
            ax.set_ylabel("")
            plt.tight_layout()
            plt.savefig(plotFile)
        ynSummary()
        
        # makes the latex pdf
        # needs MiKTeX
        #   needs to be updated after installatiion
        #   needs to add float package
        def pdfMaker(name):
            plotWidth="10cm"
            os.chdir("Summary")
            # LaTeX options
            geometry_options = {"right": "2cm", "left": "2cm"}
            # make LaTeX doc
            doc=Document(geometry_options=geometry_options)
            doc.packages.append(Package("float"))
            # insert age/school plot
            with doc.create(Section("Distribution of ages in participating schools")):
                with doc.create(Figure(position="H")) as plot1:
                    plot1.add_image("AgeDistributionPlot.pdf", width=plotWidth)
            # insert classes taken plot
            with doc.create(Section("Classes taken by participants")):
                with doc.create(Figure(position="!htb")) as plot2:
                    plot2.add_image("ClassesTakenPlot.pdf", width=plotWidth)
            # insert number response plot
            with doc.create(Section("Numerical Questions")):
                with doc.create(Figure(position="!htb")) as plot3:
                    plot3.add_image("NumbersPlot.pdf", width=plotWidth)
            # insert y/n response plot
            with doc.create(Section("Yes / No Questions")):
                with doc.create(Figure(position="!htb")) as plot4:
                    plot4.add_image("YesNoPlot.pdf", width=plotWidth)
            # insert how ppl studided list
            with doc.create(Section("How Students Prepared")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q8"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # insert what ppl enjoyed list
            with doc.create(Section("What Students Enjoyed The Most")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q9"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # insert what ppl enjoyed least list
            with doc.create(Section("What Students Enjoyed The Least")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q10"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # insert what ppl learned list
            with doc.create(Section("What Students Learned")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q11"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # insert how ppl would improve list
            with doc.create(Section("How Students Would Improve FICB")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q14"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # insert what ppl are aware of list
            with doc.create(Section("How Others in the Students'Communities are Aware of their Participation")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q16"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # insert stock list
            with doc.create(Section("What Stock Students Suggest to Buy")):
                with doc.create(Itemize()) as itemize:
                    Dict=freqList(bigDF["Q18"])
                    for key in Dict:
                        itemize.add_item(key+": (x"+str(Dict[key])+")")
            # generate pdf
            doc.generate_pdf("Summary_of_"+name, clean=True, clean_tex=True, compiler="pdfLatex")
            # return to set dir i.e. "testSet1"
            os.chdir("..")
        pdfMaker(name)

        # return to highest dir
        os.chdir("..")
        os.chdir("..")


    # makes the buttons work
    # must start in highest dir, ends in highest dir
    def sumClick(value):
        global savingDirString
        savingDirString=str(value)
        # create the button to execute the summary
        sumButton=Button(top, text="Summarize", command=lambda: summarize(name=value))
        # sumButton=Button(top, text="Summarize", command=lambda: summarize(name=savingDirString))
        sumButton.grid(column=2, row=0)
    
    # makes the buttons
    rowNum=0
    for aset in ansSets:
        Radiobutton(setFrame, text=aset, variable=setName, value=aset, command=lambda: sumClick(setName.get())).grid(column=0, row=rowNum)
        rowNum+=1

# button to open summary creator
SCButton=Button(root, text="Create Summary", command=openSummaryCreator)
SCButton.grid(column=2, row=0)









root.mainloop()