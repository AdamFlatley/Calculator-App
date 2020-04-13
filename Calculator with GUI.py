## Attempt to create a GUI - first implementation will be with a standard calculator##
##11/04/2020##
## Will be using the PYQT library to implement the GUI ## https://build-system.fman.io/pyqt5-tutorial
## found this https://doc.qt.io/qt-5/qtwidgets-widgets-calculator-example.html
# QT Designer is a possible method to create a customised GUI !# -> based on documentation just use this
# As it sucks to design it by hand :)
# There are LOTS of improvements that could be made but due to the simplicity of the project we just gon leave em
#E.g - Backspace feature instead of only clear all
# Bracket implementation

import PyQt5.QtWidgets as plt # used for buttons and other similar things
from PyQt5.QtCore import Qt


app = plt.QApplication([]) ## a REQUIREMENT for all applications to have one QApplication initialised
window = plt.QWidget() # creates the window itself

Row1 =  plt.QHBoxLayout()
Row2 =  plt.QHBoxLayout()
Row3 =  plt.QHBoxLayout()
Row4 =  plt.QHBoxLayout()  # used to layout the window
Row5 =  plt.QHBoxLayout()
Screen = plt.QLineEdit("0") # screen
Testwindow = plt.QGridLayout()

Operator_array = ['+','-','/','*'] # used to split the lineedit string 

#Need to add -> check to make sure doesn't use two operators at once(warning window?)
#Method to check that two decimals arent being used for two numbers.

def Return_Selection(Array_of_positions, This_position, The_string, operator):
    #array of all positions of operators in big string, the position of this operator, the big string itself and the type of operator 
        selection1 = [] 
        selection2 = [] 
        First = False
        Last = False
        i = This_position
        if(i == 0): #if it is the first operator ## This can be cleaned! (done at 2am Adam you know you can do better)
                selection1 = The_string[0:Array_of_positions[i]]
                First = True
        else: selection1 = The_string[Array_of_positions[i-1]+1:Array_of_positions[i]]
            
        if(i+1 == len(Array_of_positions)): # if it is the last operator
                selection2 = The_string[Array_of_positions[i]+1:]
                Last = True
        else: selection2 = The_string[Array_of_positions[i]+1:Array_of_positions[i+1]]
        
        if(First == True):
            StartPos = 0
        else: StartPos = Array_of_positions[i-1]+1
        if(Last == True):
            EndPos = len(The_string)
        else: EndPos = Array_of_positions[i+1]
        OldSelection = The_string[StartPos:EndPos]
        
        
        
        if (operator == "/"):
            try:
                float(selection1)/float(selection2)
            except ZeroDivisionError:
                 Warningbox = plt.QMessageBox()
                 Warningbox.setText("No dividing by zero silly!")
                 Warningbox.exec_()
                 The_string = "0"
                 return The_string
            NewSelection = float(selection1)/float(selection2)
            The_string = The_string.replace(OldSelection , str(NewSelection), 1)
            
            return The_string
        if(operator == "*"):
            NewSelection = float(selection1)*float(selection2)
            The_string = The_string.replace(OldSelection , str(NewSelection), 1)
            
            return The_string
        if(operator == "+"):
           
            NewSelection = float(selection1)+float(selection2)


            The_string = The_string.replace(OldSelection , str(NewSelection), 1)
            return The_string
        if(operator == "-"):
            NewSelection = float(selection1)-float(selection2)
            The_string = The_string.replace(OldSelection , str(NewSelection), 1)
            return The_string

def parse_string(The_string): # this is the function to use when pressing equals baby
    #BIDMAS - divide multiply addition subtraction
    #return an array with positions of all the operators
    Num_of_operations = 1 # used for the while loop
    
    while (Num_of_operations > 0):
        array_of_positions = []
        array_of_type = []
        for i in range(len(The_string)):
            for j in range(4):
                if(The_string[i] == Operator_array[j] and i != 0 and i != len(The_string)-1): #test every individual character and add if its a operator
                    array_of_positions.append(i)
                    array_of_type.append(Operator_array[j])
                elif(The_string[i] == Operator_array[j] and i == 0):        #operator first
                    return "0"
                elif(The_string[i] == Operator_array[j] and i == len(The_string)-1): #operator last
                    return "0"
        Num_of_operations = len(array_of_positions)    
        
        if(Num_of_operations == 0): return The_string # if no operations just return the string - why not
        
        if("/" in array_of_type): #if there is a divide
            for i in range(len(array_of_type)):
                if(array_of_type[i] == "/"):
                    The_string = Return_Selection(Array_of_positions = array_of_positions, This_position = i, The_string = The_string, operator = "/")
                    break # breaks this for loop
            continue
        if("*" in array_of_type): #if there is a divide
            for i in range(len(array_of_type)):
                if(array_of_type[i] == "*"):
                    The_string = Return_Selection(Array_of_positions = array_of_positions, This_position = i, The_string = The_string, operator = "*")
                    break # breaks this for loop
            continue
        if("+" in array_of_type): #if there is a divide
            for i in range(len(array_of_type)):
                if(array_of_type[i] == "+"):
                    The_string = Return_Selection(Array_of_positions = array_of_positions, This_position = i, The_string = The_string, operator = "+")
                    break # breaks this for loop
            continue
        if("-" in array_of_type): #if there is a divide
            for i in range(len(array_of_type)):
                if(array_of_type[i] == "-"):
                    The_string = Return_Selection(Array_of_positions = array_of_positions, This_position = i, The_string = The_string, operator = "-")
                    break # breaks this for loop
            continue        

           
            


            
