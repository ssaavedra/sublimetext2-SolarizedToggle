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

    def save_previous_color_scheme(self):
        possible = self.plugin_settings.get('color_schemes')
        old_cs = self.global_settings.get('color_scheme')

        possible = [item for sublist in possible.itervalues() for item in sublist]
        if old_cs in possible:
            return

        print old_cs
        print possible

        self.global_settings.set('color_scheme_disabled', old_cs)
        sublime.save_settings(self.global_settings_file)

    def set_state(self, value):
        possible = self.plugin_settings.get('color_schemes')[value]
        for each in possible:
            path = sublime.packages_path() + each.replace('Packages', '')
            if os.path.exists(path):
                print "Setting theme to ", path
            self.save_previous_color_scheme()
            self.global_settings.set('color_scheme', each)
            self.theme = each
            sublime.save_settings(self.global_settings_file)
            return each

    def flip(self):
        self._flip_state()
        self.set_state(self.state)
        # if self.plugin_settings.get("flip_theme"):
        #     self._set('theme', self.state)

    def erase(self):
        self.global_settings.erase('color_scheme')
        disabled = self.global_settings.get('color_scheme_disabled')
        self.global_settings.set('color_scheme', disabled)
        sublime.save_settings(self.global_settings_file)


class SolarizedToggleCommand(sublime_plugin.ApplicationCommand):
    def run(self, **args):
        _flipper.flip()


class SolarizedDisableCommand(sublime_plugin.ApplicationCommand):
    def run(self, **args):
        _flipper.erase()


_flipper = SolarizedToggle()
