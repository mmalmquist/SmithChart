#include "SmithChartControl.hpp"

#include <gtk/gtk.h>

#include <iostream>
#include <string>

#define C_CB_WRAPPER(CPP_CB) c_##CPP_CB
#define DECLARE_C_CALLBACK_WRAPPER(CPP_CALLBACK_FUNCTION)		\
  static gboolean							\
  C_CB_WRAPPER(CPP_CALLBACK_FUNCTION)(GtkWidget *widget,		\
			    GdkEventMotion *event,			\
			    gpointer data)				\
  {									\
    (void)widget; (void)event;						\
    return ((SmithChartControl *)data)->CPP_CALLBACK_FUNCTION();	\
  }

DECLARE_C_CALLBACK_WRAPPER(clear_all_btn_cb)
DECLARE_C_CALLBACK_WRAPPER(clear_last_btn_cb)

DECLARE_C_CALLBACK_WRAPPER(add_tl_series_btn_cb)
DECLARE_C_CALLBACK_WRAPPER(add_lumped_series_btn_cb)
DECLARE_C_CALLBACK_WRAPPER(add_lumped_parallel_btn_cb)
DECLARE_C_CALLBACK_WRAPPER(add_stub_open_btn_cb)
DECLARE_C_CALLBACK_WRAPPER(add_stub_short_btn_cb)

gboolean
SmithChartControl::clear_all_btn_cb()
{
  clear_history();
  
  return TRUE;
}

gboolean
SmithChartControl::clear_last_btn_cb()
{
  delete_last_history();
  
  return TRUE;
}

gboolean
SmithChartControl::add_tl_series_btn_cb()
{
  GtkEntry *ie = GTK_ENTRY(transmission_line_impedance_entry);
  GtkEntry *ele = GTK_ENTRY(transmission_line_electrical_lengthentry);
  
  gchar const *impedance = gtk_entry_get_text(ie);
  gchar const *electrical_len = gtk_entry_get_text(ele);

  // process entry content
  
  gtk_entry_set_text(ie, "");
  gtk_entry_set_text(ele, "");
  append_history("add_tl_series_btn_cb");
  
  return TRUE;
}

gboolean
SmithChartControl::add_lumped_series_btn_cb()
{
  GtkEntry *ie = GTK_ENTRY(lumped_component_impedance_entry);

  gchar const *impedance = gtk_entry_get_text(ie);
  
  // process entry content
  
  gtk_entry_set_text(ie, "");
  append_history("add_lumped_series_btn_cb");
  return TRUE;
}

gboolean
SmithChartControl::add_lumped_parallel_btn_cb()
{
  GtkEntry *ie = GTK_ENTRY(lumped_component_impedance_entry);
  gchar const *impedance = gtk_entry_get_text(ie);

  // process entry content
  
  gtk_entry_set_text(ie, "");
  append_history("add_lumped_parallel_btn_cb");
  return TRUE;
}

gboolean
SmithChartControl::add_stub_open_btn_cb()
{
  GtkEntry *ie = GTK_ENTRY(stub_impedance_entry);
  GtkEntry *ele = GTK_ENTRY(stub_electrical_length_entry);
  
  gchar const *impedance = gtk_entry_get_text(ie);
  gchar const *electrical_len = gtk_entry_get_text(ele);
  
  // process entry content
  
  gtk_entry_set_text(ie, "");
  gtk_entry_set_text(ele, "");
  append_history("add_stub_open_btn_cb");
  return TRUE;
}

gboolean
SmithChartControl::add_stub_short_btn_cb()
{
  GtkEntry *ie = GTK_ENTRY(stub_impedance_entry);
  GtkEntry *ele = GTK_ENTRY(stub_electrical_length_entry);
  
  gchar const *impedance = gtk_entry_get_text(ie);
  gchar const *electrical_len = gtk_entry_get_text(ele);

  // process entry content
  
  gtk_entry_set_text(ie, "");
  gtk_entry_set_text(ele, "");
  append_history("add_stub_short_btn_cb");
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
  CSIG(builder, "stub-add-series-btn", C_CB_WRAPPER(add_stub_open_btn_cb));
  CSIG(builder, "stub-add-parallel-btn", C_CB_WRAPPER(add_stub_short_btn_cb));
  
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
