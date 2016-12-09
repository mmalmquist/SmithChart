#!/usr/bin/python
import sys
import tkinter
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure as mplfig
import matplotlib.backends.backend_tkagg as tkagg
pi = np.pi


def cm_to_in(l):
    return l/2.54


def dpc_to_dpi(dpc):
    return dpc*2.54


class SmithChart():
    imp_clr = '#ff0000'
    adm_clr = '#0000ff'
    normal_clr = '#000000'
    intermediate_imp_style = '--'
    imp_change_style = ':'
    final_imp_style = '-'
    smith_chart_linewidth = 0.3
    imp_real_x = []
    imp_imag_x = []
    imp_real_y = []
    imp_imag_y = []
    plots_list = []
    smith_plots = 0
    _max_val = np.sqrt(sys.float_info.max) / 1e10

    def __init__(self):
        self.z_hist = []  # ?
        self.z_in = 0  # ?
        self.z_0 = 50  # characteristic impedance
        self.frame = tkinter.Tk()  # Create the frame
        self.frame.title('Smith Chart')

        self.smith_panel = tkinter.Frame(master=self.frame, bg='#00ff00')
        self.smith_panel.pack(side='top')
        # Smith chart
        self.fig = mplfig.Figure()  # figure containint the smith plot
        self.ax = self.fig.add_axes([0.1, 0.1, 0.8, 0.8], frameon=True,
                                    navigate=True, axisbg="#f8fbfc",
                                    aspect=1)
        self.ax.axis([-1, 1, -1, 1])
        self.canvas = tkagg.FigureCanvasTkAgg(self.fig,
                                              master=self.smith_panel)
        self.ax.grid(False)
        self.canvas.get_tk_widget().pack(side='left')

        # Smith control
        self.add_smith_ctl_frame()

        # Top frame
        self.add_top_frame()
        # Draw smith chart
        self.calc_smith_chart()
        self.draw_smith_chart()
        self.canvas.draw()

        self.frame.mainloop()  # Opens the frame?

    def add_top_frame(self):
        """
        Creates and places a panel with buttons and labels at the top
        of the man frame.
        """
        # The frame with the buttons
        self.frame1 = tkinter.Frame(master=self.frame, bg='#00ff00',
                                    height=200, width=240)
        self.frame1.pack(side='top', anchor='w', before=self.smith_panel)

        # Create and add the labels
        self.lab1 = self.add_label(self.frame1, 'Hello World1')
        self.lab2 = self.add_label(self.frame1, 'Hello World2')
        self.lab3 = self.add_label(self.frame1, 'Hello World3')
        self.but1 = self.add_button(self.frame1, 'remove smith', None)
        self.but2 = self.add_button(self.frame1, 'clear smith', None)
        self.but3 = self.add_button(self.frame1, 'add smith', None)
        self.but1.grid(row=0, column=0, sticky='W', padx=0, pady=0)
        self.lab1.grid(row=0, column=1, sticky='W', padx=0, pady=0)
        self.but2.grid(row=0, column=2, sticky='W', padx=0, pady=0)
        self.lab2.grid(row=0, column=3, sticky='W', padx=0, pady=0)
        self.but3.grid(row=0, column=4, sticky='W', padx=0, pady=0)
        self.lab3.grid(row=0, column=5, sticky='W', padx=0, pady=0)

    def add_smith_ctl_frame(self):
        """
        Creates and places the smith chart control panel on the right
        side of the main frame.
        """
        # The control panel itself
        self.ctl_frame = tkinter.Frame(master=self.smith_panel)
        self.ctl_frame.pack(side="left")

        # The panel where new entries are read from
        self.entries_frame = tkinter.LabelFrame(self.ctl_frame,
                                                text="Enter Details:")
        self.entries_frame.pack(side="top")
        # Create abd add everything to the entry panel
        self.add_tl_frame()
        self.add_lumped_frame()
        self.add_stub_frame()
        self.add_system_prop()
        self.add_clear_frame()
        self.add_history_frame()
        return

    def add_tl_frame(self):
        """
        Transmission line part
        """
        self.tl_frame = tkinter.Frame(master=self.entries_frame)
        self.tl_lab = self.add_label(self.tl_frame, "Add TL")
        self.apnd_tl_but = self.add_button(
            self.tl_frame, "Series", lambda: self.step_button_event(1))
        self.tl_imp_lab = self.add_label(
            self.tl_frame, "Impedance:", anchr="e")
        self.tl_electr_len_lab = self.add_label(
            self.tl_frame, "Electrical length:", anchr="e")
        self.tl_imp = tkinter.Entry(self.tl_frame)
        self.tl_electr_len = tkinter.Entry(self.tl_frame)
        self.tl_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        self.apnd_tl_but.grid(row=0, column=1, sticky="E", padx=5, pady=2)
        self.tl_imp_lab.grid(row=1, column=0, sticky="W", padx=5, pady=2)
        self.tl_imp.grid(row=1, column=1, columnspan=7, sticky="WE",
                         pady=3, padx=5)
        self.tl_electr_len_lab.grid(row=2, column=0, sticky="W",
                                    padx=5, pady=2)
        self.tl_electr_len.grid(row=2, column=1, columnspan=7, sticky="WE",
                                pady=3, padx=5)
        self.tl_frame.pack(side="top")
        return

    def add_lumped_frame(self):
        """
        Lumped in series and parallel
        """
        self.lumped_frame = tkinter.Frame(master=self.entries_frame)
        self.lumped_lab = self.add_label(self.lumped_frame, "Add Lumped")
        self.lumped_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        self.lumped_imp_lab = self.add_label(self.lumped_frame,
                                             "Impedance:", anchr="e")
        self.lumped_imp_lab.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        self.lumped_imp = tkinter.Entry(self.lumped_frame)
        self.lumped_imp.grid(row=1, column=1, columnspan=7, sticky="WE",
                             pady=3, padx=5)
        self.lumped_but_frame = tkinter.Frame(master=self.lumped_frame)
        self.lumped_ser_but = self.add_button(self.lumped_but_frame, "Series",
                                              lambda: self.step_button_event(2))
        self.lumped_ser_but.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        self.lumped_para_but = self.add_button(self.lumped_but_frame, "Parallel",
                                               lambda: self.step_button_event(3))
        self.lumped_para_but.grid(row=0, column=1, sticky="W", padx=5, pady=2)
        self.lumped_but_frame.grid(row=0, column=1, columnspan=7, sticky="WE",
                                   pady=3, padx=5)
        self.lumped_frame.pack(side="top")
        return

    def add_stub_frame(self):
        """
        Stub open and short
        """
        self.stub_frame = tkinter.Frame(master=self.entries_frame)
        self.stub_lab = self.add_label(self.stub_frame, "Add Stub")
        self.stub_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        self.stub_imp_lab = self.add_label(self.stub_frame,
                                           "Impedance:", anchr="e")
        self.stub_imp_lab.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        self.stub_len_lab = self.add_label(self.stub_frame,
                                           "Electrical length:", anchr="e")
        self.stub_len_lab.grid(row=2, column=0, sticky="E", padx=5, pady=2)
        self.stub_imp = tkinter.Entry(self.stub_frame)
        self.stub_imp.grid(row=1, column=1, columnspan=7, sticky="WE",
                           pady=3, padx=5)
        self.stub_len = tkinter.Entry(self.stub_frame)
        self.stub_len.grid(row=2, column=1, columnspan=7, sticky="WE",
                           pady=3, padx=5)
        self.stub_but_frame = tkinter.Frame(master=self.stub_frame)
        self.stub_open_but = self.add_button(self.stub_but_frame, "Open",
                                             lambda: self.step_button_event(4))
        self.stub_open_but.grid(row=0, column=0, sticky="W", padx=5, pady=2)
        self.stub_short_but = self.add_button(self.stub_but_frame, "Short",
                                              lambda: self.step_button_event(5))
        self.stub_short_but.grid(row=0, column=1, sticky="W", padx=5, pady=2)
        self.stub_but_frame.grid(row=0, column=1, columnspan=7, sticky="WE",
                                 pady=3, padx=5)
        self.stub_frame.pack(side="top")
        return

    def add_system_prop(self):
        """
        System properties
        """
        self.sys_frame = tkinter.Frame(master=self.entries_frame)
        self.sys_imp_lab = self.add_label(
            self.sys_frame, "System Impedance:")
        self.sys_load_lab = self.add_label(
            self.sys_frame, "Load Impedance:")
        self.sys_imp = tkinter.Entry(self.sys_frame)
        self.sys_imp.insert(0, "50")
        self.sys_load = tkinter.Entry(self.sys_frame)
        self.sys_imp_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        self.sys_load_lab.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        self.sys_imp.grid(row=0, column=1, columnspan=7, sticky="WE",
                          pady=3, padx=5)
        self.sys_load.grid(row=1, column=1, columnspan=7, sticky="WE",
                           pady=3, padx=5)
        self.sys_frame.pack(side="top")
        return

    def add_clear_frame(self):
        """
        The panel that controls modifying entries written to the chart
        """
        self.ctl_panel = tkinter.Frame(master=self.ctl_frame)
        self.ctl_panel.pack(side="top", before=self.entries_frame)
        self.ctl_clr_all = self.add_button(self.ctl_panel, "Clear All",
                                           lambda: self.ctl_button_event(1))
        self.ctl_clr_all.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        self.ctl_clr_last = self.add_button(self.ctl_panel, "Clear Last",
                                            lambda: self.ctl_button_event(2))
        self.ctl_clr_last.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        return

    def add_history_frame(self):
        """
        Previous entries
        """
        self.prev_entr_frame = tkinter.Frame(master=self.ctl_frame)
        self.prev_entr = tkinter.Text(master=self.prev_entr_frame)
        self.prev_scr = tkinter.Scrollbar(master=self.prev_entr_frame,
                                          orient="vertical",
                                          command=self.prev_entr.yview)
        self.prev_entr.grid(row=0, column=0)
        self.prev_scr.grid(row=0, column=1, rowspan=15,
                           columnspan=1, sticky="ns")
        self.prev_entr.config(yscrollcommand=self. prev_scr.set)
        # font=('Fixe', 12, 'bold', 'italic')
        self.prev_entr_frame.pack(side="top", after=self.entries_frame)
        return

    def plot_z_in(self):
        """
        Plot the current input impedance
        """
        gamma = (self.z_in - self.z_0) / (self.z_in + self.z_0)
        self.plots_list.append(
            self.ax.plot(np.real(gamma),
                         np.imag(gamma),
                         linewidth=1,
                         linestyle='-', marker='o', markersize=5,
                         color='#000000'))
        self.canvas.draw()

    def step_button_event(self, button_id):
        """
        Handles events when buttons are pressed in the entries_frame frame.
        """
        z = 0
        bl = 0
        history_msg = ""
        entry_type = {1: "Transmission Line in series:    ",
                      2: "Lumped component in series:     ",
                      3: "Lumped component in parallel:   ",
                      4: "Stub terminated in a short:     ",
                      5: "Stub terminated in an open:     "}
        if (button_id == 1):
            # Add transmission line towards generator
            try:
                self.z_0 = complex(self.sys_imp.get())
                z = complex(self.tl_imp.get())
                bl = self.parse_raw_input(self.tl_electr_len.get())
            except:
                print("Unable to interpret input for button_id: ", button_id)
                return
            self.z_in = z*((self.z_in + 1j*z*np.tan(bl)) /
                           (z + 1j*self.z_in*np.tan(bl)))
            history_msg = str(
                entry_type[button_id]) + \
                "Z_0 = " + str(z) + " ohm, bl = " + \
                str(round(bl, 3)) + " radians"
            self.tl_electr_len.delete(0, len(self.tl_electr_len.get()))
            self.tl_imp.delete(0, len(self.tl_imp.get()))
            print(self.z_in)
        elif (button_id == 2 or button_id == 3):
            try:
                self.z_0 = complex(self.sys_imp.get())
                z = complex(self.lumped_imp.get())
            except:
                print("Unable to interpret input for button_id: ", button_id)
                return
            if (self.sys_load.get() == ""):
                self.sys_load.insert(0, self.lumped_imp.get())
                self.sys_load.config(state="readonly")
            if (button_id == 2):
                self.z_in = self.z_in + z
            else:
                if np.abs(z) < 1e-40:
                    self.z_in = z
                else:
                    self.z_in = self.z_in * z / (self.z_in + z)
            history_msg = str(
                entry_type[button_id]) + \
                "Z = " + str(z) + " ohm"
            self.lumped_imp.delete(0, len(self.lumped_imp.get()))
        elif (button_id == 4 or button_id == 5):
            try:
                self.z_0 = complex(self.sys_imp.get())
                z_c = complex(self.stub_imp.get())
                bl = self.parse_raw_input(self.stub_len.get())
            except:
                print("Unable to interpret input for button_id: ", button_id)
                return
            if (button_id == 4):  # open
                z = z_c*((1+np.exp(1j*(bl + 2*np.pi))) /
                         (1-np.exp(1j*(bl + 2*np.pi))))
            else:  # short
                z = z_c*((1+np.exp(1j*(bl + np.pi))) /
                         (1-np.exp(1j*(bl + np.pi))))
            print("Stub ", z, self.z_in)
            self.z_in = 1/(1/self.z_in + 1/z)
            history_msg = str(
                entry_type[button_id]) + \
                "Z_0 = " + str(z) + " ohm, bl = " + \
                str(round(bl, 3)) + " radians"
            self.stub_len.delete(0, len(self.stub_len.get()))
            self.stub_imp.delete(0, len(self.stub_imp.get()))
        else:
            print("Unknown entries_frame button id: ", button_id)
            return
        print(button_id, self.z_0, z, bl, self.z_in)
        self.z_hist.append(self.z_in)
        self.prev_entr.insert('end', history_msg+"\n")
        self.plot_z_in()
        return

    def ctl_button_event(self, button_id):
        """
        Handles events when buttons are pressed in the control frame
        """
        if (button_id == 1):
            # Clears the smith chart from any input
            for i in range(self.smith_plots, np.size(self.plots_list)):
                print(i)
                self.ax.lines.pop()  # deleted the latest plot
                # delete latest entry
                self.plots_list.remove(
                    self.plots_list[np.size(self.plots_list) - 1])
                """
                self.sys_load.config(state="normal")
                self.sys_load.delete(0, len(self.sys_load.get()))
                self.tl_imp.delete(0, len(self.tl_imp.get()))
                self.tl_electr_len.delete(0, len(self.tl_electr_len.get()))
                self.lumped_imp.delete((0, len(self.lumped_imp.get())))
                self.stub_imp.delete(0, len(self.stub_imp.get()))
                """
            self.canvas.draw()
        elif (button_id == 2):
            self.ax.lines.pop()  # deleted the latest plot
            # delete latest entry
            self.plots_list.remove(
                self.plots_list[np.size(self.plots_list) - 1])
            self.canvas.draw()
        else:
            print("Unknown ctl button id: ", button_id)

    def add_label(self, parent_frame, label_text, anchr="center"):
        """
        A method to simplify the creation of lables
        """
        tmp_label = tkinter.Label(parent_frame, anchor=anchr,
                                  bg='#777874', bitmap='', image='',
                                  bd=2, cursor='arrow',
                                  font=("Times", 12),
                                  fg='#f8fbfc', height=1, width=15,
                                  justify='center', padx=0, pady=0,
                                  relief='flat', text=label_text,
                                  textvariable='',
                                  underline=-1, wraplength=-1)
        return tmp_label

    def add_button(self, parent_frame, button_text, cmd, anchr="center"):
        """
        A method to simplify the creation of buttons
        """
        tmp_button = tkinter.Button(parent_frame, anchor=anchr,
                                    bg='#272824', bitmap='', image='',
                                    bd=2, cursor='arrow',
                                    font=("Times", 12),
                                    fg='#f8fbfc', height=1, width=15,
                                    justify='center', padx=0, pady=0,
                                    relief='flat', text=button_text,
                                    textvariable='',
                                    underline=-1, wraplength=-1,
                                    command=cmd)
        return tmp_button

    def parse_raw_input(self, raw_in):
        """
        parse_raw_input(self, raw_in)

        raw_in is a string containing theta input. It sould be on the from
        "3*pi/2" or "pi/3" or "2*pi" or "1234" or "12.34"
        return theta numerical value of raw_in.
        """
        if (raw_in is None or raw_in == ""):
            print("Unable to interpret length of transmission line")
            return
        times_idx = raw_in.find("*")
        pi_idx = raw_in.find("pi")
        div_idx = raw_in.find("/")
        val = 0
        if (times_idx == -1 and pi_idx == -1 and div_idx == -1):
            # input is a float
            try:
                val = float(raw_in)
            except:
                print("Unable to interpret length of transmission line")
                return
        else:
            val1 = 1
            val2 = 1
            val3 = 1
            if (times_idx != -1):
                try:
                    val1 = float(raw_in[:times_idx])
                except:
                    print("Unable to interpret length of transmission line")
                    return
            if (pi_idx != -1):
                try:
                    val2 = np.pi
                except:
                    print("Unable to interpret length of transmission line")
                    return
            if (div_idx != -1):
                try:
                    val3 = float(raw_in[div_idx+1:])
                except:
                    print("Unable to interpret length of transmission line")
                    return
            val = val1*val2/val3
            print("parsed input: ", val1, val2, val3)
        return val

    def draw_smith_chart(self):
        """
        Draws the smith chart background which includes impedance
        and admittance lines.
        """
        print("Length of self.ax.lines",
              np.size(self.ax.lines))  # For debuggin reasons
        # Plot the Im(z)=0 line
        self.plots_list.append(
            self.ax.plot(np.linspace(-1, 1, 2), np.zeros(2),
                         linewidth=self.smith_chart_linewidth,
                         linestyle='-', marker='', markersize=1,
                         color=self.imp_clr))
        # Plot the real parts of impedance and admittance
        for k in range(0, np.size(self.imp_real_x, axis=0)):
            # Impedance
            self.plots_list.append(
                self.ax.plot(self.imp_real_x[k], self.imp_real_y[k],
                             linewidth=self.smith_chart_linewidth,
                             linestyle='-', marker='', markersize=1,
                             color=self.imp_clr))
            # Admittance
            self.plots_list.append(
                self.ax.plot(-np.array(self.imp_real_x[k]),
                             -np.array(self.imp_real_y[k]),
                             linewidth=self.smith_chart_linewidth,
                             linestyle='-', marker='', markersize=1,
                             color=self.adm_clr))
        # The abs(Gamma) = 1 ring
        self.plots_list.append(
            self.ax.plot(np.cos(np.linspace(0, 2*np.pi, 1000)),
                         np.sin(np.linspace(0, 2*np.pi, 1000)),
                         linewidth=self.smith_chart_linewidth,
                         linestyle='-', marker='', markersize=1,
                         color=self.imp_clr))
        # Plot the imaginary parts of impedance and admittance
        for k in range(0, np.size(self.imp_imag_x, axis=0)):
            # Impedance
            self.plots_list.append(
                self.ax.plot(self.imp_imag_x[k], self.imp_imag_y[k],
                             linewidth=self.smith_chart_linewidth,
                             linestyle='-', marker='', markersize=1,
                             color=self.imp_clr))
            # Admittance
            self.plots_list.append(
                self.ax.plot(-np.array(self.imp_imag_x[k]),
                             -np.array(self.imp_imag_y[k]),
                             linewidth=self.smith_chart_linewidth,
                             linestyle='-', marker='', markersize=1,
                             color=self.adm_clr))
        self.smith_plots = np.size(self.plots_list)
        self.canvas.draw()

    def calc_smith_chart(self):
        """
        Calculate the Layout for impedance and admittance circles
        """
        self.imp_real_x, self.imp_real_y = self.smith_chart_circles_real()
        self.imp_imag_x, self.imp_imag_y = self.smith_chart_circles_imag()

    def smith_chart_circles_real(self):
        """
        Calculate the circles with constant real impedance
        """
        r = np.array([[0.2], [0.5], [1], [2], [5]])
        x = []
        y = []
        for i in range(0, np.size(r, axis=0)):
            theta = np.linspace(0, 2*np.pi, int(1000/(1+r[i])))
            x_temp = r[i]/(1+r[i]) + 1/(1+r[i])*np.cos(theta)
            y_temp = 1/(1+r[i])*np.sin(theta)
            x.append(x_temp)
            y.append(y_temp)
        return x, y

    def smith_chart_circles_imag(self):
        """
        Calculate the circles with constant imaginary impedance
        """
        X_1 = np.array([[0.2], [0.5], [1], [2], [5]])
        X_2 = np.array([[-5], [-2], [-1], [-0.5], [-0.2]])
        x = []
        y = []
        for i in range(0, np.size(X_1, axis=0)):
            theta_1 = np.linspace(np.pi/2, 3*np.pi/2,
                                  int(1000/np.abs(X_1[i])))
            x_temp_1 = 1 + np.cos(theta_1)/X_1[i]
            y_temp_1 = 1/X_1[i] + np.sin(theta_1)/X_1[i]
            x_1 = []
            y_1 = []
            for j in range(0, np.size(x_temp_1)):
                if (x_temp_1[j]**2 + y_temp_1[j]**2 <= 1):
                    x_1.append(x_temp_1[j])
                    y_1.append(y_temp_1[j])
                if (j == np.size(x_temp_1) - 1):
                    x.append(np.array(x_1))
                    y.append(np.array(y_1))
        for i in range(0, np.size(X_2, axis=0)):
            theta_2 = np.linspace(3*np.pi/2, 5*np.pi/2,
                                  int(1000/np.abs(X_2[i])))
            x_temp_2 = 1 + np.cos(theta_2)/X_2[i]
            y_temp_2 = 1/X_2[i] + np.sin(theta_2)/X_2[i]
            x_2 = []
            y_2 = []
            for j in range(0, np.size(x_temp_2)):
                if (x_temp_2[j]**2 + y_temp_2[j]**2 <= 1):
                    x_2.append(x_temp_2[j])
                    y_2.append(y_temp_2[j])
                if (j == np.size(x_temp_2) - 1):
                    x.append(np.array(x_2))
                    y.append(np.array(y_2))
        return x, y


