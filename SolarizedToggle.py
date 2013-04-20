import sublime
import sublime_plugin
import os.path


class SolarizedToggle(object):
    def __init__(self):
        self.global_settings_file = 'Preferences.sublime-settings'
        self.global_settings = sublime.load_settings(self.global_settings_file)
        self.plugin_settings_file = 'SolarizedToggle.sublime-settings'
        self.plugin_settings = sublime.load_settings(self.plugin_settings_file)
        self.state = self.plugin_settings.get('current_state')
        self.theme = self.global_settings.get('color_scheme')
        self.state = self.get_group(self.theme)
        print self.global_settings.get('color_scheme')

        if not self.plugin_settings.has('color_schemes'):
            self.plugin_settings.set('color_schemes', {
                "dark": [
                    "Packages/solarized-sublimetext3/Solarized (dark).tmTheme",
                    "Packages/solarized-sublimetext2/Solarized (dark).tmTheme",
                    "Packages/Solarized Color Scheme/Solarized (dark).tmTheme",
                    "Packages/Color Scheme - Default/Solarized (Dark).tmTheme"
                ],
                "light": [
                    "Packages/solarized-sublimetext3/Solarized (light).tmTheme",
                    "Packages/solarized-sublimetext2/Solarized (light).tmTheme",
                    "Packages/Solarized Color Scheme/Solarized (light).tmTheme",
                    "Packages/Color Scheme - Default/Solarized (Light).tmTheme"
                ]})

    def get_group(self, scheme):
        if scheme is None:
            print "No current scheme"
            return None
        return "light" if "light" in scheme.lower() else "dark"

    def get_next_group(self, scheme):
        if scheme is None:
            print "No current scheme"
            return None
        return "light" if "dark" in scheme.lower() else "dark"

    def _flip_state(self):
        self.state = self.get_next_group(self.state)
        self.plugin_settings.set('current_state', self.state)
        sublime.save_settings(self.plugin_settings_file)

    def set_state(self, value):
        possible = self.plugin_settings.get('color_schemes')[value]
        for each in possible:
            path = sublime.packages_path() + each.replace('Packages', '')
            if os.path.exists(path):
                print "Setting theme to ", path
            self.global_settings.set('color_scheme', each)
            self.theme = each
            sublime.save_settings(self.global_settings_file)
            return each

    def flip(self):
        self._flip_state()
        theme = self.set_state(self.state)
        # if self.plugin_settings.get("flip_theme"):
        #     self._set('theme', self.state)
        self.update_views()

    def update_views(self):
        for window in sublime.windows()
            for view in window.views():
                view.settings().set('color_scheme', self.theme)
        # print "Setting current window theme to ", self.theme
        # (sublime.active_window().active_view()
        #  .settings().set('color_scheme', self.theme))


# class SolarizedToggleListener(sublime_plugin.EventListener):
#     def on_activated(self, view):
#         _flipper.update_views(view)


class SolarizedToggleCommand(sublime_plugin.ApplicationCommand):
    def run(self, **args):
        _flipper.flip()


_flipper = SolarizedToggle()


def plugin_loaded():
    _flipper.plugin_loaded_setup()

# plugin_loaded()
