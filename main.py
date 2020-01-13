from superwires import games, color
from random import randrange

games.init(screen_width = 640, screen_height = 480, fps = 50)

#sprites
#the bird
class Bird(games.Sprite):

    image = games.load_image("images/bird.png", transparent = True)
    score = 0
    #constructor
    def __init__(self):
        super().__init__(x = 200, y = 50, dx = 0, dy = 2, image = Bird.image)
        Bird.score = 0

        #score text
        self.score_text = games.Text(value = "Score : 0", size = 30, color = color.blue, left = 30, top = 30)
        games.screen.add(self.score_text)

    #update for each fps
    def update(self):
        #if the player presses space 
        if games.keyboard.is_pressed(games.K_SPACE):
            self.y = self.y - 5
            self.dy = 0
        else:
            self.dy += 0.1

        #bird falls down
        if self.top > games.screen.height:
            #stop all the sprites
            sprites = games.screen.all_objects
            for sprite in sprites:
                sprite.dx = 0

            #display the game over message and quit the game
            msg = games.Message(value = "Game over score is "+str(Bird.score), x = games.screen.width//2, y = games.screen.height//2, lifetime=100, after_death=games.screen.quit, size=60, color=color.red)
            games.screen.add(msg)

        #if it collides with pipe
        if self.overlapping_sprites:
            #stop the bird
            self.dy = 0
            #stop the pipes
            for pipe in games.screen.all_objects:
                pipe.dx = 0

            #display the game over message and quit the game
            msg = games.Message(value = "Game over score is "+str(Bird.score), x = games.screen.width//2, y = games.screen.height//2, lifetime=200, after_death=games.screen.quit, size=60, color=color.red)
            games.screen.add(msg)

        #bird reaches the roof
        if self.top < 0:
            self.top = 0

        #incrementing the score
        self.score_text.value = "Socre : "+str(Bird.score)

#auxiliary sprite
class Blank(games.Sprite):
    image = games.load_image("images/blank.jpg", transparent=True)

    def __init__(self):
        super().__init__(image=Blank.image, left = games.screen.width, y = games.screen.height//2, dx = 0, dy = 2)
        self.odds = 200
        self.time_for_pipe = 0

    def update(self):
        #limiting the vertical movement of the blank sprite
        if self.top < 100 or self.bottom > games.screen.height-100:
            self.dy = -self.dy
        #changing the direction randomly
        elif randrange(self.odds) == 0:
            self.dy = -self.dy
        self.check_for_new_pipe()

    def check_for_new_pipe(self):
        #function to check when to send the pipes
        #waits for 2 seconds since the fps is 50
        if self.time_for_pipe > 0:
            self.time_for_pipe -= 1
        else:
            self.time_for_pipe = 100
            #create the pipe sprites
            #upper pipe
            pipe_inv = PipeI(self.y-40)
            games.screen.add(pipe_inv)

            #lower pipe
            pipe_nor = Pipe(self.y+40)
            games.screen.add(pipe_nor)

#pipe 1
class PipeI(games.Sprite):

    image = games.load_image("images/pipe-green-i.png", transparent = True)
    #constuctor
    def __init__(self, b):
        super().__init__(image = PipeI.image,bottom = b, left = games.screen.width, dy = 0, dx = -2)
        self.incremented = False

    def update(self):
        #destroy if it goes beyond the screen
        if self.right < 0:
            self.destroy()

        #incrementing the score
        if self.right < 200 and not self.incremented:
            Bird.score += 1
            self.incremented = True

#pipe 2
class Pipe(games.Sprite):
    
    image = games.load_image("images/pipe-green.png", transparent = True)
    #constuctor
    def __init__(self, t):
        super().__init__(image = Pipe.image, top = t, left = games.screen.width, dy = 0, dx = -2)

    def update(self):
        #destroy if it goes beyond the screen
        if self.right < 0:
            self.destroy()

def main():
    #setting the background
    back_image = games.load_image("images/back.jpg", transparent=False)
    games.screen.background = back_image

    #creating sprites
    bird = Bird()
    games.screen.add(bird)

    #creating auxiliary sprite
    aux = Blank()
    games.screen.add(aux)
    
    

    #mainloop
    games.screen.mainloop()

main()
