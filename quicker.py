from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfilenames, askopenfilename, asksaveasfilename
from ttkthemes import ThemedTk
from pdf_machine import *
from os.path import split, exists
import plyer.platforms.win.notification
from plyer import notification

root = ThemedTk(theme='arc')
tabs = Notebook(root, padding=(10, 10, 10, 20))

merge_files_list = []
extract_file_data = []

add_file_icon = PhotoImage(file="打开文件.png").subsample(2, 2)
delete_item_icon = PhotoImage(file="删除一项.png").subsample(2, 2)
clear_items_icon = PhotoImage(file="删除.png").subsample(2, 2)
move_item_up_icon = PhotoImage(file="up.png").subsample(2, 2)
move_item_down_icon = PhotoImage(file='down.png').subsample(2, 2)
merge_icon = PhotoImage(file='merge.png').subsample(20, 20)
add_to_list_icon = PhotoImage(file='添加.png').subsample(2, 2)
download_icon = PhotoImage(file='下载文件.png').subsample(2, 2)


# build the merge widget
def build_merge_widget():
    def merge_add_file_on_click():
        filenames = askopenfilenames(filetypes=[("PDF文件", "*.pdf")])
        if not filenames:
            return
        for fn in filenames:
            pdf_listview.insert(END, split(fn)[-1])
            merge_files_list.append(fn)
        file_path['state'] = 'active'
        file_path.delete(0, END)
        file_path.insert(0, filenames[-1])
        file_path['state'] = 'readonly'

    def delete_one_item():
        merge_files_list.pop(pdf_listview.curselection()[0])
        pdf_listview.delete(ANCHOR)

    def clear_list():
        merge_files_list.clear()
        pdf_listview.delete(0, END)

    def move_item_up():
        index = pdf_listview.curselection()[0]
        if index == 0:
            return
        merge_files_list[index - 1], merge_files_list[index] = merge_files_list[index], merge_files_list[index - 1]
        refresh_list()
        pdf_listview.selection_set(index - 1)

    def move_item_down():
        index = pdf_listview.curselection()[0]
        if index == len(merge_files_list) - 1:
            return
        merge_files_list[index + 1], merge_files_list[index] = merge_files_list[index], merge_files_list[index + 1]
        refresh_list()
        pdf_listview.selection_set(index + 1)

    def refresh_list():
        pdf_listview.delete(0, END)
        for fn in merge_files_list:
            pdf_listview.insert(END, split(fn)[-1])

    def merge():
        out_filename = asksaveasfilename(filetypes=[("PDF文件", "*.pdf")])
        if not out_filename:
            return
        try:
            machine = PDFMergeMachine(merge_files_list)
            machine.merge(out_filename + ".pdf")
        except Exception as err:
            notification.notify(
                title='错误', message='合并错误：' + str(err), app_icon='pdf-window.ico')
        else:
            notification.notify(
                title='成功', message='成功合并PDF，已导出！', app_icon='pdf-window.ico')


    merge_tab = Frame(root)
    file_path = Entry(merge_tab)
    file_path.insert(0, "这里会显示文件路径")
    file_path['state'] = 'readonly'
    file_path.grid(row=0, column=0, sticky=NSEW)
    merge_tab.columnconfigure(index=0, weight=1)
    btn_add_file = Button(master=merge_tab, command=merge_add_file_on_click, text="添加PDF", image=add_file_icon,
                          compound="left")
    btn_add_file.grid(row=0, column=1, sticky=NSEW)
    merge_tab.columnconfigure(index=1, weight=0)
    pdf_listview = Listbox(merge_tab)
    pdf_listview.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    btn_delete_file = Button(merge_tab, text="删除选中项目", command=delete_one_item, image=delete_item_icon, compound="left")
    btn_delete_file.grid(row=2, column=0, sticky=NSEW)
    btn_clear = Button(merge_tab, text="清空列表", command=clear_list, image=clear_items_icon, compound="left")
    btn_clear.grid(row=2, column=1, sticky=NSEW)
    btn_move_up = Button(merge_tab, text="上移项目", command=move_item_up, image=move_item_up_icon, compound="left")
    btn_move_up.grid(row=3, column=0, sticky=NSEW)
    btn_move_down = Button(merge_tab, text="下移项目", command=move_item_down, image=move_item_down_icon, compound="left")
    btn_move_down.grid(row=3, column=1, sticky=NSEW)
    btn_merge = Button(merge_tab, command=merge, text="合并PDF", image=merge_icon, compound='left')
    btn_merge.grid(row=4, column=0, columnspan=2, sticky=NSEW)
    merge_tab.rowconfigure(1, weight=1)
    return merge_tab


