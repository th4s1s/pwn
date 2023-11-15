# EDGE CASE
- What if binary only has `_start` function?
-> 소스코드를 입력으로 받아서 직접 컴파일

- .init_array?
-> libc_start_main에서 호출시키므로, libc_start_main을 후킹하기때문에 문제 없음.
