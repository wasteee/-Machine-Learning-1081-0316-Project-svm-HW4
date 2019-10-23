"""The template of the main script of the machine learning process
"""
import pickle
import games.arkanoid.communication as comm
import numpy as np
from games.arkanoid.communication import ( \
    SceneInfo, GameInstruction, GameStatus, PlatformAction
)

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
    filename = "C:\\Users\\fghj8\\MLGame-master\\games\\arkanoid\\svr_example_m2.sav"
    model = pickle.load(open(filename,'rb'))

    last_ball_x = 0
    last_ball_y = 0
    games = 0
    gameover = 0
    comm.ml_ready()
    # 3. Start an endless loop.
    scene_info = comm.get_scene_info()
    while True:
        # 3.1. Receive the scene information sent from the game process.
        
    
        table = np.array(np.zeros((208,408)))
        
        last_ball_x = scene_info.ball[0]
        last_ball_y = scene_info.ball[1]
        scene_info = comm.get_scene_info()
        delta_x = int(scene_info.ball[0]) - int(last_ball_x)
        delta_y = int(scene_info.ball[1]) - int(last_ball_y)
        #get Slope
        try:
            m = delta_y/delta_x
        except:
            m = 0.0001
        if(last_ball_x - scene_info.ball[0] > 0):
            LR = 1
        else:
            LR = 0
        if(last_ball_y - scene_info.ball[1] > 0):
            UP = 0
        else:
            UP = 1
        if(last_ball_x - scene_info.ball[0] > 0):
                LR = 1
                if(last_ball_y - scene_info.ball[1] > 0):
                    #going up
                    UP = 0
                    
                    #U.L
                    j = scene_info.ball[0]
                    k = scene_info.ball[1] - 3
                    while(j > 0 and k > 0):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j-1
                        k = k-1
                        hit = False
                    if(hit==False):
                        j = scene_info.ball[0]+3
                        k = scene_info.ball[1]-3
                        while(j > 0 and k > 0):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j-1
                            k = k-1
                            hit = False
                        
                    if(hit==False):
                        j = -1
                        k = -1
                else:
                    #going down
                    UP = 1
                    
                    j = scene_info.ball[0]
                    k = scene_info.ball[1]
                    while(j > 0 and k < 400):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j-1
                        k = k+1
                        hit = False
                    if(hit==False):
                        j = scene_info.ball[0]
                        k = scene_info.ball[1]+3
                        while(j > 0 and k < 400):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j-1
                            k = k+1
                            hit = False
                    if(hit==False):
                        j = -1
                        k = -1
                    
        else:
                LR = 0
                if(last_ball_y - scene_info.ball[1] > 0):
                    #going up
                    UP = 0
                    
                    #U.R
                    j = scene_info.ball[0]
                    k = scene_info.ball[1]
                    while(j < 200 and k > 0):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j+1
                        k = k-1
                        hit = False
                    if(hit==False):
                        j = scene_info.ball[0]
                        k = scene_info.ball[1]-3
                        while(j < 200 and k > 0):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j+1
                            k = k-1
                            hit = False
                    if(hit==False):
                        j = -1
                        k = -1
                else:
                    #going down
                    UP = 1
                    
                    #D.R.
                    j =scene_info.ball[0]+3
                    k = scene_info.ball[1]
                    while(j < 200 and k < 400):
                        if(table[j][k] == 1):
                            hit = True
                            break
                        j = j+1
                        k = k+1
                        hit = False
                    if(hit==False):
                        j = scene_info.ball[0]
                        k = scene_info.ball[1]
                        while(j < 200 and k < 400):
                            if(table[j][k] == 1):
                                hit = True
                                break
                            j = j+1
                            k = k+1
                            hit = False
                    if(hit==False):
                        j = -1
                        k = -1
                    
        
        inp_temp = np.array([scene_info.ball[0],scene_info.ball[1],LR,UP,m,scene_info.platform[0],j,k])
        input = inp_temp[np.newaxis,:]
        
        if scene_info.status == GameStatus.GAME_OVER or \
            scene_info.status == GameStatus.GAME_PASS:
            games = games + 1
            print(games)
            if(scene_info.status == GameStatus.GAME_OVER):
                print('game over')
                gameover = gameover + 1
                print((games - gameover) / games)
            # Do some stuff if needed
            # 3.2.1. Inform the game process that ml process is ready
            comm.ml_ready()
            continue
        
            
        
        
        move = model.predict(input)
        print(move)
    
        # 3.3. Put the code here to handle the scene information

        # 3.4. Send the instruction for this frame to the game process
        
        if(move< -0.1):
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_LEFT)
        elif(move> 0.1):
            comm.send_instruction(scene_info.frame, PlatformAction.MOVE_RIGHT)
        else:
            comm.send_instruction(scene_info.frame, PlatformAction.NONE)
    
            

