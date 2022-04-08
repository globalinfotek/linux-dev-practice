# CC: The compiler
CC = gcc
# CFLAGS: A collection of commonly used gcc options
CFLAGS = -Wall
# DEPS: List of dependencies
DEPS = 
# DIST: Distribution directory
DIST = ./dist/
# OBJ: List of necessary object files
OBJ = 101_source.o

%.o: %.c $(DEPS)
	$(CC) -c -o $(DIST)$@ $< $(CFLAGS)

101_challenge.bin: $(OBJ)
	$(CC) -o $(DIST)$@ $(DIST)$^ $(CFLAGS)

clean:
	rm -f $(DIST)*.o $(DIST)*.exe $(DIST)*.bin $(DIST)*.lib $(DIST)*.so $(DIST)*.egg

# Formats and usage drawn from:
#	https://www.gnu.org/software/make/manual/html_node/Simple-Makefile.html
#	https://www.cs.colby.edu/maxwell/courses/tutorials/maketutor/
