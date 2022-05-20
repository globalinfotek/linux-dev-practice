# Based on examples from The Linux Kernel Module Programming Guide Chapter 2
# https://tldp.org/LDP/lkmpg/2.6/html/lkmpg.html#AEN181

obj-m += 201_source.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
