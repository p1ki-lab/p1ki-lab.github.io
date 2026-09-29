---
layout: post
math: true
title: "KOI 맛집 추천 문제 풀이와 코드 분석"
description: "트리 DP의 경계값, Frontier 자료구조, 자식 서브트리 병합 최적화를 정리한 학습 기록"
date: 2026-09-29
categories: [블로그]
tags: [KOI, 트리-DP, 문제풀이, C++]
---

## 학습 목표와 결과

 목표는 핵심 알고리즘을 설명하고, 중요한 전이를 의사코드로 작성하고, AI가 생성한 코드를 검증하는 것이다. C++의 모든 줄을 직접 작성하거나 이해하는 것을 목표로 잡지는 않았다.

---
## 1. 문제 이해 과정

도시 $N$개와 길 $N-1$개가 트리를 이룬다. $i$번 맛집은 도시 $c_i$에 있고, 배달 가능 거리 $d_i$와 선호도 $g_i$를 가진다. 두 도시 사이에 지나는 길의 수를 $\operatorname{dist}(a,b)$라고 하면, 맛집 $i$의 배달 가능 도시 집합은 다음과 같다.

$$
R_i=\{j\mid \operatorname{dist}(c_i,j)\le d_i\}
$$

맛집 집합 $S$를 골랐을 때, 서로 다른 두 맛집의 배달 구역이 한 도시라도 겹치면 안 된다. 정확한 조건은 **각 $R_i$가 공집합이라는 뜻이 아니라**, 두 집합의 **교집합**이 공집합이라는 뜻이다.

$$
\forall i\ne j\in S,\qquad R_i\cap R_j=\varnothing
$$

이 조건을 만족하는 선택 중 $\sum_{i\in S}g_i$가 최대가 되도록 한다.

### 배달 구역이 겹치는 조건

두 중심 사이 거리를 $L$, 배달 거리를 $r_A,r_B$라고 하면, 트리에서 두 구역이 겹치지 않는 조건은 다음과 같다.

$$
L>r_A+r_B\qquad\Longleftrightarrow\qquad L\ge r_A+r_B+1
$$

거리는 정수이므로 두 표현은 같다. $L=r_A+r_B$이면 경로 위에서 두 배달 구역이 한 도시를 공유한다.

공부하면서 “중심 사이 거리는 각 맛집마다 다르지 않나?”라는 의문이 들었다. $L$은 맛집 하나의 거리가 아니라 **A와 B라는 두 맛집의 쌍**에 대해 정해지는 거리다. $\operatorname{dist}(c_A,c_B)=\operatorname{dist}(c_B,c_A)$이므로 어느 쪽에서 재도 값은 같다.

> **예시** 예시
> 도시가 `1—2—3—4—5` 순서로 이어져 있다.
>
> A가 도시 2에서 거리 1까지 배달하면 $R_A=\{1,2,3\}$이다. B가 도시 5에서 거리 0까지 배달하면 $R_B=\{5\}$이므로 두 구역은 겹치지 않는다.
>
> B를 도시 4로 옮기고 배달 거리를 1로 바꾸면 $R_B=\{3,4,5\}$가 된다. 이때는 도시 3이 두 집합에 모두 들어가므로 겹친다. 중심 거리 2가 두 배달 거리의 합 2와 같은 경우다.

---
## 2. 서브트리 요약

트리에 루트를 정하고, $\operatorname{depth}(x)$를 루트에서 도시 $x$까지의 거리라고 하자. 맛집 $i$의 **중심 깊이 − 배달 거리**는 그 배달 구역이 루트 방향으로 얼마나 뻗는지를 나타내는 경계값이다. 서브트리에서 여러 맛집을 선택했다면 가장 작게 나온 경계값이 바깥 맛집과의 충돌 판단에 가장 까다롭다.

$$
h(S)=\min_{i\in S}\bigl(\operatorname{depth}(c_i)-r_i\bigr)
$$

예를 들어 맛집 A의 중심 깊이가 5이고 배달 거리가 2라면 경계값은 3이다. B의 중심 깊이가 7이고 배달 거리가 1이라면 경계값은 6이다. 함께 선택한 상태는 $h=\min(3,6)=3$으로 요약된다. 바깥쪽 맛집은 A와의 충돌을 먼저 조심해야 하기 때문이다.

### DP 값의 의미

내가 이해한 뜻은 다음과 같다.

