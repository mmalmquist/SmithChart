#include "SmithChartControl.hpp"

#include <gtk/gtk.h>

#include <iostream>
#include <string>
#include <complex>
#include <sstream>

#include "c_wrapper_macros.hpp"

CLICK_CB_DEF(clear_all_btn_cb, SmithChartControl *)
CLICK_CB_DEF(clear_last_btn_cb, SmithChartControl *)

CLICK_CB_DEF(add_tl_series_btn_cb, SmithChartControl *)
CLICK_CB_DEF(add_lumped_series_btn_cb, SmithChartControl *)
CLICK_CB_DEF(add_lumped_parallel_btn_cb, SmithChartControl *)
CLICK_CB_DEF(add_stub_open_btn_cb, SmithChartControl *)
CLICK_CB_DEF(add_stub_short_btn_cb, SmithChartControl *)

template<typename T>
static T mod(T v, T m) {
  if (v > m) { v -= v/m; };
  if (v < -m) { v += v/m; };
  return v;
}

static std::complex<double>
parse_complex(std::string const &str)
{
  std::complex<double> c;
  std::istringstream('(' + str + ')') >> c;
  return c;
}

static double
parse_double(std::string const &str)
{
  double d;
  std::istringstream(str) >> d;
  return d;
}

static double
parse_double_expr(std::string const &str)
{
  size_t i_mul = str.find("*");
  size_t i_pi = str.find("pi");
  size_t i_div = str.find("/");
  if (i_mul == std::string::npos && i_pi == std::string::npos && i_div == std::string::npos) {
    double d;
    std::istringstream(str) >> d;
    return d;
  } else {
    double val1 = 1.0;
    double val2 = i_pi != std::string::npos ? M_PI : 1.0;
    double val3 = 1.0;
    if (i_pi != std::string::npos) {
      if (i_mul != std::string::npos) {
	std::istringstream(str.substr(0, i_mul)) >> val1;
      }
      if (i_div != std::string::npos) {
	std::istringstream(str.substr(i_div+1, std::string::npos)) >> val3;
      }
    } else {
      if (i_mul != std::string::npos) {
	std::istringstream(str.substr(0, i_mul)) >> val1;
	std::istringstream(str.substr(i_mul+1, std::string::npos)) >> val3;
      }
      if (i_div != std::string::npos) {
	std::istringstream(str.substr(0, i_div)) >> val1;
	std::istringstream(str.substr(i_div+1, std::string::npos)) >> val3;
      }
    }
    return val1 * val2 / val3;
  }
}

static std::string
complex_to_str(std::complex<double> const &c)
{
  double real = c.real();
  double imag = c.imag();
  std::ostringstream os;
  if (std::abs(real) > 0 && std::abs(imag) > 0) {
    os << real;
    os << (imag < 0 ? " - j" : " + j");
    os << std::abs(imag);
  } else if (std::abs(real) > 0) {
    os << real;
  } else if (std::abs(imag) > 0) {
    os << (imag < 0 ? "-j" : "j");
    os << std::abs(imag);
  } else {
    os << "0";
  }
  return os.str();
}

void
SmithChartControl::finalize_add_component(std::string hist_entry,
					  std::vector<std::complex<double>> &z_arr)
{
  append_history(hist_entry);
  std::complex<double> const *z_load = m_scm->get_load_impedance();
  if (z_load) {
    gtk_entry_set_text(GTK_ENTRY(load_impedance_entry), complex_to_str(*z_load).c_str());
  }
  double const *z_system = m_scm->get_system_impedance();
  if (z_system) {
    gtk_entry_set_text(GTK_ENTRY(system_impedance_entry), complex_to_str(*z_system).c_str());
  }
  for (std::vector<std::complex<double>>::iterator itr = z_arr.begin(); itr != z_arr.end(); ++itr) {
    *itr = m_scm->calculate_reflection_coefficient(*itr);
  }
  m_scv->add_reflection_coefficient(m_scm->calculate_reflection_coefficient(), z_arr);
  m_scv->repaint();
}

gboolean
SmithChartControl::clear_all_btn_cb(GtkWidget *widget)
{
  (void)widget;
  clear_history();
  m_scm->clear_history();
  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(m_scm->get_z_in()).c_str());
  m_scv->clear_history();
  m_scv->repaint();
  
  return TRUE;
}

gboolean
SmithChartControl::clear_last_btn_cb(GtkWidget *widget)
{
  (void)widget;
  delete_last_history();
  m_scm->delete_last_history();
  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(m_scm->get_z_in()).c_str());
  m_scv->delete_last_history();
  m_scv->repaint();
  
  return TRUE;
}

