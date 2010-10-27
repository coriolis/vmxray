VMxray
---------
VMxray looks into VM image of a machine and provides details of installed
OS and application in it, without running the VM.

It uses Sleuthkit(http://www.sleuthkit.org), QEMU (http://wiki.qemu.org) and 
reglookup (http://projects.sentinelchicken.org/reglookup/).

VMxray runs on Linux as well as Windows.

* Requirements
- Python 2.5 or above
- scons
- Build dependencies of Sleuthkit, QEMU and readreg

Use pre-built binaries
----------------------
- Pre-built binaries for Windows and Linux are provided which can be used
instead of building all from scratch.
- Linux binaries are compiled and tested on Ubuntu 8.0.4
- Windows binaries are built with Visual Studio 8 and tested on Windows 7, XP.

- Run command
$scons install

This will create 'install' directory in current folder and copy required 
files in appropriate folders.

How to use
-----------
- Goto 'bin' directory 
- Run command

$python inspect_vm.py -d <path_to_vm_image_folder>


How to build
-------------
- In top directory run command

$make 
$make install

- This will build required tools and put them in 'build' directory.


