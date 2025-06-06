import pygame
import random
import sys
import os

# Khởi tạo pygame
pygame.init()
pygame.mixer.init()  # Khởi tạo mixer cho âm thanh

# Cài đặt màn hình
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Tạo âm thanh bắn
shoot_sound = pygame.mixer.Sound(pygame.mixer.Sound.from_buffer(bytes([128] * 1000 + [180] * 1000 + [128] * 1000)))
shoot_sound.set_volume(0.2)  # Giảm âm lượng

# Lớp người chơi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 8
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        shoot_sound.play()  # Phát âm thanh khi bắn

# Lớp kẻ địch
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 5)
        self.speedx = random.randrange(-2, 2)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        
        # Nếu kẻ địch ra khỏi màn hình, tạo lại
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 25:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 5)
            self.speedx = random.randrange(-2, 2)

# Lớp đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10
        
    def update(self):
        self.rect.y += self.speedy
        # Xóa đạn nếu ra khỏi màn hình
        if self.rect.bottom < 0:
            self.kill()

# Tạo các nhóm sprite
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Tạo người chơi
player = Player()
all_sprites.add(player)

# Tạo kẻ địch
for i in range(8):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Điểm số
score = 0
high_score = 0

# Đọc điểm cao từ file nếu tồn tại
high_score_file = os.path.join(os.path.expanduser("~"), "space_shooter_high_score.txt")
if os.path.exists(high_score_file):
    try:
        with open(high_score_file, "r") as f:
            high_score = int(f.read().strip())
    except:
        high_score = 0

font = pygame.font.SysFont(None, 36)

# Vòng lặp game
clock = pygame.time.Clock()
running = True

while running:
    # Giữ tốc độ game
    clock.tick(60)
    
    # Xử lý sự kiện
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Cập nhật
    all_sprites.update()
    
    # Kiểm tra va chạm giữa đạn và kẻ địch
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 10
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)
    
    # Kiểm tra va chạm giữa người chơi và kẻ địch
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False
    
    # Vẽ
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Hiển thị điểm
    score_text = font.render(f"Điểm: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Hiển thị điểm cao
    high_score_text = font.render(f"Điểm cao: {high_score}", True, WHITE)
    screen.blit(high_score_text, (10, 50))
    
    # Cập nhật màn hình
    pygame.display.flip()

# Cập nhật điểm cao nếu cần
if score > high_score:
    high_score = score
    try:
        with open(high_score_file, "w") as f:
            f.write(str(high_score))
    except:
        pass

# Hiển thị màn hình kết thúc
font_large = pygame.font.SysFont(None, 72)
game_over_text = font_large.render("GAME OVER", True, RED)
final_score_text = font.render(f"Điểm cuối cùng: {score}", True, WHITE)
high_score_text = font.render(f"Điểm cao: {high_score}", True, WHITE)
restart_text = font.render("Nhấn R để chơi lại hoặc Q để thoát", True, WHITE)

screen.fill(BLACK)
screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
screen.blit(final_score_text, (WIDTH//2 - final_score_text.get_width()//2, HEIGHT//2))
screen.blit(high_score_text, (WIDTH//2 - high_score_text.get_width()//2, HEIGHT//2 + 50))
screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 100))
pygame.display.flip()

# Chờ người chơi quyết định
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                # Khởi động lại game
                waiting = False
                score = 0
                
                # Xóa tất cả sprite và tạo lại
                all_sprites.empty()
                enemies.empty()
                bullets.empty()
                
                player = Player()
                all_sprites.add(player)
                
                for i in range(8):
                    enemy = Enemy()
                    all_sprites.add(enemy)
                    enemies.add(enemy)
                
                running = True
                continue
            elif event.key == pygame.K_q:
                waiting = False

# Kết thúc game
pygame.quit()
sys.exit()