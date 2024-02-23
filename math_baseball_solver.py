def digits_are_all_different(num):
    num = str(num)
    return len(num) == len(set(num))


def create_candidates():
    return [str(i).zfill(4) for i in range(123, 9877) if digits_are_all_different(i)]


def is_valid_input(result):
    valid_result = [
        "0S0B",
        "0S1B",
        "0S2B",
        "0S3B",
        "0S4B",
        "1S0B",
        "1S1B",
        "1S2B",
        "1S3B",
        "2S0B",
        "2S1B",
        "2S2B",
        "3S0B",
    ]
    return result in valid_result


def compare(num1, num2):
    num1 = str(num1)
    num2 = str(num2)
    strike = 0
    ball = 0
    for i in range(len(num1)):
        if num1[i] == num2[i]:
            strike += 1
        elif num1[i] in num2:
            ball += 1
    return f"{strike}S{ball}B"


def main():
    attempts = []
    candidate = create_candidates()

    print("Welcome to the number baseball game solver!")
    print("Is it 0123?")

    while True:
        input_string = input("Enter result: ")
        if input_string == "show-all-available":
            print(*candidate)
            continue
        elif input_string == "yes":
            print("I knew it!")
            break

        attempt = {"attempt": candidate[0], "result": input_string.upper()}
        attempts.append(attempt)

        candidate = [
            cand
            for cand in candidate
            if compare(cand, attempt["attempt"]) == attempt["result"]
        ]

        if len(candidate) == 1:
            print(f"The number must be {candidate[0]}")
            break
        elif len(candidate) == 0:
            print("No number is possible")
            break
        else:
            print(f"How about {candidate[0]}?")


def filter(candidates, guess, strike, ball):
    attempt = {"attempt": guess, "result": f"{strike}S{ball}B"}
    if is_valid_input(attempt["result"]) == False:
        return ["Wrong value"]
    candidate = [
        cand
        for cand in candidates
        if compare(cand, attempt["attempt"]) == attempt["result"]
    ]
    return candidate if candidate else ["No number is possible"]


if __name__ == "__main__":
    main()
