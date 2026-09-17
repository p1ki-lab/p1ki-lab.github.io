---
layout: post
title: "VirusTotal을 이용한 BPFDoor 악성코드 분석"
description: "VirusTotal 공개 정보를 바탕으로 smartadm 파일의 탐지 결과, ELF 정보, 행위 및 연관 정보를 분석한 기록"
date: 2026-09-17
categories: [블로그]
tags: [BPFDoor, "악성코드 분석", VirusTotal, Linux]
---

KISA 보호나라에 공개된 악성코드 중 `smartadm` 파일을 골라 VirusTotal에서 분석해보았다.
파일을 직접 다운로드하거나 실행하지는 않았고, VirusTotal에 공개된 정보만 확인하였다.

```text

파일명: smartadm

SHA-256: 3f6f108db37d18519f47c5e4182e5e33cc795564f286ae770aa03372133d15c4

KISA 공개 크기: 2,067KB

```

---

## 1. 주제 선정 이유

KISA 보호나라에서 공개한 악성코드 목록을 살펴보다가 BPFDoor를 알게 되었다. 최근 동아리 세미나에서 BPF와 관련된 발표를 들었던 것이 떠올라 흥미가 생겼고, 실제 악성코드에서는 BPF가 어떻게 사용되는지 궁금해 이 주제를 선택하였다.

---

## 2. 분석 목표와 범위
### 분석 목표

1. 여러 보안업체가 이 파일을 어떻게 탐지했는지 확인한다.
2. 파일 형식과 아키텍처를 확인한다.
3. 샌드박스에서 관찰된 행위가 있는지 확인한다.
4. IP, 도메인, URL 등 다른 객체와의 관계를 확인한다.
5. 직접 확인한 내용과 확인하지 못한 내용을 나눠서 정리한다.

### 분석 범위

| 구분    | 이번 분석에서 확인한 것               | 제외한 것              |
| ----- | --------------------------- | ------------------ |
| 분석 대상 | KISA에 공개된 해시 1개             | BPFDoor의 모든 변종     |
| 사용 자료 | KISA 공개자료, VirusTotal 공개 결과 | 비공개 CTI, 유료 정보     |
| 파일 취급 | 해시 검색과 공개 정보 확인             | 다운로드, 압축 해제, 직접 실행 |
| 판단 범위 | 탐지명과 파일 정보 비교               | 감염 여부와 공격 주체 확정    |
 

---


## 3. 관련 개념

### VirusTotal
: 여러 보안업체의 파일, URL, 도메인, IP 분석 결과를 모아서 보여주는 서비스이다.
파일의 해시를 검색하면 파일을 직접 실행하지 않고도 기존 분석 결과를 볼 수 있다.

- `Detection`: 보안업체별 탐지 결과

- `Details`: 파일 형식, 크기, 해시 등 기본 정보

- `Behavior`: 샌드박스에서 관찰된 행위

- `Relations`: 파일과 연결된 IP, 도메인, URL, 다른 파일

예를 들어 `37/56`이라면 56개 보안업체 중 37개가 해당 파일을 악성으로 탐지했다는 뜻이다.

> 탐지 수가 많다고 해서 탐지명에 적힌 악성코드 계열과 모든 기능이 바로 확정되는 것은 아니다. 파일 정보와 실제 행위를 같이 확인해야 한다.
> 
### 샌드박스
: 의심스러운 파일을 실제 사용자 환경과 분리된 공간에서 실행한 뒤 어떤 행동을 하는지 기록하는 환경이다.

샌드박스에서는 실행한 프로세스, 생성한 파일, 네트워크 연결, 자동실행 등록 등을 확인할 수 있다.
하지만 악성코드가 특정 운영체제나 권한, 실행 인자, 외부 신호를 필요로 하면 샌드박스에서 제대로 동작하지 않을 수도 있다. 따라서 결과가 보이지 않는다고 해서 악성 행위가 없다고 판단하면 안 된다.

  
### BPF
: BPF(Berkeley Packet Filter)는 네트워크 인터페이스로 들어오는 패킷 중에서 조건에 맞는 패킷을 골라내는 기술이다.
`tcpdump` 같은 정상적인 패킷 분석 도구에서도 사용한다. 따라서 BPF를 사용한다는 이유만으로 악성 프로그램이라고 판단할 수는 없다.

중요한 것은 어떤 프로세스가 어떤 패킷을 기다리고, 조건에 맞는 패킷을 받은 뒤 어떤 동작을 하는지이다.

### BPFDoor
: Linux 시스템에서 동작하며 공격자가 시스템에 다시 접근할 수 있게 하는 백도어 악성코드이다.

