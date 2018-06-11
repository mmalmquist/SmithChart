#ifndef C_WRAPPER_MACROS_HPP_
#define C_WRAPPER_MACROS_HPP_

#define C_CB_WRAPPER(CPP_CB) c_##CPP_CB

#define DECLARE_CAIRO_C_CALLBACK_WRAPPER(TYPE, CPP_CALLBACK_FUNCTION)   \
  static gboolean							\
  C_CB_WRAPPER(CPP_CALLBACK_FUNCTION)(GtkWidget *widget,		\
				      cairo_t *cr,			\
				      gpointer data)			\
  {									\
    (void)widget;							\
    if (!data) { return FALSE; }					\
    return ((TYPE *)data)->CPP_CALLBACK_FUNCTION(cr);			\
  }

#define DECLARE_C_CALLBACK_WRAPPER(TYPE, CPP_CALLBACK_FUNCTION)		\
  static gboolean							\
  C_CB_WRAPPER(CPP_CALLBACK_FUNCTION)(GtkWidget *widget,		\
				      GdkEventMotion *event,		\
				      gpointer data)			\
  {									\
    (void)widget; (void)event;						\
    return ((TYPE *)data)->CPP_CALLBACK_FUNCTION(widget);		\
  }

#endif //C_WRAPPER_MACROS_HPP_