a = SmithChart()

"""
from Tkinter import *
def roll(): pass
def links(): pass
def create(): pass
root=Tk()
root.title("CIME")

rows = 0
def create_detail_frame():
    global rows
    entries_frame = LabelFrame(root,text="Enter Details:")
    entries_frame.grid(row=rows, columnspan=7, sticky='W',padx=5, pady=5, ipadx=5, ipady=5)
    Label(entries_frame,text="Competitors",font = "Arial 8 bold italic").grid(row=0,sticky='E', padx=5, pady=2)
    Label(entries_frame,text="Keywords",font = "Arial 8 bold italic").grid(row=1,sticky='E', padx=5, pady=2)
    Label(entries_frame,text="Project Name",font = "Arial 8 bold italic").grid(row=2,sticky='E', padx=5, pady=2)
    e1 = Entry(entries_frame)
    e2 = Entry(entries_frame)
    e3 = Entry(entries_frame)
    e1.grid(row=0,column=1,columnspan=7, sticky="WE", pady=3,padx=5)
    e2.grid(row=1,column=1,columnspan=7, sticky="WE", pady=3,padx=5)
    e3.grid(row=2,column=1,columnspan=7, sticky="WE", pady=3,padx=5)
    Button(entries_frame,text ="Search Words",width=10,font = "Arial 8 bold    italic",activebackground="red",command=roll).grid(row=3,column=0,sticky=W,pady=4,padx=5)
    Button(entries_frame,text="Google Search",width=10,font = "Arial 8 bold italic",command=links).grid(row=3,column=2,sticky=W,pady=4,padx=5)
    Button(entries_frame,text="Extraxt Text",width=10,font = "Arial 8 bold italic",command = create).grid(row=3,column=4,sticky=W,pady=4,padx=5)
    rows += 1

    # Reposition text, scroll
    #self.prev_scr.grid_forget()
    #self.prev_entr.grid_forget()
    #self.prev_scr.grid(row=rows, padx=1, column=7, rowspan=15, columnspan=1, sticky=NS)
    #self.prev_entr.grid(row=rows,column=1)

    # Reposition text, scroll
    self.prev_scr.grid(row=rows)
    self.prev_entr.grid(row=rows)

self.prev_entr = Text(master=root)
self.prev_scr=Scrollbar(root,orient =VERTICAL,command=self.prev_entr.yview)
self.prev_scr.grid(row=1, padx=1, column=7, rowspan=15, columnspan=1, sticky=NS)
self.prev_entr.grid(row=1,column=1)
self.prev_entr.config(yscrollcommand=self.prev_scr.set,font=('Arial', 8, 'bold', 'italic'))

Button(root, text='Add detail frame', command=create_detail_frame).grid(row=0, column=7)
create_detail_frame()

mainloop()
"""
