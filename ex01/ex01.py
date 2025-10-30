from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    solution = defaultdict(list)

    for s in strs:
        count = [0] * 26
        for c in s:
            count[ord(c) - ord('a')] += 1

        solution[tuple(count)].append(s)

    return list(solution.values())

# if __name__ == "__main__":
#     list1 = ["eat", "tea", "tan", "ate", "nat", "bat"]
#     list2 = []
#     list3 = ['a']

#     print(group_anagrams(list1))
#     print(group_anagrams(list2))
#     print(group_anagrams(list3))