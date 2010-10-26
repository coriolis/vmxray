import os
env = Environment()

#set install directory
install_dir="./install"

#list of files to install
install_files_bin_win=[ Glob('src/bin/win/x86/*') ]
install_files_bin_linux=[ Glob('src/bin/linux/x86/*') ]
install_files_bin=[ Glob('src/bin/*.py') ] + [ Glob('src/conf/*')]

if env['PLATFORM'] == "win32" :
    install_files_bin+=install_files_bin_win
elif env['PLATFORM'] == "posix" :
    install_files_bin+=install_files_bin_linux

install_files_lib=[
                  'src/lib/vm_inspector'
                  ]

#install target related
env.Alias('install', install_dir)
env.Install(os.path.join(install_dir, 'bin'), install_files_bin)
env.Install(os.path.join(install_dir, 'lib'), install_files_lib)

if not 'rebuild' in COMMAND_LINE_TARGETS :
    Execute(Mkdir(os.path.join(install_dir, 'tmp')))

#to rebuild
env.Command('rebuild', '', 'make' )

Default('install')

