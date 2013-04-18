import sublime
import sublime_plugin
import os.path


class SolarizedToggle(sublime_plugin.ApplicationCommand):

    def set_color_scheme(self, settings):

        colorscheme = {
            "dark" : [
                "Packages/solarized-sublimetext2/Solarized (dark).tmTheme",
                "Packages/Solarized Color Scheme/Solarized (dark).tmTheme",
                "Packages/Color Scheme - Default/Solarized (Dark).tmTheme"
            ],
            "light" : [
                "Packages/solarized-sublimetext2/Solarized (light).tmTheme",
                "Packages/Solarized Color Scheme/Solarized (light).tmTheme",
                "Packages/Color Scheme - Default/Solarized (Light).tmTheme"
            ]
        }

        current_scheme = settings.get("color_scheme")
        new_scheme = "light" if "dark" in current_scheme.lower() else "dark"

        paths = colorscheme[new_scheme]

        for path in paths:
            real_path = sublime.packages_path() + path.replace('Packages', '')
            if os.path.exists(real_path):
                # Uncomment for debugging
                # print "Setting theme to", real_path
                settings.set("color_scheme", path)
                return

        print "[SolarizedToggle]::[WARN] Could find no path to Solarized.."

    def run(self, **args):
        settingsFile = "Preferences.sublime-settings"
        settings = sublime.load_settings(settingsFile)

        sublime2_path = sublime.packages_path() + "/Solarized Color Scheme"
        sublime3_path = (sublime.installed_packages_path() +
                            "/Solarized Color Scheme.sublime-package")

        self.set_color_scheme(settings)

        sublime.save_settings(settingsFile)
