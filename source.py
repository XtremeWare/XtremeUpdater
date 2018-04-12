import tkinter as tk
import tkinter.filedialog
import urllib.request
import os
from os.path import join
from tkinter import ttk
from time import sleep
from _thread import start_new

from theme import *
from style import *
from cw import center_window
from resources import *
import wgmethods
import customfont


def get_data(url):
    return urllib.request.urlopen(url).read()


def all_children(wid, _class=None):
    _list = wid.winfo_children()

    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())

    if _class != None:
        for index, wg in enumerate(_list):
            if wg.winfo_class() != _class:
                _list[index] = None

    _list = [i for i in _list if i != None]

    return _list


class DllUpdater:
    available_dlls = (
        'd3dcompiler_47.dll', 'd3dx9_43.dll', 'npswf32.dll',
        'api-ms-win-core-console-l1-1-0.dll',
        'api-ms-win-core-datetime-l1-1-0.dll',
        'api-ms-win-core-debug-l1-1-0.dll',
        'api-ms-win-core-errorhandling-l1-1-0.dll',
        'api-ms-win-core-file-l1-1-0.dll', 'api-ms-win-core-file-l1-2-0.dll',
        'api-ms-win-core-file-l2-1-0.dll', 'api-ms-win-core-handle-l1-1-0.dll',
        'api-ms-win-core-heap-l1-1-0.dll',
        'api-ms-win-core-interlocked-l1-1-0.dll',
        'api-ms-win-core-libraryloader-l1-1-0.dll',
        'api-ms-win-core-localization-l1-2-0.dll',
        'api-ms-win-core-memory-l1-1-0.dll',
        'api-ms-win-core-namedpipe-l1-1-0.dll',
        'api-ms-win-core-processenvironment-l1-1-0.dll',
        'api-ms-win-core-processthreads-l1-1-0.dll',
        'api-ms-win-core-processthreads-l1-1-1.dll',
        'api-ms-win-core-profile-l1-1-0.dll',
        'api-ms-win-core-rtlsupport-l1-1-0.dll',
        'api-ms-win-core-string-l1-1-0.dll',
        'api-ms-win-core-synch-l1-1-0.dll', 'api-ms-win-core-synch-l1-2-0.dll',
        'api-ms-win-core-sysinfo-l1-1-0.dll',
        'api-ms-win-core-timezone-l1-1-0.dll',
        'api-ms-win-core-util-l1-1-0.dll', 'api-ms-win-crt-conio-l1-1-0.dll',
        'api-ms-win-crt-convert-l1-1-0.dll',
        'api-ms-win-crt-environment-l1-1-0.dll',
        'api-ms-win-crt-filesystem-l1-1-0.dll',
        'api-ms-win-crt-heap-l1-1-0.dll', 'api-ms-win-crt-locale-l1-1-0.dll',
        'api-ms-win-crt-math-l1-1-0.dll',
        'api-ms-win-crt-multibyte-l1-1-0.dll',
        'api-ms-win-crt-private-l1-1-0.dll',
        'api-ms-win-crt-process-l1-1-0.dll',
        'api-ms-win-crt-runtime-l1-1-0.dll', 'api-ms-win-crt-stdio-l1-1-0.dll',
        'api-ms-win-crt-string-l1-1-0.dll', 'api-ms-win-crt-time-l1-1-0.dll',
        'api-ms-win-crt-utility-l1-1-0.dll', 'cg.dll', 'cgd3d9.dll',
        'cggl.dll', 'concrt140.dll', 'd3dx11_43.dll', 'msvcp140.dll',
        'tbb.dll', 'tbbmalloc.dll', 'ucrtbase.dll', 'vccorlib140.dll',
        'vcomp120.dll', 'vcomp140.dll', 'vcruntime140.dll')

    domain = "https://mobasuite.com/downloads/dlls/"
    cache_dir = ".cache"

    def __mkdir(self):
        if not os.path.exists(self.cache_dir):
            os.mkdir(self.cache_dir)

    def __download_dll(self, dllname):
        data = get_data(join(self.domain, dllname))
        with open(join(self.cache_dir, dllname), 'wb') as f:
            f.write(data)

    def __read_dll(self, dllname):
        with open(join(self.cache_dir, dllname), 'rb') as f:
            data = f.read()

        return data

    def __overwrite_dll(self, oldpath, dllname):
        with open(oldpath, 'wb') as f:
            f.write(self.__read_dll(dllname))

    def update_dlls(self, path, dllnames):
        self.__mkdir()
        for dll in dllnames:
            self.__download_dll(dll)
            self.__overwrite_dll(join(path, dll), dll)


