import pickle
import os
from os import path
import numpy as np
import json
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
class MLPlay:
    def __init__(self, player):
        self.player = player
        if self.player == "player1":
            self.player_no = 0
        elif self.player == "player2":
            self.player_no = 1
        elif self.player == "player3":
            self.player_no = 2
        elif self.player == "player4":
            self.player_no = 3
        self.car_vel = 0                            # speed initial
        self.car_pos = (0,0)   
        self.w=0                     # pos initial
        self.car_lane = self.car_pos[0] // 70       # lanes 0 ~ 8
        self.lanes = [35, 105, 175, 245, 315, 385, 455, 525, 595]  # lanes center
        
        pass

    def update(self, scene_info):
        
        coin_array=[]
        for i in range(5):
            coin_array.append(0)
        sh=[]
        sl=[]
        v=15
        r=[]
        h=[]
        vote=[]
        mylan=0
        sy=self.car_pos[1]
        for coin in scene_info["coins"]:
            coin_y=sy-coin[1]
            coin_lan=coin[0]//70
            if coin_y>100 and coin_y<400:
                if coin_lan==mylan-2:
                    coin_array[0]=1
                if coin_lan==mylan-1:
                    coin_array[1]=1
                if coin_lan==mylan:
                    coin_array[2]=1
                if coin_lan==mylan+1:
                    coin_array[3]=1
                if coin_lan==mylan+2:
                    coin_array[4]=1
        for i in range(3):
            sh.append(600)
            sl.append(-100)
        for car in scene_info["cars_info"]:
            if car["id"] ==self.player_no:
                
                sy=car["pos"][1]
                mylan=car["pos"][0]//70
                if mylan==0:
                    sh[0]=100
                if mylan==8:
                    sh[2]=100
                
        ry=0
        for car in scene_info["cars_info"]:
    
            if car["id"] !=self.player_no:
                sx=car["pos"][0]
                slan=sx//70
                ry=sy-car["pos"][1]
                if slan==mylan:
                    if ry>100 and ry<sh[1]:
                        sh[1]=ry
                        v=car["velocity"]
                    if ry<100 and ry>sl[1]:
                        sl[1]=ry
                if slan==mylan-1 :
                    if ry>100 and ry<sh[0]:
                        sh[0]=ry
                    if ry<100 and ry>sl[0]:
                        sl[0]=ry
                if slan==mylan+1:
                    if ry>100 and ry<sh[2]:
                        sh[2]=ry
                    if ry<100 and ry>sl[2]:
                        sl[2]=ry

        
        
        h.append((v,sh[0],sh[2],sl[1],sl[0],sl[2],coin_array[0],coin_array[1],coin_array[2],coin_array[3],coin_array[4]))               
        r.append((mylan,sh[1]))
        feature=np.hstack((r,h))

        h2=[]
        h2.append((v,sh[0],sh[2],sl[1],sl[0],sl[2]))
        feature2=np.hstack((r,h2))
    
    
    
    
        
        if len(scene_info[self.player]) != 0:
            self.car_pos = scene_info[self.player]
        
        filename = path.join(path.dirname(__file__), 'Predict3.pickle')
        with open(filename,"rb") as f:
            forest=pickle.load(f)
        filename = path.join(path.dirname(__file__), 'Predict4.pickle')
        with open(filename,"rb") as f:
            forest2=pickle.load(f)
        for i in range(10):
            vote.append(0)
        vote=np.array(vote)
        
        for i in range(32):
            tree=forest[i]
            d=tree.predict(feature)
            d=int(d)
            vote[d]=vote[d]+1

        for i in range(25):
            tree=forest2[i]
            d=tree.predict(feature2)
            d=int(d)
            vote[d]=vote[d]+1
        m=1
        """print(vote)"""
        for i in range(10):
            if vote[i]>vote[m]:
                m=i
        
        d=m
        self.car_lane=self.car_pos[0]//70
        
        if d==1:
            if self.car_pos[0] > self.lanes[self.car_lane]:
                return ["SPEED", "MOVE_LEFT"]
            elif self.car_pos[0 ] < self.lanes[self.car_lane]:
                    return ["SPEED", "MOVE_RIGHT"]
            else :return ["SPEED"]
        elif d==2:
            return ["MOVE_LEFT", "SPEED"]
        elif d==3:
            return ["MOVE_RIGHT", "SPEED"]
        elif d==4:
            self.w=self.w
            return ["BRAKE"]
        elif d==5:           
            return ["MOVE_LEFT"]
        elif d==6:
            return ["MOVE_RIGHT"]
        elif d==7:
            self.w=self.w+1
            return ["MOVE_RIGHT","BRAKE"]
        elif d==8:
            self.w=self.w+1
            return ["MOVE_LEFT","BRAKE"]
        else:
            return ["BRAKE"]
        if scene_info["status"] != "ALIVE":
            return "RESET"
        
        

    def reset(self):
        """
        Reset the status
        """
        pass