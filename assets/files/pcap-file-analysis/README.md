# PCAP 미션 실행 안내

## 환경과 범위
- 확인 환경: Windows 11, PowerShell, Python 3.13.3, dpkt 1.9.8, TShark 4.6.9.
- classic PCAP 2.4 / Ethernet II / 조각화되지 않은 IPv4 / TCP·UDP·ICMP를 분석한다.
- PCAPNG와 Ethernet 이외의 링크 형식은 파일 오류로 거부한다.
- IPv6·ARP·VLAN 등 미지원 EtherType, IPv4 조각과 기타 IP 프로토콜은 OTHER로 집계한다.
- 체크섬 검증, TCP 스트림 재조립, 응용 프로토콜 분석은 수행하지 않는다.
- 각 기록을 순차 읽되 출력과 통계를 위해 분석 결과는 메모리에 보관한다. 대용량 파일용은 아니다.
- 최대 허용 패킷 크기는 16 MiB다. 캡처 길이가 원래 길이보다 짧으면 ERROR로 기록한다.

## 직접 실행
작업 폴더에서 PowerShell로 실행한다. 가상환경과 dpkt는 준비되어 있다.

```powershell
& .\.venv\Scripts\python.exe analyze.py demo.pcap
& .\.venv\Scripts\python.exe check.py
```

첫 명령은 샘플을 읽어 각 패킷의 필드와 통계를 출력한다. 네트워크로 전송하지 않는다.
둘째 명령은 설치된 TShark로 대표 필드와 전체 프레임 수를 비교하고 잘린 파일 및 PCAPNG 거부를 확인한다.
검증 시 tshark_fields.tsv를 덮어쓰고 작업 폴더에 임시 파일을 생성한 후 제거한다.

예상 통계(샘플 기준): `TOTAL=8 TCP=3 UDP=2 ICMP=2 OTHER=1 ERROR=0`.
실제 실행 증거는 actual_output.txt, check_result.txt, tshark_fields.tsv에 저장했다.
ERROR=0은 이 샘플에서 검출된 파싱 오류가 없다는 뜻이며, 모든 입력에 대한 정확성 보장이 아니다.

샘플 재생성이 필요하면 다음을 실행한다. 기존 demo.pcap을 덮어쓴다.

```powershell
& .\.venv\Scripts\python.exe make_sample.py
```

## 샘플과 집계 기준
demo.pcap은 로컬 생성 합성 트래픽이며 실제 서비스 캡처가 아니다.
- 패킷 1~3: TCP 연결 수립 형태를 학습할 사례.
- 패킷 4~5: UDP 양방향 데이터 사례.
- 패킷 6~7: ICMP Echo 요청과 응답 사례.
- 패킷 8: ARP를 OTHER로 처리하는 범위 경계 사례.

각 PCAP 기록을 정확히 하나의 TCP/UDP/ICMP/OTHER/ERROR로 분류한다.
따라서 TOTAL은 이 다섯 항목의 합이다. OTHER는 미지원, ERROR는 불완전하거나 잘못된 패킷이다.
프레임 전체보다 앞서 끊긴 파일 구조 오류는 FILE ERROR로 실행을 종료하며 성공 통계를 출력하지 않는다.
포트 443이라는 사실만으로 HTTPS나 암호화 통신이 확인된 것은 아니다.

## 코드 읽기 순서
analyze.py의 read_packets → parse_packet → analyze → main 순서로 확인한다.
PCAP 기록 헤더는 직접 읽고 프로토콜 헤더 객체 해석에는 dpkt를 사용한다.

## 블로그 목차 — 본문은 직접 작성
1. 미션 목표와 구현 범위
2. PCAP과 패킷 구조 이해
3. 프로그램 구현 흐름
4. 실행 결과와 통신 해석
5. 프로토콜별 통계와 검증
6. 한계와 배운 점 및 AI 활용 범위

## 참고 원문
- dpkt: https://dpkt.readthedocs.io/en/latest/
- PCAP 형식: https://www.tcpdump.org/manpages/pcap-savefile.5.html
- IPv4: https://www.rfc-editor.org/rfc/rfc791
- TCP: https://www.rfc-editor.org/rfc/rfc9293
- UDP: https://www.rfc-editor.org/rfc/rfc768
- ICMP: https://www.rfc-editor.org/rfc/rfc792
