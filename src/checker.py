"""비밀번호 보안 등급 검사기."""

import getpass
import os
import secrets
import string
import sys

SPECIAL_CHARS = "!@#$%^&*"
RECOMMENDED_LENGTH = 16

RESET = "\033[0m"
BOLD = "\033[1m"
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"


def check_password(password):
    """각 검사 규칙의 (설명, 통과 여부) 목록을 반환한다."""
    return [
        ("8자리 이상", len(password) >= 8),
        (
            "대문자와 소문자 혼용",
            any(c.isupper() for c in password) and any(c.islower() for c in password),
        ),
        ("숫자 포함", any(c.isdigit() for c in password)),
        (f"특수문자({SPECIAL_CHARS}) 포함", any(c in SPECIAL_CHARS for c in password)),
    ]


def grade(passed_count):
    """충족한 조건 개수에 따른 (등급, 색상, 아이콘)을 반환한다."""
    if passed_count <= 1:
        return "취약", RED, "🔴"
    if passed_count <= 3:
        return "보통", YELLOW, "🟡"
    return "강력", GREEN, "🟢"


def format_report(results):
    """검사 결과를 출력용 문자열로 만든다."""
    passed_count = sum(passed for _, passed in results)
    label, color, icon = grade(passed_count)
    line = "─" * 40

    rows = [line, f"{BOLD}🔐 비밀번호 보안 검사 결과{RESET}", line]
    for description, passed in results:
        mark, mark_color = ("✅", GREEN) if passed else ("❌", RED)
        rows.append(f" {mark} {mark_color}{description}{RESET}")
    rows.append(line)
    rows.append(
        f" {icon} 보안 등급: {BOLD}{color}{label}{RESET} ({passed_count}/{len(results)}개 충족)"
    )
    rows.append(line)
    return "\n".join(rows)


def generate_password(length=RECOMMENDED_LENGTH):
    """모든 검사 규칙을 충족하는 '강력' 등급 비밀번호를 무작위로 생성한다."""
    if length < 8:
        raise ValueError("비밀번호 길이는 8자리 이상이어야 합니다.")

    groups = [string.ascii_uppercase, string.ascii_lowercase, string.digits, SPECIAL_CHARS]
    # 각 문자 종류에서 최소 1개씩 뽑아 모든 규칙 충족을 보장
    chars = [secrets.choice(group) for group in groups]
    chars += [secrets.choice("".join(groups)) for _ in range(length - len(chars))]
    secrets.SystemRandom().shuffle(chars)
    return "".join(chars)


def format_recommendation(password):
    """추천 비밀번호를 출력용 문자열로 만든다."""
    line = "─" * 40
    return "\n".join(
        [
            f" 💡 추천 비밀번호 ({len(password)}자리, 강력 등급)",
            f"    {BOLD}{GREEN}{password}{RESET}",
            line,
        ]
    )


def main():
    # Windows 콘솔에서 ANSI 색상과 이모지가 깨지지 않도록 설정
    if os.name == "nt":
        os.system("")
    sys.stdout.reconfigure(encoding="utf-8")

    # 입력한 비밀번호가 화면에 표시되지 않도록 getpass 사용
    password = getpass.getpass("비밀번호를 입력하세요: ")
    print(format_report(check_password(password)))
    print(format_recommendation(generate_password()))


if __name__ == "__main__":
    main()
