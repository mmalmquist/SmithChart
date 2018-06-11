#ifndef SMITH_CHART_VIEW_H_
#define SMITH_CHART_VIEW_H_

#include <gtk/gtk.h>

#include <vector>

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
  SmithChartView(int width=512,
		 int height=512);
  ~SmithChartView();
  
  void
  repaint();
  void
  set_gtk_widget(GtkWidget *widget);
  gboolean
  draw_cb(cairo_t *cr);
  gboolean
  configure_event_cb(GtkWidget *widget);
private:
  std::vector<MyPolygon> plots;
  
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
  draw_circles();

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
