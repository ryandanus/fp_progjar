import socket
import threading

def read_msg(clients, sock_cli, addr_cli, username_cli):
    # clients = daftar client
    # sock_cli = socket client (dipakai untuk kirim pesan (send(sock_cli, data))
    # addr_cli = address client
    # username_cli = username client (dipakai untuk iterasi clients (clients[username_cli][n])
    while True:
        # terima pesan
        data = sock_cli.recv(65535).decode("utf-8")
        if len(data) == 0:
            break

        # parsing pesan
        command, msg = data.split("|") # command dan isi pesan

        announce = "<{}>: {}|{}".format(username_cli, command, msg) # isi pesan setelah diformat (bcast dan send msg)

        # teruskan pesan ke semua client
        if command == "bcast":
            send_broadcast(clients, announce, addr_cli)

        # Add friend
        elif command == "addfriend":
            # requester = username_cli/sock_cli, target = msg/dest_sock_cli
            if msg in clients: # cek keberadaan username client
                if msg == username_cli:
                    send_msg(sock_cli, "Kamu tidak bisa berteman dengan diri sendiri!")
                elif msg in clients[username_cli][3]:
                    send_msg(sock_cli, "Kamu sudah berteman dengan " + msg)
                else:
                    # konfirmasi ke sender
                    send_msg(sock_cli, "Kamu sekarang berteman dengan " + msg)
                    clients[username_cli][3].add(msg)

                    # konfirmasi ke target
                    dest_sock_cli = clients[msg][0]
                    send_msg(dest_sock_cli, "Kamu sekarang berteman dengan " + username_cli)
                    clients[msg][3].add(username_cli)
            else:
                send_msg(sock_cli, "User {} tidak dikenali".format(msg))
        # Remove Friend
        elif command == "removefriend":
            # requester = username_cli/sock_cli, target = msg/dest_sock_cli
            if msg in clients:
                if msg == username_cli:
                    send_msg(sock_cli, "Kamu tidak bisa berteman dengan diri sendiri!")
                elif msg in clients[username_cli][3]:
                    # konfirmasi ke sender
                    send_msg(sock_cli, "Kamu tidak lagi berteman dengan " + msg)
                    clients[username_cli][3].remove(msg)

                    # konfirmasi ke target
                    dest_sock_cli = clients[msg][0]
                    send_msg(dest_sock_cli, "Kamu tidak lagi berteman dengan " + username_cli)
                    clients[msg][3].remove(username_cli)
                else:
                    send_msg(sock_cli, "Kamu belum berteman dengan " + msg)
            else:
                send_msg(sock_cli, "User {} tidak dikenali".format(msg))
        # Friend Lists
        elif command == "friendlist":
            if len(clients[username_cli][3]) == 0 :
                send_msg(sock_cli, "Kamu belum memiliki teman")
            else:
                send_msg(sock_cli, "Daftar Teman: " + str(clients[username_cli][3]))
        # Send to Friends
        elif command == "friends":
            for friend in clients[username_cli][3]:
                dest_sock_cli = clients[friend][0]
                send_msg(dest_sock_cli, announce)
        elif command == "sendfile":
            # setelah sendfile, cek string msg untuk melihat target user dan nama file yang akan dikirim
            msg = msg.replace('"', "")
            target = msg.split()[0] # Username target

            dest_sock_cli = clients[target][0]
            send_msg(dest_sock_cli, "send")

            header = sock_cli.recv(4096).decode("utf-8")
            filename = header.partition("name: ")[2]
            filesize = int(header.split()[1])
            print(f"[SERVER] {header}")
            print(f"[SERVER] {filename}, {str(filesize)}")

            filedata = b''

            while True:
                packet = sock_cli.recv(65535)
                filedata += packet
                if len(packet) < 65535:
                    break

            dest_sock_cli.send(str(header).encode("utf-8"))
            dest_sock_cli.send(filedata)
        else:
            try:
                dest_sock_cli = clients[command][0]
                send_msg(dest_sock_cli, announce)
            except:
                send_msg(sock_cli, "Command atau User {} tidak dikenali".format(command))

        print(announce)

    # client dc
    for client in clients:
        if username_cli in clients[client][3]:
            clients[client][3].remove(username_cli)
    sock_cli.close()
    print("Connection closed", addr_cli)

# fungsi broadcast
def send_broadcast(clients, data, sender_addr_cli):
    for sock_cli, addr_cli, username_cli, friends_cli in clients.values():
        if not (addr_cli[0] == sender_addr_cli[0] and addr_cli[1] == sender_addr_cli[1]):
            send_msg(sock_cli,data)

def send_msg(sock_cli, data):
    sock_cli.send(bytes(data, "utf-8"))

# buat object socket server
sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding object socket ke alamat IP dan port
sock_server.bind(("127.0.0.1", 8000))

# listen
sock_server.listen(5)

# buat dictionary untuk menyimpan info client
clients = {}

while True:
    # accept connection
    sock_cli, addr_cli = sock_server.accept()

    # read username client
    username_cli = sock_cli.recv(65535).decode("utf-8")
    print(username_cli," joined")

    # buat thread baru untuk membaca pesan dan jalankan threadnya
    thread_cli = threading.Thread(target=read_msg, args=(clients, sock_cli, addr_cli, username_cli))
    thread_cli.start()

    friends_cli = set()

    # simpan info ttg client ke dictionary
    clients[username_cli] = (sock_cli, addr_cli, thread_cli, friends_cli)