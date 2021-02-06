#Importing all the libraries
import cv2 
import numpy as np
from statistics import mode,median
import time
import tkinter as tk
import tkinter.font as font
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +'haarcascade_frontalface_default.xml')
import time
from functools import partial
from math import ceil

#Function for creating ATM BUTTONS in 3X3 grid and 0 at bottom
def btns(root):
    myFont = font.Font(size=45)
    button=[]
    col='blue'
    button.append(tk.Button(root,text='0',bg=col))
    for i in range(3):
            for j in range(3):
                val = (3*i)+j+1
                button.append(tk.Button(root,text=str(val),bg=col))
                button[val]['font'] = myFont
                button[val].grid(row=i+1,column=j,sticky=tk.W)
    #0 at the bottom
    
    button[0]['font'] = myFont
    button[0].grid(row=4,column=1,sticky=tk.W)
    return button
#Function for writing labels and PIN code when entered               
def lbls(root,vals):
    myFont = font.Font(size=30)
    l1 = tk.Label(root, textv = vals)
    l1.grid(row=0,column=1,sticky=tk.W)
    l1['font'] = myFont
#Function to chng colour of button when pressed
def chngcol(button,colr='green'):
    button.configure(background = colr)
def show(string):
    m=tk.Tk()
    myFont = font.Font(size=30)
    lab1 = tk.Label(m, text = string)
    lab1.grid(row=0,column=0,columnspan=3,rowspan=3)
    lab1['font'] = myFont
    
    m.after(1500,lambda:m.destroy())
    while True:
        try:
            m.update_idletasks()
            m.update()
        except:
            break
    print(string)
def findMode(val,vals):
    try:
        ans = mode(vals)
    except:
        ans=cnt
    return ans
def findmx(contours,S=-1):
    val = 0
    ans=-1
    for i,x in enumerate(contours):
        if i!=S:
            area = cv2.contourArea(x)
            if area > val:
                area = val
                ans = i
    return ans
def find2mx(contours):
    big = findmx(contours)
    if big == -1:
        return []
    A = [contours[big]]
    Aa = cv2.contourArea(contours[big])
    big = findmx(contours,big)
    if big == -1:
        return A
    B = contours[big]
    Ba = cv2.contourArea(contours[big])
    if Ba >= 0.2*Aa:
        A.append(B)
    return A
def distance(A,B):
    ans = (((A[0]-B[0])**2) + ((A[1]-B[1])**2))**0.5
    return ans

def center_window(window) :
    window_width = window.winfo_reqwidth() 
    window_height = window.winfo_reqheight()
    window_x = int((window.winfo_screenwidth() / 2) - (window_width / 2)) 
    window_y = int((window.winfo_screenheight() / 2) - (window_height / 2)) 

    window_geometry = str(window_width) + 'x' + str(window_height) + '+' + str(window_x) + '+' + str(window_y) 
    window.geometry(window_geometry) 
def trial_instructions():
    root = tk.Tk()
    root.title('Trial Instructions')
    root.configure(bg='black')
    ins_vals = ['First you need to press S, to start processing.',
               'Then you need to show your hand (fingers) in front of camera.',
               'At this point, the program will record time taken by you to enter first digit.',
               'After that, you need to press enter.',
               'Now you should change number of fingers, for 2nd digit.',
               'Now again press enter.',
               'At this point program will record the time you need to enter different digits',
               'Neither "Gap Time", nor the "Wait Time" can be greater than 10 seconds',
               'The trial is complete.']
    cols = ['white','green']
    for _,i in enumerate(ins_vals):
        insLabel(root,"{}.{}".format(_+1,i),cols[_%2])
    butns(root,'Ok')
    root.mainloop()
def trial():
    #root.destroy()
    trial_instructions()
    our_vals = detection(9,9,2,'Trial \nSuccessfull')
    return inpTime(str(ceil(our_vals[0])),str(ceil(our_vals[2])))

def trial_sel(root,A):
    root.destroy()
    A[0] = True
