import pygame
import time
import random
import math
import sys

# --- Cấu hình ---
WIDTH, HEIGHT = 1000, 600
FPS = 60

colors = [
    (255, 0, 0),        # đỏ
    (255, 105, 180),    # hồng baby
    (255, 182, 193),    # hồng pastel
    (0, 80, 0),         # xanh lá đậm tối (pha đen)
    (255, 20, 147),     # hồng đậm
    (128, 0, 32),       # đỏ đô
    (255, 0, 0),        # quay về đỏ
]

def lerp_color(c1, c2, t):
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

lyrics = [
    [ (0.0, "Best"), (0.5, "decision"), (1.0, "of"), (1.5, "life") ],
    [ (2.0, "Betting"), (2.4, "the"), (2.8, "love"), (3.2, "for"), (3.6, "you"), (3.8, "ride") ],
    [ (4.2, "You're"), (4.7, "gonna"), (4.9, "be"), (5.1, "the"), (5.3, "way"), (5.7, "i"), (6.0, "try") ],
    [ (6.5, "あ"), (6.7, "な"), (6.9, "た"), (7.1, "を"), (7.3, "幸"), (7.5, "せ"), (7.7, "に"), (7.9, "し"), (8.1, "た"), (8.3, "い。") ],
    [ (8.9, "You"), (9.4, "know"), (9.8, "that"), (10.2, "my"), (10.6, "husband") ],
    [ (11.1, "Our"), (11.4, "love"), (11.9, "is"), (12.4, "so"), (12.9, "perfect") ],
    [ (13.3, "No"), (13.5, "need"), (14.0, "for"), (14.5, "dessert"), (15.0, "and") ],
    [ (15.5, "Our"), (16.0, "love"), (16.5, "is"), (17.0, "still"), (17.3, "spinning") ],
    [ (18.0, "Hello"), (18.5, "my"), (19.0, "virgo"), (19.5, "girl") ],
    [ (20.5, "Even"), (21.0, "though"), (21.5, "a"), (21.7, "part"), (22.0, "10") ],
    [ (22.5, "So"), (23.0, "good"), (23.4, "in"), (23.8, "my"), (24.3, "present") ],
    [ (25.0, "Crazy"), (25.4, "love"), (25.9, "no"), (26.3, "reason") ],
]

heart_colors = [
    (255, 105, 180),
    (255, 0, 0),
    (255, 255, 255),
    (255, 182, 193),
]

class Heart:
    def __init__(self):
        size = random.randint(20, 50)
        self.original_image = pygame.image.load("heart.png").convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (size, size))
        self.image = self.original_image.copy()
        self.colorize(random.choice(heart_colors)) 
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.angle = random.uniform(0, 2 * math.pi)
        self.radius = random.uniform(10, 40)
        self.speed = random.uniform(0.005, 0.01)

    def colorize(self, color):
        tint = pygame.Surface(self.image.get_size()).convert_alpha()
        tint.fill((*color, 100))
        self.image.blit(tint, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

    def float(self):
        self.angle += self.speed
        self.y += math.sin(self.angle) * 0.5
        self.x += math.cos(self.angle) * 0.5

        if self.x < -50: self.x = WIDTH + 50
        if self.x > WIDTH + 50: self.x = -50
        if self.y < -50: self.y = HEIGHT + 50
        if self.y > HEIGHT + 50: self.y = -50

    def draw(self, surface):
        surface.blit(self.image, (int(self.x), int(self.y)))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Iu bạn mình - Shayda (Lyrics Mode)")
    clock = pygame.time.Clock()

    base_font_size = 50
    font_size = base_font_size
    font = pygame.font.Font("NotoSansJP-Bold.ttf", font_size)

    pygame.mixer.music.load("iubanminh.mp3")
    pygame.mixer.music.play()

    hearts = [Heart() for _ in range(50)]

    start_time = time.time()

    lyric_line_index = 0
    word_index = 0
    current_words = ""

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0
        now = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        duration_each = 5.0
        total_colors = len(colors)
        idx = int(now // duration_each) % total_colors
        next_idx = (idx + 1) % total_colors
        t = (now % duration_each) / duration_each

        if t < 0.5:
            t_half = t / 0.5
            bg = lerp_color(colors[idx], (0, 0, 0), t_half)
        else:
            t_half = (t - 0.5) / 0.5
            bg = lerp_color((0, 0, 0), colors[next_idx], t_half)

        screen.fill(bg)

        for heart in hearts:
            heart.float()
            heart.draw(screen)

        if lyric_line_index < len(lyrics):
            line = lyrics[lyric_line_index]

            # Thêm từng từ nếu đúng thời điểm
            if word_index < len(line) and now >= line[word_index][0]:
                current_words += line[word_index][1] + " "
                word_index += 1

            # Khi đã hết từ trong dòng, đợi thêm 0.3s trước khi sang dòng mới
            elif word_index == len(line):
                last_word_time = line[-1][0]
                if now >= last_word_time + 0.3:
                    lyric_line_index += 1
                    word_index = 0
                    current_words = ""

        if current_words:
            if " " in current_words:
                words = current_words.strip().split(" ")
            else:
                words = list(current_words.strip())

            padding = 20
            max_width = WIDTH - padding * 2

            font_size = base_font_size
            while True:
                font = pygame.font.Font("NotoSansJP-Bold.ttf", font_size)
                line_height = font.get_height()
                lines = []
                current_line = ""

                for word in words:
                    test_line = current_line + word + " "
                    test_surface = font.render(test_line, True, (255, 255, 255))
                    if test_surface.get_width() <= max_width:
                        current_line = test_line
                    else:
                        lines.append(current_line)
                        current_line = word + " "
                lines.append(current_line)

                total_height = len(lines) * line_height
                if total_height <= HEIGHT - 50 or font_size <= 20:
                    break
                font_size -= 2

            start_y = (HEIGHT - total_height) // 2
            for i, line in enumerate(lines):
                surface = font.render(line, True, (255, 255, 255))
                rect = surface.get_rect()
                rect.centerx = WIDTH // 2
                rect.top = start_y + i * font.get_height()
                screen.blit(surface, rect)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
