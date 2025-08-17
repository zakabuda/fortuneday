from django.shortcuts import render


import random

good_traits = [f"{trait}성격" for trait in [
    "창의적","활발","호기심 많은","융통성 있는","책임감 있는",
    "리더십 있는","관찰력 있는","침착한","협력적인","성실한",
    "결단력 있는","인내심 있는","감사하는","긍정적인","자기주도적인",
    "지적","논리적인","현명한","배려심 있는","계획적인",
    "적극적인","열정적인","도전적인","유연한","성장 지향적인",
    "직관적인","끈기 있는","정직한","겸손한","사려 깊은",
    "친화력 있는","적응력 있는","분석적인","창조적인","상냥한",
    "사교적인","조화로운","독립적인","열린 마음의","용감한",
    "희생적인","집중력 있는","민첩한","협상 능력 있는","긍정적 영향력 있는",
    "배움에 적극적인","세심한","통찰력 있는","감정 표현 풍부한","친절한",
    "자기 성찰하는","도덕적인","유머 감각 있는","신중한","균형 잡힌",
    "끊임없이 발전하는","문제 해결 능력 있는","호의적인","단호한","포용력 있는",
    "동기 부여 잘하는","자율적인","목표 지향적인","결과 중심적인","상호 존중하는",
    "유쾌한","감정 통제 잘하는","민첩한 판단력 있는","관계 유연한","자기 관리 잘하는",
    "신뢰할 수 있는","통합적 사고 하는","진취적인","조화와 균형 중시하는",
    "탐구심 많은","공감 능력 있는","모험을 즐기는","학습 지향적인","긍정적 에너지 발산하는",
    "공정한","책임과 신뢰 있는"
]]

bad_traits = [f"{trait}성격" for trait in [
    "충동적인","고집 센","불안정한","예민한","소극적인",
    "완벽주의적인","질투심 많은","신경질적인","우유부단한","과민한",
    "급한","무모한","의존적인","비판적인","우월감 있는",
    "경쟁심 과한","소심한","냉정한","집착하는","완고한",
    "무관심한","변덕스러운","방어적인","배타적인","회피적인",
    "냉소적인","거만한","편협한","무책임한","자기중심적인",
    "경솔한","의심 많은","무기력한","피해의식 있는","조급한",
    "긴장감 많은","냉담한","감정 기복 심한","단호하지 못한","자신감 부족한",
    "수동적인","과격한","강압적인","타협 못하는","걱정 많은",
    "비협조적인","보수적인","독단적인","무례한","과도하게 감정적인",
    "권위 도전적인","사회성 부족한","충돌이 잦은","무계획적인"
]]

# -------------------------
# 2️⃣ 직업군 샘플 10개 (실제 100개로 확장 가능)
jobs_list = [
    "기획/디자인/연구직","영업/마케팅/예술 분야","IT/프로그래밍","금융/재무",
    "교육/연구/강사","의료/보건","법률/행정","공공기관/공무원",
    "제조/생산","운송/물류"
]

# -------------------------
# 3️⃣ 천간/지지 → 오행 매핑
gan_to_element = {"갑":"목","을":"목","병":"화","정":"화",
                  "무":"토","기":"토","경":"금","신":"금",
                  "임":"수","계":"수"}
ji_to_element = {"자":"수","축":"토","인":"목","묘":"목",
                 "진":"토","사":"화","오":"화","미":"토",
                 "신":"금","유":"금","술":"토","해":"수"}

# -------------------------
# 4️⃣ 오행 계산
def calculate_elements(saju):
    elements=[]
    for k in ["년주","월주","일주","시주"]:
        gan, ji = saju[k][0], saju[k][1]
        elements.append(gan_to_element[gan])
        elements.append(ji_to_element[ji])
    return elements

def check_over_under(elements):
    counts={el: elements.count(el) for el in ["목","화","토","금","수"]}
    result={}
    for el,cnt in counts.items():
        if cnt<=1: result[el]="부족"
        elif cnt<=3: result[el]="적당"
        else: result[el]="과다"
    return result

# -------------------------
# 5️⃣ 특수살
def check_special_sals(saju):
    specials=[]
    day_branch=saju["일주"][1]
    if day_branch in ["인","사","신","해"]: specials.append("역마살")
    month_branch=saju["월주"][1]
    if (day_branch, month_branch) in [("자","사"),("인","술")]: specials.append("천덕살")
    day_gan=saju["일주"][0]
    if day_gan in ["병","임"]: specials.append("양인살")
    if day_branch in ["축","오","술"]: specials.append("망신살")
    return specials

# -------------------------
# 6️⃣ 충/형
chong_map = {"자":"오","오":"자","축":"미","미":"축","인":"신","신":"인",
             "묘":"유","유":"묘","진":"술","술":"진","사":"해","해":"사"}
xing_groups=[["인","사","신"],["축","술","미"],["자","오","술"]]

def check_chong(saju):
    branches=[saju[k][1] for k in ["년주","월주","일주","시주"]]
    return [f"{b1}충{b2}" for i,b1 in enumerate(branches) for j,b2 in enumerate(branches) if i<j and chong_map.get(b1)==b2]

def check_xing(saju):
    branches=[saju[k][1] for k in ["년주","월주","일주","시주"]]
    conflicts=[]
    for group in xing_groups:
        count=sum(1 for b in branches if b in group)
        if count>=2: conflicts.append(f"{group}형 발생")
    return conflicts

def check_patterns(saju):
    return check_chong(saju)+check_xing(saju)

