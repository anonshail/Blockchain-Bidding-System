from tkinter import *

def run():
    os.system("docker exec -it biddingclient bash & python3 client.py showItem")

def start():
	top = Tk()
	top.geometry("750x500")

	title = Label(top, text="ADD ITEM").grid(row=0,column=0)
	item_id= Label(top, text="ID:").grid(row=1,column=0)
	item_id_text= Text(top, height=2, width=5).grid(row=2,column=0)
	item_name= Label(top, text="Name:").grid(row=1,column=1)
	item_name_text= Text(top, height=2, width=5).grid(row=2,column=1)
	item_desc= Label(top, text="Description:").grid(row=3,column=0)
	item_desc_text= Text(top, height=4, width=5).grid(row=5,column=0)
	item_timestamp= Label(top, text="Time:").grid(row=3,column=1)
	timestamp_text=Text(top, height=2, width=5).grid(row=3, column=1)
	item_duration= Label(top, text="Duration:").grid(row=5,column=0)
	duration_text=Text(top, height=2, width=5).grid(row=6, column=0)
	submit_btn= Button(top, text="SUBMIT", command="run", relief=RIDGE, bg="#ff3333", activebackground="#ff3333", fg="white", font=("Times New Roman", 18), borderwidth="1", padx="10px").grid(row=7, column=0, columnspan=2)


