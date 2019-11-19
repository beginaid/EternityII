# -*- coding: utf-8 -*-
import random
from PIL import Image, ImageDraw
import IPython
import sys

def generate_puzzle(n, color):
  N = n**2
  field = [[0,0,0,0] for i in range(N)]
  palette = [i+1 for i in range(color)]
  palette = random.sample(palette, len(palette))

  count = 0
  for i in range(n-1):
    for j in range(n):
      field[n*i+j][3] = palette[count]
      field[n*i+j+n][1] = palette[count]
      if count == color-1:
        count = 0
        palette = [i+1 for i in range(color)]
        palette = random.sample(palette, len(palette))
      else:
        count += 1


  for i in range(n):
    for j in range(n-1):
      field[n*i+j][2] = palette[count]
      field[n*i+j+1][0] = palette[count]
      if count == color-1:
        count = 0
        palette = [i+1 for i in range(color)]
        palette = random.sample(palette, len(palette))
      else:
        count += 1
  return field

def check_parameters(n, color):
  N = n**2
  inner = N*4 - (n*4)
  if inner<color*2:
    print("colorを別の値にしてください！ \nとりあえず"+str(inner//2)+"色で塗り分けます！")
  else:
    print("OKです！")

def fill_corner(X, Y, Remains):
  N = len(X)
  n = int(pow(N, 0.5))

  X_index = list(range(N))
  corner_0_index = [i for i in X_index if (X[i][0]==0 and X[i][1]==0)]
  corner_0 = X[corner_0_index[0]]

  corner_1_index = [i for i in X_index if (X[i][1]==0 and X[i][2]==0)]
  corner_1 = X[corner_1_index[0]]

  corner_2_index = [i for i in X_index if (X[i][0]==0 and X[i][3]==0)]
  corner_2 = X[corner_2_index[0]]

  corner_3_index = [i for i in X_index if (X[i][2]==0 and X[i][3]==0)]
  corner_3 = X[corner_3_index[0]]

  corner = [corner_0, corner_1, corner_2, corner_3]

  for i in range(4):
    Remains.remove(corner[i])

  Y[0] = corner_0
  Y[n-1] = corner_1
  Y[N-n] = corner_2
  Y[N-1] = corner_3

  return Y, Remains

# インデックスからピースの場所を出力する関数
def judge(n, index):
  N = n**2
  corner0 = [0]
  corner1 = [n-1]
  corner2 = [N-n]
  corner3 = [N-1]
  left = [n + i*n for i in range(n-2)]
  above = [1 + i for i in range(n-2)]
  right = [2*n-1 + i*n for i in range(n-2)]
  below = [N-n+1 + i for i in range(n-2)]
  lookup = [corner0,corner1,corner2,corner3,left, above, right, below]
  element = [flatten for inner in lookup for flatten in inner]
  if index < 0 or index > N:
    return None
  elif index in element:
    for i in range(len(lookup)):
      if index in lookup[i]:
        return i
  else:
    return 8
# 0-3:corner, 4:left, 5:above, 6:right, 7:below, 8:center

# 周りにinしているピース数を返す関数
def get_around_in_nm(n, index, estimate):
  if judge(n, index)==0:
    count = 2
    if type(estimate[index+1]) == list or estimate[index+1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+n]) == list or estimate[index+n]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==1:
    count = 2
    if type(estimate[index-1]) == list or estimate[index-1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+n]) == list or estimate[index+n]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==2:
    count = 2
    if type(estimate[index-n]) == list or estimate[index-n]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+1]) == list or estimate[index+1]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==3:
    count = 2
    if type(estimate[index-n]) == list or estimate[index-n]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index-1]) == list or estimate[index-1]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==4:
    count = 1
    if type(estimate[index-n]) == list or estimate[index-n]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+1]) == list or estimate[index+1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+n]) == list or estimate[index+n]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==5:
    count = 1
    if type(estimate[index-1]) == list or estimate[index-1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+1]) == list or estimate[index+1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+n]) == list or estimate[index+n]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==6:
    count = 1
    if type(estimate[index-n]) == list or estimate[index-n]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index-1]) == list or estimate[index-1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+n]) == list or estimate[index+n]==[-1,-1,-1,-1]:
        count += 1
    return count

  elif judge(n, index)==7:
    count = 1
    if type(estimate[index-n]) == list or estimate[index-n]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index-1]) == list or estimate[index-1]==[-1,-1,-1,-1]:
        count += 1
    if type(estimate[index+1]) == list or estimate[index+1]==[-1,-1,-1,-1]:
        count += 1
    return count

  try:
    if judge(n, index)==8:
      count = 0
      if type(estimate[index-n]) == list or estimate[index-n]==[-1,-1,-1,-1]:
          count += 1
      if type(estimate[index-1]) == list or estimate[index-1]==[-1,-1,-1,-1]:
          count += 1
      if type(estimate[index+1]) == list or estimate[index+1]==[-1,-1,-1,-1]:
          count += 1
      if type(estimate[index+n]) == list or estimate[index+n]==[-1,-1,-1,-1]:
          count += 1
      return count
  except:
    print(len(estimate))
    print(index)
    print(n)


