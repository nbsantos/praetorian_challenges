import argparse
import csv
import sys
from machine_server import Server

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Generate a file with training samples.')
	parser.add_argument('samples', type=int, help='number of samples to download')
	parser.add_argument('features', help='features file name')
	parser.add_argument('labels', help='labels file name')
	args = parser.parse_args()

	x_writer = csv.writer(open(args.features, 'a'))
	y_writer = csv.writer(open(args.labels, 'a'))

	s = Server()

	for i in range(args.samples):
		if i % 100 == 0:
			print(f"Generated {i} samples.")

		# query the /challenge endpoint
		s.get()

		# choose a random target and /solve
		target = 'arm'
		s.post(target)

		x_writer.writerow([b for b in s.binary])
		y_writer.writerow([s.ans])
