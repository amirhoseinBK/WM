def main():
	from log import log
	log.info("start main proccess and importing")
	from generator import convert
	from sound import Audio, getaudio
	from argparse import ArgumentParser
	from os import system, listdir, makedirs, get_terminal_size as size
	from os.path import exists, join
	from reader import reader

	log.info("imported")
	
	log.info("parsing arguments...")
	parser = ArgumentParser()
	parser.add_argument("path")
	parser.add_argument("-o", "--out", required = False)
	parser.add_argument("--width", type = int, required = False)
	parser.add_argument("--height", type = int, required = False)
	args = parser.parse_args()
	log.info("parsed")
	
	path = args.path
	out = args.out or "output"
	if not exists(out):
		makedirs(out)
	else:
		log.warning("output path is existing. text files will be overwritten.")
	log.info("set width and height of output...")
	width = args.width or size().columns
	height = args.height or size().lines
	
	log.info("start convert proccess")
	details = convert(path, out, width, height, log)
	fps = details["fps"]
	
	log.info("extracting audio...")
	getaudio(path, join(out, "sound.mp3"), log)
	log.info("extracted. make Audio object")
	
	reader(fps, out)
	
	

if __name__ == "__main__":
	main()