gboolean
SmithChartControl::add_tl_series_btn_cb(GtkWidget *widget)
{
  (void)widget;
  GtkEntry *ie = GTK_ENTRY(transmission_line_impedance_entry);
  GtkEntry *ele = GTK_ENTRY(transmission_line_electrical_lengthentry);
  
  double z, bl;
  try {
    z = parse_double(std::string(gtk_entry_get_text(ie)));
    bl = mod(parse_double_expr(std::string(gtk_entry_get_text(ele))), 2*M_PI);
  } catch (...) {
    std::cerr << "Error parsing transmission line properties" << std::endl;
    return TRUE;
  }
  std::vector<std::complex<double>> z_arr;
  double ibl = 0, ebl = bl / 100.0;
  for (int i = 0; i < 101; ++i) {
    z_arr.push_back(m_scm->compute_tl_series(z, ibl));
    ibl += ebl;
  }
  std::complex<double> z_in = m_scm->add_tl_series(z, bl);

  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(z_in).c_str());
  
  gtk_entry_set_text(ie, "");
  gtk_entry_set_text(ele, "");
  finalize_add_component("Transmission Line in series: Z_0 = " + complex_to_str(z) + " ohm, bl = " + complex_to_str(bl) + " rad", z_arr);
  
  return TRUE;
}

gboolean
SmithChartControl::add_lumped_series_btn_cb(GtkWidget *widget)
{
  (void)widget;
  GtkEntry *ie = GTK_ENTRY(lumped_component_impedance_entry);
  
  std::complex<double> c;
  try {
    c = parse_complex(std::string(gtk_entry_get_text(ie)));
  } catch (...) {
    std::cerr << "Error parsing lumped component properties" << std::endl;
    return TRUE;
  }
  std::vector<std::complex<double>> z_arr;
  std::complex<double> ic = 0, ec = c / 100.0;
  for (int i = 0; i < 101; ++i) {
    z_arr.push_back(m_scm->compute_lumped_series(c));
    ic += ec;
  }
  std::complex<double> z_in = m_scm->add_lumped_series(c);

  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(z_in).c_str());
  
  gtk_entry_set_text(ie, "");
  finalize_add_component("Lumped component in series: Z = " + complex_to_str(c) + " ohm", z_arr);
  
  return TRUE;
}

gboolean
SmithChartControl::add_lumped_parallel_btn_cb(GtkWidget *widget)
{
  (void)widget;
  GtkEntry *ie = GTK_ENTRY(lumped_component_impedance_entry);

  std::complex<double> c;
  try {
    c = parse_complex(std::string(gtk_entry_get_text(ie)));
  } catch (...) {
    std::cerr << "Error parsing lumped component properties" << std::endl;
    return TRUE;
  }
  std::vector<std::complex<double>> z_arr;
  std::complex<double> ic = 0, ec = c / 100.0;
  for (int i = 0; i < 101; ++i) {
    z_arr.push_back(m_scm->compute_lumped_parallel(c));
    ic += ec;
  }
  std::complex<double> z_in = m_scm->add_lumped_parallel(c);

  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(z_in).c_str());
  
  gtk_entry_set_text(ie, "");
  finalize_add_component("Lumped component in parallel: Z = " + complex_to_str(c) + " ohm", z_arr);
  
  return TRUE;
}

gboolean
SmithChartControl::add_stub_open_btn_cb(GtkWidget *widget)
{
  (void)widget;
  GtkEntry *ie = GTK_ENTRY(stub_impedance_entry);
  GtkEntry *ele = GTK_ENTRY(stub_electrical_length_entry);
  
  double z, bl;
  try {
    z = parse_double(std::string(gtk_entry_get_text(ie)));
    bl = mod(parse_double_expr(std::string(gtk_entry_get_text(ele))), 2*M_PI);
  } catch (...) {
    std::cerr << "Error parsing stub properties" << std::endl;
    return TRUE;
  }
  std::vector<std::complex<double>> z_arr;
  double ibl = 0, ebl = bl / 100.0;
  for (int i = 0; i < 101; ++i) {
    z_arr.push_back(m_scm->compute_stub_open(z, ibl));
    ibl += ebl;
  }
  std::complex<double> z_in = m_scm->add_stub_open(z, bl);

  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(z_in).c_str());
  
  gtk_entry_set_text(ie, "");
  gtk_entry_set_text(ele, "");
  finalize_add_component("Stub terminated in a open: Z_0 = " + complex_to_str(z) + " ohm, bl = " + complex_to_str(bl) + " rad", z_arr);
  
  return TRUE;
}