def build_extract_widget():
    def extract_add_file_on_click():
        filename = askopenfilename(filetypes=[("PDF文件", "*.pdf")])
        if not filename:
            return
        file_path['state'] = 'active'
        file_path.delete(0, END)
        file_path.insert(0, filename)
        file_path['state'] = 'readonly'

    def add_to_list():
        start = int(spin_start_page.get())
        end = int(spin_end_page.get())
        if start > end or start < 1 or end < 1:
            return
        if not file_path.get():
            return
        if not exists(file_path.get()):
            return
        extract_file_data.append((file_path.get(), start, end))
        pdf_listview.insert(END, split(file_path.get())[-1]+'中的第'+str(start)+'页至'+str(end)+'页')

    def delete_one_item():
        extract_file_data.pop(pdf_listview.curselection()[0])
        pdf_listview.delete(ANCHOR)

    def clear_list():
        extract_file_data.clear()
        pdf_listview.delete(0, END)

    def move_item_up():
        index = pdf_listview.curselection()[0]
        if index == 0:
            return
        extract_file_data[index - 1], extract_file_data[index] = extract_file_data[index], extract_file_data[index - 1]
        refresh_list()
        pdf_listview.selection_set(index - 1)

    def move_item_down():
        index = pdf_listview.curselection()[0]
        if index == len(merge_files_list) - 1:
            return
        extract_file_data[index + 1], extract_file_data[index] = extract_file_data[index], extract_file_data[index + 1]
        refresh_list()
        pdf_listview.selection_set(index + 1)

    def refresh_list():
        pdf_listview.delete(0, END)
        for (filename, start, end) in extract_file_data:
            pdf_listview.insert(END, split(filename)[-1])

    def extract():
        save_filename = asksaveasfilename(filetypes=[("PDF文件", "*.pdf")])
        if not save_filename:
            return
        extract_machine = PDFExtractMachine(extract_file_data)
        try:
            extract_machine.extract_all(save_filename)
        except Exception as err:
            notification.notify(
                title='错误', message='抽取PDF错误：' + str(err), app_icon='pdf-window.ico')
        else:
            notification.notify(
                title='成功', message='成功抽取PDF，已导出！', app_icon='pdf-window.ico')


    tab_extract = Frame(root)
    file_path = Entry(tab_extract)
    file_path.insert(0, "这里会显示文件路径")
    file_path['state'] = 'readonly'
    file_path.grid(row=0, column=0, sticky=NSEW)
    btn_add_file = Button(master=tab_extract, command=extract_add_file_on_click, text="添加PDF", image=add_file_icon,
                          compound="left")
    btn_add_file.grid(row=0, column=1, sticky=NSEW)
    second_line_frame = Frame(tab_extract)
    spin_start_page = Spinbox(second_line_frame)
    spin_start_page.grid(row=0, column=0, sticky=NSEW)
    spin_start_page.set(1)
    spin_end_page = Spinbox(second_line_frame)
    spin_end_page.grid(row=0, column=1, sticky=NSEW)
    spin_end_page.set(1)
    btn_add_to_list = Button(second_line_frame, text='添加项目至列表', command=add_to_list, image=add_to_list_icon, compound='left')
    btn_add_to_list.grid(row=0, column=2, sticky=NSEW)
    second_line_frame.grid(row=1, column=0, columnspan=2, sticky=NSEW)
    pdf_listview = Listbox(tab_extract)
    pdf_listview.grid(row=2, column=0, columnspan=2, sticky=NSEW)
    btn_delete_file = Button(tab_extract, text="删除选中项目", command=delete_one_item, image=delete_item_icon,
                             compound="left")
    btn_delete_file.grid(row=3, column=0, sticky=NSEW)
    btn_clear = Button(tab_extract, text="清空列表", command=clear_list, image=clear_items_icon, compound="left")
    btn_clear.grid(row=3, column=1, sticky=NSEW)
    btn_move_up = Button(tab_extract, text="上移项目", command=move_item_up, image=move_item_up_icon, compound="left")
    btn_move_up.grid(row=4, column=0, sticky=NSEW)
    btn_move_down = Button(tab_extract, text="下移项目", command=move_item_down, image=move_item_down_icon, compound="left")
    btn_move_down.grid(row=4, column=1, sticky=NSEW)
    btn_extract = Button(tab_extract, command=extract, text="抽取PDF", image=download_icon, compound='left')
    btn_extract.grid(row=5, column=0, columnspan=2, sticky=NSEW)
    tab_extract.columnconfigure(index=0, weight=1)
    tab_extract.rowconfigure(index=2, weight=1)
    return tab_extract


tab_merge = build_merge_widget()
tab_extract = build_extract_widget()
tab_delete = Frame(root)
tabs.add(tab_merge, text="合并PDF")
tabs.add(tab_extract, text="抽取PDF页码")
tabs.add(tab_delete, text="删除PDF页码")
tabs.pack(fill=BOTH, expand=True)
root.resizable(False, False)
root.mainloop()