$$
dp[u][x]
=\text{정점 }u\text{의 서브트리에서 경계값이 }x\text{ 이상인 선택의 최대 선호도 합}
$$

$u$는 도시이고, $D=\operatorname{depth}(u)$는 그 도시의 깊이다. 아무 맛집도 고르지 않은 선택의 점수는 0이고, 어떤 바깥 맛집과도 충돌하지 않는다.

**경계값 하나만 저장하면 되는 것은 아니다.** 다음 두 선택은 모두 필요할 수 있다.

| 선택 | 경계값 $h$ | 선호도 합 |
|---|---:|---:|
| X | 3 | 20 |
| Y | 6 | 12 |

X는 점수가 높지만, Y는 바깥 맛집과 합칠 수 있는 조건이 더 넓다.
이렇게 서로 장단점이 있어 남겨야 하는 상태들의 경계를 **파레토 프런티어(Pareto frontier)** 라고 한다.

반대로 P가 `(경계 3, 점수 10)`, Q가 `(경계 6, 점수 12)`라면 P는 버려도 된다. Q가 점수와 경계값 모두에서 P보다 낫기 때문이다. 

> 처음에는 `(경계 3, 점수 10)`인 A와 `(경계 7, 점수 3)`인 B 중 점수가 낮은 B를 버려도 된다고 생각했다. 하지만 B만 바깥 맛집과 합칠 수 있는 상황이 가능하다. 한쪽은 점수가 높고 다른 쪽은 경계가 높으므로, 이 두 상태는 모두 남겨야 한다.

---
## 3. 현재 도시의 맛집을 선택하는 전이

현재 도시 $u$의 깊이를 $D$, 새로 선택할 맛집의 배달 거리를 $r$, 선호도를 $g$라고 하자. 새 맛집은 자식 방향으로 깊이 $D+r$까지 닿을 수 있다. 기존 선택의 경계값은 적어도 한 칸 더 아래인 $D+r+1$이어야 구역이 겹치지 않는다.

새 맛집 자체가 루트 방향으로 뻗는 경계는 $D-r$이다. 기존 선택의 경계가 $D+r+1$ 이상이라면, 새 맛집을 추가한 선택의 경계값은 $D-r$가 된다.

```
u에 있는 각 맛집 (배달 거리 r, 선호도 g)에 대해:
    기존_선호도 = DP_조회(u, D+r+1)
    새_경계값 = D-r
    DP_갱신(u, 새_경계값, 기존_선호도+g)
```

> **예시** $D=4$, $r=1$일 때
> 새 맛집은 깊이 5까지 배달한다. 따라서 기존 선택의 경계값은 최소 6이어야 한다. 새 맛집의 루트 방향 경계는 $4-1=3$이므로, 선택 후의 경계값은 3이다.

---
## 4. 서로 다른 자식 서브트리 합치기

부모 도시 $u$의 깊이가 $D$이고, 서로 다른 자식 가지에 있는 맛집 A와 B의 중심 깊이가 각각 $a,b$라고 하자. 두 중심을 잇는 유일한 경로는 $u$를 지나므로 중심 사이 거리는 다음과 같다.

$$
L=(a-D)+(b-D)
$$

두 배달 거리 $r_A,r_B$를 넣어 비겹침 조건 $L\ge r_A+r_B+1$을 적용하면 다음과 같다.

$$
(a-D)+(b-D)\ge r_A+r_B+1
$$

$h_A=a-r_A$, $h_B=b-r_B$로 묶으면 형제 서브트리의 호환 조건이 된다.

$$
h_A+h_B\ge 2D+1
$$

따라서 A쪽 경계값이 $h_A=h$로 정해지면 B쪽에는 $h_B\ge2D+1-h$가 필요하다. 합친 상태의 경계값은 $\min(h_A,h_B)$이고, 선호도 합은 두 점수의 합이다.

```
A의 각 상태 (hA, 점수A)에 대해:
    B의 각 상태 (hB, 점수B)에 대해:
        만약 hA+hB >= 2D+1 이면:
            합친_경계값 = min(hA, hB)
            합친_점수 = 점수A+점수B
            DP_갱신(합친_경계값, 합친_점수)
```

이 의사코드는 **어떤 선택끼리 합칠 수 있는지**를 보여준다. 
만약 상태 쌍을 전부 확인하면 상태가 각각 1,000개일 때만 해도 100만 번을 검사해야 한다. 

