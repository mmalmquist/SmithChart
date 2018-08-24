#include "SmithChartModel.hpp"

#include <cmath>

std::complex<double>
SmithChartModel::compute_tl_series(double impedance,
				   double electrical_length) const
{
  double z = impedance;
  double bl = electrical_length;
  return z * ((m_z_in + std::complex<double>(0, z*std::tan(bl))) / (z + std::complex<double>(0, 1)*m_z_in*std::tan(bl)));
}

std::complex<double>
SmithChartModel::compute_lumped_series(std::complex<double> impedance) const
{
  return m_z_in + impedance;
}

std::complex<double>
SmithChartModel::compute_lumped_parallel(std::complex<double> impedance) const
{
  if (m_z_in + impedance != std::complex<double>(0, 0)) {
    return m_z_in * impedance / (m_z_in + impedance);
  } else {
    return impedance;
  }
}

std::complex<double>
SmithChartModel::compute_stub_open(double impedance,
				   double electrical_length) const
{
  if (!std::sin(electrical_length)) {
    return m_z_in;
  }
  return compute_lumped_parallel(-std::complex<double>(0, 1) * impedance / std::tan(electrical_length));
}

std::complex<double>
SmithChartModel::compute_stub_short(double impedance,
				    double electrical_length) const
{
  if (!std::cos(electrical_length)) {
    return m_z_in;
  }
  return compute_lumped_parallel(std::complex<double>(0, 1) * impedance * std::tan(electrical_length));
}

std::complex<double>
SmithChartModel::add_tl_series(double impedance,
			       double electrical_length)
{
  m_z_in = compute_tl_series(impedance, electrical_length);
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_lumped_series(std::complex<double> impedance)
{
  m_z_in = compute_lumped_series(impedance);
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_lumped_parallel(std::complex<double> impedance)
{
  m_z_in = compute_lumped_parallel(impedance);
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_stub_open(double impedance,
			       double electrical_length)
{
  m_z_in = compute_stub_open(impedance, electrical_length);
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

std::complex<double>
SmithChartModel::add_stub_short(double impedance,
				double electrical_length)
{
  m_z_in = compute_stub_short(impedance, electrical_length);
  m_z_hist.push_back(m_z_in);
  return m_z_in;
}

void
SmithChartModel::clear_history()
{
  m_z_hist.clear();
  m_z_in = std::complex<double>(0, 0);
}

void
SmithChartModel::delete_last_history()
{
  if (m_z_hist.size() > 0) {
    m_z_hist.pop_back();
  }
  m_z_in = m_z_hist.size() > 0 ? *(m_z_hist.end()-1) : std::complex<double>(0, 0);
}
