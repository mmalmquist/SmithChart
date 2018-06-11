#include "SmithChartModel.hpp"

#include <cmath>

static const std::complex<double> c1j(0, 1);
static const std::complex<double> c1(1, 0);
static const std::complex<double> c0(0, 0);

std::complex<double>
SmithChartModel::add_tl_series(double impedance,
			       double electrical_length)
{
  double z = impedance;
  double bl = electrical_length;

  m_z_in = z*((m_z_in + c1j*z*std::tan(bl)) / (z + c1j*m_z_in*std::tan(bl)));
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_lumped_series(std::complex<double> impedance)
{
  std::complex<double> z = impedance;
  m_z_in += z;
  
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_lumped_parallel(std::complex<double> impedance)
{
  std::complex<double> z = impedance;
  if (m_z_in + z != c0) {
    m_z_in = m_z_in * z / (m_z_in + z);
  } else {
    m_z_in = z;
  }
  
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_stub_open(double impedance,
			       double electrical_length)
{
  double z_c = impedance;
  double bl = electrical_length;
                
  std::complex<double> z = z_c*((1.0 + std::exp(-2.0*c1j*(bl + M_PI))) / (1.0 - std::exp(-2.0*c1j*(bl + M_PI))));
    
  m_z_in = m_z_in * z / (m_z_in + z);
  
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_stub_short(double impedance,
				double electrical_length)
{
  double z_c = impedance;
  double bl = electrical_length;
                
  std::complex<double> z = z_c*((1.0 + std::exp(-2.0*c1j*(bl + M_PI/2))) / (1.0 - std::exp(-2.0*c1j*(bl + M_PI/2))));
  m_z_in = m_z_in * z / (m_z_in + z);
  
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

void
SmithChartModel::clear_history()
{
  m_z_hist.clear();
  m_z_in = c0;
}

void
SmithChartModel::delete_last_history()
{
  if (m_z_hist.size() > 0) {
    m_z_hist.pop_back();
  }
  m_z_in = m_z_hist.size() > 0 ? *(m_z_hist.end()-1) : c0;
}