class CalculatorButton():
    def __init__(self, Contents):
        super().__init__()
      
        self.Contents = Contents
        self.button =  plt.QPushButton(self.Contents) # create a class with the button as a content
        self.button.clicked.connect(self.Pressed)
    def Pressed(self):
        current_text = Screen.text() # stores current screen display
        if(self.Contents == 'Clear'): # clears screen display and sets to 0
            Screen.clear()
            Screen.setText("0")
        elif(self.Contents  in Operator_array): ## if button pressed is an operator
            if(current_text[len(current_text)-1] in Operator_array): # if previous entry is an operator also
                Warningbox = plt.QMessageBox()
                Warningbox.setText("Invalid entry! Can't use an operator if one has just been used.")
                Warningbox.exec_()
            else: 
                Screen.setText(current_text+self.Contents)
        elif(self.Contents == "="): #takes the entire string and performs the maths for it 
            Screen.setText(parse_string(current_text)) # Check the above functions
            #
        elif(self.Contents == "."): # check to make sure there aren't two decimals within a number
            positions = []
            for i in range(len(current_text)):
                if(current_text[i] in Operator_array):
                    positions.append(i)
            if(len(positions)>0):
                if("." in  current_text[positions[len(positions)-1]:] ):
                    Warningbox = plt.QMessageBox()
                    Warningbox.setText("Can't have two decimals in one number")
                    Warningbox.exec_()
                else:
                    Screen.setText(current_text+self.Contents)
            elif(len(positions) == 0):
                if("." in current_text):
                    Warningbox = plt.QMessageBox()
                    Warningbox.setText("Can't have two decimals in one number")
                    Warningbox.exec_()
                else:
                    Screen.setText(current_text+self.Contents)
            
        else:    
            current_text = Screen.text() #retrieves the text from the screen (String)
            if(current_text == "0"):
                Screen.setText(self.Contents)
            else:
                Screen.setText(current_text+self.Contents)
        
def NumberPush():
    alert = plt.QMessageBox()
    alert.setText("wha")
    alert.exec_()
def BadPush():
    alert = plt.QMessageBox()
    alert.setText('What are you doin you muppet, don\'t push me!')
    alert.exec_()
    
## Creation of all the buttons and their corresponding string to contain
    # Would it be possible to implement all of these as objects instead??
    # -> removes the repetition
    
One = CalculatorButton('1')
Two = CalculatorButton('2')
Three = CalculatorButton('3')
Four = CalculatorButton('4')
Five = CalculatorButton('5')
Six = CalculatorButton('6')
Seven = CalculatorButton('7')
Eight = CalculatorButton('8')
Nine = CalculatorButton('9')
Zero = CalculatorButton('0')
Plus = CalculatorButton('+')
Minus = CalculatorButton('-')
Divide = CalculatorButton('/')
Times = CalculatorButton('*')
Clear = CalculatorButton('Clear') # Creates all buttons to be used
Decimal = CalculatorButton('.') # blank buttons just for visual reasons
Result = CalculatorButton('=')
#change properties of the display

Screen.setMinimumSize(300,30)
Screen.setMaximumSize(300,30) # set a fixed size to the calculator of 200x30 (X by Y)
Screen.setAlignment(Qt.AlignRight) #set numbers to right hand side of the input
Screen.setReadOnly(True)

Row1.addWidget(Screen) # row 1 is screen and clear
Row1.addWidget(Clear.button)

Row2.addWidget(One.button) 
Row2.addWidget(Two.button)
Row2.addWidget(Three.button)
Row2.addWidget(Plus.button)

Row3.addWidget(Four.button)
Row3.addWidget(Five.button)
Row3.addWidget(Six.button)
Row3.addWidget(Minus.button)

Row4.addWidget(Seven.button)
Row4.addWidget(Eight.button)
Row4.addWidget(Nine.button)
Row4.addWidget(Times.button)

Row5.addWidget(Decimal.button)
Row5.addWidget(Zero.button)
Row5.addWidget(Result.button)
Row5.addWidget(Divide.button)

Testwindow.addLayout(Row1, 0, 0) # Layer, row, column
Testwindow.addLayout(Row2, 1, 0)
Testwindow.addLayout(Row3, 2, 0)
Testwindow.addLayout(Row4, 3, 0)
Testwindow.addLayout(Row5, 4, 0)


#Push.clicked.connect(NumberPush)
#Dont_Push.clicked.connect(BadPush)

window.setLayout(Testwindow) #sets the windows with that layout
window.setMaximumHeight(250)
window.setMaximumWidth(450)
window.setMinimumHeight(250)
window.setMinimumWidth(450)
window.show() # show the window

#label = plt.QLabel('Hello World!') # creates the label hello world
#label.show()    # shows the label
#push_button = plt.QPushButton("push me joe lad")
#push_button.show()

app.exec_() ## without this line the program will break and simply become unresponsive!
