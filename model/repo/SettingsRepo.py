from model.ThemeEnum import Theme


class SettingsRepo:

    def __init__(self):
        self.__common_theme = None

    def provide_common_theme(self) -> Theme:
        if self.__common_theme is None:
            raise RuntimeError("Data is not initialized")
        return self.__common_theme

    def set_common_theme(self, theme: Theme):
        self.__common_theme = theme


settings_repo = SettingsRepo()