# 周りで一致している模様を返す関数
def get_around_pattern_nm(n, index, piece, estimate):
  if judge(n, index) == 4:
    if type(estimate[index - n]) == int:
      estimate[index - n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + 1]) == int:
      estimate[index + 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + n]) == int:
      estimate[index + n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    num = set(enumerate(piece)) & set(enumerate([0,estimate[index - n][3], estimate[index + 1][0],estimate[index+n][1]]))
  elif judge(n, index) == 5:
    if type(estimate[index - 1]) == int:
      estimate[index - 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + 1]) == int:
      estimate[index + 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + n]) == int:
      estimate[index + n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    try:
      num = set(enumerate(piece)) & set(enumerate([estimate[index - 1][2], 0, estimate[index + 1][0],estimate[index+n][1]]))
    except:
      print(piece)
      print(estimate)
  elif judge(n, index) == 6:
    if type(estimate[index - n]) == int:
      estimate[index - n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index - 1]) == int:
      estimate[index - 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + n]) == int:
      estimate[index + n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    num = set(enumerate(piece)) & set(enumerate([estimate[index - 1][2], estimate[index - n][3], 0, estimate[index+n][1]]))
  elif judge(n, index) == 7:
    if type(estimate[index - n]) == int:
      estimate[index - n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index - 1]) == int:
      estimate[index - 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + 1]) == int:
      estimate[index + 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    num = set(enumerate(piece)) & set(enumerate([estimate[index - 1][2], estimate[index - n][3], estimate[index + 1][0], 0]))
  elif judge(n, index) == 8:
    if type(estimate[index - n]) == int:
      estimate[index - n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index - 1]) == int:
      estimate[index - 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + 1]) == int:
      estimate[index + 1] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    if type(estimate[index + n]) == int:
      estimate[index + n] = [-1,-1,-1,-1] #適当な負の数を入れることでsetで数え上げないようにしている
    num = set(enumerate(piece)) & set(enumerate([estimate[index - 1][2], estimate[index - n][3], estimate[index + n][0], estimate[index + n][1]]))
  return num

def select_piece(n, index, estimate, remains):
  number = [0 for i in range(len(remains))]
  for i in range(len(remains)):
    if get_around_in_nm(n, index, estimate) == get_around_pattern_nm(n, index, remains[i], estimate):
      return remains.pop(i)
    else:
      number[i] = len(get_around_pattern_nm(n, index, remains[i], estimate))
  print(number)
  max_index = number.index(max(number))
  if (judge(n,index)==8) and (0 in remains[max_index]):
    while 0 in remains[max_index]:
      number.pop(max_index)
      max_index = number.index(max(number))
      if len(number)==1:
        break
  if (judge(n, index)==(4 or 5 or 6 or 7) and (0 not in remains[max_index])) == True:
    while 0 not in remains[max_index]:
      number.pop(max_index)
      max_index = number.index(max(number))
      if len(number)==1:
        break
  return remains.pop(max_index)

def calc_remain_index(Y):
  index = []
  for i in range(len(Y)-1):
    if type(Y[i])==int or Y[i]==[-1,-1,-1,-1] :
      index.append(i)
  return index

