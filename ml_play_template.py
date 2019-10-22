"""The template of the main script of the machine learning process
"""

import games.arkanoid.communication as comm
import numpy as np
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

np.set_printoptions(threshold=np.inf)
#
#def bricks_filter(brickslist,up,left,ball_x,ball_y):
#    k = len(brickslist)
#    if(up == 1):
#        if(left ==1):
#            #U.L
#            for i in range(len(brickslist)):
#                if(brickslist[i][0]>ball_x):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#                if(brickslist[i][1]<ball_y):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#                    
#        else:
#            #U.R
#            for i in range(len(brickslist)):
#                if(brickslist[i][0]<ball_x):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#                if(brickslist[i][1]<ball_y):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#    else:
#        if(left ==1):
#            #D.L
#            for i in range(len(brickslist)):
#                if(brickslist[i][0]>ball_x):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#                if(brickslist[i][1]>ball_y):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#        else:
#            #D.R
#            for i in range(k):
#                if(brickslist[i][0]<ball_x):
#                    brickslist.remove(brickslist[i])
#                    k = len(brickslist)
#                    print('del')
#                if(brickslist[i][1]>ball_y):
#                    brickslist.remove(brickslist[i])
#                    print('del')
#    return brickslist

def ml_loop():
    """The main loop of the machine learning process

    This loop is run in a separate process, and communicates with the game process.

    Note that the game process won't wait for the ml process to generate the
    GameInstruction. It is possible that the frame of the GameInstruction
    is behind of the current frame in the game process. Try to decrease the fps
    to avoid this situation.
    """

    # === Here is the execution order of the loop === #
    # 1. Put the initialization code here.

    # 2. Inform the game process that ml process is ready before start the loop.
    ball_location = [0,0]
    plat_location = [0,0]
    bricks = []
    hit = False
    comm.ml_ready()
    # 3. Start an endless loop.
    while True:
        # 3.1. Receive the scene information sent from the game process.
        scene_info = comm.get_scene_info()
		
		
        # 3.2. If the game is over or passed, the game process will reset
        #      the scene and wait for ml process doing resetting job.
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            # Do some stuff if needed
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
        last_ball_location = ball_location
        ball_location = scene_info.ball
        plat_location = scene_info.platform
        bricks = scene_info.bricks
        table = np.array(np.zeros((208,408)))
            
        for k in range(len(bricks)):
            for p in range(0,25):
                for j in range(0,10):
                    table[bricks[k][0] + p][bricks[k][1] + j ] = 1
    
            
            
            
            
        delta_x = int(ball_location[0]) - int(last_ball_location[0])
        delta_y = int(ball_location[1]) - int(last_ball_location[1])
            #get Slope
        try:
            m = delta_y/delta_x
        except:
            m = 0.0001
                
                
        if(int(ball_location[1]) - int(last_ball_location[1]) > 0):
              # dowing
                
            next_x = (400-int(ball_location[1]))/m + int(ball_location[0])

            if(next_x>200):
                next_x = 400-next_x
            if(next_x<0):
                if(next_x>-200):
                    next_x = np.abs(next_x)
                else:
                    next_x = next_x+400

  
                
            if(int(ball_location[0]) > int(last_ball_location[0]) ):
                    #D.R.
                j = ball_location[0]+3
                k = ball_location[1]
                while(j < 200 and k < 400):
                    if(table[j][k] == 1):
                        hit = True
                        break
                    j = j+1
                    k = k+1
                    hit = False
                if(hit==False):
                    j = ball_location[0]+3
                    k = ball_location[1]-3
                    while(j < 200 and k < 400):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j+1
                        k = k+1
                        hit = False
                if(hit):
                    print('DR')
                    print(j,k)
                    if(table[j-1][k]==0):
                        if(j+k < 400):
                            next_x = 400-(j+k)
                        else:
                            next_x = j+k -400
#                    
                    
            else:
                    #D.L
                j = ball_location[0]
                k = ball_location[1]
                while(j > 0 and k < 400):
                    if(table[j][k] == 1):
                        hit = True
                        break
                    j = j-1
                    k = k+1
                    hit = False
                if(hit==False):
                    j = ball_location[0]
                    k = ball_location[1]+3
                    while(j > 0 and k < 400):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j-1
                        k = k+1
                        hit = False
                if(hit):
                    print('DL')
                    print(j,k)
                    if(table[j+1][k]==0):
                        if(200-j+k < 400):
                            next_x = k-j
                        else:
                            next_x = 400-j+k

#                    if(hit):
#                        print('hit222')
                
                if(next_x>200):
                    next_x = next_x - 200
                if(next_x<0):
                    next_x = next_x * -1
                
                
        else:
            if(int(ball_location[0]) > int(last_ball_location[0]) ):
                #U.R
                j = ball_location[0]
                k = ball_location[1]
                while(j < 200 and k > 0):
                    
                    if(table[j][k] == 1):
                        hit = True
                        break
                    j = j+1
                    k = k-1
                    hit = False
                        
                        
                if(hit==False):
                    j = ball_location[0]
                    k = ball_location[1]-3
                    while(j < 200 and k > 0):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j+1
                        k = k-1
                        hit = False
                            
                if(hit):  
                    print('UR')
                    print(j,k)
                    if(table[j][k+1]==0):
                        if(200-j+k < 400):
                            next_x = k-j
                        else:
                            next_x = 400-j+k
                        
              

            else:
                #U.L
                j = ball_location[0]
                k = ball_location[1] - 3
                while(j > 0 and k > 0):
                    if(table[j][k] == 1):
                        hit = True
                        break
                    j = j-1
                    k = k-1
                    hit = False
                if(hit==False):
                    j = ball_location[0]+3
                    k = ball_location[1]-3
                    while(j > 0 and k > 0):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j-1
                        k = k-1
                        hit = False
                        
                if(hit):
                    print('UL')
                    print(j,k)
                    if(table[j][k+1]==0):
                        if(j+k < 400):
                            next_x = 400-(j+k)
                        else:
                            next_x = j+k -400
       
                if(next_x>200):
                    next_x = next_x - 200
                if(next_x<0):
                    next_x = next_x * -1
            
        
        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        
#        if(int(ball_location[1]) - int(last_ball_location[1]) > 0):
        next_x = next_x - next_x%5
#        if(j == 150 and k == 189):
#            next_x = 155
        print(next_x)

        if(int(plat_location[0])+20>next_x):
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif(int(plat_location[0])+20<next_x):
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
#        else:
#            if(left == 1):
#                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
#            elif(left == 0):
#                comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
#            else:
#                comm.send_instruction(scene_info.frame, PlatformAction.NONE)
                
    
            

