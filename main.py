# %%
import os
import random
from typing import Dict, List, Tuple
import numpy as np
from decimal import Decimal, ROUND_HALF_UP
import pandas as pd


# --------オッズ変数----------
Pmax = 20
# Smax = 10
Smin = 2.0

# ---------投票数------------
total = 80

# ランキング表示するチーム数
# odds_team_num = 5

# --------1票以上を獲得するチーム数-----------
max_rank_team = 10
min_rank_team = 6

# ---------順位が重複した際のオッズ倍率の変更-----------
duplicate_changes = 2

# ---------ランダム投票試行数------------
try_num = 1

# ----------保存ファイルpath-------------
savefile = '/workspaces/natugaku/odds.xlsx'


def make_random_rank() -> Tuple[List[int], List[int]]:
    random_team_num = random.randrange(min_rank_team, max_rank_team)
    float_list = np.array([random.random() for i in range(random_team_num)])
    votes_float_list = float_list*(total/np.sum(float_list))
    votes_int_list = np.array([Decimal(str(vote)).quantize(Decimal('0'), rounding=ROUND_HALF_UP) for vote in votes_float_list], dtype=int)
    sorted_votes_list = np.sort(votes_int_list)[::-1]
    votes_dif_list = np.array([sorted_votes_list[i]-sorted_votes_list[i+1] for i in range(random_team_num-1)])
    not_duplicate_list = np.append(sorted_votes_list[:1],sorted_votes_list[1:][votes_dif_list!=0])

    return sorted_votes_list, not_duplicate_list


def check_standard_index(votes_list) -> int:
    min = 100
    for i in range(1,len(votes_list)-1):
        num = votes_list[i-1]-votes_list[i+1]
        if num < min:
            min = num
            s_ind = i
    return s_ind

def cal_P0(votes_list) -> float:
    s_ind = check_standard_index(votes_list)
    # print(f"starndard_index:{s_ind}")
    dif_1 = votes_list[s_ind-1]-votes_list[s_ind]
    dif_2 = votes_list[s_ind]-votes_list[s_ind+1]
    p0 = (Pmax*dif_1*dif_2)**0.5
    return p0

def make_p_list(votes_list) -> Tuple[Dict[int, Decimal], Dict[int, Decimal]]:
    p0 = cal_P0(votes_list)
    p_dict: Dict[int, Decimal] = {}
    s1_dict: Dict[int, Decimal] = {}
    s2_dict: Dict[int, Decimal] = {}
    for i in range(len(votes_list)):
        if i == 0:
            p = p0/(votes_list[i]-votes_list[i+1])
        elif i == len(votes_list)-1:
            p = p0/(votes_list[i-1]-votes_list[i])
        else:
            p = (p0/(votes_list[i-1]-votes_list[i]))*(p0/(votes_list[i]-votes_list[i+1]))
        p_dict[i+1] = p
    Pmin = sorted(p_dict.values())[0]
    s1_rate = Smin / Pmin
    for i in range(len(votes_list)):
        s1_dict[i+1] = Decimal(str(s1_rate * p_dict[i+1])).quantize(Decimal('0.0'),rounding=ROUND_HALF_UP)
        s2 = ((p_dict[i+1] - Pmin) * (Pmax - Smin) / (Pmax - Pmin)) + Smin
        s2_dict[i+1] = Decimal(str(s2)).quantize(Decimal('0.0'),rounding=ROUND_HALF_UP)
    return s1_dict, s2_dict

def make_odds_pd() -> pd.DataFrame:
    sorted_votes_list, not_duplicate_list = np.array([1000, 700, 300, 200, 0]), np.array([1000, 700, 300, 200, 0])
    s1, s2 = make_p_list(not_duplicate_list)
    rank_ind = 1
    data = np.empty((0,4))
    columns = ["順位", "得票数", "オッズ1", "オッズ2"]
    for i in range(len(sorted_votes_list)-1):
        # print(rank_ind)
        odds1 = s1[rank_ind]
        odds2 = s2[rank_ind]
        rank_str = f"{i+1}位 "
        if sorted_votes_list[i] == sorted_votes_list[i+1]:
            odds1 = f"{s1[rank_ind] * Decimal(duplicate_changes)}({s1[rank_ind]})"
            odds2 = f"{s2[rank_ind] * Decimal(duplicate_changes)}({s2[rank_ind]})"
                
        if i > 0:
            if sorted_votes_list[i-1] == sorted_votes_list[i]:
                odds1 = f"{s1[rank_ind] * Decimal(duplicate_changes)}({s1[rank_ind]})"
                odds2 = f"{s2[rank_ind] * Decimal(duplicate_changes)}({s2[rank_ind]})"
                rank_str = " 　 "
        row = [[f"{rank_ind}", f"{sorted_votes_list[i]}", odds1, odds2]]
        data = np.append(row, data, axis=0)
        print(f"{rank_str}得票数：{sorted_votes_list[i]}  オッズ1：{odds1}  オッズ2：{odds2}")
        if sorted_votes_list[i] != sorted_votes_list[i+1]:
            rank_ind += 1
    df = pd.DataFrame(data=data, columns=columns)
    df = df.sort_index(ascending=False)
    print(f"合計投票数：{np.sum(sorted_votes_list)}")
    print("")
    return df


def main():
    df = make_odds_pd()
        

if __name__ == '__main__':
    main()