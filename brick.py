import tkinter as tk # untuk membuat antarmuka grafis (GUI).
import random # untuk mengatur arah bola secara acak saat permainan dimulai atau setelah kalah.
import time # untuk mengatur timer tantangan waktu.

class BrickBreaker: # Membuat kelas BrickBreaker 
    def __init__(self, master):
        self.master = master
        self.master.title("Brick Breaker")

        
        self.canvas = tk.Canvas(self.master, width=700, height=500, bg="black") # Mengatur ukuran dan memberikan  warna latar belakang hitam pada kanvas.
        self.canvas.pack()

        self.paddle = self.canvas.create_rectangle(350, 480, 450, 490, fill="yellow") # Mengatur posisi awal paddle dan memberikan warna kuning pada paddle
        self.ball = self.canvas.create_oval(390, 470, 410, 490, fill="pink") # Mengatur posisi awal bola dan memberikan warna pink pada bola
        self.ball_dx = 2 # mengatur kecepatan bola pada sumbu x
        self.ball_dy = -2 # mengatur kecepatan bola pada sumbu y
        self.bricks = [] # Menyimpan semua balok yang akan dihancurkan.
        self.score = 0 # Menyimpan skor pemain.
        self.level = 1 # Mengatur level permainan.
        self.lives = 3 #  Mengatur jumlah nyawa pemain.
        self.time_left = 60  # Tantangan waktu 60 detik per level
        self.is_paused = False # Status permainan apakah sedang dijeda atau tidak.
        self.create_bricks() #  Membuat balok-balok baru pada kanvas untuk dihancurkan oleh bola.
        self.update_score() # Memperbarui tampilan informasi permainan (skor, nyawa, level, waktu tersisa) di kanvas.
        self.create_controls() # Membuat tombol kontrol untuk menjeda (pause) dan mengulang (restart) permainan.

        self.canvas.bind_all("<KeyPress-Left>", self.move_left) # Menggerakkan paddle ke kiri saat tombol panah kiri ditekan.
        self.canvas.bind_all("<KeyPress-Right>", self.move_right) # Menggerakkan paddle ke kanan saat tombol panah kanan ditekan.

        self.game_start_time = time.time()  # Start timer for challenge time
        self.game_loop()

    def create_bricks(self): # membuat balok
        for i in range(7):  # Membuat 7 kolom
            for j in range(5):  # Membuat 5 baris
                brick = self.canvas.create_rectangle(60 * i + 30, 30 * j + 30, 60 * i + 90, 30 * j + 60, fill="purple") # Setiap balok memiliki ukuran tetap dengan warna ungu.
                self.bricks.append(brick) # Menambahkan balok baru ke daftar self.bricks.

    def move_left(self, event): # Menggerakkan paddle ke kiri jika tidak dijeda dan belum mencapai batas kiri kanvas.
        if not self.is_paused and self.canvas.coords(self.paddle)[0] > 0:
            self.canvas.move(self.paddle, -20, 0)

    def move_right(self, event): # Menggerakkan paddle ke kanan jika tidak dijeda dan belum mencapai batas kanan kanvas.
        if not self.is_paused and self.canvas.coords(self.paddle)[2] < 700:  # Sesuaikan batas kanan kanvas
            self.canvas.move(self.paddle, 20, 0)

    def update_score(self): # Menampilkan informasi permainan (skor, nyawa, level, dan waktu tersisa)
        self.canvas.delete("score")
        self.canvas.create_text(600, 20, text=f"Score: {self.score}", fill="white", tags="score")
        self.canvas.create_text(600, 40, text=f"Lives: {self.lives}", fill="white", tags="score")
        self.canvas.create_text(600, 60, text=f"Level: {self.level}", fill="white", tags="score")
        self.canvas.create_text(600, 80, text=f"Time Left: {self.time_left}s", fill="white", tags="score")

    def create_controls(self): # Membuat tombol untuk menjeda (Pause) dan mengulang permainan (Restart).
        self.pause_button = tk.Button(self.master, text="Pause", command=self.pause_game)
        self.pause_button.pack(side=tk.LEFT, padx=10, pady=10)

        self.restart_button = tk.Button(self.master, text="Restart", command=self.restart_game)
        self.restart_button.pack(side=tk.LEFT, padx=10, pady=10)

    def pause_game(self): # Mengatur mode jeda permainan dan menampilkan/menghapus tulisan "PAUSED".
        self.is_paused = not self.is_paused
        if self.is_paused:
            self.canvas.create_text(350, 250, text="PAUSED", fill="yellow", font=("Arial", 30))
        else:
            self.canvas.delete("pause")

    def restart_game(self): # Mereset permainan ke kondisi awal dan memulai ulang game loop.
        self.score = 0
        self.level = 1
        self.lives = 3
        self.time_left = 60
        self.create_bricks()
        self.update_score()
        self.canvas.coords(self.ball, 390, 470, 410, 490)
        self.ball_dx = 2
        self.ball_dy = -2
        self.game_start_time = time.time()
        self.is_paused = False
        self.game_loop()

    def game_loop(self): # Menjalankan logika permainan, termasuk pergerakan bola, deteksi tabrakan, dan pengecekan waktu.
        if self.is_paused:
            return

        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        self.check_collision()
        self.check_boundaries()
        self.update_time()

        # Check if the time is over for the level
        if self.time_left <= 0:
            self.game_over("Time's Up!")

        self.master.after(10, self.game_loop) # Menjalankan game loop setiap 10 milidetik.

    def check_collision(self): # Menghapus balok saat bola menabrak dan menambah skor.
        ball_coords = self.canvas.coords(self.ball)
        for brick in self.bricks:
            if self.canvas.bbox(brick) and self.collides(ball_coords, self.canvas.coords(brick)):
                self.canvas.delete(brick)
                self.bricks.remove(brick)
                self.ball_dy = -self.ball_dy
                self.score += 10
                self.update_score()
                if len(self.bricks) == 0:
                    self.level_up()

        paddle_coords = self.canvas.coords(self.paddle) # Membuat bola memantul kembali jika menyentuh paddle.
        if self.collides(ball_coords, paddle_coords):
            self.ball_dy = -self.ball_dy

    def check_boundaries(self): # Memeriksa batas permainan dan mengatur pantulan bola saat menyentuh dinding atau kehilangan nyawa jika keluar dari batas bawah.
        ball_coords = self.canvas.coords(self.ball)
        if ball_coords[1] <= 0:
            self.ball_dy = -self.ball_dy
        if ball_coords[0] <= 0 or ball_coords[2] >= 700:  # Sesuaikan batas kanan kanvas
            self.ball_dx = -self.ball_dx
        if ball_coords[3] >= 500:  # Sesuaikan batas bawah kanvas
            self.lives -= 1
            if self.lives == 0:
                self.game_over("Game Over")
            else:
                self.reset_ball()

    def reset_ball(self): # Mereset posisi dan arah bola secara acak.
        self.canvas.coords(self.ball, 390, 470, 410, 490)
        self.ball_dx = random.choice([-2, 2])
        self.ball_dy = -2

    def collides(self, ball_coords, object_coords): # Memeriksa apakah bola bertabrakan dengan objek lain di kanvas.
        return ball_coords[2] >= object_coords[0] and ball_coords[0] <= object_coords[2] and ball_coords[3] >= object_coords[1] and ball_coords[1] <= object_coords[3]

    def level_up(self): # Meningkatkan level permainan, mereset waktu tantangan, memperbarui skor, dan membuat ulang susunan brick.
        self.level += 1
        self.create_bricks()
        self.update_score()
        self.time_left = 60  # Reset challenge time
        self.game_start_time = time.time()

    def update_time(self): # Menghitung sisa waktu permainan berdasarkan waktu yang telah berlalu dan memperbarui tampilan skor.
        elapsed_time = time.time() - self.game_start_time
        self.time_left = 60 - int(elapsed_time)
        self.update_score()

    def game_over(self, message): # Menampilkan pesan akhir permainan dan skor akhir di tengah kanvas saat permainan selesai.
        self.canvas.create_text(350, 250, text=message, fill="red", font=("Arial", 30))
        self.canvas.create_text(350, 300, text=f"Final Score: {self.score}", fill="red", font=("Arial", 20))

root = tk.Tk() # Membuat jendela utama aplikasi menggunakan modul Tkinter sebagai antarmuka grafis.
game = BrickBreaker(root) # Membuat objek permainan dan menghubungkannya dengan jendela.
root.mainloop() # Memulai loop utama aplikasi untuk menjaga jendela tetap berjalan dan merespons setiap interaksi pengguna.
