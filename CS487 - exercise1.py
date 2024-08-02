import requests
import json
from typing import Dict, Tuple
import re

def send_prompt_to_llm(prompt: str) -> Tuple[str, int, int]:
    url = "http://localhost:1234/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "messages": [
            {"role": "system", "content": "You are a helpful assistant for analyzing election data."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "max_tokens": -1,
        "stream": False
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        response_json = response.json()
        content = response_json['choices'][0]['message']['content'].strip()
        prompt_tokens = response_json['usage']['prompt_tokens']
        completion_tokens = response_json['usage']['completion_tokens']
        return content, prompt_tokens, completion_tokens
    else:
        raise Exception(f"Error from LLM: {response.text}")

# function to process election data
def process_election_data(data: str) -> Dict[str, int]:
    results = {}
    pattern = re.compile(r"(\D+)\s(\d+)")
    results = {}
    matches = pattern.findall(data)
    for party, votes in matches:
        party = party.strip()
        votes = int(votes.strip())
        if party in results:
            results[party] += votes
        else:
            results[party] = votes

    return results

# solving questions (a,b,c) here
def solve_election_result(data: str) -> Tuple[str, int, int]:
    processed_data = process_election_data(data)
    prompt = f"""
    Analyze the following election data and provide:
    1. The winning party along with total votes
    2. The runner-up party along with total votes
    3. The victory margin (difference in votes between winner and runner-up)

    Election data:
    {processed_data}

    Please provide the answer in the following format:
    Winner: [Party name] Votes: [Total votes]
    Runner-up: [Party name] Votes: [Total votes]
    Victory margin: [Difference in number of votes]
    """
    return send_prompt_to_llm(prompt)

# solving (d) here
def solve_party_comparison(data_a: str, data_b: str, data_c: str) -> Tuple[str, int, int]:
    processed_data_a = process_election_data(data_a)
    processed_data_b = process_election_data(data_b)
    processed_data_c = process_election_data(data_c)
    
    prompt = f"""
    Compare the performance of INC and BJP across three constituencies:

    Constituency 1: {processed_data_a}
    Constituency 2: {processed_data_b}
    Constituency 3: {processed_data_c}

    Provide the following information:
    1. Total votes polled by INC and BJP in each constituency
    2. Vote percentage for INC and BJP in each constituency
    3. Aggregated vote percentage for INC and BJP across all three constituencies

    Please format the answer clearly and concisely.
    """
    return send_prompt_to_llm(prompt)

if __name__ == "__main__":

    total_tokens_input = 0
    total_tokens_output = 0

    data_a = """
    TDP 54056
BJP 1753
YSRCP 69588
INC 1327
JnP 2987
JAJGP 203
IND 568
IND 418
IND 743
IND 636
TDP 51399
BJP 3273
YSRCP 71694
INC 1954
JnP 5391
JAJGP 469
IND 1082
IND 886
IND 1127
IND 793
TDP 57159
BJP 1474
YSRCP 68836
INC 1362
JnP 4995
JAJGP 189
IND 530
IND 390
IND 664
IND 386
TDP 59128
BJP 1684
YSRCP 76281
INC 1730
JnP 3349
JAJGP 261
IND 755
IND 483
IND 1154
IND 707
TDP 23849
BJP 3354
YSRCP 83652
INC 3599
JnP 8761
JAJGP 2034
IND 3902
IND 6430
IND 3157
IND 2653
TDP 27101
BJP 3629
YSRCP 82473
INC 4151
JnP 4637
JAJGP 807
IND 1964
IND 1748
IND 2163
IND 1528
TDP 63471
BJP 2411
YSRCP 105037
INC 3533
JnP 12125
JAJGP 742
IND 1410
IND 3455
IND 2223
IND 1160
    """

    data_b = """
    TDP 83375
INC 2370
YSRCP 69572
BJP 1609
PPOI 316
JnP 9347
IND 910
IND 858
IND 661
TDP 70050
INC 1650
YSRCP 66319
BJP 975
PPOI 157
JnP 5338
IND 575
IND 662
IND 448
TDP 86897
INC 1308
YSRCP 78289
BJP 754
PPOI 180
JnP 2163
IND 634
IND 931
IND 513
TDP 65828
INC 1616
YSRCP 72134
BJP 1159
PPOI 242
JnP 4047
IND 776
IND 791
IND 741
TDP 86800
INC 2007
YSRCP 77144
BJP 1387
PPOI 224
JnP 5737
IND 675
IND 614
IND 516
TDP 63490
INC 1256
YSRCP 75759
BJP 692
PPOI 142
JnP 2611
IND 517
IND 538
IND 343
TDP 72773
INC 3249
YSRCP 81714
BJP 781
PPOI 180
JnP 2076
IND 742
IND 757
IND 592
    """

    data_c = """
    TDP 81865
INC 2136
YSRCP 96447
BJP 830
SAPRP 771
ACP 269
JnP 4534
JAJGP 112
PPOI 130
IND 158
IND 214
IND 312
IND 1351
IND 1123
TDP 70709
INC 1901
YSRCP 77231
BJP 798
SAPRP 653
ACP 170
JnP 4491
JAJGP 109
PPOI 121
IND 169
IND 161
IND 192
IND 444
IND 981
TDP 77990
INC 1997
YSRCP 82816
BJP 1081
SAPRP 1172
ACP 225
JnP 4249
JAJGP 126
PPOI 138
IND 177
IND 201
IND 210
IND 404
IND 806
TDP 64250
INC 2438
YSRCP 87430
BJP 849
SAPRP 713
ACP 179
JnP 3442
JAJGP 124
PPOI 100
IND 136
IND 151
IND 213
IND 924
IND 909
TDP 71872
INC 2710
YSRCP 82956
BJP 801
SAPRP 645
ACP 151
JnP 3627
JAJGP 111
PPOI 148
IND 150
IND 214
IND 178
IND 501
IND 1100
TDP 72449
INC 2707
YSRCP 85233
BJP 657
SAPRP 624
ACP 169
JnP 6426
JAJGP 118
PPOI 97
IND 140
IND 159
IND 201
IND 529
IND 1020
TDP 88172
INC 1718
YSRCP 61353
BJP 1886
SAPRP 403
ACP 98
JnP 7010
JAJGP 87
PPOI 88
IND 80
IND 72
IND 155
IND 397
IND 397
    """

    print("Solving part (a):")
    response_a, tokens_in_a, tokens_out_a = solve_election_result(data_a)
    print(response_a)
    total_tokens_input += tokens_in_a
    total_tokens_output += tokens_out_a

    print("\nSolving part (b):")
    response_b, tokens_in_b, tokens_out_b = solve_election_result(data_b)
    print(response_b)
    total_tokens_input += tokens_in_b
    total_tokens_output += tokens_out_b

    print("\nSolving part (c):")
    response_c, tokens_in_c, tokens_out_c = solve_election_result(data_c)
    print(response_c)
    total_tokens_input += tokens_in_c
    total_tokens_output += tokens_out_c

    print("\nSolving part (d):")
    response_d, tokens_in_d, tokens_out_d = solve_party_comparison(data_a, data_b, data_c)
    print(response_d)
    total_tokens_input += tokens_in_d
    total_tokens_output += tokens_out_d

    print(f"\nPart (f) - Token usage:")
    print(f"Total input tokens: {total_tokens_input}")
    print(f"Total output tokens: {total_tokens_output}")
    print(f"Total tokens consumed and emitted: {total_tokens_input + total_tokens_output}")