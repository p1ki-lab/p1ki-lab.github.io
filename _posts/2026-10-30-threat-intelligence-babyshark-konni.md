---
layout: post
title: "Threat Intelligence: BABYSHARK와 Konni의 관계 비교"
description: "Huntress와 ASEC 보고서를 바탕으로 BABYSHARK 사용 공격자와 Konni의 관계를 비교한 기록"
date: 2026-10-30 00:00:00 +0900
categories: [블로그]
tags: [Threat Intelligence, BABYSHARK, Konni, APT]
---

**Threat Intelligence(위협 인텔리전스)** 는 사이버 위협에 관한 정보를 수집·분석해, 보안 판단과 대응에 활용할 수 있도록 만든 증거 기반의 지식이다.

이번 포스트에서는 아래 두 보고서에서 등장하는 두 공격자가 서로 어떤 관계가 있는지 비교해보았다. 

자료 A : [https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood "https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood") 
자료 B : [https://asec.ahnlab.com/ko/59625/](https://asec.ahnlab.com/ko/59625/ "https://asec.ahnlab.com/ko/59625/")

자료 A는 Huntress의 BABYSHARK 침해 사고 분석이고, 자료 B는 AhnLab ASEC의 Konni 피싱 메일 분석이다. 편의상 자료 A의 공격자를 P, 자료 B의 공격자를 Q라고 두었다.

---

## 1. 이름 구분 

### 1-1. 자료 A,B
Huntress는 BABYSHARK를 북한 관련 공격자가 사용하는 **악성코드 계열**이라고 설명한다. ASEC는 자료 B의 공격 주체를 **Konni 공격 그룹**으로 표현한다.

>BABYSHARK는 공격자 명이 아니라, 악성코드 계열의 이름이다. 

앞으로 나올 설명에서 P는 ‘자료 A의 BABYSHARK 사용 공격자’, Q는 ‘자료 B에서 ASEC가 Konni로 분류한 공격자’ 라는 의미이다. 

출처: [Huntress 자료 A](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC 자료 B](https://asec.ahnlab.com/ko/59625/)

---

### 1-2. BABYSHARK의 최초 명명 자료

Unit 42는 2019년 2월 22일 공개한 보고서에서 새로 확인한 VBScript 기반 악성코드에 BabyShark라는 이름을 붙였다. 
분석 대상은 2018년 11월 발송된 표적 피싱 메일이었다. 
*표적피싱 : 특정 인물이나 조직을 속이도록 내용을 맞춘 피싱이다*

Unit 42가 분석한 초기 BabyShark 유포 사례에서는 공격자가 핵 안보 전문가를 사칭하고, 악성 매크로가 포함된 Excel 문서를 첨부했다. 매크로는 문서에서 작업을 자동 실행하는 기능인데, 여기서는 악성코드를 실행하는 데 사용됐다. 

출처: [Unit 42 최초 명명 보고서](https://unit42.paloaltonetworks.com/new-babyshark-malware-targets-u-s-national-security-think-tanks/)

---

### 1-3. KONNI의 최초 명명 자료

Cisco Talos가 2017년 5월 3일 공개한 최초 명명 보고서를 보면 "Talos has named this malware KONNI" 라는 문장이 나오는데, 이걸 통해 KONNI도 처음에는 공격자 그룹명이 아니라 악성코드의 이름이었다는 걸 알 수 있었다. 

Talos는 KONNI(악성코드)를 감염된 컴퓨터를 원격으로 조작하는 RAT라고 설명했고, 2014년부터 이어지는 활동을 분석했다.

출처: [Cisco Talos 최초 명명 보고서](https://blog.talosintelligence.com/konni-malware-under-radar-for-years/)

---

## 2. 두 사건 비교 

### 2-1. 보고서 내용 비교

|비교 항목|자료 A: P|자료 B: Q|
|---|---|---|
|유인 방식|VOA 기자 사칭 후 대화를 이어가며 문서 검토 요청|개인정보 유출 관련 자료로 위장|
|실행 출발점|악성 매크로가 포함된 Word 문서|악성 EXE|
|후속 실행|VBScript 등 여러 단계 사용|JSE와 PowerShell 사용|
|지속성|예약 작업·레지스트리 활용|예약 작업으로 1분마다 반복 실행|
|외부 통신|Google Drive와 공격자 서버 활용|공격자 서버에서 명령 수신|
|분석 한계|일부 DLL 확보 실패|서버 접속 불가로 최종 명령 확인 실패|
*지속성 : 재부팅이나 시간 경과 뒤에도 공격자의 접근을 유지하는 방식이다.*
출처: [Huntress 자료 A](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC 자료 B](https://asec.ahnlab.com/ko/59625/)

공통적으로 눈에 들어온 것은 미끼 문서, 스크립트 실행, 예약 작업인데, 이것만으로는 두 공격자가 같다고 판단하긴 어려웠다. 꼭 같은 공격자가 아니어도 여러 공격자가 사용할 수 있는 방법이기 때문이다.

---

### 2-2. 인프라 비교

두 사건에서 같은 서버나 도메인을 사용했는지도 살펴보았다.
인프라는 공격에 사용된 서버·도메인·계정 등을 뜻하는데, **같은 서버나 도메인이 여러 사건에서 반복해서 등장하면, 공격에 쓰인 자원이 재사용됐는지 살펴볼 단서**가 된다. 그래서 두 사건 사이에 이런 연결점이 있는지 알아보려고, 보고서에 공개된 주소를 모아 도메인과 경로를 비교해 보았다.

자료 A의 IOC(침해 흔적) 목록에는 도메인 5개가, 자료 B의 URL 항목에는 주소 1개가 공개되어 있었다.

>주소의 점은 실수로 접속하는 것을 막기 위해 `[.]`으로 표시했다.

|자료|공개된 도메인|
|---|---|
|A|`retmodul[.]com`, `hodbeast[.]com`, `worldinfocontact[.]club`, `frebough[.]com`, `beastmodser[.]club`|
|B|`gjdow[.]atwebpages[.]com`|

목록에서 일치하는 도메인은 없었다. 

#### 주소별 용도와 근거

`hodbeast[.]com`은 수집한 정보를 업로드하는 데 사용됐다. 자료 A의 **Following Breadcrumbs**에서는 시스템 정보를 파일에 저장하고 인코딩한 뒤, 이 도메인의 `/silver/upload.php`로 POST 요청을 보내 전송했다고 설명한다. POST는 데이터를 서버로 보내는 HTTP 요청 방식이다.

`worldinfocontact[.]club`은 명령을 받아오는 C2로 사용됐다. 같은 절에서는 악성코드가 일정한 간격으로 이 주소에 접속해 대기 중인 명령을 받고 실행한다고 설명한다.

> C2는 공격자가 악성코드에 명령을 전달하거나 정보를 받는 서버를 뜻한다.

`beastmodser[.]club`은 미끼 문서와 DLL을 전달하는 데 사용됐다. 자료 A의 **Finding the Phish**에 나오는 매크로 분석에서는 이 도메인에서 사용자에게 보여줄 Word 문서와 `version.tmp`를 내려받고, `version.tmp`의 이름을 `version.dll`로 바꾸는 과정을 설명한다.

출처: [Huntress 자료 A — Following Breadcrumbs / Finding the Phish](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood)

자료 B에서는 `WindowsHotfixUpdate.ps1`이 C2에서 명령을 받아온다고 설명한다. 이어 다른 스크립트가 그 명령을 복호화해 XML 형태로 로드하는 과정도 소개한다. 자료 B의 URL 항목에는 `gjdow[.]atwebpages[.]com`이 공개되어 있다.

출처: [ASEC 자료 B — WindowsHotfixUpdate.ps1 분석 및 URL 항목](https://asec.ahnlab.com/ko/59625/)

도메인 뒤의 경로와 요청에 붙는 값도 비교했다.

|자료|보고서에서 확인한 경로와 요청 값|설명|
|---|---|---|
|A|`/silver/upload.php`|수집 정보 업로드|
|A|`/111/alex/expres.php?op=2`|명령 수신|
|A|`/sil/0304/d.php?na=version.gif`|이후 DLL로 이름이 바뀌는 파일 다운로드|
|B|`/dn.php?name=[Computer`|보고서 URL 항목에 공개된 부분|

자료 B의 주소는 보고서에 표시된 부분 그대로 옮겼다. 비교한 경로도 서로 달랐다. 두 자료 모두 `.php`가 등장해 전체 경로와 요청에 붙는 값까지 함께 살펴보았다.

비교 결과, 공개된 도메인과 경로는 서로 달랐고 외부 서버에서 명령을 받아온다는 공통점이 있었다.

출처: [Huntress 자료 A — IOC 목록 및 본문 분석](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC 자료 B — URL 항목 및 PowerShell 분석](https://asec.ahnlab.com/ko/59625/)

---

## 3. 추가 보고서 비교

두 사건을 비교한 뒤, BabyShark와 Konni가 다른 보고서에서는 어떻게 다뤄지는지 찾아보았다.

### 3-1. Proofpoint

Proofpoint의 2021년 11월 보고서에서는 TA406이 사용하는 악성코드에 KONNI와 BabyShark가 함께 나열되어 있었다. 또 TA406으로 추적하는 활동이 다른 곳에서는 Kimsuky, Thallium, Konni Group으로도 불린다고 설명한다.

사용 시점에 관한 설명도 있었다. Proofpoint는 TA406이 적어도 2019년 초에는 BabyShark를 사용할 수 있었지만, 최초 사용자는 아니라고 평가했다. TA427의 BabyShark 사용은 늦어도 2018년 11월까지 거슬러 올라간다고 설명한다. 이를 바탕으로 연구진은 TA406이 TA427의 도구나 코드에 접근했거나, 개발 자원을 공유했을 가능성을 제시했다.

출처: [Proofpoint 보고서 — 5쪽 TA406 attribution, 6쪽 TA406, 7쪽 TA427](https://www.proofpoint.com/us/resources/threat-reports/triple-threat-north-korea-aligned-ta406-scams-spies-and-steals)

---

### 3-2. ESET

ESET의 T2 2022 보고서는 BabyShark 관련 활동과 Konni 활동을 별도 항목에서 다뤘다. Kimsuky 항목에서는 홍콩 금융회사를 대상으로 한 공격을 BabyShark cluster의 장기 캠페인으로 설명했고, Konni 항목에서는 변조된 Sumatra PDF 뷰어를 이용한 외교 분야 공격을 소개했다. 여기서 cluster는 연구자가 관련 있다고 보고 묶어 추적하는 활동 집합을 뜻한다.

Proofpoint에서는 TA406의 사용 악성코드에 두 이름이 함께 등장했고, ESET에서는 BabyShark 관련 활동과 Konni 활동이 각각 소개되어 있었다. 두 보고서를 나란히 읽으며, 기관마다 활동을 묶고 이름을 붙이는 방식에도 차이가 있다는 점을 알게 됐다.

출처: [ESET APT Activity Report T2 2022 — 10쪽 Kimsuky / Konni](https://web-assets.eset.com/fileadmin/ESET/INT/B2B_Resource_centrum/Reports/T2-2022_APT-Activity-Report.pdf#page=10)


---

## 4. 두 공격자의 관계에 대한 내 생각

### 4-1. 정보 정리

지금까지 찾은 내용을 정리하면 다음과 같다.

| 항목    | 확인한 내용                                                             | 아직 확인하지 못한 내용                    |
| ----- | ------------------------------------------------------------------ | -------------------------------- |
| 악성코드  | Proofpoint가 TA406의 KONNI·BabyShark 사용 이력을 보고했다                     | 자료 A·B의 악성코드 사이에 직접적인 코드 일치가 있는지 |
| 공격 방식 | 두 사건 모두 미끼 문서, 스크립트, 예약 작업을 활용했다                                   | 이 조합이 두 공격자를 식별할 만큼 고유한 특징인지     |
| 인프라   | 공개 도메인은 A 5개·B 1개로 일치하지 않았고, 비교한 경로도 달랐다. 두 사건 모두 외부 서버에서 명령을 받아왔다 | 공개 주소 외에 서버·계정의 공유 이력이 있는지       |
| 활동 시기 | 관련 악성코드의 과거 사용 이력이 존재한다                                            | 두 사건이 하나의 연속된 작전인지               |


---

### 4-2. 내 판단

결론부터 말하자면, 내가 조사한 자료에서는 P와 Q가 같은 공격자라고 판단할 만한 직접적인 근거를 찾지 못했다.

두 사건에는 미끼 문서, 스크립트 실행, 예약 작업이라는 공통점이 있었다. 외부 서버에서 명령을 받아 실행하는 방식도 비슷했다. 다른 보고서를 찾아보니 Proofpoint에서는 TA406이 KONNI와 BabyShark를 모두 사용했다고 설명하고 있었다. 또 TA406이 TA427의 도구나 코드에 접근했거나 개발 자원을 공유했을 가능성도 제시했다.

이런 내용을 보면 두 활동 사이에 연관성이 있을 가능성은 있다. 하지만 같은 악성코드를 사용한 이력이 있다고 해서, 이번에 비교한 두 사건도 같은 공격자가 일으켰다고 볼 수는 없었다.

인프라도 비교해 보았는데, 자료 A의 도메인 5개와 자료 B의 도메인 1개 중 겹치는 것은 없었다. 자료 A의 `/silver/upload.php`, `/111/alex/expres.php`, `/sil/0304/d.php`와 자료 B의 `/dn.php`도 서로 달랐다. 명령을 받아오는 용도는 비슷했지만, 비교한 도메인과 경로에서는 같은 주소를 다시 사용한 흔적을 찾지 못했다. 두 사건에서 악성코드의 코드가 일치하는지, 같은 공격자 통제 계정을 사용했는지도 이번 조사에서는 확인하지 못했다.

그래서 두 활동 사이의 연관 가능성은 남겨 두고, P와 Q가 같은 공격자라는 결론은 보류했다. 두 공격자가 서로 다르다고 판단한 것은 아니다. 지금까지 찾은 자료로는 둘의 관계를 확정하기 어렵다고 판단했다.

출처: [Huntress 자료 A — IOC 목록 및 본문 분석](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC 자료 B — URL 항목 및 PowerShell 분석](https://asec.ahnlab.com/ko/59625/), [Proofpoint 보고서 — 6–7쪽](https://www.proofpoint.com/us/resources/threat-reports/triple-threat-north-korea-aligned-ta406-scams-spies-and-steals)

---
## 5. 느낀 점

서로 다른 두 자료를 보며, 두 공격자가 같은지 분석해 보는 활동을 처음 해보았다. 매번 자료나 기사를 읽을 때 각자 다른 공격자일 것이라고 무의식중에 생각했었는데, 이번 과제를 하면서 고정관념을 하나 깬 것 같다. 

위협 인텔리전스를 평소에도 잘 활용하려면, 여러 자료를 평소에 많이 읽고, 자료 간의 연결점을 떠올리는 능력이 필요할 것 같다. 그리고 ai를 활용해서 가능성이 있는 자료들을 찾아 연습하다 보면 나중에는 스스로 자료들을 선별해 분석해 볼 수 있을 것이다.