def draw_puzzle(Y, name, color_code, n):
  N = n**2
  n = int(pow(N, 0.5))

  im = Image.new('RGB', (n*100,n*100), color_code[0])
  draw = ImageDraw.Draw(im)

  a = 100
  count = 0

  for i in range(n):
    for j in range(n):
      draw.polygon((0+j*a,0+i*a,a//2+j*a,a//2+i*a,0+j*a,a+i*a), fill=color_code[Y[count][0]], outline=(0,0,0))
      draw.polygon((0+j*a,0+i*a,a//2+j*a,a//2+i*a,a+j*a,0+i*a), fill=color_code[Y[count][1]], outline=(0,0,0))
      draw.polygon((a+j*a,0+i*a,a//2+j*a,a//2+i*a,a+j*a,a+i*a), fill=color_code[Y[count][2]], outline=(0,0,0))
      draw.polygon((0+j*a,a+i*a,a//2+j*a,a//2+i*a,a+j*a,a+i*a), fill=color_code[Y[count][3]], outline=(0,0,0))
      count +=1

  im.save(name+".png")
  IPython.display.Image(name+".png")


def shuffle(answer):
  X = random.sample(answer, len(answer))
  return X

def puzzle_making(answer):
  N = len(answer)
  X = list(answer)
  center_index = (N-1)//2
  center = answer[center_index]
  X.pop(center_index)
  X = shuffle(X)
  X.insert(center_index, center)
  return X

def data_making(X, n):
  N = n**2
  center_index = (N-1)//2
  center = X[center_index]
  Y = list(range(N))
  Y[center_index] = center

  Remains = list(X)
  Remains.remove(center)

  return Y, Remains

def check(Y):
  N = len(Y)
  n = int(pow(N, 0.5))
  count = 0
  # vertex
  if Y[0][0]==0:
    count +=1
  if Y[0][1]==0:
    count +=1
  if Y[0][2]==Y[1][0]:
    count +=1
  if Y[0][3]==Y[n][1]:
    count +=1

  if Y[n-1][0]==Y[n-2][2]:
    count +=1
  if Y[n-1][1]==0:
    count +=1
  if Y[n-1][2]==0:
    count +=1
  if Y[n-1][3]==Y[n-1+n][1]:
    count +=1


  if Y[N-n][0]==0:
    count +=1
  if Y[N-n][1]==Y[N-n-n][3]:
    count +=1
  if Y[N-n][2]==Y[N-n+1][0]:
    count +=1
  if Y[N-n][3]==0:
    count +=1


  if Y[N-1][0]==Y[N-2][2]:
    count +=1
  if Y[N-1][1]==Y[N-1-n][3]:
    count +=1
  if Y[N-1][2]==0:
    count +=1
  if Y[N-1][3]==0:
    count +=1

  # edge
  for i in range(n-2):
    if Y[i+1][0]==Y[i][2]:
      count +=1
    if Y[i+1][1]==0:
      count +=1
    if Y[i+1][2]==Y[i+2][0]:
      count +=1
    if Y[i+1][3]==Y[i+1+n][1]:
      count +=1

    if Y[n+i*n][0]==0:
      count +=1
    if Y[n+i*n][1]==Y[i*n][3]:
      count +=1
    if Y[n+i*n][2]==Y[n+i*n+1][0]:
      count +=1
    if Y[n+i*n][3]==Y[n+i*n+n][1]:
      count +=1

    if Y[n+n-1 + n*i][0]==Y[n+n-1 + n*i -1][2]:
      count +=1
    if Y[n+n-1 + n*i][1]==Y[n-1 + n*i][3]:
      count +=1
    if Y[n+n-1 + n*i][2]==0:
      count +=1
    if Y[n+n-1 + n*i][3]==Y[n+n-1 + n*i +n][1]:
      count +=1

    if Y[N-n++1 + i][0]==Y[N-n + i][2]:
      count +=1
    if Y[N-n+1 + i][1]==Y[N-n+1 + i -n][3]:
      count +=1
    if Y[N-n+1 + i][2]==Y[N-n+1 + i+1][0]:
      count +=1
    if Y[N-n+1 + i][3]==0:
      count +=1

  # inner
  for i in range(n-2):
    for j in range(n-2):
      if Y[i+(j+1)*n+1][0]==Y[i+(j+1)*n][2]:
        count += 1
      if Y[i+(j+1)*n+1][1]==Y[i+(j+1)*n+1-n][3]:
        count += 1
      if Y[i+(j+1)*n+1][2]==Y[i+(j+1)*n+1+1][0]:
        count += 1
      if Y[i+(j+1)*n+1][3]==Y[i+(j+1)*n+1+n][1]:
        count += 1
  return count

def index_sorting(n,estimate, remains):
  score = []
  piece = []
  for index in calc_remain_index(estimate):
    number = [0 for i in range(len(remains))]
    for i in range(len(remains)):
      number[i] = len(get_around_pattern_nm(n, index, remains[i], estimate))
    max_index = number.index(max(number))
    if (judge(n,index)==8) and (0 in remains[max_index]):
      while 0 in remains[max_index]:
        number.pop(max_index)
        max_index = number.index(max(number))
        if len(number)==1:
          break
    if (judge(n, index)==(4 or 5 or 6 or 7) and (0 not in remains[max_index])) == True:
      while 0 not in remains[max_index]:
        number.pop(max_index)
        max_index = number.index(max(number))
        if len(number)==1:
          break
    score.append(number[max_index])
    piece.append(remains[max_index])
  return score, piece

def solve(X, n):
  Y, Remains = data_making(X, n)
  Y, Remains = fill_corner(X, Y, Remains)
  for i in range(len(Remains)):
    remain_index = calc_remain_index(Y)
    score,piece = index_sorting(n,Y,Remains)
    max_index = score.index(max(score))
    index = remain_index[max_index]
    max_piece = piece[max_index]
    Y[index] = max_piece
    print("\r"+str(int(round((i/len(Remains)),2)*100))+"%完了", end="")
  return Y

def generate_random_color():
  r = lambda: random.randint(0,255)
  code = '#%02X%02X%02X' % (r(),r(),r())
  return code

def making_color(color):
  color_code = [generate_random_color() for i in range(color+1)]
  color_code[0] = "#000000"
  color_code[-1] = "#ffffff"
  return color_code
