def calc(td):
    result = 1
    for t, d in td:
        result *= len([x for x in range(t) if x * (t - x) > d])
    print(result)


if __name__ == "__main__":
    calc([(56, 546), (97, 1927), (78, 1131), (75, 1139)])  # 1,624,896
    calc([(56977875, 546192711311139)])  # 32,583,852