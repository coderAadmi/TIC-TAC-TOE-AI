import random

import pygame as pg
import shelve


BOX_POS = [(10,10,180,180), (210,10,180,180),(410,10,180,180),(10,210,180,180),(210,210,180,180),(410,210,180,180),(10,410,180,180),(210,410,180,180),(410,410,180,180)]

class Game1():
    def __init__(self):
        pg.init()
        self.Clock = pg.time.Clock()
        self.screen = pg.display.set_mode((610,810))
        self.stored_KB = shelve.open("GameBase_UnBeatable.dat")
        self.running = True
        self.players = ['YELLOW',"GREEN"]
        self.player_score = [0,0]
        self.knowledge_base = []
        if "winning" in self.stored_KB.keys():
            self.knowledge_base = self.stored_KB["winning"]
        self.background = pg.image.load("bg.png")
        self.background = pg.transform.scale(self.background, (610, 610))
        self.font_name = pg.font.match_font('Tonto', 5)  # for displaying score
        self.font = pg.font.Font(self.font_name, 30)
        self.meta_screen = pg.transform.scale(pg.image.load("black.jpg"),(610,205))
        self.player_icon = [pg.transform.scale(pg.image.load("yellowCoin.png"),(170,170)),pg.transform.scale(pg.image.load("redCoin.png"),(170,170))]
        self.new_game()
        self.game_loop()

    def drawScore(self):
        """This method displays the user's current score on the game screen."""
        self.meta_screen = pg.transform.scale(pg.image.load("black.jpg"), (610, 205))
        score = f'YELLOW :{self.player_score[0]}  GREEN :{self.player_score[1]}'
        text = self.font.render(score, True, pg.color.Color("WHITE"))  # returns text surface to show current score
        self.meta_screen.blit(text,(300,40)) # renders text surface to the display
        self.screen.blit(self.meta_screen,(0,605))

    def game_loop(self):
        while self.running:
            self.Clock.tick(40)

            if self.isActive:
                self.win_chk()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    self.stored_KB.sync()
                    self.stored_KB.close()
                    print("Quit")

                if self.isActive:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_1:
                            self.fill_box(1)
                        elif event.key == pg.K_2:
                            self.fill_box(2)
                        elif event.key == pg.K_3:
                            self.fill_box(3)
                        elif event.key == pg.K_4:
                            self.fill_box(4)
                        elif event.key == pg.K_5:
                            self.fill_box(5)
                        elif event.key == pg.K_6:
                            self.fill_box(6)
                        elif event.key == pg.K_7:
                            self.fill_box(7)
                        elif event.key == pg.K_8:
                            self.fill_box(8)
                        elif event.key == pg.K_9:
                            self.fill_box(9)

                else:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_n:
                            self.new_game();
                    pass

            pg.display.update()


        pg.quit()

    def make_move(self):
        for pat in self.knowledge_base:
            if self.matches(pat) and pat not in self.pattern:
                self.pattern.append(pat)
                print("Patterns: ",self.pattern)
            elif not(self.matches(pat)) and pat in self.pattern:
                self.pattern.remove(pat)
                print('removing : ',pat)
        #print('Patterns ::',self.pattern)
        if self.pattern:
            min = self.pattern[0]
            for p in self.pattern:
                if len(p) < len(min):
                    min = p
            print("Choose : ", min)
            self.fill_box(int(min[self.yellow_count]))
        else:
            rand = random.randrange(1,10)
            print("choosing random pos : ",rand)
            if self.game_array[rand-1] == 0:
                self.fill_box(rand)
        pass

    def matches(self,pat):
        for i in range(len(self.move_Order)):
            if pat[i] != self.move_Order[i]:
                return False
        return True

    def new_game(self):
        self.screen.blit(self.background, (0, 0))
        self.draw_grid()
        self.drawScore()
        self.isActive = True
        self.running = True
        self.game_array = [0] * 9
        self.move_Order = ""
        self.pattern = []
        self.moves = 0;
        self.yellow_count = 0
        self.isYellowPlaying = True


    def win_chk(self):
        winner = 0
        for i in range(0,3):
            if self.game_array[i] == self.game_array[i+1] and self.game_array[i]==self.game_array[i+2] and self.game_array[i]!=0 and (i==0 or i==3 or i==6):
                print('pattern : i =',i )
                winner = self.game_array[i]
                break
            if self.game_array[i] == self.game_array[i+3] and self.game_array[i] == self.game_array[i+6] and self.game_array[i]!=0 and (i==0 or i==1 or i==2):
                winner = self.game_array[i]
                print('pattern : i =', i)
                break

        if winner ==0 :
            if self.game_array[0] == self.game_array[4] and self.game_array[4] == self.game_array[8]:
                winner = self.game_array[4]
            elif self.game_array[2] == self.game_array[4] and self.game_array[4] == self.game_array[6]:
                winner= self.game_array[4]

        if winner != 0:
            print(self.players[winner - 1], " Won")
            self.player_score[winner-1] += 1
            self.save_moves(winner)
            self.isActive = False
            self.drawScore()

        elif self.moves== 9:
            print("TIE")
            self.isActive = False

    def save_moves(self,winner):
        if winner == 2:
            self.reverse()

        if self.move_Order not in self.knowledge_base:
            self.knowledge_base.append(self.move_Order)
            self.stored_KB["winning"] = self.knowledge_base
            print("Progress saved ", self.move_Order)



    def reverse(self):
        self.move_Order = self.move_Order.replace('Y','T')
        self.move_Order = self.move_Order.replace('G', 'Z')
        self.move_Order = self.move_Order.replace('Z', 'Y')
        self.move_Order = self.move_Order.replace('T', 'G')

    def fill_box(self,box_no):
        if self.game_array[box_no-1] == 0:
            self.moves+=1
            color = None
            if self.isYellowPlaying:
                self.game_array[box_no - 1] = 1;
                self.yellow_count += 4
                self.move_Order += str(box_no)+"Y"
                self.isYellowPlaying = False
                self.screen.blit(self.player_icon[0],(BOX_POS[box_no-1][0],BOX_POS[box_no-1][1]))
                color = pg.color.Color("YELLOW")
            else:
                self.game_array[box_no - 1] = 2;
                self.move_Order += str(box_no)+"G"
                self.isYellowPlaying = True
                self.screen.blit(self.player_icon[1], (BOX_POS[box_no - 1][0], BOX_POS[box_no - 1][1]))
                color = pg.color.Color("GREEN")

            #pg.draw.rect(self.screen, color, BOX_POS[box_no - 1])
        else:
            print("Invalid move")



    def draw_grid(self):
        pg.draw.line(self.screen, pg.color.Color("WHITE"), (0, 200), (600, 200), 5)
        pg.draw.line(self.screen, pg.color.Color("WHITE"), (200, 0), (200, 600), 5)
        pg.draw.line(self.screen, pg.color.Color("WHITE"), (0, 400), (600, 400), 5)
        pg.draw.line(self.screen, pg.color.Color("WHITE"), (400, 0), (400, 600), 5)




Game1()

