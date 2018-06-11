#include <gtk/gtk.h>

#include <iostream>
#include <memory>

#include "root_directory.h"
#include "SmithChartView.hpp"
#include "SmithChartControl.hpp"

static std::unique_ptr<SmithChartControl> scc;

static void
close_window_cb(void)
{
  gtk_main_quit();
}

static bool
init_ui()
{
  GtkBuilder *builder = gtk_builder_new();
  GError *error = NULL;
  if (!gtk_builder_add_from_file(builder, SYS_PATH("/res/smith-chart.glade"), &error)) {
    std::cerr << "Error loading file: " << std::string(error->message) << std::endl;
    g_clear_error(&error);
    return false;
  }

  scc = std::make_unique<SmithChartControl>(std::make_unique<SmithChartView>());
  scc->init_ui(builder);

  g_signal_connect(GTK_WIDGET(gtk_builder_get_object(builder, "app-window")),
		   "destroy", G_CALLBACK(close_window_cb), NULL);
  
  gtk_builder_connect_signals(builder, NULL);
  g_object_unref(G_OBJECT(builder));

  return true;
}

int
main(int argc,
     char *argv[])
{
  if (!gtk_init_check(&argc, &argv)) {
    std::cerr << "Failed to init GTK. Exiting..." << std::endl;
    return EXIT_FAILURE;
  }

  if (!init_ui()) {
    return EXIT_FAILURE;
  }
  
  gtk_main();
  
  return EXIT_SUCCESS;
}