def stop_watch(cT):
        root = tk.Tk()
        root.config(bg='black')
        TV=tk.StringVar()
        TV.set('0')
        myFont = font.Font(size=100)
        label = tk.Label(root,text = 'Stopwatch',font=myFont,bg='black',fg='white').pack()
        label = tk.Label(root,textvariable = str(TV),font=myFont,bg='black',fg='white').pack()
        while True:
            try:
                valT = int((time.time()-cT)//1)
                TV.set(str(valT))
                root.update_idletasks()
                root.update()
                time.sleep(1)
            except Exception as E:
                print(E)
                return valT
            
def insLabel(root,string,col='white',f_size=25):
    myFont = font.Font(size=f_size)
    lab1 = tk.Label(root, text = string,font=myFont,bg='black',fg=col)
    lab1.pack()
    
def butns(root,string):
    myFont = font.Font(size=25)
    tk.Button(root,text=string,font=myFont,command = root.destroy).pack()
    
def instructions():
    root = tk.Tk()
    root.title('Instructions')
    root.configure(bg='black')
    ins_vals=['Input for PIN would be taken using fingers of your hand.',
             'You need to show fingers equal to your PIN digit.',
             'You can show numbers using both your hands.',
             'For example for showing 3 you can either show 3 finger of one hand, or 2 finger of 1 hand and 2 of other.',
             'To start entering PIN, you need to press S.',
             'After pressing S, you need to show fingers in front of camera.',
              'The program will start processing input few seconds after you press S.("wait time")',
             'There will be gap of few seconds between entry of each digit.("gap time")',
             'You will be asked to enter the gap time and wait time, after this instruction.',
             'You can also request for a trial run to estimate the time you need.',
             'HAPPY BANKING :)']
    cols = ['white','green']
    for _,i in enumerate(ins_vals):
        insLabel(root,"{}.{}".format(_+1,i),cols[_%2])
    butns(root,'Got It')
    root.mainloop()
    
def submit(root,entry1,entry2):
    gap_time,time_before_start
    val1 = entry1.get()
    val2 = entry2.get()
    print(val1,val2)
    root.destroy()
    gap_time,time_before_start=val1,val2
    return val1,val2

def inpTime(g_t='3',t_b_s='2'):
    
    Root = tk.Tk()
    Root.configure(bg='black')
    Root.title('The Times')
    myFont = font.Font(size=50)
    insLabel(Root,'Enter Gap Time','white',50)
    gap_time = tk.StringVar()
    time_before_start = tk.StringVar()
    
#     lab1 = tk.Label(Root, text = 'Enter Time',bg='black',fg='white')
#     lab1['font'] = myFont
#     lab1.pack()
    
    gap_time.set(g_t)
    time_before_start.set(t_b_s)
    A=[False]
    entry1 = tk.Entry(Root,bd=10,font=myFont,textvariable=gap_time,relief=tk.SUNKEN,bg='black',fg='white') 
    entry1.pack()
    insLabel(Root,'Enter wait time before start','white',50)
    entry2 = tk.Entry(Root,bd=10,font=myFont,textvariable=time_before_start,relief=tk.SUNKEN,bg='black',fg='white') 
    entry2.pack()
    act_with_arg1=(submit,Root,entry1,entry2)
    act_with_arg2=(trial,Root)
    ok_but = tk.Button(Root,text='submit',font=myFont,bg='black',fg='white',command = Root.destroy,relief=tk.SUNKEN)
    ok_but.pack()
    tr_but=tk.Button(Root,text='Take a Trial',font=myFont,bg='black',fg='white',command = lambda: trial_sel(Root,A),relief=tk.GROOVE).pack()
    Root.mainloop()
    print('vals',int(gap_time.get()),int(time_before_start.get()))
    if A[0]:
        return A
    return False,int(gap_time.get()),int(time_before_start.get()) 
# instructions()
# A = inpTime()
# if A[0]:
#     A = trial()
# print(A)

def detection(g_t=3,w_t=2,ToDigReq=4,ByeByeString='PIN entered \nSuccessfully'):
    g_t = min(10,g_t)
    w_t = min(10,w_t)
    #creating the graphical window
    returnables=[]
    hasItStarted=True
    root = tk.Tk()
    
    #creating the buttons
    buttons=btns(root)
    Vals=''
    #accessing camera, 1 for accessing second camera (phone camera), 0 is for laptop webcam
    #cap = cv2.VideoCapture(1)
    cap = cv2.VideoCapture('http://192.168.0.103:4747/video')
    #initializing value for number of frames processed
    frs=-10
    #inintialising list for saving number of fingers shown to find mode and print them.
    to_fings=[]
    #initialzing value of number of fingers to be printed
    ans='0'
    #loop for camera starts
    noP=0
    PIN=[]
    cnt=0
    vals=tk.StringVar()
    ins_vals = tk.StringVar()
    INS="Press 'S'\nto Start"
    vals.set(Vals)
    ins_vals.set(INS)
    ForS=0
    startTime = time.time()
    if cap.isOpened():
        _,frame = cap.read()
        #print(frame)
        wW=frame.shape[1]
        wH=frame.shape[0]
        Farea=wW*wH*0.05
    hasStarted = False
    while True:
        _, frame = cap.read()
        if time.time()-startTime > 20:
            print('jeez')
            returnables=[10,10,10]
            root.destroy()
            break
        if _ ==False:
            break
        try:
            fps = cap.get(cv2.CAP_PROP_FPS)
            #frame being converted to HSV(Hue Saturation Value) for thresholding of skin colour
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            #lower and upper values for background colour (dark green)
            l_h,l_s,l_v = 73,104,0
            u_h,u_s,u_v =179,255,255
            #converting values to array
            lower_blue = np.array([l_h, l_s, l_v])
            upper_blue = np.array([u_h, u_s, u_v])
            #creating mask for background
            mask = cv2.inRange(hsv, lower_blue, upper_blue)
            #detecting the background
            result = cv2.bitwise_and(frame, frame, mask=mask)
            #doing bitwise not for background mask to detect everything that is not background i.e. our hand
            mask1 = cv2.bitwise_not(mask)
            #marking region of interest that is hand of user
            hand = cv2.bitwise_and(frame, frame, mask=mask1)
            #finding contours of our reign of interest
            contours, hierarchy = cv2.findContours(mask1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            if len(contours)>0:
                
                #finding the biggest contour in terms of area to remove all the noise
                #contours = max(contours,key=lambda x:cv2.contourArea(x))
                #contours = contours[findmx(contours)]
                Contours = [c for c in contours if cv2.contourArea(c)>Farea]
                #Contours = find2mx(contours)
                cnt=0
                dflg=False
                for contours in Contours:
                    #drawing contours around hand
                    cv2.drawContours(hand, [contours], -1, (255,255,0), 2)
                    #finding the convex hull using the contours
                    hull = cv2.convexHull(contours)
                    top    = tuple(hull[hull[:, :, 1].argmin()][0])
                    bottom = tuple(hull[hull[:, :, 1].argmax()][0])
                    left   = tuple(hull[hull[:, :, 0].argmin()][0])
                    right  = tuple(hull[hull[:, :, 0].argmax()][0])

                    cX = (left[0] + right[0]) // 2
                    cY = (top[1] + bottom[1]) // 2
                    C = (cX,cY)
                    r = int((distance(C,top) + distance(C,bottom) + distance(C,left) + distance(C,right))//8)
                    #print(r)
                    #cv2.circle(hand, C, r, [0, 0, 255], 2)
                    #drawing convexhull around hand
                    cv2.drawContours(hand, [hull], -1, (0, 255, 255), 2)
                    #conex hull with indices of convex hull points
                    hull = cv2.convexHull(contours, returnPoints=False)
                    try:
                        dflg=True
                        defects = cv2.convexityDefects(contours, hull)
                    except:
                        pass

                    thumb=False
                    dF=False
                    #finding defects in convex hull
                    if defects is not None:

                        thumb=False
                        #calculating the angle of defects
                        for i in range(defects.shape[0]):  
                            #returns four points start, end, farthest point, distance of farthest point fromstart
                            try:
                                s, e, f, d = defects[i][0]
                                start = tuple(contours[s][0])
                                end = tuple(contours[e][0])
                                far = tuple(contours[f][0])
                                #print(far[1])
                            except:
                                #print('time out',len(contours),i,s,e,f)
                                break
                            #finding the length of lines along the fingers
                            a = np.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
                            b = np.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
                            c = np.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
                            #finding angle using cosine theorem
                            angle = np.arccos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) 
                            thumb=False
                            is_inside = distance(C,far)<=r
                            #angle between or fingers is always less than 90, so to eliminate defects other than between fingers
                            if is_inside and angle>=np.pi/36 and angle < np.pi / 2:
                                if hasItStarted and hasStarted:
                                    returnables.append((time.time()-startTime))
                                    hasItStarted = False
                                #print(angle)
                                if angle>np.pi/4:
                                    thumb=True
                                cnt += 1
                                cv2.circle(hand, far, 4, [0, 0, 255], -1)
                                dF=True
                        if cnt>0:
                            cnt+=1

                    if cnt > 1:
                        frs+=1
                        if frs>0:
                            to_fings.append(cnt)
                    elif dflg:
                        #print(defects)
                        frs+=1
                        if frs>0:
                            cnt = cnt+1
                            to_fings.append(cnt)

    #             if cnt<5 and thumb:
    #                 cnt+=5
                #waiting for algorithm to process enough data before predincting
                #if frs>30:
                    #finding mode of processed data
                ans="0"
                ans=str(cnt)
                if frs>0:
                    ins_vals.set('')
    #                 #cnt = int(findMode(cnt,to_fings))
    #                 if len(to_fings)>50:
    #                     to_fings=to_fings[-50:]
    #                 cnt = int(median(to_fings)) 
    #                 #cnt = int(median(to_fings))
    #                 ans=str(cnt)
                #printing predicted text on screen        
            cv2.putText(hand, ans, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,3, (255, 0, 0) , 2, cv2.LINE_AA)
            #cv2.imwrite(file_name.format(i),hand)
            cv2.imshow("frame", frame)
            #cv2.imshow("mask", mask)
            #cv2.imshow("result", result)
            cv2.imshow("hand", hand)
            #i+=1
            root.update()
            center_window(root)
        except Exception as e:
            print(e,'oops')
    #         pass
        key = cv2.waitKey(1)
        try:
            
            myFont = font.Font(size=30)
            l2 = tk.Label(root, textvariable = ins_vals)
            l2.grid(row=5,column=0,columnspan=3)
            l2['font'] = myFont
            l1 = tk.Label(root, textvariable = vals)
            l1.grid(row=0,column=1,columnspan=2,sticky=tk.W)
            l1['font'] = myFont
            root.update()
            center_window(root)
        except:
            break
        CNT=cnt
        cnt=int(ans)
        if key==83 or key==115:
            #show('started')
            ins_vals.set('Started')
            startTime = time.time()
            frs=-1*fps*w_t
            cnt = 0
            to_fings = []
            hasStarted=True
        #ESC to strt current digit fresh, backspace to erase and enter to save
        if key == 8 or key == 27:


            print(key)
            frs = -1*fps*w_t
            ans='0'
            cnt = 0
            to_fings=[]
            ForS=0
            if key == 8:
                #print('del')
                #lbls(root,vals[:-1])
                root.update()
                Vals=Vals[:-1]
                vals.set(Vals)
                noP-=1
                chngcol(buttons[PIN[-1]],'blue')

        elif (key == 13 or ((time.time()-startTime)>=g_t)) and hasStarted:
    #         if ForS==0:
    #             show('Enter Second Number')
    #             prev = cnt
    #             ForS=1
    #         else:
    #         cnt+=prev
            returnables.append((time.time()-startTime))    
            ForS=0
            if cnt<=9:
                #show('Number Accepted')
                ins_vals.set('Number \nAccepted')
                chngcol(buttons[cnt])
                Vals+='*'
                vals.set(Vals)
                #lbls(root,vals)
                PIN.append(cnt)
                noP+=1
                if noP==ToDigReq:
                    myFont = font.Font(size=30)
                    l1 = tk.Label(root, textvariable = vals)
                    l1.grid(row=0,column=1,columnspan=2,sticky=tk.W)
                    l1['font'] = myFont
                    root.update()
                    center_window(root)
                    #show(ByeByeString)
                    ins_vals.set(ByeByeString)
                    root.update()
                    center_window(root)
                    print(PIN)
                    root.destroy()
                    break
            else:
                #show('Invalid Number...Try Again')
                ins_vals.set('Invalid Number...\nTry Again')
            startTime = time.time()
            to_fings=[]
            #print('ans')
            ans = '0'
            frs = -15
            cnt=0
        cnt=CNT
    #     if key == 27:
    #         break

        #time.sleep(1)
    cap.release()
    cv2.destroyAllWindows()
    if ToDigReq == 2:
        return returnables
    return PIN

instructions()
B=[True]
while B[0]:
    B = inpTime()
    if B[0]:
        B = trial()
A = [True]
def done(root,A):
    A[0] = False
    root.destroy()
while A[0]:
    PIN = detection(int(B[1]),int(B[2]))
    #print('hi')
    root = tk.Tk()
    root.config(bg='black')
    myFont = font.Font(size=50)
    Done = tk.Button(root,text='Done',command = lambda:done(root,A),font=myFont,fg='white',bg='black')
    Done.grid(row=0,column=0)
    Re_enter = tk.Button(root,text='Re Enter PIN',command = root.destroy,font=myFont,fg='white',bg='black')
    Re_enter.grid(row=1,column=0)
    root.mainloop()