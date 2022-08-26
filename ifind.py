from subprocess import *
from re import *
#import other python program to get input for searching
print("""
██╗    ███████╗██╗███╗   ██╗██████╗ 
██║    ██╔════╝██║████╗  ██║██╔══██╗
██║    █████╗  ██║██╔██╗ ██║██║  ██║
██║    ██╔══╝  ██║██║╚██╗██║██║  ██║
██║    ██║     ██║██║ ╚████║██████╔╝
╚═╝    ╚═╝     ╚═╝╚═╝  ╚═══╝╚═════╝ 
 
""")

search = "अच्छा"
#pop = Popen(['pwsh', 'rg -i --no-crlf --vimgrep{}'.format(search)]) #BINDOZZZ
command = ['bash', '-c', 'rg -i --no-crlf --vimgrep {}'.format(search)]
output = check_output(command)
decoded_output = output.decode('utf-8')
filename = split("[:]", decoded_output, 1)[0]
run(['xdg-open', filename])