---
## 5. 전체 계산 순서

1. 모든 정점에서 ‘아무 맛집도 고르지 않음’이라는 점수 0의 선택을 생각한다.
2. 자식 서브트리의 DP를 먼저 계산한다.
3. 자식들의 상태를 현재 도시 $u$에서 병합한다.
4. $u$에 있는 맛집들을 하나씩 선택하는 전이를 적용한다.
5. 완성된 DP를 부모에게 전달하고, 루트에서는 가능한 최대 선호도 합을 답으로 얻는다.

자식의 경계값을 먼저 알아야 $u$의 맛집을 추가할 수 있는 기존 선택을 조회할 수 있으므로 이 순서가 필요하다. 자식도 맛집도 없는 정점에서도 공집합 선택의 점수 0이 시작점이 된다.

---

## 6. 문제 제출 결과 

- [제출 #13753934](https://jungol.co.kr/problem/4808/submission?sid=13753934): 100점 정답, **296ms**, 28.3MB, C++20
- 미션 목표: 500ms 이내 → **달성**


---

## 7. 코드 전문 
```c
#include <algorithm>

#include <cstdio>

#include <map>

#include <vector>

using int64 = long long;

constexpr int MAX_N = 100000;

constexpr int64 SENTINEL = 1'000'000'000'000'000'000LL;

struct Restaurant { int radius; int64 value; };

struct Frontier {

    std::map<int, int64> states;

    Frontier() { states.emplace(-1, SENTINEL); }

    int largest_key() const { return std::max(0, states.rbegin()->first); }

    int64 best(int key) const {

        if (key > largest_key()) return 0;

        return states.lower_bound(key)->second;

    }

    void relax(int key, int64 value) {

        auto it = states.lower_bound(key);

        if (it != states.end() && it->second >= value) return;

        if (it != states.end() && it->first == key) it->second = value;

        else it = states.emplace(key, value).first;

        auto left = std::prev(it);

        while (left->first >= 0 && left->second <= value) {

            auto previous = std::prev(left);

            states.erase(left);

            left = previous;

        }

    }

    void swap(Frontier& other) { states.swap(other.states); }

    void clear() { states.clear(); }

};

int n, m;

std::vector<int> tree[MAX_N + 1];

std::vector<Restaurant> restaurants[MAX_N + 1];

Frontier dp[MAX_N + 1];

void merge_frontiers(int depth, Frontier& source, Frontier& target) {

    if (source.largest_key() > target.largest_key()) source.swap(target);

    if (source.largest_key() == target.largest_key() && source.states.size() > target.states.size()) source.swap(target);

    const auto mirror = [depth](int h) { return 2 * depth - h + 1; };

    const int source_max = source.largest_key();

    for (const auto& [h, ignored] : source.states) {

        if (h >= mirror(source_max)) break;

        target.relax(h, source.best(h) + target.best(mirror(h)));

    }

    for (int h = std::max(0, mirror(source_max)); h <= depth; ++h)

        target.relax(h, std::max(source.best(h) + target.best(mirror(h)), target.best(h) + source.best(mirror(h))));

    for (int h = depth + 1; h <= source_max; ++h)

        target.relax(h, source.best(h) + target.best(h));

    source.clear();

}

int main() {

    if (std::scanf("%d%d", &n, &m) != 2) return 0;

    for (int i = 0; i < n - 1; ++i) {

        int a, b;

        std::scanf("%d%d", &a, &b);

        tree[a].push_back(b);

        tree[b].push_back(a);

    }

    for (int i = 0; i < m; ++i) {

        int city, radius;

        long long value;

        std::scanf("%d%d%lld", &city, &radius, &value);

        restaurants[city].push_back({radius, value});

    }

    std::vector<int> parent(n + 1, 0), depth(n + 1, 0), order;

    order.reserve(n);

    parent[1] = -1;

    depth[1] = n;

    order.push_back(1);

    for (size_t i = 0; i < order.size(); ++i) {

        int u = order[i];

        for (int v : tree[u]) {

            if (v == parent[u]) continue;

            parent[v] = u;

            depth[v] = depth[u] + 1;

            order.push_back(v);

        }

    }

    for (int i = n - 1; i >= 0; --i) {

        int u = order[i];

        for (int v : tree[u]) if (parent[v] == u) merge_frontiers(depth[u], dp[v], dp[u]);

        dp[u].relax(depth[u], 0);

        for (const Restaurant& restaurant : restaurants[u]) {

            int required = depth[u] + restaurant.radius + 1;

            int new_boundary = depth[u] - restaurant.radius;

            dp[u].relax(new_boundary, restaurant.value + dp[u].best(required));

        }

    }

    std::printf("%lld\n", dp[1].best(0));

    return 0;

}

```

---
## 8. 기본 코드 이해

>gpt의 가이드라인에 따라서 코드를 해석하였다.

### 8-1 현재 도시의 맛집 선택하기
```c
int required = depth[u] + restaurant.radius + 1;
int new_boundary = depth[u] - restaurant.radius;
dp[u].relax(new_boundary,
            restaurant.value + dp[u].best(required));
```

필요한 기존 경계 = D+r+1
새 맛집의 경계   = D-r
새 점수           = 기존 가능한 최대 점수+g


- `D+r+1`: 기존 선택이 얼마나 아래에 있어야 하는가?
- `D-r`: 새 맛집이 위로 어디까지 올라오는가?

## 8-2 서로 다른 자식 서브트리 합치기
A와 B의 경계값이 각각 $h_A,h_B$ 일때 두 서브트리를 합치는 조건 식은 다음과 같다. 

$$
h_B\ge2D+1-h_A
$$

```cpp
const auto mirror = [depth](int h) {
    return 2 * depth - h + 1;
};
```

mirror(h)
= 한쪽 경계가 h일 때 반대쪽에 필요한 최소 경계 

## 8-3 한 도시에서 실행되는 전체 알고리즘 

1. 자식들의 DP가 계산되어있다.
2. 자식 DP들을 하나씩 합친다.
3. 아무 맛집도 고르지 않는 경우는 점수 0 상태를 보장한다.
4. 현재 도시 u의 맛집을 선택하는 전이를 적용한다.
5. 완성된 dp[u]를 부모가 사용하게 한다

```cpp
for (int i = n - 1; i >= 0; --i) {
    int u = order[i];

    // 1~2. 자식 DP 합치기
    for (int v : tree[u])
        if (parent[v] == u)
            merge_frontiers(depth[u], dp[v], dp[u]);

    // 3. 아무 맛집도 고르지 않는 경우
    dp[u].relax(depth[u], 0);

    // 4. 현재 도시의 맛집 선택
    for (const Restaurant& restaurant : restaurants[u]) {
        int required = depth[u] + restaurant.radius + 1;
        int new_boundary = depth[u] - restaurant.radius;

        dp[u].relax(
            new_boundary,
            restaurant.value + dp[u].best(required)
        );
    }
}
```

### 8-4 `Frontier`코드 

**Frontier** : 유리한 (경계, 점수) 상태만 저장하는 자료구조이다. 
`Frontier`는 **특정 경계 이상에서 최대 점수를 빠르게 찾기 위해** 사용한다. 

`Frontier`는 위에 나왔던 '파레토 프런티어' 를 관리한다. 

`Frontier` 구조 
```
dp[u]
  └─ Frontier
       ├─ states
       ├─ best()
       └─ relax()
```
best(x)
= 경계가 x 이상인 상태 중 최대 점수 조회

relax(h, score)
= 새로운 상태를 넣고, 그 상태에 완전히 밀리는 상태 제거

#### best()
```c
int64 best(int key) const {
    if (key > largest_key()) return 0;
    return states.lower_bound(key)->second;
}
```
`lower_bound(key)`는 키가 `key` 이상인 첫 상태를 찾는다.

예를 들어, (3,20) (6,12) 인 경우, 다음과 같은 결과가 나온다.

| 조회 | 결과 | 이유 |
|---|---:|---|
| `best(2)` | 20 | 두 상태 모두 가능하며 20이 큼 |
| `best(4)` | 12 | 경계 3은 조건을 만족하지 못함 |
| `best(7)` | 0 | 저장된 맛집 선택은 없지만 공집합 선택 가능 |

#### relax()
```c
while (left->first >= 0 && left->second <= value) {
    auto previous = std::prev(left);
    states.erase(left);
    left = previous;
}
```
 상태보다 경계가 낮고 점수도 낮은 왼쪽 상태를 삭제한다

예를 들어, 기존 상태가 (3,10) 이고, 새 상태가 (6, 12)라면 **새 상태가 경계와 점수 모두 좋으므로 기존 상태를 지운다.** 

반면 (3, 20), (6, 12)인 경우에는 둘 다 남긴다. 


---

## 9. 최적화 관련 코드 이해

4에서 작성한 의사코드를 그대로 구현하면 A의 상태와 B의 상태를 하나씩 전부 비교해야 한다.

상태가 각각 1,000개라면 $1,000\times1,000$번을 비교해야 하므로 느려질 수 있다. 실제 코드에서는 `Frontier`의 `best()`를 사용해서 이 부분을 줄였다.

### 9-1 `mirror(h)`

두 자식 상태를 합칠 수 있는 조건은 다음과 같았다.

$$
h_A+h_B\ge2D+1
$$

A의 경계가 $h$라고 정하면 B에 필요한 경계는 다음과 같다.

$$
h_B\ge2D+1-h
$$

```cpp
const auto mirror = [depth](int h) {
    return 2 * depth - h + 1;
};
```

`mirror(h)`는 한쪽 경계가 `h`일 때 반대쪽에 필요한 최소 경계이다.

```cpp
target.best(mirror(h))
```

이 코드는 `target`의 상태를 전부 확인하지 않고, 필요한 경계 이상에서 가장 높은 점수를 바로 찾는다.

> **예시** 부모 깊이가 4이고 한쪽 경계가 3인 경우
> $2\times4+1-3=6$이므로 반대쪽 경계는 6 이상이어야 한다.

### 9-2 두 방향을 확인하는 부분

합친 상태의 경계는 두 경계 중 작은 값이다. 그런데 `source`와 `target` 중 어느 쪽이 작은 경계를 가지는지는 미리 알 수 없다.

```cpp
std::max(
    source.best(h) + target.best(mirror(h)),
    target.best(h) + source.best(mirror(h))
)
```

첫 번째 값은 `source`의 경계가 `h`인 경우이고, 두 번째 값은 `target`의 경계가 `h`인 경우이다. 둘 중 점수가 더 높은 것을 저장한다.

### 9-3 반복문이 세 부분인 이유

`merge_frontiers()`의 반복문은 경계의 위치에 따라 나뉘어 있다.

1. `h < mirror(source_max)`인 부분

이 구간에서는 `source`에 `mirror(h)`만큼 높은 경계가 없다. 따라서 `source`가 작은 경계를 담당하는 방향만 계산한다.

```cpp
source.best(h) + target.best(mirror(h))
```

2. `mirror(source_max) <= h <= depth`인 부분

어느 쪽이 작은 경계를 담당할지 모르기 때문에 앞에서 설명한 두 방향을 모두 계산한다.

3. `h > depth`인 부분

두 경계가 모두 부모 깊이보다 크다면 다음이 성립한다.

$$
h_A+h_B\ge2D+2
$$

필요한 조건인 $2D+1$보다 크므로 두 상태는 자동으로 합칠 수 있다.

```cpp
source.best(h) + target.best(h)
```

처음에는 세 반복문의 정확한 범위를 외우기보다 다음과 같이 이해했다.

```text
경계가 낮은 부분: 반대쪽에 mirror(h)를 요구한다.
양쪽 방향이 가능하면 두 경우를 비교한다.
두 경계가 모두 D보다 크면 그냥 점수를 더한다.
```

### 9-4 `source`와 `target`

```cpp
if (source.largest_key() > target.largest_key())
    source.swap(target);
```

반복할 범위가 작은 Frontier를 `source`로 두기 위한 코드이다. 두 자식 중 어느 쪽을 `source`로 두어도 합친 결과는 같지만, 작은 쪽을 순회하면 확인하는 횟수를 줄일 수 있다.

병합이 끝나면 `source`는 더 이상 사용하지 않으므로 비운다.

```cpp
source.clear();
```

**정리:** `merge_frontiers()`에서 새로운 병합 조건을 사용하는 것은 아니다. 4에서 구한 $h_A+h_B\ge2D+1$을 `mirror()`와 `best()`로 빠르게 계산한 것이다.


## 10. 참고자료

- [JUNGOL 4808번 - 맛집 추천](https://jungol.co.kr/problem/4808)
- [JUNGOL 제출 #13753934](https://jungol.co.kr/problem/4808/submission?sid=13753934)

>AI는 다음 부분에 활용했다.

- 문제 조건과 DP 수식 검토
- 잘못 이해한 내용 수정
- `Frontier`, `best()`, `relax()` 코드 해석
- 자식 병합과 최적화 코드 분석
