#include "SmithChartView.hpp"

#include <cmath>
#include <complex>
#include <stdlib.h>
#include <iostream>
#include <vector>

#include "c_wrapper_macros.hpp"

DECLARE_CAIRO_C_CALLBACK_WRAPPER(SmithChartView, draw_cb)
DECLARE_C_CALLBACK_WRAPPER(SmithChartView, configure_event_cb)

template<typename T>
static std::vector<T> vec_mul(std::vector<T> lhs, T rhs)
{
  std::vector<T> prod;
  for (T &e : lhs) {
    prod.push_back(e * rhs);
  }
  return std::move(prod);
}

SmithChartView::SmithChartView(std::shared_ptr<SmithChartModel> scm,
			       int width,
			       int height)
  : m_scm(scm),
    m_width(width),
    m_height(height)
{
  create_circles();
}

SmithChartView::~SmithChartView()
{
  cairo_destroy(m_cr);
  cairo_surface_destroy(m_surface);
}

void
SmithChartView::add_reflection_coefficient(std::complex<double> gamma,
			     std::vector<std::complex<double>> &gamma_arr)
{
  int size = scale_factor();
  entries.push_back({{gamma.real()*size}, {gamma.imag()*size}, 0, 0, 0});
  MyPolygon mp;
  mp.red = 0;
  mp.green = 0;
  mp.blue = 0;
  std::vector<std::complex<double>>::const_iterator itr = gamma_arr.begin();
  for (; itr != gamma_arr.end(); ++itr) {
    mp.x.push_back(itr->real()*size);
    mp.y.push_back(itr->imag()*size);
  }
  centries.push_back(std::move(mp));
}

void
SmithChartView::clear_history()
{
  entries.clear();
  centries.clear();
}

void
SmithChartView::delete_last_history()
{
  if (entries.size() > 0) {
    entries.pop_back();
    centries.pop_back();
  }
}


void
SmithChartView::repaint()
{
  gtk_widget_queue_draw(m_canvas);
}

void
SmithChartView::set_gtk_widget(GtkWidget *widget)
{
  m_canvas = widget;
  
  g_signal_connect(m_canvas, "draw", G_CALLBACK(C_CB_WRAPPER(draw_cb)), this);
  g_signal_connect(m_canvas, "configure-event", G_CALLBACK(C_CB_WRAPPER(configure_event_cb)), this);
}

void
SmithChartView::add_polygon(std::vector<double> &x,
			    std::vector<double> &y,
			    double red,
			    double green,
			    double blue)
{
  plots.push_back({x, y, red, green, blue});
}

void
SmithChartView::create_imag_circle(double v_start,
				   double v_stop,
				   double v_step,
				   double r,
				   std::vector<double> &xverts,
				   std::vector<double> &yverts)
{
  int size = scale_factor();
  for (double v = v_start; v < v_stop; v += v_step) {
    double x = 1.0 + std::cos(v) / r;
    double y = (1.0 + std::sin(v)) / r;
    if (x*x + y*y <= 1.0) {
      xverts.push_back(x*size);
      yverts.push_back(y*size);
    }
  }
}

void
SmithChartView::create_real_circle(double v_start,
				   double v_stop,
				   double v_step,
				   double r,
				   std::vector<double>& xreal,
				   std::vector<double>& yreal)
{
  int size = scale_factor();
  for (double v = v_start; v < v_stop; v += v_step) {
    xreal.push_back(((r + std::cos(v)) / (1.0 + r)) * size);
    yreal.push_back((std::sin(v) / (1.0 + r)) * size);
  }
}