gboolean
SmithChartControl::add_stub_short_btn_cb(GtkWidget *widget)
{
  (void)widget;
  GtkEntry *ie = GTK_ENTRY(stub_impedance_entry);
  GtkEntry *ele = GTK_ENTRY(stub_electrical_length_entry);
  
  double z, bl;
  try {
    z = parse_double(std::string(gtk_entry_get_text(ie)));
    bl = mod(parse_double_expr(std::string(gtk_entry_get_text(ele))), 2*M_PI);
  } catch (...) {
    std::cerr << "Error parsing stub properties" << std::endl;
    return TRUE;
  }
  std::vector<std::complex<double>> z_arr;
  double ibl = M_PI/2, ebl = (bl-M_PI/2) / 100.0;
  for (int i = 0; i < 101; ++i) {
    z_arr.push_back(m_scm->compute_stub_short(z, ibl));
    ibl += ebl;
  }
  std::complex<double> z_in = m_scm->add_stub_short(z, bl);

  gtk_entry_set_text(GTK_ENTRY(z_in_entry), complex_to_str(z_in).c_str());
  
  gtk_entry_set_text(ie, "");
  gtk_entry_set_text(ele, "");
  finalize_add_component("Stub terminated in an short: Z_0 = " + complex_to_str(z) + " ohm, bl = " + complex_to_str(bl) + " rad", z_arr);
  
  return TRUE;
}

#define CSIG(bldr, btn, c_function_cb)					\
  g_signal_connect(GTK_WIDGET(gtk_builder_get_object(bldr, btn)),	\
		   "clicked", G_CALLBACK(c_function_cb), this)
  
void
SmithChartControl::init_ui(GtkBuilder *builder)
{
  m_scv->set_gtk_widget(GTK_WIDGET(gtk_builder_get_object(builder, "smith-chart")));
  
  CSIG(builder, "clear-all-btn", C_CB_WRAPPER(clear_all_btn_cb));
  CSIG(builder, "clear-last-btn", C_CB_WRAPPER(clear_last_btn_cb));
  
  CSIG(builder, "transmission-line-add-series-btn", C_CB_WRAPPER(add_tl_series_btn_cb));
  CSIG(builder, "lumped-component-add-series-btn", C_CB_WRAPPER(add_lumped_series_btn_cb));
  CSIG(builder, "lumped-component-add-parallel-btn", C_CB_WRAPPER(add_lumped_parallel_btn_cb));
  CSIG(builder, "stub-add-open-btn", C_CB_WRAPPER(add_stub_open_btn_cb));
  CSIG(builder, "stub-add-short-btn", C_CB_WRAPPER(add_stub_short_btn_cb));
  
  z_in_entry = GTK_WIDGET(gtk_builder_get_object(builder, "z-in-entry"));
  transmission_line_impedance_entry = GTK_WIDGET(gtk_builder_get_object(builder, "transmission-line-impedance-entry"));
  transmission_line_electrical_lengthentry = GTK_WIDGET(gtk_builder_get_object(builder, "transmission-line-electrical-length-entry"));
  lumped_component_impedance_entry = GTK_WIDGET(gtk_builder_get_object(builder, "lumped-component-impedance-entry"));
  stub_impedance_entry = GTK_WIDGET(gtk_builder_get_object(builder, "stub-impedance-entry"));
  stub_electrical_length_entry = GTK_WIDGET(gtk_builder_get_object(builder, "stub-electrical-length-entry"));
  system_impedance_entry = GTK_WIDGET(gtk_builder_get_object(builder, "system-impedance-entry"));
  load_impedance_entry = GTK_WIDGET(gtk_builder_get_object(builder, "load-impedance-entry"));
  history_view = GTK_WIDGET(gtk_builder_get_object(builder, "history-view"));
}


void
SmithChartControl::clear_history()
{
  GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(history_view));

  GtkTextIter start_find, end_find;
  gtk_text_buffer_get_start_iter(buffer, &start_find);
  gtk_text_buffer_get_end_iter(buffer, &end_find);
  
  gtk_text_buffer_delete(buffer, &start_find, &end_find);
}

void
SmithChartControl::delete_last_history()
{
  GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(history_view));
  
  GtkTextIter start_find, end_find;
  gtk_text_buffer_get_end_iter(buffer, &start_find);
  gtk_text_iter_backward_line(&start_find);
  gtk_text_buffer_get_end_iter(buffer, &end_find);
  
  gtk_text_buffer_delete(buffer, &start_find, &end_find);
}

void
SmithChartControl::append_history(std::string entry)
{
  GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(history_view));

  GtkTextIter end_find;
  gtk_text_buffer_get_end_iter(buffer, &end_find);
  
  gtk_text_buffer_insert(buffer, &end_find, (entry + "\n").c_str(), -1);
}
