import os
import socket
import sys
import threading

def read_msg(sock_cli):
    while True:
        # terima pesan
        data = sock_cli.recv(65535)
        if len(data) == 0:
            break

        if data.decode("utf-8") == "send":
            # print("testsendfile")

            header = sock_cli.recv(4096).decode("utf-8")
            filename = header.partition("name: ")[2]
            filesize = int(header.split()[1])
            print(f"[SERVER] {header}")
            print(f"[SERVER] {filename}, {str(filesize)}")

            filedata = sock_cli.recv(filesize)

            file = open("{}\\".format(username)+filename, "wb")
            file.write(filedata)
            file.close()
        else:
            print(data)
    sock_cli.close()

# ambil nama user dari command line arguments
username = sys.argv[1]

if not os.path.exists(username):
    os.mkdir(username)

# buat obj socket
sock_cli = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect
sock_cli.connect(("127.0.0.1", 8000))

# kirim username
sock_cli.send(bytes(username, "utf-8"))

# buat thread untuk membaca pesan dan jalankan thread
thread_cli = threading.Thread(target=read_msg, args=(sock_cli,))
thread_cli.start()

while True:
    # kirim/terima pesan
    command = input("Masukkan Command/Tujuan: ")
    msg = input("Masukkan Argumen/Pesan: ")
    if msg == "exit":
        sock_cli.close()
        break

    sock_cli.send(bytes("{}|{}".format(command, msg), "utf_8"))

    if command == "sendfile":
        msg = msg.replace('"', "")
        target = msg.split()[0] # Username target

        filename = msg.partition("{} ".format(target))[2]
        fullname = "{}\\".format(username)+filename
        file = open(fullname, "rb")
        filestats = os.stat(fullname)
        filesize = filestats.st_size
        filedata = file.read()

        # make and send header
        header = "[HEADER]size: "+str(filesize)+" name: "+filename
        sock_cli.send(str(header).encode("utf-8"))

        # send and close file
        sock_cli.send(filedata)
        file.close()