from sha256 import sha256_hash as sha256
from server import start_server
import random
import time
import threading


UINT16 = (2 ** 16)
records = {}

def create_record():
	# Generate a random number
	r = random.randint(0, UINT16)

	# Hash the generated number
	hash256 = sha256(r)

	# Return a new record values
	return r, hash256


def main():
	# Continously create and store new records
	while True:
		# Crate a new record
		key, val = create_record()

		# Print new record values on the screen
		print(f"{key} -> {val[:4]}..{val[-6:]}")

		# Store the new record in a dict
		records[key] = val
		time.sleep(2.5)


if __name__ == '__main__':
	# Create and start a thread
	thread = threading.Thread(target=start_server)
	thread.start()

	main()