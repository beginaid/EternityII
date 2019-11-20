import my_functions
import IPython
import sys

args = sys.argv

n = int(args[1])
color = int(args[2])
my_functions.check_parameters(n, color)

# answer: 正解例
# X: シャッフルしたパズル（真ん中同じ）
# Y: 正解をうめるフィールド
# Remains: 残りのピース
#color_code: 毎回同じ出力をするためのカラーコード

answer = my_functions.generate_puzzle(n, color)
color_code = my_functions.making_color(color)
N = len(answer)

X = my_functions.puzzle_making(answer)
Y = my_functions.solve(X, n)

my_functions.draw_puzzle(Y, "output", color_code, n)
IPython.display.Image("output.png")

score = (my_functions.check(Y)/(N*4)) * 100
print("Accuracy rate:"+str(int(score)) + "%")
