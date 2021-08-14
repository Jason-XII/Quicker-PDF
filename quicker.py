from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilenames, askopenfilename, asksaveasfilename
from ttkthemes import ThemedTk 
from pdf_machine import *
from os.path import split
	
root = Tk()
tabs = Notebook(root, padding=(10, 10, 10, 20))
merge_files_list = []
add_file_icon = None
# build the merge widget
def build_merge_widget():
    global add_file_icon
    def merge_add_file_on_click():
        filenames = askopenfilenames(filetypes=[("PDF文件", "*.pdf")])
        if not filenames:
            return
        for fn in filenames:
        	pdf_listview.insert(END, split(fn)[-1])
        	merge_files_list.append(fn)
        file_path.delete(0, END)
        file_path.insert(0, filenames[-1])

    def delete_one_item():
        merge_files_list.pop(pdf_listview.curselection()[0])
        pdf_listview.delete(ANCHOR)

    def clear_list():
        merge_files_list = []
        pdf_listview.delete(0, END)

    def move_item_up():
        index = pdf_listview.curselection()[0]
        if index == 0:
            return
        merge_files_list[index-1], merge_files_list[index] = merge_files_list[index], merge_files_list[index-1]
        refresh_list()
        pdf_listview.selection_set(index-1)

    def move_item_down():
        index = pdf_listview.curselection()[0]
        if index == len(merge_files_list)-1:
            return
        merge_files_list[index+1], merge_files_list[index] = merge_files_list[index], merge_files_list[index+1]
        refresh_list()
        pdf_listview.selection_set(index+1)

    def refresh_list():
        pdf_listview.delete(0, END)
        for fn in merge_files_list:
            pdf_listview.insert(END, split(fn)[-1])

    def merge():
        out_filename = asksaveasfilename(filetypes=[("PDF文件", "*.pdf")])
        if not out_filename:
            return
        machine = PDFMergeMachine(merge_files_list)
        machine.merge(out_filename + '.pdf')

    tab_merge = Frame(root)
    file_path = Entry(tab_merge)
    file_path.insert(0, "这里会显示文件路径")
    file_path.grid(row=0, column=0, sticky=NSEW)
    tab_merge.columnconfigure(index=0, weight=1)
    add_file_icon = PhotoImage(file="打开文件.png")
    add_file_icon = add_file_icon.subsample(2, 2)
    btn_add_file = Button(master=tab_merge, command=merge_add_file_on_click, text="添加PDF", image=add_file_icon, compound="left")
    btn_add_file.grid(row=0, column=1, sticky=NSEW)
    tab_merge.columnconfigure(index=1, weight=0)
    pdf_listview = Listbox(tab_merge)
    pdf_listview.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    btn_delete_file = Button(tab_merge, text="删除选中项目", command=delete_one_item)
    btn_delete_file.grid(row=2, column=0, sticky=NSEW)
    btn_clear = Button(tab_merge, text="清空列表", command=clear_list)
    btn_clear.grid(row=2, column=1, sticky=NSEW)
    btn_move_up = Button(tab_merge, text="上移项目", command=move_item_up)
    btn_move_up.grid(row=3, column=0, sticky=NSEW)
    btn_move_down = Button(tab_merge, text="下移项目", command=move_item_down)
    btn_move_down.grid(row=3, column=1, sticky=NSEW)
    btn_merge = Button(tab_merge, command=merge, text="合并PDF")
    btn_merge.grid(row=4, column=0, columnspan=2, sticky=NSEW)
    return tab_merge


tab_merge = build_merge_widget()
tab_extract = Frame(root)
tab_delete = Frame(root)
tabs.add(tab_merge, text="合并PDF")
tabs.add(tab_extract, text="抽取PDF页码")
tabs.add(tab_delete, text="删除PDF页码")
tabs.pack(fill=BOTH, expand=True)
root.mainloop()


	
