---
layout: post
title: "Threat Intelligence: BABYSHARK와 Konni의 관계 비교"
date: 2026-10-30 00:00:00 +0900
categories: [블로그]
tags: [Threat Intelligence, BABYSHARK, Konni, APT]
---

**Threat Intelligence(위협 인텔리전스)** 는 사이버 위협에 관한 정보를 수집·분석해, 보안 판단과 대응에 활용할 수 있도록 만든 증거 기반의 지식이다.

이번 포스트에서는 아래 두 보고서에서 등장하는 두 공격자가 서로 어떤 관계가 있는지 구체적인 비교 기준을 세운 뒤 비교해보았다.

자료 A는 Huntress의 BABYSHARK 침해 사고 분석이고, 자료 B는 AhnLab ASEC의 Konni 피싱 메일 분석이다. 편의상 자료 A의 공격자를 P, 자료 B의 공격자를 Q라고 두었다.

자료 A — [https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood "https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood")   
자료 B — [https://asec.ahnlab.com/ko/59625/](https://asec.ahnlab.com/ko/59625/ "https://asec.ahnlab.com/ko/59625/")

---
## 1. 두 공격자의 관계를 판단할 기준

### 1-1. 비교 기준

먼저 사용한 악성코드, 공격 방식, 인프라, 활동 시기를 기준으로 정했다.

인프라 : 공격에 사용한 서버·도메인·계정 등의 자원. 

| 비교 기준      | 확인할 내용                         | 관계를 판단할 때 살펴볼 점                   |
| ---------- | ------------------------------ | --------------------------------- |
| 악성코드와 구현   | 고유 문자열, 설정값, 복호화 방식, 코드 중복     | 같은 기능인지, 같은 코드가 재사용된 것인지 구분       |
| 공격 방식      | 유인 내용, 실행 순서, 예약 작업, 명령과 저장 경로 | 일반적인 기법보다 구체적인 구현과 반복되는 운영 습관에 주목 |
| 인프라        | 도메인, URL 경로, IP, 계정과 인증 정보     | 같은 서비스 이용인지, 통제 자원의 재사용인지 확인      |
| 활동 시기      | 실제 공격·사용 시점과 보고서 발행 시점         | 도구와 자원의 사용이 시간상 어떻게 이어지는지 비교      |
| 추가 보고서의 분류 | 기관이 활동을 묶거나 나눈 근거              | 같은 이름이 같은 범위의 활동을 가리키는지 확인        |

---
### 1-2. 이런 기준을 세운 이유

Proofpoint는 행위자를 구분할 때 표적, 계정 사용, 인프라, 악성 도구, 운영자의 행동 등을 함께 살펴본다고 설명한다. ESRC도 코드 유사도와 공격 전술, 침투 대상, 인프라, 언어 습관 등을 종합해 조직을 분류한다고 밝혔다.

비교할 관계는 세 가지로 나눴다. 같은 운영 주체인지, 다른 운영 주체가 도구나 개발 자원을 공유한 것인지, 아니면 흔히 쓰이는 기법만 겹치는지를 살펴보았다.

출처: [Proofpoint — Triple Threat, 5쪽](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-threat-insight-paper-triple-threat-N-Korea-aligned-TA406-steals-scams-spies.pdf#page=5), [ESRC — Konni를 Thallium으로 통합 분류](https://blog.alyac.co.kr/3558)

---
## 2. 최초 명명 자료 분석석

### 2-1. 자료 A

Huntress는 BABYSHARK를 북한 관련 공격자가 사용하는 악성코드 계열로 설명한다. 따라서 BABYSHARK가 곧 P의 그룹명인 것은 아니다. P는 자료 A의 사건에서 이 악성코드를 사용한 공격자이다.

최초 명명 자료는 Unit 42가 2019년 2월 22일 공개한 「New BabyShark Malware Targets U.S. National Security Think Tanks」이다. 보고서에서는 2018년 11월 발송된 표적 피싱 메일을 조사하다가 새 VBScript 기반 악성코드를 발견하고 BabyShark라고 명명했다고 설명한다.

*표적 피싱 : 특정 인물이나 조직에 맞춰 내용을 꾸민 피싱.*

당시 메일은 핵 안보 전문가를 사칭했으며 악성 매크로가 포함된 Excel 문서를 첨부했다. 악성코드는 시스템 정보를 외부 서버로 보내고, 재실행될 수 있도록 설정한 뒤 추가 명령을 기다렸다. 이 자료에서 처음 이름을 붙인 대상은 운영 조직이 아니라 악성코드였다.

출처: [Unit 42 — BabyShark 최초 명명 보고서](https://unit42.paloaltonetworks.com/new-babyshark-malware-targets-u-s-national-security-think-tanks/)

---

### 2-2. 자료 B

KONNI라는 이름은 Cisco Talos가 2017년 5월 3일 공개한 「KONNI: A Malware Under The Radar For Years」에서 확인했다. Talos는 파일 탈취, 키 입력 수집, 화면 캡처, 임의 코드 실행 기능을 가진 악성코드를 KONNI라고 명명했다. 보고서가 추적한 사례는 2014년부터 2017년까지 이어졌으며, 초기 정보 탈취 기능에서 원격 제어 기능으로 발전한 과정을 설명한다.

그렇다면 자료 B에서는 왜 Konni를 공격 그룹이라고 부르는가. Unit 42의 「The Fractured Statue Campaign」에는 명칭이 확장된 배경이 나온다. 이후 Konni RAT를 사용하지 않으면서 기존 활동과 전술·기술·절차(TTP)가 상당히 겹치는 캠페인들이 나타나자, 일부 연구자들이 그 활동의 배후를 Konni라고 부르기 시작했다.

*RAT : 감염된 컴퓨터를 원격으로 제어하는 악성코드.*
*TTP : 공격자가 사용하는 전술·기술·절차를 묶어 부르는 말.*

처음에는 악성코드명이었던 Konni가 관련 활동의 배후를 가리키는 이름으로도 쓰이게 된 것이다. Q는 자료 B에서 ASEC가 Konni로 분류한 공격자라는 의미로 사용했다.

출처: [Cisco Talos — KONNI 최초 명명 보고서](https://blog.talosintelligence.com/konni-malware-under-radar-for-years/), [Unit 42 — Konni: Malware or Actor?](https://unit42.paloaltonetworks.com/the-fractured-statue-campaign-u-s-government-targeted-in-spear-phishing-attacks/)

---
## 3.  두 사건 비교

### 3-1. 공격 흐름과 구현

자료 A는 VOA 기자를 사칭해 대화를 이어간 뒤 문서 검토를 요청한 사례이고, 자료 B는 개인정보 유출 자료로 위장한 EXE를 유포한 사례이다. 사용자에게 문서를 보여주면서 악성 행위를 수행한다는 점은 비슷했지만, 실행 출발점과 스크립트 구성은 달랐다.

| 비교 항목 | 자료 A: P | 자료 B: Q |
|---|---|---|
| 실행 출발점 | 악성 매크로가 포함된 Word 문서 | 악성 EXE |
| 스크립트 | `qwert.vbs` 등 VBScript | JSE와 PowerShell |
| 예약 작업 이름 | `GoogleUpdater` | `WindowsHotfixUpdate[B409302303-02940492024]` |
| 후속 처리의 특징 | Google Drive 페이지의 파일명에 포함된 데이터를 `johnbegin`·`johnend`로 구분 | PowerShell로 명령을 받고 별도 JSE가 복호화해 XML 형태로 로드 |

두 사건 모두 정상 업데이트처럼 보이는 작업 이름을 사용했다. 다만 표에 정리한 작업 이름과 후속 처리 방식은 서로 달랐다.

출처: [Huntress — Right of Boom and Backwards / Lures and Phishbait](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC — 파일 생성 및 스크립트 분석](https://asec.ahnlab.com/ko/59625/)

---
### 3-2. 인프라와 통신

공개된 IOC 중에서는 통신에 사용된 도메인과 URL 경로를 비교했다. 

>주소는 실수로 접속하지 않도록 점을 `[.]`으로 표시했다.

*IOC : 침해 여부를 확인하는 데 사용하는 파일 해시나 주소 등의 지표.*

| 자료 | 공개된 도메인 |
|---|---|
| A | `retmodul[.]com`, `hodbeast[.]com`, `worldinfocontact[.]club`, `frebough[.]com`, `beastmodser[.]club` |
| B | `gjdow[.]atwebpages[.]com` |

자료 A의 Following Breadcrumbs 에서는 수집한 정보를`/silver/upload.php`로 POST 전송하고, `/111/alex/expres.php?op=2`에 주기적으로 접속해 명령을 받아 실행한다고 설명한다. 

자료 B에서는 `WindowsHotfixUpdate.ps1`이 C2에서 명령을 받아온다고 설명하며, URL 항목에 `/dn.php?name=[Computer`를 공개했다. 두 보고서에 나온 도메인과 경로를 직접 대조해 보니 일치하는 주소는 없었다.

*C2 : 공격자가 명령을 전달하거나 정보를 받는 데 사용하는 서버 또는 통신 체계.*

출처: [Huntress — Following Breadcrumbs / IOC 목록](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ASEC — PowerShell 분석 및 URL 항목](https://asec.ahnlab.com/ko/59625/)

---
## 4. 추가 연결 근거

### 4-1. ESRC

ESRC의 2019년 6월 10일 보고서는 Konni와 Thallium(Kimsuky)의 공통점을 직접 분석한다. 보고서에는 Konni 사례와 Kimsuky의 Cobra Venom 사례 사이에서 파일뿐 아니라 설정과 구현도 겹친다고 나와 있다.

| 연결 근거 | 보고서에서 설명한 내용 |
|---|---|
| 파일과 설정 | `ChromSrch.egg_`, 내부 `ChromSrch.dat`, 압축 설정 암호의 일치 |
| 실행 및 복호화 구현 | `insrchmdl` 인자와 디코딩 루틴의 일치 |
| 운영 기록 | Konni 관련 메일 헤더와 Kimsuky 관련 거래소 로그인 이력의 동일 IP |

보고서에 나온 `202.168.155[.]156`은 메일 헤더의 `X-EN-OrigIP`와 거래소 로그인 이력에서 나온 주소이다. 

ESRC는 이후 2021년 2월 3일 글에서 Konni를 Thallium으로 통합 분류하고, 앞으로 Thallium이라는 대표명을 사용하겠다고 밝혔다. 2019년의 공통점 분석이 후속 분류로 이어진 것이다.

출처: [ESRC — Konni와 Thallium(Kimsuky) 조직의 공통점 발견](https://blog.alyac.co.kr/2347)
	 [ESRC — Konni 조직을 Thallium으로 통합 분류](https://blog.alyac.co.kr/3558)

---
### 4-2. Proofpoint

Proofpoint의 2021년 11월 보고서에서는 넓게 Kimsuky로 알려진 활동을 TA406·TA408·TA427로 나누어 추적한다. TA406의 도구 목록에는 KONNI와 BabyShark가 함께 나온다.

사용 시점을 보면 TA427은 늦어도 2018년 11월 BabyShark를 사용했고, TA406은 적어도 2019년 초부터 접근할 수 있었다. Proofpoint는 TA406의 사용이 2019년 중후반 중단됐을 가능성을 제시하면서, TA427의 사용은 2021년 10월에도 관찰했다고 설명한다. 이 사용 이력을 바탕으로 TA406의 TA427 도구·코드 접근 또는 개발 자원 공유를 연결 가설로 제시했다.

7쪽에는 TA427이 인터뷰나 질문으로 대화를 시작한 뒤 수정한 내용을 검토해 달라며 악성 링크나 첨부파일을 보내는 방식도 나온다. 자료 A의 기자 사칭과 문서 검토 요청은 이 설명과 닮아 있다. 

출처: [Proofpoint — Triple Threat, 5~7쪽](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-threat-insight-paper-triple-threat-N-Korea-aligned-TA406-steals-scams-spies.pdf#page=5)

---
### 4-3. ESET

ESET의 T2 2022 보고서는 2022년 5~8월 활동을 다루며, Kimsuky 항목에서 6월 홍콩 금융회사 공격을 BabyShark cluster의 장기 캠페인 일부로 설명한다. Konni 항목에서는 변조된 Sumatra PDF 뷰어를 이용한 외교 분야 공격을 소개했다.

*cluster : 관련 있다고 보고 묶어 추적하는 활동 집합.*

ESRC는 통합 분류를 발표했고 Proofpoint는 더 세부적인 행위자를 나눴으며, ESET은 두 활동을 별도 항목에 배치했다. 

출처: [ESET — APT Activity Report T2 2022, 3·10쪽](https://web-assets.eset.com/fileadmin/ESET/INT/B2B_Resource_centrum/Reports/T2-2022_APT-Activity-Report.pdf#page=10)

---
## 5. 활동 시기 정리

보고서 발행일과 실제 활동 시점을 나누어 정리했다. 

| 활동·관찰 시점        | 내용                               | 근거 자료                                                                                                                                                                                                                                                                                             |
| --------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2014~2017년      | Talos가 최초 보고서에서 추적한 KONNI 캠페인    | Talos                                                                                                                                                                                                                  |
| 2018년 11월       | 초기 BabyShark 유포 메일, TA427의 사용 이력 | Unit 42, Proofpoint 7쪽 |
| 적어도 2019년 초     | TA406의 BabyShark 접근              | Proofpoint 6쪽                                                                                                                  |
| 2018~2019년 사례   | ESRC가 코드·설정·운영 기록의 연결을 분석        | ESRC 2019년 보고서                                                                                                                                                                                                                                                   |
| 2021년 3월        | Huntress가 자료 A에서 찾은 가장 이른 침해 지표  | 자료 A                                                                                                                                                                                                            |
| 2022년 5~8월      | ESET 보고서의 활동 관찰 기간               | ESET                                                                                                                                                                               |
| 2023년 12월 6일 공개 | ASEC의 자료 B. 본문은 최근 유포 사례로 설명     | 자료 B                                                                                                                                                                                                                                                         |

출처: [Talos](https://blog.talosintelligence.com/konni-malware-under-radar-for-years/), [Unit 42](https://unit42.paloaltonetworks.com/new-babyshark-malware-targets-u-s-national-security-think-tanks/), [Proofpoint 7쪽](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-threat-insight-paper-triple-threat-N-Korea-aligned-TA406-steals-scams-spies.pdf#page=7), [Proofpoint 6쪽](https://www.proofpoint.com/sites/default/files/threat-reports/pfpt-us-tr-threat-insight-paper-triple-threat-N-Korea-aligned-TA406-steals-scams-spies.pdf#page=6), [ESRC 2019년 보고서](https://blog.alyac.co.kr/2347), [자료 A](https://www.huntress.com/blog/targeted-apt-activity-babyshark-is-out-for-blood), [ESET](https://web-assets.eset.com/fileadmin/ESET/INT/B2B_Resource_centrum/Reports/T2-2022_APT-Activity-Report.pdf), [자료 B](https://asec.ahnlab.com/ko/59625/)

---

## 6. 두 공격자의 관계에 대한 내 판단

결론부터 말하자면, 내가 조사한 자료에서는 P와 Q가 같은 공격자라고 판단할 만한 직접적인 근거를 찾지 못했다. 두 사건 모두 미끼 문서, 스크립트, 예약 작업을 사용했지만 세부 구현은 달랐고, 공개된 도메인과 경로에도 겹치는 부분이 없었다.

ESRC 보고서에는 과거 Konni와 Kimsuky 관련 사례에서 코드·설정과 운영 기록에 공통점이 있었다고 나와 있다. 또한 Proofpoint에 따르면 TA406은 KONNI와 BabyShark를 모두 사용했고, TA427의 도구·코드에 접근했거나 개발 자원을 공유했을 가능성이 있다고 적혀 있었다. 

따라서, 추가 보고서에서는 코드나 도구를 공유한 흔적이 나왔지만, 내가 비교한 두 사건에서는 같은 구현이나 주소를 사용한 흔적을 찾지 못했다. 그래서 이번 자료 분석 결과로는 P와 Q가 같은 공격자라고 단정 지을 수 없다. 

---
## 7. 느낀 점

서로 다른 두 자료를 보며, 두 공격자가 같은지 분석해 보는 활동을 처음 해보았다. 매번 자료나 기사를 읽을 때 각자 다른 공격자일 것이라고 무의식중에 생각했었는데, 이번 과제를 하면서 고정관념을 하나 깬 것 같다. 

위협 인텔리전스를 평소에도 잘 활용하려면, 여러 자료를 평소에 많이 읽고, 자료 간의 연결점을 떠올리는 능력이 필요할 것 같다. 그리고 ai를 활용해서 가능성이 있는 자료들을 찾아 연습하다 보면 나중에는 스스로 자료들을 선별해 분석해 볼 수 있을 것이다.
