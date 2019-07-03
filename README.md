# python实现简单五子棋

## # 背景

   学校项目实训项目之一

## # 实现思路

  #### 使用python语言进行逻辑操作： ####
  
  1. 主要变量定义：
  
   * 定义并使用循环将棋盘所有坐标放入list变量all_pos中备用；
   * 定义并初始化list变量white_pos和black_pos作为存储黑白子的实时坐标；
   * 定义list变量player_pos作为实时存放棋盘中已有旗子的坐标；
   * 定义状态开关switch、game_state、black_state、white_state；
   * 其他简单变量和局部变量
   
  2. 自定义的主要函数：
   
   * paint()函数，用于初始化棋盘和重置棋盘，重新开始功能的关键函数，无返回值；
   * get_pos(mx,my)函数mx鼠标点x坐标，my鼠标点y坐标，用于获取棋盘中的棋子的合理坐标位置(用于校验鼠标位置为最近的棋盘坐标位置)，返回正确的坐标位置；
   * get_five(testFive),参数testFive是需要判断的棋子(黑子还是白子)，该函数用于判断五子连珠,return Bool值
   * decisionTree(black_point, white_point, player_point, all_point)函数，参数见参数名，此函数为决策树，用于实现NPC下棋的思路；
   * down_chess(black_point, white_point, player_point, all_point)函数，参数见参数名，该函数用于实现npc下棋动作。
  
  3. 已经实现的下棋思想
   
   * get_one_point函数：活1进攻及防守
   * get_live_two_points函数：活2进攻及防守
   * get_live_three_points函数：活3进攻及防守
   * get_live_four_points函数：活4进攻及防守
   * get_punching_four函数：冲4进攻及防守
   * get_sleep_five函数：眠5进攻及防守
   * get_punching_three函数：冲3经过及防守
   * get_sleep_three函数：眠3进攻及防守
  
  4. 待完成的下棋思路
   
   * 眠4
   * 眠冲4
   * 眠冲3？
   * 双活3，双眠4，眠4活3
   * 4冲3
   * 双冲
   * 双眠5
   * 冲4眠五
   
  #### 调用pygame对图像进行操作： ####
  
  1. pygame.display.set_mode：申请屏幕
  2. pygame.draw.rect：绘制矩形
  3. pygame.draw.line：绘制直线
  4. pygame.image.load：加载背景图
  5. init()，初始化pygame
  6. pygame.font.SysFont()、pygame.font.Font()设置字体,pygame.font.Font().render输出字符串在屏幕上
  7. pygame.mouse.get_pressed()获取鼠标点击事件，pygame.mouse.get_pos()获取鼠标点击位置
  8. pygame.draw.circle(),用于输出棋子
  
  #### 当前bug： ####
  
  1. 在左边棋盘落子的时候会出现重复落子情况
  
  ## # 图片
  
  #### 棋盘
   
   ![ipso](http://api.ipso.live/uploads/3fc642ee2db8da08c707433cc4bb684c.png)

  ####　胜利过程
   
   ![](http://api.ipso.live/uploads/21da859b7b1d1c30f4fe8b38f4fad8b0.png)
  