# -------------------------
# 7️⃣ 점수 기반 장점/단점
def score_traits(saju):
    elements=calculate_elements(saju)
    over_under=check_over_under(elements)
    specials=check_special_sals(saju)
    patterns=check_patterns(saju)

    good_scores=[0]*len(good_traits)
    for i,t in enumerate(good_traits):
        if "창의" in t and over_under.get("목")=="부족": good_scores[i]+=3
        if "호기심" in t and "역마살" in specials: good_scores[i]+=2
        if "융통" in t and "양인살" in specials: good_scores[i]+=2

    bad_scores=[0]*len(bad_traits)
    for i,t in enumerate(bad_traits):
        if "충동" in t and patterns: bad_scores[i]+=3
        if "완벽" in t and over_under.get("토")=="과다": bad_scores[i]+=2
        if "예민" in t and "망신살" in specials: bad_scores[i]+=2

    return good_scores,bad_scores

# -------------------------
# 8️⃣ 귀인/인연
def get_gwiin(saju):
    elements=calculate_elements(saju)
    gwiin=[]
    for el in ["목","화","토","금","수"]:
        if elements.count(el)<=1:
            gwiin.append({"오행":el,"사람_유형":"신중하고 안정적인 사람"})
        elif elements.count(el)>=3:
            gwiin.append({"오행":el,"사람_유형":"활발하고 창의적인 사람"})
    return gwiin

# -------------------------
# 9️⃣ 직업군 점수 기반 추천
def score_jobs(saju, good_scores, bad_scores):
    elements=calculate_elements(saju)
    specials=check_special_sals(saju)
    patterns=check_patterns(saju)

    job_scores=[0]*len(jobs_list)
    for i,job in enumerate(jobs_list):
        if "기획" in job and good_scores[0]>1: job_scores[i]+=3
        if "영업" in job and "역마살" in specials: job_scores[i]+=2
        if "IT" in job and good_scores[1]>1: job_scores[i]+=2
        if "금융" in job and bad_scores[0]>1: job_scores[i]+=1

    top_jobs=[jobs_list[i] for i in sorted(range(len(job_scores)), key=lambda x:job_scores[x], reverse=True)[:5]]
    return top_jobs

# -------------------------
# 10️⃣ 최종 출력
def generate_personality_print(saju):
    good_scores,bad_scores=score_traits(saju)
    final_good=[good_traits[i] for i in sorted(range(len(good_scores)), key=lambda x:good_scores[x], reverse=True)[:20]]
    final_bad=[bad_traits[i] for i in sorted(range(len(bad_scores)), key=lambda x:bad_scores[x], reverse=True)[:20]]
    
    direction="장점은 살리고 단점은 관리하면, 대인관계와 직업에서 최적의 성과를 얻을 수 있다"
    gwiin=get_gwiin(saju)
    jobs=score_jobs(saju,good_scores,bad_scores)
    return {
        "장점_traits": final_good,       # <--- 공백을 언더바로 변경
        "단점_traits": final_bad,        # <--- 공백을 언더바로 변경
        "앞으로_나아갈_방향": direction,    # <--- 공백을 언더바로 변경
        "귀인_인연": gwiin,               # <--- 공백을 언더바로 변경
        "추천_직업군": jobs                # <--- 공백을 언더바로 변경
    }

    # print("=== 사주 분석 결과 ===")
    # print("장점 traits:", final_good)
    # print("단점 traits:", final_bad)
    # print("앞으로 나아갈 방향:", direction)
    # print("귀인/인연:")
    # for g in gwiin: print(f"  오행: {g['오행']}, 사람 유형: {g['사람 유형']}")
    # print("추천 직업군:", jobs)

# -------------------------
# 테스트
saju_input = {"년주":"갑자","월주":"병인","일주":"신사","시주":"경오"}
result = generate_personality_print(saju_input)
# print(result)
# print("반갑다냥~ 나는 너의 성격을 점춰주는 스님고양이다 냥!")
# print("흐음....보자..")
# print("너는의 성격은....")
# print("너는의 성격은...." + result["장점 traits"][0]+ "이고 " +result["장점 traits"][1]+  "이구나 냥! 또....")
# print("너는의 성격은...." + result["장점 traits"][2]+ "이고 " +result["장점 traits"][3]+  "도 있네 냥 ! ")
# print("너는의 성격은...." +result["장점 traits"][4]+ "까지있다 냥~! ")
# print("그런데.. 너 성격의 단점은...." + result["단점 traits"][0]+ "이고 " +result["단점 traits"][1]+  "이구나 냥! 또....")
# print("너 성격의 단점은...." + result["단점 traits"][2]+ "이고 " +result["단점 traits"][3]+  "도 있네 냥 ! ")
# print("흠.... 그렇다면 너의 귀인/인연은 어떤 타입일까....")
# print("바로..."+ result["귀인/인연"][0]["오행"] + " 오행을 가진 " + result["귀인/인연"][0]["사람 유형"] + "이구나 냥!")
# print("또..."+ result["귀인/인연"][1]["오행"] + " 오행을 가진 " + result["귀인/인연"][1]["사람 유형"] + "이구나 냥!")
# print("마지막으로 너에게 추천하는 직업군은... " + ", ".join(result["추천 직업군"]) + "이야 냥!")
# print("앞으로 나아갈 방향은... " + result["앞으로 나아갈 방향"] + " 냥!")
# print("도움이 되었으면 좋겠다 냥!!!! 담에 또 찾아오라 냥~!")


# Create your views here.
def home(request):
    saju_input = {"년주":"갑자","월주":"병인","일주":"신사","시주":"경오"}
    result = generate_personality_print(saju_input)
    context = {'result': result}
    return render(request, 'index.html', context)