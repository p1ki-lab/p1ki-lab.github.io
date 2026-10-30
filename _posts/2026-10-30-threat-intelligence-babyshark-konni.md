---
layout: post
title: "Threat Intelligence: BABYSHARK와 Konni의 관계 비교"
description: "Huntress와 ASEC 보고서를 바탕으로 BABYSHARK 사용 공격자와 Konni의 관계를 비교한 기록"
date: 2026-10-30 00:00:00 +0900
categories: [블로그]
tags: [Threat Intelligence, BABYSHARK, Konni, APT]
---

**Threat Intelligence(위협 인텔리전스)**는 사이버 위협에 관한 정보를 수집·분석해, 보안 판단과 대응에 활용할 수 있도록 만든 증거 기반의 지식이다.

이번 포스트에서는 아래 두 보고서에서 등장하는 두 공격자가 서로 어떤 관계가 있는지 비교해보았다. 

자료 A : [https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood "https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood") 
자료 B : [https://asec.ahnlab.com/ko/59625/](https://asec.ahnlab.com/ko/59625/ "https://asec.ahnlab.com/ko/59625/")

자료 A는 Huntress의 BABYSHARK 침해 사고 분석이고, 자료 B는 AhnLab ASEC의 Konni 피싱 메일 분석이다. 편의상 자료 A의 공격자를 P, 자료 B의 공격자를 Q라고 두었다.

---

## 1. 이름 구분 

### 1. 자료 A,B
Huntress는 BABYSHARK를 북한 관련 공격자가 사용하는 **악성코드 계열**이라고 설명한다. ASEC는 자료 B의 공격 주체를 **Konni 공격 그룹**으로 표현한다.

>BABYSHARK는 공격자 명이 아니라, 악성코드 계열의 이름이다. 

앞으로 나올 설명에서 P는 ‘자료 A의 BABYSHARK 사용 공격자’, Q는 ‘자료 B에서 ASEC가 Konni로 분류한 공격자’ 라는 의미이다. 

출처: [Huntress 자료 A](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC 자료 B](https://asec.ahnlab.com/ko/59625/)

---

### 2. BABYSHARK의 최초 명명 자료

Unit 42는 2019년 2월 22일 공개한 보고서에서 새로 확인한 VBScript 기반 악성코드에 BabyShark라는 이름을 붙였다. 
분석 대상은 2018년 11월 발송된 표적 피싱 메일이었다. 
*표적피싱 : 특정 인물이나 조직을 속이도록 내용을 맞춘 피싱이다*

Unit 42가 분석한 초기 BabyShark 유포 사례에서는 공격자가 핵 안보 전문가를 사칭하고, 악성 매크로가 포함된 Excel 문서를 첨부했다. 매크로는 문서에서 작업을 자동 실행하는 기능인데, 여기서는 악성코드를 실행하는 데 사용됐다. 

출처: [Unit 42 최초 명명 보고서](https://unit42.paloaltonetworks.com/new-babyshark-malware-targets-u-s-national-security-think-tanks/)

---

### 3. KONNI의 최초 명명 자료

Cisco Talos가 2017년 5월 3일 공개한 최초 명명 보고서를 보면 "Talos has named this malware KONNI" 라는 문장이 나오는데, 이걸 통해 KONNI도 처음에는 공격자 그룹명이 아니라 악성코드의 이름이었다는 걸 알 수 있었다. 

Talos는 KONNI(악성코드)를 감염된 컴퓨터를 원격으로 조작하는 RAT라고 설명했고, 2014년부터 이어지는 활동을 분석했다.

출처: [Cisco Talos 최초 명명 보고서](https://blog.talosintelligence.com/konni-malware-under-radar-for-years/)

---

## 2. 두 자료 특징 비교 

|비교 항목|자료 A: P|자료 B: Q|
|---|---|---|
|유인 방식|VOA 기자 사칭 후 대화를 이어가며 문서 검토 요청|개인정보 유출 관련 자료로 위장|
|실행 출발점|악성 매크로가 포함된 Word 문서|악성 EXE|
|후속 실행|VBScript 등 여러 단계 사용|JSE와 PowerShell 사용|
|지속성|예약 작업·레지스트리 활용|예약 작업으로 1분마다 반복 실행|
|외부 통신|Google Drive와 공격자 서버 활용|공격자 서버에서 명령 수신|
|분석 한계|일부 DLL 확보 실패|서버 접속 불가로 최종 명령 확인 실패|

출처: [Huntress 자료 A](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC 자료 B](https://asec.ahnlab.com/ko/59625/)

공통적으로 눈에 들어온 것은 미끼 문서, 스크립트 실행, 예약 작업인데, 이것만으로는 두 공격자가 같다고 판단하긴 어려웠다. 꼭 같은 공격자가 아니어도 여러 공격자가 사용할 수 있는 방법이기 때문이다. 

---

## 3. 추가 자료에서 확인한 연결과 한계

두 자료만 봤을 땐, P와 Q가 서로 같은 공격자라고 확신할 수 없었기 때문에, 추가 자료를 찾아보았다. 

### 1. Proofpoint 보고서 

Proofpoint의 2021년 보고서에 따르면 Proofpoint가 TA406으로 추적하는 공격자의 사용 악성코드에 KONNI와 BabyShark가 모두 포함되어 있다고 나와있다. 

>  이 내용은 KONNI와 BabyShark의 사용 주체가 일부 겹쳤다는 근거가 되지만, 자료 A의 P와 자료 B의 Q가 동일한 공격자라는 사실을 직접 보여주지는 않는다.

추가로 Proofpoint는 TA406이 TA427의 도구·코드에 접근했거나, 두 주체가 개발 자원을 공유했을 가능성을 제시했다. 이는 연구진의 추정이며, 자료 A와 B의 공격자 사이에서 직접 확인된 관계는 아니다. 

또 이 보고서는 2021년에 발행됐기 때문에, 2023년 공개된 자료 B의 사건을 직접 설명하는 자료로 받아들일 수 없었다. 따라서 두 악성코드의 과거 사용 이력이 겹친다는 참고 근거로 받아들였다.

출처: [Proofpoint 원문 보고서, 인쇄 페이지 6–7](https://www.proofpoint.com/us/resources/threat-reports/triple-threat-north-korea-aligned-ta406-scams-spies-and-steals)

### 2. ESET 보고서

ESET의 2022년 보고서에서도 BabyShark 관련 활동과 Konni 활동을 함께 확인할 수 있었다.

ESET는 Kimsuky 항목에서 홍콩 금융회사를 대상으로 한 공격을 BabyShark Cluster의 장기 캠페인에 속하는 활동이라고 설명했다. 반면 Konni는 별도 항목으로 구분했고, 변조된 Sumatra PDF 뷰어를 이용해 외교 분야를 공격한 사례를 소개했다.

ESET는 이 보고서에서 두 활동을 별도 항목으로 소개했다. 다만 이것만으로 두 활동이 서로 무관하다고 판단할 수는 없다. 따라서 이 보고서는 직접적인 연결 근거보다는 활동 분류를 비교하는 보조 자료로 참고했다.

출처: [ESET APT Activity Report T2 2022, 10쪽](https://web-assets.eset.com/fileadmin/ESET/INT/B2B_Resource_centrum/Reports/T2-2022_APT-Activity-Report.pdf)

### 3. 추가 자료로 확인한 범위

지금까지 찾은 내용을 정리하면 다음과 같다.

|항목|확인한 내용|아직 확인하지 못한 내용|
|---|---|---|
|악성코드|Proofpoint가 TA406의 KONNI·BabyShark 사용 이력을 보고했다|자료 A·B의 악성코드 사이에 직접적인 코드 일치가 있는지|
|공격 방식|두 사건 모두 미끼 문서, 스크립트, 예약 작업을 활용했다|이 조합이 두 공격자를 식별할 만큼 고유한 특징인지|
|인프라|각 보고서에서 외부 서버와의 통신을 확인할 수 있었다|두 사건이 같은 공격자 통제 서버·계정을 공유했는지|
|활동 시기|관련 악성코드의 과거 사용 이력이 존재한다|두 사건이 하나의 연속된 작전인지|

---

## 4. 두 공격자의 관계에 대한 내 생각

결론부터 말하자면, 내가 조사한 자료에서는 P와 Q가 동일한 공격자라고 판단할 만한 직접적인 근거를 찾지 못했다.

두 사건에는 미끼 문서, 스크립트 실행, 예약 작업이라는 공통점이 있었다. 추가로 Proofpoint가 TA406의 KONNI와 BabyShark 사용 이력을 함께 보고한 점도 확인했다.

하지만 과거의 악성코드 사용 이력이 지정된 두 사건의 수행 주체까지 증명하지는 않는다. 이번 조사에서는 두 사건 사이의 코드 일치나 같은 공격자 통제 서버·계정의 재사용을 확인하지 못했다.

따라서 두 활동 사이의 연관 가능성은 남겨 두되, P와 Q가 동일한 공격자라는 결론은 보류했다. 이는 두 공격자가 서로 다르다는 뜻도 아니다. 현재 확보한 자료만으로는 관계를 확정하기 어렵다는 의미이다.

출처: [Proofpoint 원문 보고서, 인쇄 페이지 6–7](https://www.proofpoint.com/us/resources/threat-reports/triple-threat-north-korea-aligned-ta406-scams-spies-and-steals)

---
## 5. 느낀 점

서로 다른 두 자료를 보며, 두 공격자가 같은지 분석해 보는 활동을 처음 해보았다. 매번 자료나 기사를 읽을 때 각자 다른 공격자일 것이라고 무의식중에 생각했었는데, 이번 과제를 하면서 고정관념을 하나 깬 것 같다. 

위협 인텔리전스를 평소에도 잘 활용하려면, 여러 자료를 평소에 많이 읽고, 자료 간의 연결점을 떠올리는 능력이 필요할 것 같다. 그리고 ai를 활용해서 가능성이 있는 자료들을 찾아 연습하다 보면 나중에는 스스로 자료들을 선별해 분석해 볼 수 있을 것이다.