class Root(tk.Tk):
    def __init__(self, **kwargs):
        tk.Tk.__init__(self, **kwargs)
        self.attributes("-alpha", 0.0)
        self.iconbitmap(resource_path("img/icon_32.ico"))

        self.top = Window(self)

        self.bind("<Map>", lambda *args: self.top.deiconify())
        self.bind("<Unmap>", lambda *args: self.top.withdraw())
        self.bind("<FocusIn>", lambda *args: self.top.lift())

        self.lift()
        self.top.lift()
        center_window(self.top)
        self.top.attributes("-alpha", 1.0)


class Window(tk.Toplevel):
    def __init__(self, parent=None):
        self.active_tab = "Games"
        self.cont_frm_id = None
        self.flash_browse_button = True
        self.listbox_item_height_defined = False
        self.last_listbox_item_highlight = -1

        def nav_comm(id):
            self.tab_switch(id)

        tk.Toplevel.__init__(self, parent)

        # Window configuration
        self.config(bg=BG, padx=0, pady=0)
        self.title("XtremeUpdater")
        self.transient(parent)
        self.overrideredirect(True)
        self.attributes("-alpha", 0.0)

        # Widget creation
        self.head_frame = tk.Frame(self, width=800, height=32, **frm_cnf)
        self.title_label = tk.Label(
            self.head_frame, text=self.title(), **hlb_cnf)
        self.close_button = tk.Button(
            self.head_frame,
            text="×",
            command=exit,
            **{
                **btn_cnf,
                **btn_head_cnf
            })
        self.minimize_button = tk.Button(
            self.head_frame,
            text="-",
            command=parent.iconify,
            **{
                **btn_cnf,
                **btn_head_cnf
            })
        self.nav_frame = tk.Frame(self, **{**frm_cnf, **nav_frm_cnf})
        self.games_button = tk.Button(
            self.nav_frame,
            text="Games",
            command=lambda: nav_comm("Games"),
            **btn_nav_cnf)
        self.chat_button = tk.Button(
            self.nav_frame,
            text="Chat",
            command=lambda: nav_comm("Chat"),
            **btn_nav_cnf)
        self.system_button = tk.Button(
            self.nav_frame,
            text="System",
            command=lambda: nav_comm("System"),
            **btn_nav_cnf)
        self.cont_canvas = tk.Canvas(self, width=800, height=400, **cnv_cnf)
        self.games_frame = tk.Frame(self, **cont_frm_cnf)
        self.game_path_frame = tk.Frame(self.games_frame, **cont_frm_cnf)
        self.selected_game_label = tk.Label(
            self.game_path_frame, text="Select a game directory", **lb_cnf)
        self.browse_button = tk.Button(
            self.game_path_frame,
            text="\u2026",
            command=self.__update_game_path,
            **btn_cnf)
        self.dll_frame = tk.Frame(
            self.games_frame, **{
                **cont_frm_cnf,
                **{
                    "padx": 0,
                    "pady": 0,
                    "highlightthickness": 0,
                    "bd": 0
                }
            })
        self.dll_selection_nav_frame = tk.Frame(self.dll_frame, **cont_frm_cnf)
        self.available_updates_label = tk.Label(
            self.dll_selection_nav_frame,
            text="Available dll updates",
            **seclb_cnf)
        self.select_all_button = tk.Button(
            self.dll_selection_nav_frame,
            text="Select all",
            command=self.__select_all,
            **btn_cnf)
        self.dll_listbox = tk.Listbox(
            self.dll_frame, width=90, height=13, **listbox_cnf)
        self.listbox_scrollbar = ttk.Scrollbar(
            self.dll_frame, command=self.dll_listbox.yview)
        self.update_button = tk.Button(self.dll_frame, text="Update", command=self.__update_callback, **btn_cnf)
        self.dll_listbox.config(yscrollcommand=self.listbox_scrollbar.set)
        self.system_frame = tk.Frame(self, **cont_frm_cnf)
        self.spectre_patch_lbframe = tk.LabelFrame(
            self.system_frame,
            text="Spectre and Meltdown patch:",
            **lbfrm_cnf,
            width=300,
            height=120)
        self.spectre_patch_disable = tk.Button(
            self.spectre_patch_lbframe,
            text="Disable",
            command=None,
            **btn_cnf)
        self.spectre_patch_enable = tk.Button(
            self.spectre_patch_lbframe, text="Enable", command=None, **btn_cnf)
        self.spectrewrn_label = tk.Label(
            self.spectre_patch_lbframe,
            text=
            "Disabling spectre patch can exhibit you to attacks from hackers, but it can significantly improve system performance on old CPUs. By right-clicking this label you agree with that we dont have any responsibility on potentional damage caused by attackers!",
            **wrnlb_cnf)

        self.spectre_patch_lbframe.pack_propagate(False)

        # Widget display
        self.head_frame.pack(**head_frm_pck)
        self.title_label.pack(**title_lb_pck)
        self.close_button.pack(**btn_head_pck)
        self.minimize_button.pack(**btn_head_pck)
        self.nav_frame.pack(**nav_frm_pck)
        self.games_button.pack(**btn_nav_pck)
        self.chat_button.pack(**btn_nav_pck)
        self.system_button.pack(**btn_nav_pck)
        self.cont_canvas.pack(**cnv_pck)
        # games frame
        self.game_path_frame.pack(anchor='w', fill='x')
        self.selected_game_label.pack(side='left', fill='x')
        self.browse_button.pack(side='right')
        self.dll_frame.pack(fill='both')
        self.dll_selection_nav_frame.pack(fill='x')
        self.available_updates_label.pack(side='left', anchor='w')
        self.select_all_button.pack(side='right')
        self.dll_listbox.pack(fill='both')
        self.update_button.pack()
        # self.listbox_scrollbar.pack(side='left', fill='y')
        # system frame
        self.spectre_patch_lbframe.pack(anchor="w")
        self.spectrewrn_label.pack()
        self.spectre_patch_disable.pack()
        self.spectre_patch_enable.pack()

        # Bindings
        self.buttons = all_children(self, 'Button')
        for btn in self.buttons:
            btn.bind(
                "<Enter>",
                lambda *args, btn=btn: wgmethods.fade(btn, tuple(btn_hover_cnf_cfg.keys()), tuple(btn_hover_cnf_cfg.values()))
            )
            btn.bind(
                "<Leave>",
                lambda *args, btn=btn: wgmethods.fade(btn, tuple(btn_normal_from_hover_cnf_cfg.keys()), tuple(btn_normal_cnf_cfg.values()))
            )
        self.spectrewrn_label.bind(
            "<Button-3>", lambda *args: self.spectrewrn_label.pack_forget())
        # self.dll_frame.bind("<Enter>", lambda *args: self.listbox_scrollbar.pack(side='left', fill='y'))
        self.dll_frame.bind("<Leave>",
                            lambda *args: self.listbox_scrollbar.pack_forget())
        self.dll_listbox.bind("<<ListboxSelect>>",
                              lambda *args: self.__update_select_button())
        self.dll_listbox.bind("<Motion>", self.__listbox_hover_callback)
        self.dll_listbox.bind("<MouseWheel>", self.__listbox_hover_callback)

        self.title_label.bind("<Button-1>", self.__clickwin)
        self.title_label.bind("<B1-Motion>", self.__dragwin)

        # Canvas setup
        self.cont_canvas.create_image(
            -40,
            -40,
            image=get_img("img/acrylic_dark.png"),
            anchor="nw",
            tags="logo")
        start_new(self.__browse_button_remind_loop, ())

        self.__update_dll_listbox(["Hello", "world", "spam", "egg", "!!!"])
        self.__disable_unavailable_dlls()
        self.__update_select_button()

    def __get_selection(self):
        selection = [self.dll_listbox.get(i) for i in self.dll_listbox.curselection()]
        selection = [item for item in selection if selection.index(item) not in self.dll_listbox.disabled]
        print(selection)

        return selection

    def __update_callback(self):
        dlls = self.__get_selection()
        updater.update_dlls(self.path, dlls)

    def __update_listbox_item_height(self):
        self.listbox_item_height = (self.dll_frame.winfo_height() -
                                    self.dll_frame["highlightthickness"] * 2
                                    ) // self.dll_listbox["height"]
        self.listbox_item_height_defined = True

    def __listbox_hover_callback(self, event):
        if not self.listbox_item_height_defined:
            self.__update_listbox_item_height()

        new_listbox_item_highlight = event.y // self.listbox_item_height + self.dll_listbox.nearest(
            0) + ((-4 if event.delta > 0 else 4) if event.delta != 0 else 0)
        if new_listbox_item_highlight + 1 > self.dll_listbox.size(): return
        # wgmethods.fade_listbox_item(self.dll_listbox,
        #                             self.last_listbox_item_highlight,
        #                             "foreground", FG)
        if new_listbox_item_highlight != self.last_listbox_item_highlight and self.last_listbox_item_highlight != -1:
            self.dll_listbox.itemconfig(
                self.last_listbox_item_highlight, fg=FG)
        if new_listbox_item_highlight not in self.dll_listbox.disabled:
            # wgmethods.fade_listbox_item(self.dll_listbox,
            #                             new_listbox_item_highlight,
            #                             "foreground", PRIM)
            self.dll_listbox.itemconfig(new_listbox_item_highlight, fg=PRIM)
            self.last_listbox_item_highlight = new_listbox_item_highlight

    def __update_select_button(self):
        """Updates the Select all button automatically based on states of items of dll_listbox"""
        selectable = 0
        for i in range(self.dll_listbox.size()):
            if i not in self.dll_listbox.disabled:
                selectable += 1

        selection = len(self.dll_listbox.curselection())

        if not selectable:
            self.select_all_button.config(text="Select all", state='disabled')
            return

        if selectable <= selection:
            all_selected = True

        else:
            all_selected = False

        if all_selected:
            self.select_all_button.config(
                text="Deselect all",
                command=self.__deselect_all,
                state='normal')
        else:
            self.select_all_button.config(
                text="Select all", command=self.__select_all, state='normal')

    def __select_all(self):
        """Selects all items in dll_listbox"""
        self.dll_listbox.selection_set(0, 'end')
        self.select_all_button.config(
            text="Deselect all", command=self.__deselect_all)

    def __deselect_all(self):
        """Deselects all items in dll_listbox"""
        self.dll_listbox.selection_clear(0, 'end')
        self.select_all_button.config(
            text="Select all", command=self.__select_all)

    def __browse_button_remind_loop(self):
        """Creates an fading animation on the browse_button reminding the user of selecting a directory"""
        sleep(2)
        while self.flash_browse_button:
            wgmethods.fade(self.browse_button, 'bg', PRIM, 50)
            sleep(1)
            wgmethods.fade(self.browse_button, 'bg', DARK, 10)
            sleep(1)

    def __update_game_path(self):
        """Asks user for a game path and updates everything tied together with it"""
        self.flash_browse_button = False

        self.path = tk.filedialog.askdirectory(title="Select game directory")

        ext = ".dll"
        dll_names = [
            name.lower() for name in os.listdir(self.path)
            if os.path.splitext(name)[1] == ext
        ]

        self.__update_dll_listbox(dll_names)
        self.__disable_unavailable_dlls()
        self.__select_all()
        self.__update_select_button()

        self.selected_game_label.config(text=os.path.basename(self.path))

    def __update_dll_listbox(self, dll_names):
        """Overwrites dll_listbox items with new ones given in the dll_names parameter"""
        self.dll_listbox.delete(0, 'end')
        self.dll_listbox.disabled = []
        for dll_name in dll_names:
            self.dll_listbox.insert('end', dll_name)

    def __disable_unavailable_dlls(self):
        for index, dll_name in enumerate(self.dll_listbox.get(0, 'end')):
            if dll_name not in [s.lower() for s in DllUpdater.available_dlls]:
                self.dll_listbox.itemconfig(
                    index,
                    foreground=DISABLED,
                    background=SEC,
                    selectforeground=DISABLED,
                    selectbackground=SEC)
                self.dll_listbox.disabled.append(index)
            else:
                self.dll_listbox.itemconfig(
                    index,
                    foreground=FG,
                    background=SEC,
                    selectforeground=FG,
                    selectbackground=PRIM)

    def __remove_content_frame(self):
        """Removes active content frame from cont_canvas"""
        self.cont_canvas.delete(self.cont_frm_id)

    def display_cont_frame(self, frame):
        """This function overwrites frame content frame currently disaplayed on the canvas, 
        frame attribute represents a tk.Frame instance which will be displayed on the canvas"""
        self.__remove_content_frame()
        self.cont_frm_id = self.cont_canvas.create_window(
            (10, 10),
            window=frame,
            anchor="nw",
            width=self.cont_canvas.winfo_width() - 20,
            height=self.cont_canvas.winfo_height() - 20)

    def logo_animation(self):
        """Animates background image on the canvas"""
        for i in range(50):
            self.cont_canvas.move("logo", -1, -1)
            self.cont_canvas.update()
            sleep(i / 1000)

    def tab_switch(self, id):
        """Displays a frame of given id on cont_canvas"""
        id_frm = {"System": self.system_frame, "Games": self.games_frame}

        try:
            self.display_cont_frame(id_frm[id])

        except KeyError:
            self.__remove_content_frame()

        # Navigation bar configuration
        for btn in self.nav_frame.pack_slaves():
            if btn["text"] == id:
                btn.unbind("<Leave>")
                btn.unbind("<Enter>")
                wgmethods.fade(btn, tuple(btn_active_cnf_cfg.keys()),
                               tuple(btn_active_cnf_cfg.values()))

            elif btn["text"] == self.active_tab:
                btn.bind(
                "<Enter>",
                lambda *args, btn=btn: wgmethods.fade(btn, tuple(btn_hover_cnf_cfg.keys()), tuple(btn_hover_cnf_cfg.values()))
                )
                btn.bind(
                "<Leave>",
                lambda *args, btn=btn: wgmethods.fade(btn, tuple(btn_normal_cnf_cfg.keys()), tuple(btn_normal_cnf_cfg.values()))
                )
                wgmethods.fade(btn, tuple(btn_normal_cnf_cfg.keys()),
                               tuple(btn_normal_cnf_cfg.values()))

        self.active_tab = id

    def __clickwin(self, event):
        """Prepares variables for __dragwin function"""
        self.offsetx = self.winfo_pointerx() - self.winfo_x()
        self.offsety = self.winfo_pointery() - self.winfo_y()

    def __dragwin(self, event):
        """Updates window position"""
        x = self.winfo_pointerx() - self.offsetx
        y = self.winfo_pointery() - self.offsety
        self.geometry('+%d+%d' % (x, y))


customfont.loadfont(resource_path("fnt/Roboto-Regular.ttf"))
customfont.loadfont(resource_path("fnt/Roboto-Light.ttf"))

updater = DllUpdater()

root = Root()
start_new(root.top.logo_animation, ())
start_new(root.top.tab_switch, (root.top.active_tab, ))

root.mainloop()