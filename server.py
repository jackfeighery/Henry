import socket
from _thread import *
from fighter import Fighter
import pygame
import pickle
from pickable_surface import PickleableSurface

# Server configuration
host = '192.168.0.15'  # Server IP address
port = 5555       # Server port number

# Create a socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except socket.error as e:
    str(e)

s.listen(2)  # Listen for up to 2 clients

print("Server is listening on {}:{}".format(host, port))

idle_frames_r = [PickleableSurface(pygame.image.load(f'0{i}.gif')) for i in range(1, 5)]
idle_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in idle_frames_r]  # Flip frames for idle left

walk_frames_r = [PickleableSurface(pygame.image.load(f'walk/0{i}.gif')) for i in range(1, 9)]
walk_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in walk_frames_r]  # Flip frames for walking left

punch_frames_r = [PickleableSurface(pygame.image.load(f'punch/0{i}.gif')) for i in range(1, 9)]
punch_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in punch_frames_r]  # Flip frames for punching left

block_frames_r = [PickleableSurface(pygame.image.load(f'block/0{i}.gif')) for i in range(1, 4)]
block_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in block_frames_r]  # Flip frames for blocking left

duck_frames_r = [PickleableSurface(pygame.image.load(f'duck/d0{i}.gif')) for i in range(1, 4)]
duck_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in duck_frames_r]  # Flip frames for ducking left

special_frames_r = [PickleableSurface(pygame.image.load(f'special/f0{i}.gif')) for i in range(1, 4)]
special_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in special_frames_r]

# Load jump frames
jump_frames_r = [PickleableSurface(pygame.image.load(f'jump/f0{i}.gif')) for i in range(1, 9)]
jump_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in jump_frames_r]

hit_reaction_frames_r = [PickleableSurface(pygame.image.load(f'hitdetect/h0{i}.gif')) for i in range(1, 4)]
hit_reaction_frames_l = [PickleableSurface(pygame.transform.flip(frame, True, False)) for frame in hit_reaction_frames_r]  # Flip frames for hit reaction left

fighter = Fighter(100, 400)
fighter2 = Fighter(500, 400)
# pos = [(100, 400), (500, 400)]
players = [fighter, fighter2]
def threaded_client(conn, player):
    conn.send(pickle.dumps(players[player]))
    reply = ""
    while True:
        try:
            data = pickle.loads(conn.recv(8192*16))# number can be changed 
            players[player] = data
            
            if not data:  
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = players[0]
                else:
                    reply = players[1]
                print("Received: ", data)
                print("Sending: ", reply)

            conn.sendall(pickle.dumps(reply))
        except:
            break

    print("Lost connection")
    conn.close()

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print("Accepted connection from {}:{}".format(addr[0], addr[1]))
   
    start_new_thread(threaded_client, (conn,currentPlayer))
    currentPlayer += 1





# # Function to handle client connections
# def handle_client(client_socket):
#     while True:
#         data = client_socket.recv(1024).decode('utf-8')
#         if not data:
#             break
#         print("Received from client: {}".format(data))
#         response = "Server received your message: {}".format(data)
#         client_socket.send(response.encode('utf-8'))
#     client_socket.close()
    

    # fighter_images = {
#     "idle_frames_r": ['0{}.gif'.format(i) for i in range(1, 5)],
#     "idle_frames_l": ['0{}.gif'.format(i) for i in range(1, 5)],
#     "walk_frames_r": ['walk/0{}.gif'.format(i) for i in range(1, 9)],
#     "walk_frames_l": ['walk/0{}.gif'.format(i) for i in range(1, 9)],
#     "punch_frames_r": ['punch/0{}.gif'.format(i) for i in range(1, 9)],
#     "punch_frames_l": ['punch/0{}.gif'.format(i) for i in range(1, 9)],
#     "block_frames_r": ['block/0{}.gif'.format(i) for i in range(1, 4)],
#     "block_frames_l": ['block/0{}.gif'.format(i) for i in range(1, 4)],
#     "duck_frames_r": ['duck/d0{}.gif'.format(i) for i in range(1, 4)],
#     "duck_frames_l": ['duck/d0{}.gif'.format(i) for i in range(1, 4)],
#     "special_frames_r": ['special/f0{}.gif'.format(i) for i in range(1, 4)],
#     "special_frames_l": ['special/f0{}.gif'.format(i) for i in range(1, 4)],
#     "jump_frames_r": ['jump/f0{}.gif'.format(i) for i in range(1, 9)],
#     "jump_frames_l": ['jump/f0{}.gif'.format(i) for i in range(1, 9)],
#     "hit_reaction_frames_r": ['hitdetect/h0{}.gif'.format(i) for i in range(1, 4)],
#     "hit_reaction_frames_l": ['hitdetect/h0{}.gif'.format(i) for i in range(1, 4)]
# }
# idle_frames_r = [pygame.image.load(f'0{i}.gif') for i in range(1, 5)]
# idle_frames_l = [pygame.transform.flip(frame, True, False) for frame in idle_frames_r]  # Flip frames for idle left
# walk_frames_r = [pygame.image.load(f'walk/0{i}.gif') for i in range(1, 9)]
# walk_frames_l = [pygame.transform.flip(frame, True, False) for frame in walk_frames_r]  # Flip frames for walking left
# punch_frames_r = [pygame.image.load(f'punch/0{i}.gif') for i in range(1, 9)]
# punch_frames_l = [pygame.transform.flip(frame, True, False) for frame in punch_frames_r]  # Flip frames for punching left
# block_frames_r = [pygame.image.load(f'block/0{i}.gif') for i in range(1, 4)]
# block_frames_l = [pygame.transform.flip(frame, True, False) for frame in block_frames_r]  # Flip frames for blocking left
# duck_frames_r = [pygame.image.load(f'duck/d0{i}.gif') for i in range(1, 4)]
# duck_frames_l = [pygame.transform.flip(frame, True, False) for frame in duck_frames_r]
# special_frames_r = [pygame.image.load(f'special/f0{i}.gif') for i in range(1, 4)]
# special_frames_l = [pygame.transform.flip(frame, True, False) for frame in special_frames_r]
# # Load jump frames
# jump_frames_r = [pygame.image.load(f'jump/f0{i}.gif') for i in range(1, 9)]
# jump_frames_l = [pygame.transform.flip(frame, True, False) for frame in jump_frames_r]
# hit_reaction_frames_r = [pygame.image.load(f'hitdetect/h0{i}.gif') for i in range(1, 4)]
# hit_reaction_frames_l = [pygame.transform.flip(frame, True, False) for frame in hit_reaction_frames_r]  # Flip frames for hit reaction left
# Function to create a dictionary containing fighter positions and game state data