void SmithChartView::create_circles() {
  std::vector<double> vals{ 1/5.0, 1/2.0, 1.0, 2.0, 5.0 };

  for (double r : vals) {
    std::vector<double> xreal, yreal;
    create_real_circle(0, 2*M_PI, 2*M_PI*(1.0+r)/1000, r, xreal, yreal);
    add_polygon(xreal, yreal, 1, 0, 0);
    for (double &d : xreal) { d = -d; }
    for (double &d : yreal) { d = -d; }
    add_polygon(xreal, yreal, 0, 0, 1);
  }

  for (double r : vals) {
    std::vector<double> ximag, yimag;
    create_imag_circle(M_PI/2, 3*M_PI/2, 2*M_PI*r/1000, r, ximag, yimag);
    add_polygon(ximag, yimag, 1, 0, 0);
    for (double &d : ximag) { d = -d; }
    for (double &d : yimag) { d = -d; }
    add_polygon(ximag, yimag, 0, 0, 1);
  }

  for (double r : vals) {
    std::vector<double> ximag, yimag;
    create_imag_circle(3*M_PI/2, 5*M_PI/2, 2*M_PI*r/1000, -r, ximag, yimag);
    add_polygon(ximag, yimag, 1, 0, 0);
    for (double &d : ximag) { d = -d; }
    for (double &d : yimag) { d = -d; }
    add_polygon(ximag, yimag, 0, 0, 1);
  }

  int size = scale_factor();
  {
    std::vector<double> x, y;
    for (double v = 0; v < 2*M_PI; v += 2*M_PI/1000) {
      x.push_back(std::cos(v)*size);
      y.push_back(std::sin(v)*size);
    }
    add_polygon(x, y, 0, 0, 0);
  }
  
  {
    std::vector<double> x{(double) -size, (double) size};
    std::vector<double> y{(double) 0, (double) 0};
    add_polygon(x, y, 0, 0, 0);
  }
}

void
SmithChartView::draw_background()
{
  cairo_set_source_rgb(m_cr, 1, 1, 1);
  cairo_paint(m_cr);
}

void
SmithChartView::draw_circles(std::vector<MyPolygon> const &polygon,
			     double line_wdith)
{
  cairo_set_line_width(m_cr, line_wdith);
  for (MyPolygon const &poly : polygon) {
    cairo_set_source_rgb(m_cr, poly.red, poly.green, poly.blue);
    
    size_t len = std::min(poly.x.size(), poly.y.size());
    if (len == 0) {
      continue;
    }
    int xc = x_center();
    int yc = y_center();
    for (size_t i = 0; i < len-1; ++i) {
      cairo_move_to(m_cr, xc + poly.x[i], yc - poly.y[i]);
      cairo_line_to(m_cr, xc + poly.x[i+1], yc - poly.y[i+1]);
    }
    cairo_stroke(m_cr);
  }
}

void
SmithChartView::draw_entries()
{
  draw_entry(entries);
  draw_circles(centries, 1.0);
}

void
SmithChartView::draw_entry(std::vector<MyPolygon> const &polygon)
{
  cairo_set_line_width(m_cr, 0);
  for (MyPolygon const &poly : polygon) {
    cairo_set_source_rgb(m_cr, poly.red, poly.green, poly.blue);
    cairo_arc(m_cr, x_center() + poly.x[0], y_center() - poly.y[0], 2.5, 0, 2*M_PI);
    cairo_fill(m_cr);
  }
  if (polygon.size() > 0) {
    std::vector<MyPolygon>::const_iterator poly = polygon.end() - 1;
    cairo_set_source_rgb(m_cr, poly->red, poly->green, poly->blue);
    cairo_arc(m_cr, x_center() + poly->x[0], y_center() - poly->y[0], 5.0, 0, 2*M_PI);
    cairo_fill(m_cr);
  }
}

gboolean
SmithChartView::draw_cb(cairo_t *cr)
{
  draw_background();
  draw_circles(plots, 0.5);
  draw_entries();

  if (m_scale_required) {
    cairo_scale(cr, m_x_scale, m_y_scale);
  }
  cairo_set_source_surface(cr, m_surface, 0, 0);
  cairo_paint(cr);
  
  return FALSE;
}

gboolean
SmithChartView::configure_event_cb(GtkWidget *widget)
{
  int width = gtk_widget_get_allocated_width(widget);
  int height = gtk_widget_get_allocated_height(widget);
  m_scale_required = width != m_width || height != m_height;
  m_x_scale = (double)width / (double)m_width;
  m_y_scale = (double)height / (double)m_height;

  if (m_surface) {
    return TRUE;
  }
  m_surface = gdk_window_create_similar_surface(gtk_widget_get_window(m_canvas),
						CAIRO_CONTENT_COLOR,
						m_width,
						m_height);
  m_cr = cairo_create(m_surface);
  
  return TRUE;
}
