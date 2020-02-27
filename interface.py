from tkinter import *

from tkinter.ttk import *
import commands

def start():
   window = Tk()

   window.title("Antonio Andraues Scanner App")
   options_host = IntVar()
   options_tcp_udp = IntVar()

   def sel():
      if(options_host.get()==1):
         selection = "Specific Host to scan (example: 192.168.0.10)  :"
         texto_s_host.config(text = selection)
      else:
         selection = "Range of scan  (example: 192.168.0.0/24)  :"
         texto_s_host.config(text = selection)
   

   def clicked():

      host=txt.get()
   
      if(not chk_state.get()):
         port_range = ports_entry.get()
      else:
         port_range = "1-65535"
      start_port, end_port = port_range.split("-")
      start_port, end_port = int(start_port), int(end_port)
      ports = [ p for p in range(start_port, end_port)]
      if(options_host.get()==1):
         commands.main(host,ports,options_tcp_udp.get())
      else:
         all_ips = commands.discover_hosts(host)
         for ip in all_ips:
            commands.main(ip,ports,options_tcp_udp.get())


   main_text = Label(window, text="Welcome to Antonio Andraues Scanner App",font=("Arial Bold", 30))
   chk_text =  Label(window, text="Select range of ports (example :  0 - 1023) :",font=("Arial Bold",10))
   texto_s_host = Label(window,font=("Arial Bold",10))
   txt = Entry(window,width=10)
   ports_entry = Entry(window,width=10)


   main_text.grid(column=2, row=0)


   
   rad1 = Radiobutton(window,text='TCP', value=1, variable=options_tcp_udp)
   rad2 = Radiobutton(window,text='UDP', value=0, variable=options_tcp_udp)
   rad_s = Radiobutton(window,text='Specific Host to scan', value=1, variable=options_host,command=sel)
   rad_r = Radiobutton(window,text='Range of scan', value=2, variable=options_host,command=sel)




   btn = Button(window, text="Run", command=clicked)

   rad1.grid(column=2, row=4)

   rad2.grid(column=2, row=5)

   rad_s.grid(column=2,row=1)
   rad_r.grid(column=2,row=2)
   texto_s_host.grid(column=1,row=3)
   txt.grid(column=2, row=3)
   
   ports_entry.grid(column=3,row=6)
   chk_text.grid(column=2,row=6)
   btn.grid(column=3, row=7) 
   window['bg'] = '#ECECEC'
   chk_state = BooleanVar()
   

   chk_state.set(True) #set check state
      
   chk = Checkbutton(window, text='Port Default - (Default = 1-65535)', var=chk_state)

   chk.grid(column=1, row=6)


   window.mainloop()