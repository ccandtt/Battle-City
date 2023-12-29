import sys
import pygame
import time as time_for
import config

# 开始界面显示
from src.basic_class import tank, food, scene, home, bullet


# 开始菜单设置，并返回是玩家1，还是玩家2
def show_start_interface(screen, width, height):
    tfont = pygame.font.Font('./font/simkai.ttf', width // 5)
    cfont = pygame.font.Font('./font/simkai.ttf', width // 20)
    title = tfont.render(u'TANK', True, (255, 0, 0))  # 渲染文本“Tank”
    content1 = cfont.render(u'1 PLAYER（按1）', True, (0, 0, 255))
    content2 = cfont.render(u'2 PLAYER（按2）', True, (0, 0, 255))
    content3 = cfont.render(u'3 BattleMode（按3）', True, (0, 0, 255))  # 新增双人对抗模式
    # 设置title,content1,content2的位置
    trect = title.get_rect()
    trect.midtop = (width / 2, height / 5)
    crect1 = content1.get_rect()
    crect1.midtop = (width / 2, height / 1.8)
    crect2 = content2.get_rect()
    crect2.midtop = (width / 2, height / 1.6)
    crect3 = content3.get_rect()
    crect3.midtop = (width / 2, height / 1.4)
    screen.blit(title, trect)
    screen.blit(content1, crect1)
    screen.blit(content2, crect2)
    screen.blit(content3, crect3)

    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return 1
                if event.key == pygame.K_2:
                    return 2
                if event.key == pygame.K_3:
                    return 3  # 新增vs mode


# 结束界面显示
def show_end_interface(screen, width, height, is_win):
    bg_img = pygame.image.load("./images/others/background.png")  # 修改结束背景图
    screen.blit(bg_img, (0, 0))
    if is_win:
        font = pygame.font.Font('./font/simkai.ttf', width // 10)
        content = font.render(u'恭喜通关！', True, (255, 0, 0))
        rect = content.get_rect()
        rect.midtop = (width / 2, height / 2)
        screen.blit(content, rect)
    else:
        fail_img = pygame.image.load("./images/others/gameover.png")
        rect = fail_img.get_rect()
        rect.midtop = (width / 2, height / 2)
        screen.blit(fail_img, rect)
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


# 关卡切换
def show_switch_stage(screen, width, height, stage):
    bg_img = pygame.image.load("./images/others/background.png")
    screen.blit(bg_img, (0, 0))
    font = pygame.font.Font('./font/simkai.ttf', width // 10)
    content = font.render(u'第%d关' % stage, True, (0, 255, 0))
    rect = content.get_rect()
    rect.midtop = (width / 2, height / 2)
    screen.blit(content, rect)
    pygame.display.update()
    """关卡切换： 1. 用户自动退出，则游戏结束 2. 一秒以后没有输入，自动切入下一关卡"""
    delay_event = pygame.constants.USEREVENT  # 自定义事件
    pygame.time.set_timer(delay_event, 1000)  # 定时器，1000ms =1s 触发
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == delay_event:
                return


def draw_button(surface, button_rectsize, color, music_on):
    """
    绘制出button图形化展示
    color:(a,b,c)
    button_rectsize：(50, 50, 100, 80)，左上角坐标为 (50, 50)，宽度为 100，高度为 80
    """
    bk = pygame.draw.rect(surface, color, button_rectsize)
    action = False
    # 打开音乐是on
    if (music_on):
        # 增加音乐打开
        font = pygame.font.Font(None, 36)
        text = font.render('on', True, (0, 0, 255))  # 渲染文本
        text_rect = text.get_rect(center=bk.center)
        surface.blit(text, text_rect)
    else:
        font = pygame.font.Font(None, 36)
        text = font.render('off', True, (0, 0, 255))  # 渲染文本
        text_rect = text.get_rect(center=bk.center)
        surface.blit(text, text_rect)

    return bk


# bk = pygame.draw.rect(surface, self.bk_color, self.rect)

# 定义菜单栏及其展示
def display_menu():
    pass

# 绘制
# 主函数
def main():
    # 初始化
    pygame.init()
    """以下为一些开关部分"""
    pygame.mixer.init()  # 初始化音效
    music_on = True  # 音乐播放开关
    pause_is = False  # 控制游戏暂停还是继续

    screen_width = 630
    screen_height = 630
    screen = pygame.display.set_mode((screen_width, screen_height))  # 宽和高
    pygame.display.set_caption("TANK")  # 窗口标题
    # 加载图片
    bg_img = pygame.image.load("./images/others/background.png")
    # 加载音效
    add_sound = pygame.mixer.Sound("./audios/add.wav")
    add_sound.set_volume(1)  # 音量设置，范围0-1
    bang_sound = pygame.mixer.Sound("./audios/bang.wav")
    bang_sound.set_volume(1)
    blast_sound = pygame.mixer.Sound("./audios/blast.wav")
    blast_sound.set_volume(1)
    fire_sound = pygame.mixer.Sound("./audios/fire.wav")
    fire_sound.set_volume(1)
    Gunfire_sound = pygame.mixer.Sound("./audios/Gunfire.wav")
    Gunfire_sound.set_volume(1)
    hit_sound = pygame.mixer.Sound("./audios/hit.wav")
    hit_sound.set_volume(1)
    start_sound = pygame.mixer.Sound("./audios/start.wav")
    start_sound.set_volume(1)

    # 开始界面
    game_mode = show_start_interface(screen, screen_width, screen_height)  # 这里为了防止 后续没有改名，但是其实是游戏模式

    # 进入游戏关卡
    screen = pygame.display.set_mode((screen_width + 400, screen_height))  # 增加每个关卡窗口用于文字提示
    # 播放游戏开始的音乐
    start_sound.play()  # 内置播放方法
    # 关卡
    stage = 0
    num_stage = config.stage_num[game_mode - 1]  # 2,2,3对应模式 single,multiple,vs
    # 游戏是否结束
    is_gameover = False
    # 时钟
    clock = pygame.time.Clock()
    # 自定义事件
    # 	-生成敌方坦克事件
    genEnemyEvent = pygame.constants.USEREVENT + 0
    pygame.time.set_timer(genEnemyEvent, 100)
    # 	-敌方坦克静止恢复事件
    recoverEnemyEvent = pygame.constants.USEREVENT + 1
    pygame.time.set_timer(recoverEnemyEvent, 8000)
    # 	-我方坦克无敌恢复事件
    noprotectMytankEvent = pygame.constants.USEREVENT + 2
    pygame.time.set_timer(noprotectMytankEvent, 8000)
    # 主循环
    while not is_gameover:
        # 关卡
        stage += 1
        if stage > num_stage:
            break
        show_switch_stage(screen, screen_width, screen_height, stage)  # 关卡切换提示

        bulletsGroup = pygame.sprite.Group()
        myfoodsGroup = pygame.sprite.Group()
        if game_mode == 1 or game_mode == 2:
            # 该关卡坦克总数量
            enemytanks_total = min(stage * 12, 60)
            # 场上存在的敌方坦克总数量
            enemytanks_now = 0
            # 场上可以存在的敌方坦克总数量
            enemytanks_now_max = min(max(stage * 2, 4), 8)
            # 精灵组
            tanksGroup = pygame.sprite.Group()
            mytanksGroup = pygame.sprite.Group()
            enemytanksGroup = pygame.sprite.Group()
            bulletsGroup = pygame.sprite.Group()
            mybulletsGroup = pygame.sprite.Group()
            enemybulletsGroup = pygame.sprite.Group()
            # 我方坦克群
            tank_player1 = tank.myTank(1)  # 1-player
            tanksGroup.add(tank_player1)
            mytanksGroup.add(tank_player1)
            if game_mode == 2:  # 判断是几人模式
                t_tank = tank.myTank(2)
                tanksGroup.add(t_tank)
                mytanksGroup.add(t_tank)
            # 敌方坦克生成
            for i in range(0, 3):
                if enemytanks_total > 0:
                    enemytank = tank.enemyTank(i)  # 不知道此时传入的i是哪个参数
                    tanksGroup.add(enemytank)
                    enemytanksGroup.add(enemytank)
                    enemytanks_now += 1
                    enemytanks_total -= 1  # 关卡success条件为，击败所有total= 场上+ 被击败 + 未击败
        elif game_mode == 3:
            # 设置最长一局时间
            task_time = config.task_time
            # 设置两方初始生命值
            ct_hp = 5
            t_hp = 5
            # 初始化两方坦克  ct,t
            tanksGroup = pygame.sprite.Group()
            ctGroup = pygame.sprite.Group()  # ct反恐方
            tGroup = pygame.sprite.Group()  # t方
            itemGroup = pygame.sprite.Group()  # 道具组  -- 需要新增根据模式修改道具
            bulletsGroup = pygame.sprite.Group()
            ctbulletsGroup = pygame.sprite.Group()
            tbulletsGroup = pygame.sprite.Group()

            # 生成两方坦克,
            ct_tank = tank.myTank(1)  # 1号玩家为ct
            t_tank = tank.myTank(2)  # 2号玩家为t
            tanksGroup.add(ct_tank, t_tank)
            ctGroup.add(ct_tank)
            tGroup.add(t_tank)

        # 关卡地图
        map_stage = scene.Map(stage)  # 第stage关 --- 需要新增根据mode,匹配stage

        is_switch_tank = True
        player1_moving = False
        player2_moving = False
        # 为了轮胎的动画效果
        times = 0

        # """新增游戏界面右方提示栏"""
        # enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        # content1 = enemytank_num_font.render(f'敌方未歼灭坦克数:{enemytanks_total}', True, (0, 0, 255))
        # screen.blit(content1, (1.05 * screen_width, 0.44 * screen_height))
        #
        # enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        # content1 = enemytank_num_font.render(f'我方坦克生命值:', True, (0, 0, 255))
        # screen.blit(content1, (1.05 * screen_width, 0.55 * screen_height))

        # 需要更新双方的hp
        # for i in range(My_hp):
        # 	hp_img = pygame.image.load(".\images\others\HP.jpg")
        # 	width, height = hp_img.get_size()
        # 	new_hp_img = pygame.transform.scale(hp_img, (width / 20, height / 20))
        # 	rect = new_hp_img.get_rect()
        # 	rect.midtop = ((1.12+0.083*i)* screen_width, 0.64 * screen_height)
        # 	screen.blit(new_hp_img, rect)

        enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        content1 = enemytank_num_font.render(f'关数 :{stage}', True, (0, 0, 255))
        screen.blit(content1, (1.05 * screen_width, 0.11 * screen_height))

        enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        content1 = enemytank_num_font.render(f'倒计时:', True, (0, 0, 255))
        screen.blit(content1, (1.05 * screen_width, 0.22 * screen_height))

        enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        content1 = enemytank_num_font.render(f'0 5:2 0', True, (0, 0, 255))
        screen.blit(content1, (1.25 * screen_width, 0.22 * screen_height))

        enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        content1 = enemytank_num_font.render(f'音乐：开', True, (0, 0, 255))
        screen.blit(content1, (1.05 * screen_width, 0.33 * screen_height))

        enemytank_num_font = pygame.font.Font('./font/simkai.ttf', screen_width // 20)
        content1 = enemytank_num_font.render(f'暂停', True, (0, 0, 255))
        screen.blit(content1, (1.35 * screen_width, 0.33 * screen_height))

        # 绘制切换背景音乐按键
        button_rectsize = (1.2 * screen_width, 0.33 * screen_height, screen_width // 18, screen_width // 18)
        color = (233, 34, 78)
        bk = draw_button(screen, button_rectsize, color, music_on)

        # 大本营
        myhome = home.Home()  # 对于vs mode 相当于是t方的大本营，ct方需要炸毁t方大本营

        # 出场特效
        appearance_img = pygame.image.load("./images/others/appear.png").convert_alpha()
        appearances = [appearance_img.subsurface((0, 0), (48, 48)), appearance_img.subsurface((48, 0), (48, 48)),
                       appearance_img.subsurface((96, 0), (48, 48))]

        start_time = time_for.time()  # 获取当前时间
        # 关卡主循环
        while True:
            if is_gameover is True:  # 可能在任意关卡的任意时间就lose
                break
            # 判断游戏是否结束
            if game_mode == 2 or game_mode == 1:
                if enemytanks_total < 1 and enemytanks_now < 1:
                    is_gameover = False
                    break
            elif game_mode == 3:
                """vs mode的游戏结束说明： 1. 双方血量<0 2. 规定task任务时间，ct方未胜利"""
                now_time = time_for.time()
                time_pass = now_time - start_time
                time_left = task_time - time_pass
                if time_left < 0:
                    break
            for event in pygame.event.get():
                print("event_collect")
                if event.type == pygame.QUIT:
                    pygame.quit()  # 确保所有的资源都被清空
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause_is = not pause_is
                        while pause_is:
                            for event_now in pygame.event.get():
                                print('暂停中')
                                if event_now.type == pygame.KEYDOWN:
                                    if event_now.key == pygame.K_SPACE:
                                        print('恢复中')
                                        pause_is = not pause_is
                                        break
                if game_mode == 1 or game_mode == 2:
                    if event.type == genEnemyEvent:
                        if enemytanks_total > 0:
                            if enemytanks_now < enemytanks_now_max:
                                enemytank = tank.enemyTank()
                                if not pygame.sprite.spritecollide(enemytank, tanksGroup, False,
                                                                   None):  # 当敌方坦克未与坦克组发生碰撞
                                    tanksGroup.add(enemytank)
                                    enemytanksGroup.add(enemytank)
                                    enemytanks_now += 1
                                    enemytanks_total -= 1
                    if event.type == recoverEnemyEvent:
                        for each in enemytanksGroup:
                            each.can_move = True
                    if event.type == noprotectMytankEvent:
                        for _ in mytanksGroup:
                            mytanksGroup.protected = False

                    # 检查用户键盘操作
                    key_pressed = pygame.key.get_pressed()
                    # 玩家一
                    """按下对应的键并且更新状态"""
                    if key_pressed[pygame.K_w]:
                        tanksGroup.remove(tank_player1)
                        tank_player1.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(tank_player1)
                        player1_moving = True
                    elif key_pressed[pygame.K_s]:
                        tanksGroup.remove(tank_player1)
                        tank_player1.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(tank_player1)
                        player1_moving = True
                    elif key_pressed[pygame.K_a]:
                        tanksGroup.remove(tank_player1)
                        tank_player1.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(tank_player1)
                        player1_moving = True
                    elif key_pressed[pygame.K_d]:
                        tanksGroup.remove(tank_player1)
                        tank_player1.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(tank_player1)
                        player1_moving = True
                    elif key_pressed[pygame.K_j]:
                        if not tank_player1.bullet.being:
                            fire_sound.play()
                            tank_player1.shoot()
                    # 玩家二
                    if game_mode == 2:
                        if key_pressed[pygame.K_UP]:
                            tanksGroup.remove(t_tank)
                            t_tank.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                            tanksGroup.add(t_tank)
                            player2_moving = True
                        elif key_pressed[pygame.K_DOWN]:
                            tanksGroup.remove(t_tank)
                            t_tank.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                            tanksGroup.add(t_tank)
                            player2_moving = True
                        elif key_pressed[pygame.K_LEFT]:
                            tanksGroup.remove(t_tank)
                            t_tank.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                            tanksGroup.add(t_tank)
                            player2_moving = True
                        elif key_pressed[pygame.K_RIGHT]:
                            tanksGroup.remove(t_tank)
                            t_tank.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                            tanksGroup.add(t_tank)
                            player2_moving = True
                        elif key_pressed[pygame.K_0]:
                            if not t_tank.bullet.being:
                                fire_sound.play()
                                t_tank.shoot()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    print("点击成功")
                    # 切换背景音乐按键
                    button_rectsize = (
                        1.05 * screen_width, 0.33 * screen_height, screen_width // 18, screen_width // 18)
                    color = (233, 34, 78)
                    # 判断是否触发按钮你

                    # 获取鼠标位置：
                    pos = pygame.mouse.get_pos()
                    # pos = (
                    # list(pos)[0] - button_rectsize[0], list(pos)[1] - button_rectsize[1])  # 求出鼠标与button_surface的相对坐标
                    # if self.effect:
                    # 	pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)
                    # 鼠标划过按钮并点击
                    if bk.collidepoint(pos):
                        print("点击成功")
                        # if self.effect:
                        # 	pygame.draw.rect(surface, (255, 0, 0), self.rect, 3)
                        music_on = (not music_on)
                        # 绘制切换背景音乐按键
                        button_rectsize = (
                            1.2 * screen_width, 0.33 * screen_height, screen_width // 18, screen_width // 18)
                        color = (233, 34, 78)
                        bk = draw_button(screen, button_rectsize, color, music_on)
                    # 		if(music_on):
                    # 			pygame.mixer.music.play()
                    # 		else:
                    # 			pygame.mixer.music.stop()
                # mode 3
                if game_mode == 3:
                    # 检查用户键盘操作
                    key_pressed = pygame.key.get_pressed()
                    # 玩家一
                    """按下对应的键并且更新状态"""
                    if key_pressed[pygame.K_w]:
                        tanksGroup.remove(ct_tank)
                        ct_tank.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(ct_tank)
                        player1_moving = True
                    elif key_pressed[pygame.K_s]:
                        tanksGroup.remove(ct_tank)
                        ct_tank.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(ct_tank)
                        player1_moving = True
                    elif key_pressed[pygame.K_a]:
                        tanksGroup.remove(ct_tank)
                        ct_tank.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(ct_tank)
                        player1_moving = True
                    elif key_pressed[pygame.K_d]:
                        tanksGroup.remove(ct_tank)
                        ct_tank.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(ct_tank)
                        player1_moving = True
                    elif key_pressed[pygame.K_j]:
                        if not ct_tank.bullet.being:
                            fire_sound.play()
                            ct_tank.shoot()
                    # 玩家二 -- t方
                    if key_pressed[pygame.K_UP]:
                        tanksGroup.remove(t_tank)
                        t_tank.move_up(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(t_tank)
                        player2_moving = True
                    elif key_pressed[pygame.K_DOWN]:
                        tanksGroup.remove(t_tank)
                        t_tank.move_down(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(t_tank)
                        player2_moving = True
                    elif key_pressed[pygame.K_LEFT]:
                        tanksGroup.remove(t_tank)
                        t_tank.move_left(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(t_tank)
                        player2_moving = True
                    elif key_pressed[pygame.K_RIGHT]:
                        tanksGroup.remove(t_tank)
                        t_tank.move_right(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                        tanksGroup.add(t_tank)
                        player2_moving = True
                    elif key_pressed[pygame.K_0]:
                        if not t_tank.bullet.being:
                            fire_sound.play()
                            t_tank.shoot()
                    elif key_pressed[pygame.K_RETURN]:
                        if not t_tank.bullet.being:
                            fire_sound.play()
                            t_tank.shoot()

            # 背景
            screen.blit(bg_img, (0, 0))
            # 石头墙
            for each in map_stage.brickGroup:
                screen.blit(each.brick, each.rect)
            # 钢墙
            for each in map_stage.ironGroup:
                screen.blit(each.iron, each.rect)
            # 冰
            for each in map_stage.iceGroup:
                screen.blit(each.ice, each.rect)
            # 河流
            for each in map_stage.riverGroup:
                screen.blit(each.river, each.rect)
            # 树
            for each in map_stage.treeGroup:
                screen.blit(each.tree, each.rect)
            times += 1
            if times == 5:
                times = 0
                is_switch_tank = not is_switch_tank
            # 对于前两种模式
            if game_mode == 1 or game_mode == 2:
                # 我方坦克
                if tank_player1 in mytanksGroup:
                    if is_switch_tank and player1_moving:
                        screen.blit(tank_player1.tank_0, (tank_player1.rect.left, tank_player1.rect.top))
                        player1_moving = False
                    else:
                        screen.blit(tank_player1.tank_1, (tank_player1.rect.left, tank_player1.rect.top))
                    if tank_player1.protected:
                        screen.blit(tank_player1.protected_mask1, (tank_player1.rect.left, tank_player1.rect.top))
                if game_mode == 2:
                    if t_tank in mytanksGroup:
                        if is_switch_tank and player2_moving:
                            screen.blit(t_tank.tank_0, (t_tank.rect.left, t_tank.rect.top))
                            player1_moving = False
                        else:
                            screen.blit(t_tank.tank_1, (t_tank.rect.left, t_tank.rect.top))
                        if t_tank.protected:
                            screen.blit(tank_player1.protected_mask1, (t_tank.rect.left, t_tank.rect.top))
                # 敌方坦克
                for each in enemytanksGroup:
                    # 出生特效
                    if each.born:
                        if each.times > 0:
                            each.times -= 1
                            if each.times <= 10:
                                screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 20:
                                screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 30:
                                screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 40:
                                screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 50:
                                screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 60:
                                screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 70:
                                screen.blit(appearances[2], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 80:
                                screen.blit(appearances[1], (3 + each.x * 12 * 24, 3))
                            elif each.times <= 90:
                                screen.blit(appearances[0], (3 + each.x * 12 * 24, 3))
                        else:
                            each.born = False
                    else:
                        if is_switch_tank:
                            screen.blit(each.tank_0, (each.rect.left, each.rect.top))
                        else:
                            screen.blit(each.tank_1, (each.rect.left, each.rect.top))
                        if each.can_move:
                            tanksGroup.remove(each)
                            each.move(tanksGroup, map_stage.brickGroup, map_stage.ironGroup, myhome)
                            tanksGroup.add(each)
                # 我方子弹
                for tank_player in mytanksGroup:
                    if tank_player.bullet.being:
                        tank_player.bullet.move()
                        screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
                        # 子弹碰撞敌方子弹
                        for each in enemybulletsGroup:
                            if each.being:
                                if pygame.sprite.collide_rect(tank_player.bullet, each):
                                    tank_player.bullet.being = False
                                    each.being = False
                                    enemybulletsGroup.remove(each)
                                    break
                            else:
                                enemybulletsGroup.remove(each)
                        # 子弹碰撞敌方坦克
                        for each in enemytanksGroup:
                            if each.being:
                                if pygame.sprite.collide_rect(tank_player.bullet, each):
                                    if each.is_red == True:
                                        myfood = food.Food()
                                        myfood.generate()
                                        myfoodsGroup.add(myfood)
                                        each.is_red = False
                                    each.blood -= 1
                                    each.color -= 1
                                    if each.blood < 0:
                                        bang_sound.play()
                                        each.being = False
                                        enemytanksGroup.remove(each)
                                        enemytanks_now -= 1
                                        tanksGroup.remove(each)
                                    else:
                                        each.reload()
                                    tank_player.bullet.being = False
                                    break
                            else:
                                enemytanksGroup.remove(each)
                                tanksGroup.remove(each)
                        # 子弹碰撞石头墙
                        if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
                            tank_player.bullet.being = False
                        '''
                        # 等价方案(更科学点)
                        for each in map_stage.brickGroup:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                tank_player.bullet.being = False
                                each.being = False
                                map_stage.brickGroup.remove(each)
                                break
                        '''
                        # 子弹碰钢墙
                        if tank_player.bullet.stronger:
                            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
                                tank_player.bullet.being = False
                        else:
                            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
                                tank_player.bullet.being = False
                        '''
                        # 等价方案(更科学点)
                        for each in map_stage.ironGroup:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                tank_player.bullet.being = False
                                if tank_player.bullet.stronger:
                                    each.being = False
                                    map_stage.ironGroup.remove(each)
                                break
                        '''
                        # 子弹碰大本营
                        if pygame.sprite.collide_rect(tank_player.bullet, myhome):
                            tank_player.bullet.being = False
                            myhome.set_dead()
                            is_gameover = True
                # 敌方子弹
                for each in enemytanksGroup:
                    if each.being:
                        if each.can_move and not each.bullet.being:
                            enemybulletsGroup.remove(each.bullet)
                            each.shoot()
                            enemybulletsGroup.add(each.bullet)
                        if not each.born:
                            if each.bullet.being:
                                each.bullet.move()
                                screen.blit(each.bullet.bullet, each.bullet.rect)
                                # 子弹碰撞我方坦克
                                for tank_player in mytanksGroup:
                                    if pygame.sprite.collide_rect(each.bullet, tank_player):
                                        if not tank_player.protected:
                                            bang_sound.play()
                                            tank_player.life -= 1
                                            if tank_player.life < 0:
                                                mytanksGroup.remove(tank_player)
                                                tanksGroup.remove(tank_player)
                                                if len(mytanksGroup) < 1:
                                                    is_gameover = True
                                            else:
                                                tank_player.reset()
                                        each.bullet.being = False
                                        enemybulletsGroup.remove(each.bullet)
                                        break
                                # 子弹碰撞石头墙
                                if pygame.sprite.spritecollide(each.bullet, map_stage.brickGroup, True, None):
                                    each.bullet.being = False
                                    enemybulletsGroup.remove(each.bullet)
                                '''
                                # 等价方案(更科学点)
                                for one in map_stage.brickGroup:
                                    if pygame.sprite.collide_rect(each.bullet, one):
                                        each.bullet.being = False
                                        one.being = False
                                        enemybulletsGroup.remove(one)
                                        break
                                '''
                                # 子弹碰钢墙
                                if each.bullet.stronger:
                                    if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, True, None):
                                        each.bullet.being = False
                                else:
                                    if pygame.sprite.spritecollide(each.bullet, map_stage.ironGroup, False, None):
                                        each.bullet.being = False
                                '''
                                # 等价方案(更科学点)
                                for one in map_stage.ironGroup:
                                    if pygame.sprite.collide_rect(each.bullet, one):
                                        each.bullet.being = False
                                        if each.bullet.stronger:
                                            one.being = False
                                            map_stage.ironGroup.remove(one)
                                        break
                                '''
                                # 子弹碰大本营
                                if pygame.sprite.collide_rect(each.bullet, myhome):
                                    each.bullet.being = False
                                    myhome.set_dead()
                                    is_gameover = True
                    else:
                        enemytanksGroup.remove(each)
                        tanksGroup.remove(each)

            # 对于vs mode
            elif game_mode == 3:
                # 我方坦克
                if ct_tank in ctGroup:
                    if is_switch_tank and player1_moving:
                        screen.blit(ct_tank.tank_0, (ct_tank.rect.left, ct_tank.rect.top))
                        player1_moving = False
                    else:
                        screen.blit(ct_tank.tank_1, (ct_tank.rect.left, ct_tank.rect.top))
                    if ct_tank.protected:
                        screen.blit(ct_tank.protected_mask1, (ct_tank.rect.left, ct_tank.rect.top))
                if t_tank in tGroup:
                    if is_switch_tank and player2_moving:
                        screen.blit(t_tank.tank_0, (t_tank.rect.left, t_tank.rect.top))
                        player1_moving = False
                    else:
                        screen.blit(t_tank.tank_1, (t_tank.rect.left, t_tank.rect.top))
                    if t_tank.protected:
                        screen.blit(t_tank.protected_mask1, (t_tank.rect.left, t_tank.rect.top))
                # 我方子弹ct方子弹碰撞t方子弹
                for tank_player in ctGroup:
                    if tank_player.bullet.being:
                        tank_player.bullet.move()
                        screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
                        # 子弹碰撞敌方子弹
                        for each in tGroup:
                            if each.being:
                                if pygame.sprite.collide_rect(tank_player.bullet, each):
                                    tank_player.bullet.being = False
                                    each.being = False
                                    tbulletsGroup.remove(each)
                                    break
                            else:
                                tbulletsGroup.remove(each)
                        # ct方子弹碰撞敌t方
                        if t_tank.being:
                            if pygame.sprite.collide_rect(tank_player.bullet, t_tank):
                                if t_tank.is_red == True:
                                    myfood = food.Food()
                                    myfood.generate()
                                    myfoodsGroup.add(myfood)
                                    t_tank.is_red = False
                                t_tank.blood -= 1
                                t_tank.color -= 1
                                if t_tank.blood < 0:
                                    bang_sound.play()
                                    t_tank.being = False
                                    t_tank.remove(t_tank)
                                    enemytanks_now -= 1
                                    tanksGroup.remove(t_tank)
                                else:
                                    t_tank.reload()
                                tank_player.bullet.being = False
                                break
                        else:
                            t_tank.remove(t_tank)
                            tanksGroup.remove(t_tank)


                        # 子弹碰撞石头墙
                        if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
                            tank_player.bullet.being = False
                        '''
                        # 等价方案(更科学点)
                        for each in map_stage.brickGroup:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                tank_player.bullet.being = False
                                each.being = False
                                map_stage.brickGroup.remove(each)
                                break
                        '''
                        # 子弹碰钢墙
                        if tank_player.bullet.stronger:
                            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
                                tank_player.bullet.being = False
                        else:
                            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
                                tank_player.bullet.being = False
                        '''
                        # 等价方案(更科学点)
                        for each in map_stage.ironGroup:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                tank_player.bullet.being = False
                                if tank_player.bullet.stronger:
                                    each.being = False
                                    map_stage.ironGroup.remove(each)
                                break
                        '''
                        # 子弹碰大本营
                        if pygame.sprite.collide_rect(tank_player.bullet, myhome):
                            tank_player.bullet.being = False
                            myhome.set_dead()
                            is_gameover = True

                # 我方子弹ct方子弹碰撞t方子弹
                for tank_player in tGroup:
                    if tank_player.bullet.being:
                        tank_player.bullet.move()
                        screen.blit(tank_player.bullet.bullet, tank_player.bullet.rect)
                        # 子弹碰撞敌方子弹
                        for each in ctGroup:
                            if each.being:
                                if pygame.sprite.collide_rect(tank_player.bullet, each):
                                    tank_player.bullet.being = False
                                    each.being = False
                                    tbulletsGroup.remove(each)
                                    break
                            else:
                                tbulletsGroup.remove(each)
                        # ct方子弹碰撞敌t方
                        if t_tank.being:
                            if pygame.sprite.collide_rect(tank_player.bullet, t_tank):
                                if t_tank.is_red == True:
                                    myfood = food.Food()
                                    myfood.generate()
                                    itemGroup.add(myfood)
                                    t_tank.is_red = False
                                t_tank.blood -= 1
                                t_tank.color -= 1
                                if t_tank.blood < 0:
                                    bang_sound.play()
                                    t_tank.being = False
                                    t_tank.remove(t_tank)
                                    enemytanks_now -= 1
                                    tanksGroup.remove(t_tank)
                                else:
                                    t_tank.reload()
                                tank_player.bullet.being = False
                                break
                        else:
                            t_tank.remove(t_tank)
                            tanksGroup.remove(t_tank)
                        # 子弹碰撞石头墙
                        if pygame.sprite.spritecollide(tank_player.bullet, map_stage.brickGroup, True, None):
                            tank_player.bullet.being = False
                        '''
                        # 等价方案(更科学点)
                        for each in map_stage.brickGroup:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                tank_player.bullet.being = False
                                each.being = False
                                map_stage.brickGroup.remove(each)
                                break
                        '''
                        # 子弹碰钢墙
                        if tank_player.bullet.stronger:
                            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, True, None):
                                tank_player.bullet.being = False
                        else:
                            if pygame.sprite.spritecollide(tank_player.bullet, map_stage.ironGroup, False, None):
                                tank_player.bullet.being = False
                        '''
                        # 等价方案(更科学点)
                        for each in map_stage.ironGroup:
                            if pygame.sprite.collide_rect(tank_player.bullet, each):
                                tank_player.bullet.being = False
                                if tank_player.bullet.stronger:
                                    each.being = False
                                    map_stage.ironGroup.remove(each)
                                break
                        '''
                        # 子弹碰大本营
                        if pygame.sprite.collide_rect(tank_player.bullet, myhome):
                            tank_player.bullet.being = False
                            myhome.set_dead()
                            is_gameover = True

            # 家
            screen.blit(myhome.home, myhome.rect)
            # 食物
            for myfood in myfoodsGroup:
                if myfood.being and myfood.time > 0:
                    screen.blit(myfood.food, myfood.rect)
                    myfood.time -= 1
                    for tank_player in mytanksGroup:
                        if pygame.sprite.collide_rect(tank_player, myfood):
                            # 消灭当前所有敌人
                            if myfood.kind == 0:
                                for _ in enemytanksGroup:
                                    bang_sound.play()
                                enemytanksGroup = pygame.sprite.Group()
                                enemytanks_total -= enemytanks_now
                                enemytanks_now = 0
                            # 敌人静止
                            if myfood.kind == 1:
                                for each in enemytanksGroup:
                                    each.can_move = False
                            # 子弹增强
                            if myfood.kind == 2:
                                add_sound.play()
                                tank_player.bullet.stronger = True
                            # 使得大本营的墙变为钢板
                            if myfood.kind == 3:
                                map_stage.protect_home()
                            # 坦克获得一段时间的保护罩
                            if myfood.kind == 4:
                                add_sound.play()
                                for tank_player in mytanksGroup:
                                    tank_player.protected = True
                            # 坦克升级
                            if myfood.kind == 5:
                                add_sound.play()
                                tank_player.up_level()
                            # 坦克生命+1
                            if myfood.kind == 6:
                                add_sound.play()
                                tank_player.life += 1
                            myfood.being = False
                            myfoodsGroup.remove(myfood)
                            break
                else:
                    myfood.being = False
                    myfoodsGroup.remove(myfood)
            pygame.display.flip()
            clock.tick(60)
        if not is_gameover:
            show_end_interface(screen, 630, 630, True)
        else:
            show_end_interface(screen, 630, 630, False)


if __name__ == '__main__':
    main()
