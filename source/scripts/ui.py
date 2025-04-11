import pygame

# Trieda HUD – zobrazuje názov levelu a ovládanie hráčov počas hry
class HUD:
    def __init__(self, game, level_name="Level 1"):
        self.game = game  # Odkaz na hernú inštanciu
        self.level_name = level_name  # Zobrazený názov levelu

        # Načítanie písma (predvolené pygame písmo)
        self.font = pygame.font.Font(None, 28)

        # Farba textu (biela)
        self.text_color = (255, 255, 255)

    # Vykreslenie HUD prvkov na obrazovku
    def render(self, screen):
        screen_width, screen_height = screen.get_size()
        padding = 10  # Vzdialenosť medzi prvkami

        # Vytvorenie textových plôch
        level_text = self.font.render(f"Level: {self.level_name}", True, self.text_color)
        restart_text = self.font.render("Press R to Restart", True, self.text_color)

        player1_text = self.font.render("P RED: [WASD]", True, self.text_color)
        player2_text = self.font.render("P GREEN: [Arrow Keys]", True, self.text_color)

        # Umiestnenie textu na obrazovke
        screen.blit(level_text, (padding, padding))  # Ľavý horný roh
        screen.blit(restart_text, (padding, padding + level_text.get_height()))  # Pod názvom levelu

        screen.blit(player1_text, (padding, screen_height - player1_text.get_height() - padding))  # Ľavý dolný roh
        screen.blit(player2_text, (screen_width - player2_text.get_width() - padding, screen_height - player2_text.get_height() - padding))  # Pravý dolný roh

    # Aktualizácia názvu levelu (napr. pri zmene levelu)
    def update_level_name(self, new_name):
        self.level_name = new_name


# Trieda HUD_Editor – zobrazuje legendu farieb pri úprave mapy v editore
class HUD_Editor:
    def __init__(self, editor):
        self.editor = editor  # Odkaz na editor
        self.font = pygame.font.Font(None, 24)
        self.text_color = (255, 255, 255)
        self.show_help = False


    def toggle_help(self):
        self.show_help = not self.show_help
        

    # Získanie zoznamu objektov a ich farieb pre legendu
    def get_legend_items(self):
        return [
            ("Button", (255, 0, 0)),
            ("Door ", (0, 0, 255)),
            ("Finish ", (0, 255, 0)),
            ("Player 1 ", (255, 255, 0)),
            ("Player 2 ", (0, 255, 255)),
        ]

    # Vykreslenie legendy (farby a ich význam)
    def render(self, screen):
        x, y = 10, 10
        spacing = 24

        # Vždy zobraz legendu farieb
        screen.blit(self.font.render("Legend:", True, self.text_color), (x, y))
        y += spacing

        for label, color in self.get_legend_items():
            pygame.draw.rect(screen, color, (x, y + 4, 20, 20))  # Farebný box
            text_surface = self.font.render(label, True, self.text_color)
            screen.blit(text_surface, (x + 30, y))
            y += spacing

        # Zobraz klávesy iba ak je zapnutý help
        if self.show_help:
            y += spacing
            screen.blit(self.font.render("Hotkeys (H to hide):", True, self.text_color), (x, y))
            y += spacing

            hotkeys = [
                ("S", "Save map"),
                ("O", "Toggle object mode"),
                ("G", "Toggle grid placement"),
                ("SHIFT + Scroll", "Change tile variant"),
                ("Scroll", "Change tile type / object"),
                ("Left Click", "Place tile/object"),
                ("Right Click", "Delete tile/object"),
                ("P", "Play test level"),
                ("H", "Toggle this help"),
            ]

            for key, desc in hotkeys:
                key_text = self.font.render(f"{key}:", True, self.text_color)
                desc_text = self.font.render(desc, True, self.text_color)

                # Čierne pozadie pre celý riadok
                bg_rect = pygame.Rect(x - 5, y - 2, 350, spacing)
                pygame.draw.rect(screen, (0, 0, 0), bg_rect)

                screen.blit(key_text, (x, y))
                screen.blit(desc_text, (x + 150, y))  # zväčšený rozostup
                y += spacing

        else:
            y += spacing
            screen.blit(self.font.render("Press H for help", True, self.text_color), (x, y))
        
        # Zobrazenie aktuálneho objektu (iba ak v objektovom režime)
        if self.editor.objectMode:
            selected = self.editor.object_list[self.editor.object_group]
            selected_text = self.font.render(f"Selected object: {selected}", True, self.text_color)

            # Čierne pozadie za textom
            bg_rect = selected_text.get_rect(topleft=(x, y + spacing))
            bg_rect.inflate_ip(10, 4)
            pygame.draw.rect(screen, (0, 0, 0), bg_rect)

            screen.blit(selected_text, (bg_rect.x + 5, bg_rect.y + 2))




class LevelCompleteMessage:
    def __init__(self, screen, text="Level Completed!"):
        self.screen = screen
        self.text = text
        self.font = pygame.font.Font(None, 64)
        self.color = (255, 255, 255)
        self.visible = False

    def render(self):
        if not self.visible:
            return

        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        text_surface = self.font.render(self.text, True, self.color)
        rect = text_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))

        # polopriesvitné pozadie
        overlay.fill((0, 0, 0, 100))
        overlay.blit(text_surface, rect)
        self.screen.blit(overlay, (0, 0))
