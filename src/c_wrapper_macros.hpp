#ifndef C_WRAPPER_MACROS_HPP_
#define C_WRAPPER_MACROS_HPP_

#define C_CB_WRAPPER(CPP_CB) c_##CPP_CB

#define CAIRO_CB_DEF(FN, T)			\
  static gboolean				\
  C_CB_WRAPPER(FN)(GtkWidget *widget,		\
		   cairo_t *cr,			\
		   gpointer data)		\
  { (void)widget;				\
    return ((T)data)->FN(cr);			\
  }

#define CLICK_CB_DEF(FN, T)			\
  static gboolean				\
  C_CB_WRAPPER(FN)(GtkWidget *widget,		\
		   gpointer data)		\
  { (void)widget;				\
    return ((T)data)->FN(widget);		\
  }

#define CONFIG_CB_DEF(FN, T)			\
  static gboolean				\
  C_CB_WRAPPER(FN)(GtkWidget *widget,		\
		   GdkEventConfigure *event,	\
		   gpointer data)		\
  { (void)widget; (void)event;			\
    return ((T)data)->FN(widget);		\
  }

#endif //C_WRAPPER_MACROS_HPP_
