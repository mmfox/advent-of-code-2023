from collections import defaultdict
from enum import Enum
from heapq import heapify, heappop, heappush


class HandType(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6


def make_hand_sortable(hand: str) -> str:
    """
    Make a hand sortable by converting it to a string of numbers.
    """
    card_values = {
        "T": "B",
        "J": "1",
        "Q": "D",
        "K": "E",
        "A": "F",
    }
    return "".join([card_values.get(card, card) for card in hand])


def reclassify_hand(hand: str, hand_type: HandType) -> HandType:
    has_joker = "J" in hand
    num_jokers = hand.count("J")
    if not has_joker:
        return hand_type

    if hand_type == HandType.FIVE_OF_A_KIND:
        return hand_type
    elif hand_type == HandType.FOUR_OF_A_KIND:
        return HandType.FIVE_OF_A_KIND
    elif hand_type == HandType.FULL_HOUSE:
        return HandType.FIVE_OF_A_KIND
    elif hand_type == HandType.THREE_OF_A_KIND:
        return HandType.FOUR_OF_A_KIND
    elif hand_type == HandType.TWO_PAIR:
        if num_jokers == 1:
            return HandType.FULL_HOUSE
        else:
            return HandType.FOUR_OF_A_KIND
    elif hand_type == HandType.ONE_PAIR:
        return HandType.THREE_OF_A_KIND
    else:
        return HandType.ONE_PAIR


def classify_hand(hand: str) -> HandType:
    card_counts = defaultdict(int)
    for card in hand:
        card_counts[card] += 1

    card_counts = sorted(card_counts.items(), key=lambda x: x[1], reverse=True)
    if card_counts[0][1] == 5:
        return HandType.FIVE_OF_A_KIND
    elif card_counts[0][1] == 4:
        return HandType.FOUR_OF_A_KIND
    elif card_counts[0][1] == 3:
        if card_counts[1][1] == 2:
            return HandType.FULL_HOUSE
        else:
            return HandType.THREE_OF_A_KIND
    elif card_counts[0][1] == 2:
        if card_counts[1][1] == 2:
            return HandType.TWO_PAIR
        else:
            return HandType.ONE_PAIR
    else:
        return HandType.HIGH_CARD


def solution() -> int:
    total_winnings = 0

    hands = {}
    with open("data.txt") as data_file:
        for line in data_file:
            [hand, bid] = line.strip().split(" ")
            hand_type = classify_hand(hand)
            final_hand_type = reclassify_hand(hand, hand_type)
            if final_hand_type not in hands:
                hands[final_hand_type] = []
                heapify(hands[final_hand_type])
            heappush(hands[final_hand_type], (make_hand_sortable(hand), hand, bid))

    rank = 1
    for hand_type in sorted(hands.keys(), key=lambda x: x.value):
        print("\n\nHandType: ", hand_type)
        while hands[hand_type]:
            _, hand, bid = heappop(hands[hand_type])
            print(f"HAND: {hand} BID: {bid} RANK: {rank}")
            total_winnings += rank * int(bid)
            rank += 1

    return total_winnings


if __name__ == "__main__":
    print(f"Result is {solution()}")
