import csv
import os

CONVERSATION_BREAK = "=============================="


class AnswerError(Exception):
    pass


def ask_name(robot_name):
    """
    名前を尋ねる。アイスブレイクは大事。
    :param robot_name: roboter()から渡しています。
    :return: ユーザーの名前を返します。
    """
    print(CONVERSATION_BREAK)
    print("{robot_name}: こんにちは！私は{robot_name}です。あなたの名前は何ですか？".format(robot_name=robot_name))
    print(CONVERSATION_BREAK)
    user_name = input()
    return user_name


def recommend_restaurants(restaurant_name, robot_name):
    """
    レストランをオススメし続けるメンヘラの根源たる関数
    :param restaurant_name: roboter()から渡しています。
    :param robot_name: roboter()から渡しています。
    :return: yes or no を返す
    """
    print(CONVERSATION_BREAK)
    print("{robot_name}: 私のオススメのレストランは{restaurant_name}です。\n"
          "このレストランは好きですか？[Yes/No]".format(robot_name=robot_name, restaurant_name=restaurant_name))
    print(CONVERSATION_BREAK)
    answer = input()
    if answer == 'yes' or answer == 'YES' or answer == 'y':
        answer = 'Yes'
    elif answer == 'no' or answer == 'NO' or answer == 'n':
        answer = 'No'
    else:
        raise AnswerError('answer is not [Yes/No].')
    return answer


def ask_restaurant(user_name, robot_name):
    """
    好きなレストランを聞く
    :param user_name: roboter()から渡しています。
    :param robot_name: roboter()から渡しています。
    :return:　好きなレストランの回答を返す。
    """
    print(CONVERSATION_BREAK)
    print("{robot_name}: {user_name}さん。どこのレストランが好きですか？".format(robot_name=robot_name, user_name=user_name))
    print(CONVERSATION_BREAK)
    restaurant_name = input()
    restaurant_name = restaurant_name.title()
    return restaurant_name


def have_a_good_day(user_name, robot_name):
    """
    お別れの挨拶
    :param user_name: roboter()から渡しています。
    :param robot_name: roboter()から渡しています。
    """
    print(CONVERSATION_BREAK)
    print("{robot_name}: {user_name}さん。ありがとうございました。\n"
          "良い一日を！さようなら。".format(robot_name=robot_name, user_name=user_name))


def search_ranking_file():
    """
    ranking.csvファイルの存在の有無を確認し、1位のレストランをリストで返す
    :return: 1位のレストランのリスト。ファイルが存在しない、もしくはファイル内の情報が空の場合は空のリストを返す。
    """
    if os.path.exists('ranking.csv'):
        recommend_rankings = {}
        max_count = 0
        with open('ranking.csv', 'r') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                recommend_rankings[row['NAME']] = int(row['COUNT'])
                max_count = max(max_count, int(row['COUNT']))

            # ranking.csvファイルが空の場合は、top_restaurants = []となる。
            top_restaurants = [k for k, v in recommend_rankings.items() if v == max_count]
        return top_restaurants, recommend_rankings
    else:
        return []


def update_ranking_file(restaurant, recommend_rankings):
    """
    ranking.csvファイルが存在しない場合は、header情報を記述したranking.csvを作成。
    渡されたレストラン情報がranking.csvファイルに存在するかを確認し、存在する場合はcountを増やし、ない場合はCOUNT = 1で行を追加
    """
    if not os.path.exists('ranking.csv'):
        with open('ranking.csv', 'w', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['NAME', 'COUNT'])

    if restaurant in recommend_rankings:
        recommend_rankings[restaurant] += 1
        with open('ranking.csv', 'w', newline="") as csv_file:
            fields = ['NAME', 'COUNT']
            writer = csv.DictWriter(csv_file, fieldnames = fields)
            writer.writeheader()
            for k, v in recommend_rankings.items():
                writer.writerow({'NAME': k, 'COUNT': v})

    else:
        with open('ranking.csv', 'a', newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow([restaurant, 1])


def roboter(robot_name="Roboko"):
    """
    ロボコが、過去のユーザーの好みのレストラン回答結果に合わせてレストランをオススメしてくれるシステム。
    これまでに一番多くのユーザーから好きと回答されたレストランの候補がなくなるか、オススメレストランに好きと言われるまで愚直にオススメする。
    最後に、ユーザーに好きなレストランを尋ね、回答してもらう。
    ややメンヘラ気味のレストランリコメンドbot
    :param robot_name: 指定することで、ロボコ以外の名前でも利用可能です。
    """
    user_name = ask_name(robot_name)
    top_restaurants, recommend_rankings = search_ranking_file()
    if top_restaurants:
        for restaurant in top_restaurants:
            answer = recommend_restaurants(restaurant, robot_name)
            if answer == 'Yes':
                break

    restaurant = ask_restaurant(user_name, robot_name)
    update_ranking_file(restaurant, recommend_rankings)
    have_a_good_day(user_name, robot_name)