일반적인 서버 프로그램처럼 항상 특정 포트를 열어두는 방식이 아니라, 특정 형태의 패킷을 신호로 사용할 수 있다. 그래서 열린 포트만 확인해서는 발견하지 못할 가능성이 있다.

>BPFDoor라는 이름에 BPF가 들어가지만 BPF를 사용하는 모든 프로그램이 BPFDoor인 것은 아니다.

  

### RAW 소켓
: 일반적인 TCP·UDP 애플리케이션보다 낮은 수준에서 네트워크 패킷을 다룰 수 있게 해주는 소켓이다.

>RAW 소켓도 네트워크 분석이나 보안 도구에서 정상적으로 사용된다. 따라서 RAW 소켓 사용 여부 하나만으로 악성코드라고 판단할 수 없다.



---

## 4. 분석 과정


VirusTotal의 `Detection` 탭을 먼저 확인하였다.

![VirusTotal 탐지 비율 요약](/assets/img/posts/bpfdoor-virustotal-analysis/detection-summary.png)
전체 56개 보안업체 중 37개가 이 파일을 악성으로 탐지했다.
 

![VirusTotal 보안업체별 탐지 결과](/assets/img/posts/bpfdoor-virustotal-analysis/detection-vendors.png)

| 항목                      | 관찰 결과                                                                                |
| ----------------------- | ------------------------------------------------------------------------------------ |
| 전체 탐지 비율                | 37/56                                                                                |
| 공통 계열명                  | BPFDoor                                                                              |
| `Backdoor` 포함 탐지명       | AhnLab-V3: `Backdoor/Linux.BPFDoor.2116536`, Microsoft: `Backdoor:Linux/BPFDoor!MSR` |
| `Linux` 또는 `ELF` 포함 탐지명 | Elastic: `Linux.Trojan.BPFDoor`, CTX: `Elf.trojan.bpfdoor`                           |
| 다른 계열명                  | AliCloud: `Backdoor:Linux/Multiverze.Gen`                                            |
| 확인 시각                   | 2026년 9월 17일 10시 12분 KST                                                             |
업체마다 탐지명은 달랐지만 `BPFDoor`라는 이름이 반복해서 나타났다.
탐지명을 나눠보면 다음과 같다.  

```text

기능: Backdoor 또는 Trojan

대상 운영체제: Linux

파일 형식: ELF

공통 계열명: BPFDoor

업체별 표기: MSR, 2116536, 50 등

```

여러 업체가 이 파일을 Linux에서 동작하는 BPFDoor 계열 백도어로 보고 있다는 것을 알 수 있었다.


`Details` 탭에서 Basic properties와 ELF Info를 확인하였다.

![VirusTotal Basic properties 정보](/assets/img/posts/bpfdoor-virustotal-analysis/basic-properties.png)

![VirusTotal ELF Info 정보](/assets/img/posts/bpfdoor-virustotal-analysis/elf-info.png)

| 확인 항목 | 관찰 결과 | 이 정보가 필요한 이유 |
|---|---|---|
| 파일 형식 | ELF64 실행 파일 | 실행 대상 운영체제 확인 |
| 아키텍처 | x86-64(AMD64) 64비트 | 실행 가능한 CPU 환경 확인 |
| 파일 크기 | 2.02MB(2,116,536바이트) | 다른 변종·복사본과 비교 |
| 매직/헤더 | `ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked` | 확장자가 아닌 실제 형식 확인 |
| 인터프리터 | `/lib64/ld-linux-x86-64.so.2` | Linux 동적 실행 파일인지 확인 |
| 서명 정보 | 공개 화면에서 확인하지 못함 | 배포 주체와 무결성 판단 보조 |
| 의미 있는 문자열 | 공개 Details 화면에서 확인하지 못함 | 경로·명령어·통신 단서 확인 |
| 패커 여부 | 공개 화면에서 확인하지 못함 | 난독화 여부 확인 |
먼저 `ELF64`, `x86-64`, 인터프리터 경로를 보고 Linux x86-64 환경에서 실행되는 파일이라고 판단했다. Detection 탭에서 확인한 `Linux`, `ELF`라는 탐지명과도 맞았다.

서명, 문자열, 패커 여부는 공개 화면에서 찾지 못했다. 
  

`Behavior` 탭에서 프로세스, 파일, 자동실행, 환경변수 정보를 찾았다.

