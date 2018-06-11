#ifndef SMITH_CHART_MODEL_HPP_
#define SMITH_CHART_MODEL_HPP_

#include <vector>
#include <complex>

class SmithChartModel {
public:
  std::complex<double>
  add_tl_series(double impedance,
		double electrical_lengh);
  std::complex<double>
  add_lumped_series(std::complex<double> impedance);
  std::complex<double>
  add_lumped_parallel(std::complex<double> impedance);
  std::complex<double>
  add_stub_open(double impedance,
		double electrical_lengh);
  std::complex<double>
  add_stub_short(double impedance,
		 double electrical_lengh);

  void
  clear_history();
  void
  delete_last_history();
  inline std::complex<double> const&
  get_z_in() const
  {
    return m_z_in;
  }
  inline std::complex<double>
  calculate_reflection_coefficient() const
  {
    return (m_z_in - m_z_0) / (m_z_in + m_z_0);
  }
  inline std::complex<double> const *
  get_load_impedance() const
  {
    return m_z_hist.size() > 0 ? &m_z_hist[0] : NULL;
  }
  inline double const *
  get_system_impedance() const
  {
    return m_z_0 > 0 ? &m_z_0 : NULL;
  }
private:
  std::vector<std::complex<double> > m_z_hist;
  std::complex<double> m_z_in = std::complex<double>(0, 0);
  double m_z_0 = 50;
};

#endif //SMITH_CHART_MODEL_HPP_
