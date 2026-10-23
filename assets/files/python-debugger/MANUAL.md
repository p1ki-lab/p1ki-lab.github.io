# Python 디버거 사용 매뉴얼

## 구현 전 기능 설계

사용자가 추가 기능으로 `exceptions on|off`를 선택했다. 이 절을 구현 코드보다 먼저 작성한다.

| 항목 | 동작 |
| --- | --- |
| `exceptions on` | 대상의 `exception` 이벤트에서 멈추고 예외 타입과 메시지를 표시한다. 처리되는 예외도 포함한다. |
| `exceptions off` | 예외 이벤트만으로는 멈추지 않는다. 기본값이다. |
| `exceptions` | 현재 설정을 표시한다. |
| 잘못된 인자 | 사용법을 표시하고 현재 설정과 정지 상태를 유지한다. |
| 예외 이후 | 조회 명령을 사용할 수 있다. `continue`로 원래 예외 처리를 이어 간다. 예외를 없애거나 복구하지 않는다. |

## 실행

Windows PowerShell, CPython 3.13에서 이 폴더로 이동한 뒤 실행한다. 표준 라이브러리만 필요하다.

```powershell
python demo.py
```

목적은 로컬 예제 함수의 실행 관찰이다. `(debugger)`에서 명령을 입력한다. 대상 코드와 입력 표현식은 실제 실행되므로 신뢰하는 로컬 코드만 사용한다.

다른 파일에서는 `from debugger import Debugger` 후 `with Debugger():` 안에서 대상 함수를 호출한다. 이미 실행 중인 블록 자체가 아니라 새 함수 호출부터 관찰한다.

## 명령

| 명령 | 동작 |
| --- | --- |
| `help` | 명령 목록 |
| `print [EXPR]` | 선택한 프레임에서 식 평가. 생략하면 지역변수 표시 |
| `list` | 선택한 함수의 소스. `>`는 현재 위치 |
| `step` | 다음 call/line/return 이벤트에서 정지 |
| `continue` | 중단점·감시점·켜진 예외 정지까지 진행 |
| `break [LINE 또는 FUNCTION]` | 현재 파일의 줄 또는 함수 이름 중단점 설정. 생략하면 목록 |
| `delete [LINE 또는 FUNCTION 또는 EXPR]` | 일치하는 설정 삭제. 생략하면 모든 중단점·감시 삭제 |
| `next` | 실제 정지 프레임의 다음 line/return까지 진행. 내부 함수는 실행 |
| `where` | 가장 안쪽 #0부터 호출 스택 표시 |
| `up` / `down` | 관찰 프레임 변경. 실행 위치는 그대로 |
| `until [LINE]` | 실제 정지 프레임에서 기준보다 큰 줄 또는 반환까지 진행. 생략하면 현재 줄 |
| `finish` | 실제 정지 프레임의 return 이벤트에서 정지 |
| `watch EXPR` | 실제 실행 프레임에서 식의 값이 변하면 정지 |
| `exceptions [on 또는 off]` | 추가 기능: 예외 정지 설정 |
| `quit` | 추적을 해제하고 대상은 끝까지 실행. 대상 프로그램을 강제 종료하지 않음 |

조회·설정 명령은 실행하지 않는다. 진행 명령은 `up/down`의 선택과 무관하게 실제 정지 프레임을 기준으로 한다. `next/until/finish` 중에도 중단점·감시점·예외 설정은 우선한다. 줄 중단점은 파일과 줄 번호를 함께 저장한다. 함수 중단점은 이름 또는 qualname과 비교하며 동명 함수가 여러 파일에 있으면 모두 해당한다.

감시는 등록한 시점의 프레임에 연결된다. 미정의 값은 `<undefined>`로 표시하며 정의·소멸도 변화로 취급한다. `repr()` 문자열을 비교하므로 정수와 일반 리스트 변경은 감지하지만, 표현이 같거나 사용자 정의 repr이 내부 상태를 생략하면 놓칠 수 있다. 상위 프레임에서 받은 감시도 해당 프레임에 적용한다.

