#ifndef SMITH_CHART_CONTROL_HPP_
#define SMITH_CHART_CONTROL_HPP_

#include <gtk/gtk.h>

#include <memory>
#include <string>
#include <vector>

#include "SmithChartView.hpp"
#include "SmithChartModel.hpp"

class SmithChartControl {
public:
  SmithChartControl(std::shared_ptr<SmithChartModel> scm,
		    std::unique_ptr<SmithChartView> scv)
    : m_scm(scm),
      m_scv(std::move(scv))
  {
  }
  void
  finalize_add_component(std::string hist_entry,
			 std::vector<std::complex<double>> &z_arr);
  gboolean
  clear_all_btn_cb(GtkWidget *widget);
  gboolean
  clear_last_btn_cb(GtkWidget *widget);

  gboolean
  add_tl_series_btn_cb(GtkWidget *widget);
  gboolean
  add_lumped_series_btn_cb(GtkWidget *widget);
  gboolean
  add_lumped_parallel_btn_cb(GtkWidget *widget);
  gboolean
  add_stub_open_btn_cb(GtkWidget *widget);
  gboolean
  add_stub_short_btn_cb(GtkWidget *widget);
  
  void init_ui(GtkBuilder *builder);
private:
  std::shared_ptr<SmithChartModel> m_scm;
  std::unique_ptr<SmithChartView> m_scv;
  GtkWidget *z_in_entry;
  GtkWidget *transmission_line_impedance_entry;
  GtkWidget *transmission_line_electrical_lengthentry;
  GtkWidget *lumped_component_impedance_entry;
  GtkWidget *stub_impedance_entry;
  GtkWidget *stub_electrical_length_entry;
  GtkWidget *system_impedance_entry;
  GtkWidget *load_impedance_entry;
  GtkWidget *history_view;

  void clear_history();
  void delete_last_history();
  void append_history(std::string entry);
};

#endif //SMITH_CHART_CONTROL_HPP_
