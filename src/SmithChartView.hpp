#ifndef SMITH_CHART_VIEW_H_
#define SMITH_CHART_VIEW_H_

#include <gtk/gtk.h>

#include <vector>
#include <complex>
#include <memory>

#include "SmithChartModel.hpp"

struct MyPolygon {
  std::vector<double> x;
  std::vector<double> y;
  double red;
  double green;
  double blue;
};

class SmithChartView
{
public:
  SmithChartView(std::shared_ptr<SmithChartModel> scm,
		 int width,
		 int height);
  ~SmithChartView();

  void
  add_reflection_coefficient(std::complex<double> gamma,
			     std::vector<std::complex<double>> &gamma_arr);
  void
  clear_history();
  void
  delete_last_history();
  
  void
  repaint();
  void
  set_gtk_widget(GtkWidget *widget);
  gboolean
  draw_cb(cairo_t *cr);
  gboolean
  configure_event_cb(GtkWidget *widget);
private:
  std::shared_ptr<SmithChartModel> m_scm;
  std::vector<MyPolygon> plots;
  std::vector<MyPolygon> entries;
  std::vector<MyPolygon> centries;
  
  cairo_surface_t *m_surface = NULL;
  GtkWidget *m_canvas = NULL;

  cairo_t *m_cr = NULL;
  int m_width;
  int m_height;

  bool m_scale_required = false;
  double m_x_scale = 1;
  double m_y_scale = 1;

  void
  add_polygon(std::vector<double> &x,
	      std::vector<double> &y,
	      double red,
	      double green,
	      double blue);
  
  void
  draw_background();
  void
  draw_circles(std::vector<MyPolygon> const &polygon,
	       double line_wdith);
  void
  draw_entries();
  void
  draw_entry(std::vector<MyPolygon> const &polygon);

  void
  create_imag_circle(double v_start,
		     double v_stop,
		     double v_step,
		     double r,
		     std::vector<double> &xverts,
		     std::vector<double> &yverts);
  void
  create_real_circle(double v_start,
		     double v_stop,
		     double v_step,
		     double r,
		     std::vector<double> &xreal,
		     std::vector<double> &yreal);
  void
  create_circles();
  
  inline int32_t x_center() const { return m_width/2; }
  inline int32_t y_center() const { return m_height/2; }
  inline int32_t scale_factor() const { return 0.9*std::max(m_height, m_width)/2; }
};

#endif //SMITH_CHART_VIEW_H_
