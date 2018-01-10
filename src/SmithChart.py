#!/usr/bin/python

from copy import copy
from numpy import real, imag, tan, abs, pi, exp, size, sin, cos, linspace, float64, array
from tkinter import Tk, Frame, LabelFrame, Label, Button, Entry, Text, Scrollbar, END
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def cm_to_in(l):
    return l/2.54


def dpc_to_dpi(dpc):
    return dpc*2.54


def complx_str(z):
    return "({:.3f})".format(z)


class SmithChart(object):
    _impedance_color_ = "#ff0000"
    _admittance_color_ = "#0000ff"
    _normal_color_ = "#000000"
    _intermediate_impedance_style_ = "--"
    _impedance_change_style_ = ":"
    _final_impedance_style_ = "-"
    _smith_chart_linewidth_ = 0.5
    _font_ = ("Times", 12)
    _component_args_ = {"bd": 2, "height": 1, "width": 16, "font": _font_, "justify": "center", "padx": 0, "pady": 0}
    # _component_args_ = {"bitmap": "", "image": "", "bg": "#777874", "bd": 2, "cursor": "arrow", "fg": "#f8fbfc", anchr="center", "height": 1, "width": 16, "font": ("Times", 12), "justify": "center", "padx": 0, "pady": 0, "relief": "flat", "textvariable": "", "underline": -1, "wraplength": -1}

    def __init__(self):
        self._z_hist = list()  # ?
        self._z_in = 0  # ?
        self._z_0 = 50  # characteristic impedance
        self._imp_real_x = list()
        self._imp_real_y = list()
        self._imp_imag_x = list()
        self._imp_imag_y = list()
        self._plots_list = list()
        self._smith_plots = 0
        self._init_gui()

    def display(self):
        return self.frame.mainloop() # call tkinter mainloop

    def _init_gui(self):
        self.frame = Tk()
        self.frame.title("Smith Chart")
        main_panel = Frame(master=self.frame)
        main_panel.pack(side="top", expand=True)
        smith_panel = Frame(master=main_panel)
        smith_panel.pack(side="left", expand=True)
        smith_control = Frame(master=main_panel)
        smith_control.pack(side="right", expand=True)
        # Smith chart
        # figure containing the smith plot
        fig = Figure(facecolor="#f8fbfc", frameon=True, figsize=(7, 7))
        self.chart_handle = fig.add_axes([0.05, 0.05, 0.9, 0.9], frame_on=False, navigate=True, facecolor="#f8fbfc", aspect=1)
        self.chart_handle.axis([-1, 1, -1, 1]) # Not really needed
        self.chart_handle.get_yaxis().set_visible(False)
        self.chart_handle.get_xaxis().set_visible(False)
        self.chart_handle.grid(False)
        self.canvas = FigureCanvasTkAgg(fig, master=smith_panel)
        self.canvas.get_tk_widget().pack()
        self._make_control_panel(smith_control)
        
        # Draw smith chart
        self._draw_chart_background()
        self.canvas.draw()

    def _make_control_panel(self, parent_panel):
        # The control panel itself
        ctl_frame = Frame(master=parent_panel)
        ctl_frame.pack(side="left", expand=True)

        # The panel where new entries are read from
        entries_frame = LabelFrame(ctl_frame, text="Enter Details:")
        entries_frame.grid(row=2, column=0, padx=0, pady=0)
        # Create and add everything to the entry panel
        self._make_transmissionline_panel(entries_frame)
        self._make_lumped_component_panel(entries_frame)
        self._make_stub_panel(entries_frame)
        self._make_system_props_panel(entries_frame)
        self._make_z_in_panel(ctl_frame)
        self._make_clear_panel(ctl_frame)
        self._make_history_panel(ctl_frame)

    def _make_z_in_panel(self, parent_panel):
        """
        Displaying current _z_in.
        """
        z_in_frame = Frame(master=parent_panel)
        z_in_frame.grid(row=1, column=0, padx=0, pady=0)
        z_in_lab = self._make_label(z_in_frame, "Z_in:", anchr="e")
        self.z_in_entr = Entry(master=z_in_frame, state="disabled")
        
        z_in_lab.grid(row=0, column=0, padx=0, pady=0, sticky="E")
        self.z_in_entr.grid(row=0, column=1, padx=0, pady=0, sticky="W")

    def _make_transmissionline_panel(self, parent_panel):
        """
        Transmission line part
        """
        tl_frame = LabelFrame(master=parent_panel)
        tl_frame.grid(row=0, column=0, padx=0, pady=0, sticky="W")
        
        tl_lab = self._make_label(tl_frame, "Add TL")
        apnd_tl_but = self._make_button(tl_frame, "Series", lambda: self._component_button_event(1))
        tl_imp_lab = self._make_label(tl_frame, "Impedance:", anchr="e")
        tl_electr_len_lab = self._make_label(tl_frame, "Electrical length:", anchr="e")
        self.tl_imp = Entry(tl_frame, font=self._font_)
        self.tl_electr_len = Entry(tl_frame, font=self._font_)
        
        tl_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        apnd_tl_but.grid(row=0, column=1, sticky="E", padx=5, pady=2)
        tl_imp_lab.grid(row=1, column=0, sticky="W", padx=5, pady=2)
        self.tl_imp.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        tl_electr_len_lab.grid(row=2, column=0, sticky="W", padx=5, pady=2)
        self.tl_electr_len.grid(row=2, column=1, columnspan=7, sticky="WE", pady=3, padx=5)

    def _make_lumped_component_panel(self, parent_panel):
        lumped_frame = LabelFrame(master=parent_panel)
        lumped_frame.grid(row=1, column=0, padx=0, pady=0, sticky="W")
        
        lumped_lab = self._make_label(lumped_frame, "Add Lumped")
        lumped_imp_lab = self._make_label(lumped_frame, "Impedance:", anchr="e")
        self.lumped_imp = Entry(lumped_frame, font=self._font_)
        
        lumped_but_frame = Frame(master=lumped_frame)
        lumped_ser_but = self._make_button(lumped_but_frame, "Series", lambda: self._component_button_event(2))
        lumped_para_but = self._make_button(lumped_but_frame, "Parallel", lambda: self._component_button_event(3))
        
        lumped_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        lumped_imp_lab.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        self.lumped_imp.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        
        lumped_but_frame.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        lumped_ser_but.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        lumped_para_but.grid(row=0, column=1, sticky="W", padx=5, pady=2)

    def _make_stub_panel(self, parent_panel):
        stub_frame = LabelFrame(master=parent_panel)
        stub_lab = self._make_label(stub_frame, "Add Stub")
        stub_imp_lab = self._make_label(stub_frame, "Impedance:", anchr="e")
        stub_len_lab = self._make_label(stub_frame, "Electrical length:", anchr="e")
        self.stub_imp = Entry(stub_frame, font=self._font_)
        self.stub_len = Entry(stub_frame, font=self._font_)
        
        stub_but_frame = Frame(master=stub_frame)
        stub_open_but = self._make_button(stub_but_frame, "Open", lambda: self._component_button_event(4))
        stub_short_but = self._make_button(stub_but_frame, "Short", lambda: self._component_button_event(5))
        
        stub_frame.grid(row=2, column=0, padx=0, pady=0, sticky="W")
        stub_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        stub_imp_lab.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        stub_len_lab.grid(row=2, column=0, sticky="E", padx=5, pady=2)
        self.stub_imp.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        self.stub_len.grid(row=2, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        
        stub_but_frame.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        stub_open_but.grid(row=0, column=0, sticky="W", padx=5, pady=2)
        stub_short_but.grid(row=0, column=1, sticky="W", padx=5, pady=2)

    def _make_system_props_panel(self, parent_panel):
        sys_frame = Frame(master=parent_panel)
        sys_imp_lab = self._make_label(sys_frame, "System Impedance:", anchr="w")
        sys_load_lab = self._make_label(sys_frame, "Load Impedance:", anchr="w")
        self.sys_imp = Entry(sys_frame, font=self._font_)
        self.sys_imp.insert(0, "50")
        self.sys_load = Entry(sys_frame, font=self._font_)
        
        sys_frame.grid(row=3, column=0, padx=0, pady=0, sticky="W")
        sys_imp_lab.grid(row=0, column=0, sticky="E", padx=5, pady=2)
        sys_load_lab.grid(row=1, column=0, sticky="E", padx=5, pady=2)
        self.sys_imp.grid(row=0, column=1, columnspan=7, sticky="WE", pady=3, padx=5)
        self.sys_load.grid(row=1, column=1, columnspan=7, sticky="WE", pady=3, padx=5)

    def _make_clear_panel(self, parent_panel):
        ctl_panel = Frame(master=parent_panel)
        ctl_clr_all = self._make_button(ctl_panel, "Clear All", lambda: self._control_button_event(1))
        ctl_clr_last = self._make_button(ctl_panel, "Clear Last", lambda: self._control_button_event(2))
        
        ctl_panel.grid(row=0, column=0, padx=0, pady=0, sticky="n")
        ctl_clr_all.grid(row=0, column=0, padx=5, pady=2)
        ctl_clr_last.grid(row=0, column=1, padx=5, pady=2)

    def _make_history_panel(self, parent_panel):
        prev_entr_frame = Frame(master=parent_panel)
        prev_entr_frame.grid(row=3, column=0, padx=0, pady=0, sticky="W")
        self.prev_entr = Text(master=prev_entr_frame, wrap='word', height=20, width=60, state="disabled")
        prev_scr = Scrollbar(master=prev_entr_frame, orient="vertical", command=self.prev_entr.yview)
        self.prev_entr.grid(row=0, column=0)
        prev_scr.grid(row=0, column=1, rowspan=10, columnspan=1, sticky="ns")
        self.prev_entr.config(yscrollcommand=prev_scr.set)
        return

    def _plot_z_in(self):
        gamma = (self._z_in-self._z_0) / (self._z_in+self._z_0)
        plt_settings = {"linewidth": "1", "linestyle": "-", "marker": "o", "markersize": "5", "color": "#000000"}
        self._plots_list.append(self.chart_handle.plot(real(gamma), imag(gamma), **plt_settings))
        self.canvas.draw()

    def _component_button_event(self, button_id):
        z = 0
        bl = 0
        history_msg = ""
        entry_type = {1: "Transmission Line in series:    ",
                      2: "Lumped component in series:     ",
                      3: "Lumped component in parallel:   ",
                      4: "Stub terminated in a open:      ",
                      5: "Stub terminated in an short:    "}
        try:
            if (button_id == 1):
                # Add transmission line towards generator
                self._z_0 = complex(self.sys_imp.get())
                z = complex(self.tl_imp.get())
                bl = self._parse_raw_input(self.tl_electr_len.get())
                self._z_in = z*((self._z_in + 1j*z*tan(bl)) / (z + 1j*self._z_in*tan(bl)))
                history_msg = "%s Z_0 = %s ohm, bl = %s radians" % (entry_type[button_id], complx_str(z), str(round(bl, 3)))
                self.tl_electr_len.delete(0, len(self.tl_electr_len.get()))
                self.tl_imp.delete(0, len(self.tl_imp.get()))
            elif (button_id == 2 or button_id == 3):
                self._z_0 = complex(self.sys_imp.get())
                z = complex(self.lumped_imp.get())
                
                if (self.sys_load.get() == ""):
                    self.sys_load.insert(0, self.lumped_imp.get())
                    self.sys_load.config(state="readonly")
                if (button_id == 2):
                    self._z_in = self._z_in + z
                else:
                    if abs(z) < 1e-40:
                        self._z_in = z
                    else:
                        self._z_in = self._z_in * z / (self._z_in + z)
                history_msg = "%s Z = %s ohm" % (entry_type[button_id], complx_str(z))
                self.lumped_imp.delete("0", len(self.lumped_imp.get()))
            elif (button_id == 4 or button_id == 5):
                self._z_0 = complex(self.sys_imp.get())
                z_c = complex(self.stub_imp.get())
                bl = self._parse_raw_input(self.stub_len.get())
                
                if (button_id == 4):  # open
                    z = z_c*((1+exp(-2j*(bl + pi))) / (1-exp(-2j*(bl + pi))))
                else:  # short
                    z = z_c*((1+exp(-2j*(bl + pi/2))) / (1-exp(-2j*(bl + pi/2))))
                self._z_in = 1/(1/self._z_in + 1/z)
                history_msg = "%s Z_0 = %s ohm, bl = %s radians" % (entry_type[button_id], complx_str(z), str(round(bl, 3)))
                self.stub_len.delete("0", len(self.stub_len.get()))
                self.stub_imp.delete("0", len(self.stub_imp.get()))
            else:
                raise ValueError()
        except ValueError:
            print("Unable to interpret input for button_id: ", button_id)
            return
        
        self._z_hist.append(self._z_in)
        self.z_in_entr.config(state="normal")
        self.z_in_entr.delete("0", "end")
        self.z_in_entr.insert("0", "%s ohm" % complx_str(self._z_hist[-1]) if len(self._z_hist) > 0 else "")
        self.z_in_entr.config(state="readonly")
        self.prev_entr.config(state="normal")
        self.prev_entr.insert(END, "%s\n" % history_msg)
        self.prev_entr.config(state="disabled")
        self._plot_z_in()


    def _remove_last_entry(self, redraw=True):
        if (size(self._plots_list) > self._smith_plots):
            self.chart_handle.lines.pop()
            del self._plots_list[-1]
            del self._z_hist[-1]
            self.z_in_entr.config(state="normal")
            self.z_in_entr.delete("0", "end")
            self.z_in_entr.insert("0", "%s ohm" % complx_str(self._z_hist[-1]) if len(self._z_hist) > 0 else "")
            self.z_in_entr.config(state="readonly")
            entrs = self.prev_entr.get("1.0", "end").strip().split("\n")
            self.prev_entr.config(state="normal")
            self.prev_entr.delete("1.0", END)
            self.prev_entr.insert(END, "\n".join(entrs[:-1]))
            self.prev_entr.config(state="disabled")
            if (redraw):
                self.canvas.draw()

    def _control_button_event(self, button_id):
        if (button_id == 1):
            # Clears the smith chart from any input
            for _ in range(size(self._plots_list)-self._smith_plots):
                self._remove_last_entry(redraw=False)
            self.canvas.draw()
        elif (button_id == 2):
            self._remove_last_entry()
        else:
            print("Unknown ctl button id: ", button_id)

    def _make_label(self, parent_frame, label_text, anchr="center"):
        return Label(parent_frame, anchor=anchr, text=label_text, **self._component_args_)

    def _make_button(self, parent_frame, button_text, cmd, anchr="center"):
        return Button(parent_frame, anchor=anchr, text=button_text, command=cmd, **self._component_args_)

    def _parse_raw_input(self, raw_in):
        """
        Converts raw_in to the numerical representation.
        Valid formats: '1234', '12.34', '2*pi', 'pi/3', '2*pi/3'.
        
        raises SyntaxError if the raw_in has incorrect format
        """
        if (raw_in is None or raw_in == ""):
            raise SyntaxError("Unable to interpret length of transmission line")
        times_idx = raw_in.find("*")
        pi_idx = raw_in.find("pi")
        div_idx = raw_in.find("/")
        if (times_idx == -1 and pi_idx == -1 and div_idx == -1):
            return float(raw_in)
        else:
            val1 = float(raw_in[:times_idx]) if (times_idx != -1) else 1
            val2 = pi if (pi_idx != -1) else 1
            val3 = float(raw_in[div_idx+1:]) if (div_idx != -1) else 1
            return val1*val2/val3
        raise SyntaxError("Valid formats: '1234', '12.34', '2*pi', 'pi/3', '2*pi/3'")

    def _draw_chart_background(self):
        self._make_circles()
        
        plt_settings = {"linewidth": str(self._smith_chart_linewidth_), "linestyle": "-", "marker": "", "markersize": "1", "color": self._normal_color_}
        plt_imp = copy(plt_settings)
        plt_imp["color"] = str(self._impedance_color_)
        plt_adm = copy(plt_settings)
        plt_adm["color"] = str(self._admittance_color_)
        
        self._plots_list.append(self.chart_handle.plot([-1, 1], [0, 0], **plt_settings))  # Plot the Im(z)=0 line
        
        for i, j in zip(self._imp_real_x, self._imp_real_y):  # Real parts of impedance and admittance
            self._plots_list.append(self.chart_handle.plot(i, j, **plt_imp))
            self._plots_list.append(self.chart_handle.plot(-i, -j, **plt_adm))
        
        v = linspace(0, 2*pi, 1001)
        self._plots_list.append(self.chart_handle.plot(cos(v), sin(v), **plt_settings))  # The abs(Gamma) = 1 ring
        
        for i, j in zip(self._imp_imag_x, self._imp_imag_y):  # Imaginary parts of impedance and admittance
            self._plots_list.append(self.chart_handle.plot(i, j, **plt_imp))
            self._plots_list.append(self.chart_handle.plot(-i, -j, **plt_adm))
        
        self._smith_plots = size(self._plots_list)

    def _make_circles(self):
        vals = [0.2, 0.5, 1, 2, 5]
        self._make_real_circles(self._imp_real_x, self._imp_real_y, vals)
        self._make_imag_circles(self._imp_imag_x, self._imp_imag_y, vals)

    def _make_real_circles(self, x, y, vals):
        for r in array(vals, dtype=float64):
            v = linspace(0, 2*pi, int(1001/(1+r)))
            x.append(r/(1+r) + 1/(1+r)*cos(v))
            y.append(1/(1+r)*sin(v))

    def _make_imag_circles(self, x, y, vals):
        self._add_imag_pts(array(vals, dtype=float64), x, y, pi/2, 3*pi/2)
        self._add_imag_pts(-array(vals, dtype=float64), x, y, 3*pi/2, 5*pi/2)

    def _add_imag_pts(self, X, x_pts, y_pts, v_start, v_stop):
        for x in X:
            v = linspace(v_start, v_stop, int(1001/abs(x)))
            _x = 1 + cos(v)/x
            _y = (1 + sin(v)) / x
            x_pts.append(array([i for i, j in zip(_x, _y) if (i**2 + j**2 <= 1)]))
            y_pts.append(array([j for i, j in zip(_x, _y) if (i**2 + j**2 <= 1)]))


if __name__ == "__main__":
    SmithChart().display()