| 분류 | 관찰 결과 | BPFDoor 관련성 |
|---|---|---|
| 생성·실행 프로세스 | 공개 화면에서 확인하지 못함 | 프로세스 위장 여부 확인 불가 |
| 생성·수정 파일 | 공개 화면에서 확인하지 못함 | 뮤텍스·락 파일 흔적 확인 불가 |
| 자동실행·지속성 | 공개 화면에서 확인하지 못함 | 재부팅 후 실행 여부 확인 불가 |
| 환경변수 | 공개 화면에서 확인하지 못함 | 환경변수 변경 여부 확인 불가 |

이번 결과에서는 파일의 기본 구조는 확인할 수 있었지만 실제 실행 행위는 확인하지 못했다.
  
마지막으로 `Relations` 탭을 확인하였다.

| 확인 항목 | 관찰 결과 |
|---|---|
| Contacted IP addresses | 공개 관계 정보 확인 불가 |
| Contacted domains | 공개 관계 정보 확인 불가 |
| Contacted URLs | 공개 관계 정보 확인 불가 |
| Embedded URLs | 공개 관계 정보 확인 불가 |
| Execution parents | 공개 관계 정보 확인 불가 |
| Dropped files | 공개 관계 정보 확인 불가 |
| Bundled files | 공개 관계 정보 확인 불가 |
| 관련 파일·변종 | Relations 정보만으로 확인 불가 |

  

구체적인 IP, 도메인, URL 또는 관련 파일은 확인하지 못했다.

  

> Relations에 정보가 없다고 해서 네트워크 통신이나 파일 생성 행위가 없었다고 단정할 수는 없다. 공개된 분석 결과가 없거나 접근할 수 있는 정보가 제한됐을 가능성도 있다.

  

KISA 공지에는 공격에 악용된 IP `165.232.174[.]130`도 같이 공개되어 있다. 하지만 VirusTotal에서 이 파일과 해당 IP가 직접 연결된 것은 확인하지 못했다. 따라서 이 IP를 파일이 실제로 통신한 주소라고 적지는 않았다.

  

---

  

## 5. 결론

  

`smartadm` 파일은 Linux x86-64 환경에서 실행되는 64비트 ELF 파일이다.

VirusTotal에서는 56개 업체 중 37개가 악성으로 탐지했고, 여러 업체의 탐지명에서 `BPFDoor`가 반복되었다. 파일 형식도 Linux 실행 파일과 일치했기 때문에 BPFDoor 계열 백도어일 가능성이 높다고 판단하였다.

하지만 실제 실행 과정에서 어떤 프로세스를 만들었는지, 파일을 생성했는지, RAW 소켓을 사용했는지, 외부 IP와 통신했는지는 확인하지 못했다.

이번 분석을 하면서 탐지명과 실제 행위는 따로 봐야 한다는 것을 알게 되었다.

> 여러 보안업체의 탐지명과 ELF 정보를 종합하면 `smartadm`은 Linux용 BPFDoor 계열 백도어일 가능성이 높다. 다만 VirusTotal의 공개 정보만 사용했기 때문에 구체적인 실행 행위와 네트워크 통신은 확인하지 못했다.


---

  

## 6. 참고 자료

### 공식 자료
1. KISA 보호나라,  

   [최근 해킹공격에 악용된 악성코드, IP 등 위협정보 공유 및 주의 안내](https://www.boho.or.kr/kr/bbs/view.do?bbsId=B0000133&menuNo=205020&nttId=71726)  

2. VirusTotal,  

   [`smartadm` Detection 결과](https://www.virustotal.com/gui/file/3f6f108db37d18519f47c5e4182e5e33cc795564f286ae770aa03372133d15c4/detection)  

3. VirusTotal,  

   [`smartadm` Details 결과](https://www.virustotal.com/gui/file/3f6f108db37d18519f47c5e4182e5e33cc795564f286ae770aa03372133d15c4/details)  
  
4. VirusTotal,  

   [`smartadm` Behavior 결과](https://www.virustotal.com/gui/file/3f6f108db37d18519f47c5e4182e5e33cc795564f286ae770aa03372133d15c4/behavior)  

5. VirusTotal,  

   [`smartadm` Relations 결과](https://www.virustotal.com/gui/file/3f6f108db37d18519f47c5e4182e5e33cc795564f286ae770aa03372133d15c4/relations)  

6. VirusTotal 공식 문서,  

   [File relationships](https://gtidocs.virustotal.com/reference/files-relationships)  

### AI 활용

- OpenAI ChatGPT
  - VirusTotal 분석 순서를 정리하는 데 사용하였다.
  - 탐지명에 포함된 기능, 운영체제, 파일 형식과 계열명을 구분하는 데 참고하였다.
  - 표 구성 틀을 제공받았다.
