#include <stdio.h>
#include <string.h>
#include <gtk/gtk.h>

static void activate (GtkApplication* app, gpointer user_data){
  GtkWidget *mainWindow;

  mainWindow = gtk_application_window_new (app);
  gtk_window_set_title (GTK_WINDOW (mainWindow), "Window");
  gtk_window_set_default_size (GTK_WINDOW (mainWindow), 200, 200);
  gtk_widget_show_all (mainWindow);
}

int main (int argc, char **argv){
  GtkApplication *app;
  int status;

  app = gtk_application_new ("test", G_APPLICATION_FLAGS_NONE);
  g_signal_connect (app, "activate", G_CALLBACK (activate), NULL);
  status = g_application_run (G_APPLICATION (app), argc, argv);
  g_object_unref (app);

  return status;
}