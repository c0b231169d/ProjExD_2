import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1600, 900
DELTA = {  # 移動量辞書
    pg.K_UP: (0, -5), 
    pg.K_DOWN: (0, 5), 
    pg.K_LEFT: (-5, 0), 
    pg.K_RIGHT: (5, 0)
}
KKMUKI = {  # 移動量の合計値辞書
    (5, 0):"kk_img", (5, 5):" kk_img2", (0, 5):" kk_img3", (-5, 5):" kk_img4", 
    (-5, 0):" kk_img5", (-5, -5):" kk_img6", (0, -5):" kk_img7", (5, -5):" kk_img8"
}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(obj_rct:pg.Rect) -> tuple[bool, bool]:
    """
    こうかとんRectまたは爆弾Rectの画面内外判定用の関数
    引数：こうかとんRect または　爆弾Rect
    戻り値：横方向判定結果　縦方向判定結果　画面内ならTrue、画面外ならFalse
    """
    yoko, tate = True, True
    if obj_rct.left < 0 or WIDTH < obj_rct.right:
        yoko = False
    if obj_rct.top < 0 or HEIGHT < obj_rct.bottom:
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 2.0)
    kk_img2 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -45, 2.0)
    kk_img3 = pg.transform.rotozoom(pg.image.load("fig/3.png"), -90, 2.0)
    kk_img7 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 90, 2.0)
    kk_img8 = pg.transform.rotozoom(pg.image.load("fig/3.png"), 45, 2.0)
    kk_img4 = pg.transform.flip(kk_img2, True, False)
    kk_img5 = pg.transform.flip(kk_img, True, False)
    kk_img6 = pg.transform.flip(kk_img8, True, False)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400
    bakudan_img = pg.Surface((20, 20))
    pg.draw.circle(bakudan_img, (255, 0, 0), (10, 10), 10)
    bakudan_img.set_colorkey((0, 0, 0))
    bakudan_rct = bakudan_img.get_rect()
    bakudan_rct.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5  #横移動速度、縦移動速度
    blackout_img = pg.Surface((WIDTH, HEIGHT))
    pg.draw.rect(blackout_img, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    blackout_img.set_alpha(127)
    fonto = pg.font.Font(None, 80)
    go_txt = fonto.render("Game Over", True, (255, 255, 255))
    kkcry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 2.0)
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bakudan_rct):  # こうかとんと爆弾がぶつかったら
            screen.blit(blackout_img, [0, 0])
            screen.blit(go_txt, [620, HEIGHT/2])
            screen.blit(kkcry_img, [500, HEIGHT/2])
            screen.blit(kkcry_img, [960, HEIGHT/2])
            pg.display.update()
            pg.time.delay(5000)  # 5秒間ゲームオーバー画面を表示し続ける
            return

        screen.blit(bg_img, [0, 0]) 
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)  # こうかとんの画像を表示
        bakudan_rct.move_ip(vx, vy)
        screen.blit(bakudan_img, bakudan_rct)
        yoko, tate = check_bound(bakudan_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