## 예외 기능 사용 예

`demo.py`에서 `help`, `exceptions on`, `continue`를 입력한다. 예제는 0으로 나누는 오류를 자체 처리한다. `ZeroDivisionError`에서 멈추면 `where`, `print price`, `continue`로 확인한다. 사용자 처리 흐름이 그대로 진행되어 마지막 결과가 출력되어야 한다.

## 검증

```powershell
python -m unittest -v test_debugger.py
```

실제 검증 결과는 `TEST_RESULTS.txt`에 별도로 기록한다. 실행 전에는 통과했다고 간주하지 않는다.

2026-10-18 Windows PowerShell / Python 3.13.3에서 자동 테스트 10개가 통과했다. 기본 조회·단계 실행, 줄·함수 중단점과 삭제, 호출 스택 이동, next/finish/until, 감시와 삭제, 잘못된 명령, EOF·quit, 예외 전파와 추적 복원, exceptions on/off를 확인했다. 모든 입력과 실행 환경에 대한 완전성을 보장하는 결과는 아니다.

`EXAMPLE_SESSION.txt`는 실제 콘솔 실행 기록이다. 예외 정지를 켠 뒤 `calculate()`의 `ZeroDivisionError`에서 정지했고, `price`는 3000, 계속 실행한 최종 결과는 4800.0이었다. 대상이 자체적으로 예외를 처리했으며 디버거가 예외를 제거한 것은 아니다.

참고 원리: [The Debugging Book — How Debuggers Work](https://www.debuggingbook.org/html/Debugger.html). 책과 동일한 소스가 아니라 과제의 명령 요구에 맞춘 별도 교육용 구현이다.

## 한계

단일 스레드의 일반 동기 Python 함수용이다. async, generator, 멀티스레드, C 함수 내부는 지원 범위에서 제외한다. `eval`과 `repr`은 부작용이 있을 수 있다. 소스 파일이 없으면 소스 표시가 불가능하다. 다른 디버거와 중첩 사용하지 않는다. 종료·예외 시 기존 전역 추적 설정은 복원한다. 빈 입력은 다시 명령을 기다리고 EOF는 quit으로 처리한다.

## HTML 예제의 결함 수정 실험

2026-10-22에 책의 따옴표 조건식 결함을 별도 대상 함수로 재현했다. 기존 프로젝트에는 HTML 처리 함수가 없었으며, 기존 `debugger.py`와 할인 예제 `demo.py`는 이 작업에서 변경하지 않았다.

- `html_markup_before.py`: 실험을 위해 추가한 결함 재현본. 수정 전 비교용으로만 사용한다.
- `html_markup.py`: 조건에 괄호를 추가한 수정본. 완전한 HTML 파서나 보안용 HTML 필터가 아니다. 서로 다른 따옴표가 속성 안에서 섞이는 경우는 이번 수정 범위 밖이다.
- `verify_html_fix.py`: 두 모듈을 실제 호출해 기대값과 비교하고, 수정본을 디버거 안에서도 실행한다.
- `test_html_markup.py`: 회귀 입력, 기존 결함 재현, 디버거와의 결합을 검사한다.

```powershell
python verify_html_fix.py
python -m unittest -v test_debugger.py test_html_markup.py
```

두 명령 모두 이 폴더에서 실행한다. 로컬 고정 문자열의 함수 실행이며 파일·네트워크를 변경하지 않는다. 첫 명령은 수정 전 실패 3/7, 수정 후 통과 7/7을 표시한다. 두 번째 명령의 저장된 실행 결과는 총 13개 테스트 통과다. 로그는 `HTML_FIX_RESULTS.txt`, `HTML_FIX_TESTS.txt`에 저장했다. 이 검증으로 모든 HTML 입력의 정확성을 보장하지는 않는다.
