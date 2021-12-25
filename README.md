# MailedIt 15기 파트장 투표 서비스
- <a href="https://mailedit-vote.vercel.app/" target="_blank">투표하러 가기</a>
- <a href="https://documenter.getpostman.com/view/17298535/UVJbHd2g" target="_blank">API 문서</a>
- ERD\
  ![](src/django-vote-erd.png)


## 협업 방식
- gitflow

협업 시의 충돌을 방지하고자 gitflow 방식으로 브랜치 관리
```
master
develop
  ㄴ  feature-account
  ㄴ  feature-vote
  ㄴ  feature-cookie
  ㄴ  feature-login
```

> 기능 추가할 때는 develop에서 분기하여 feature-name으로 브랜치 생성\
> `merge` feature -> develop \
> `merge` develop -> master


- 커밋 메시지 관리
  - 기능 추가 => "feat: message"
  - 기능 수정 => "fix: message"


## JWT 토큰 인증
simplejwt 라이브러리에서 일반적으로 사용하는 api 두개
- api/token
  - 로그인. 사용자 정보를 담은 `access token` & `refresh token` 토큰 생성해서 반환
- api/token/refresh
  - 유효한 refresh token을 담아 요청을 보내면 새로운 access token 반환

### 커스텀 세팅
```python
SIMPLE_JWT = {
    # access token 유효기간 하루로 설정
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    # refresh token 유효기간 7일로 설정
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    # Authorization 헤더에 JWT ~~ 형식으로 입력
    "AUTH_HEADER_TYPES": ("JWT",),
}
```

회원가입 시에도 토큰을 반환하도록 세팅
```python
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class RegisterAPIView(APIView):
    def post(self, request):
        # 유저 생성
        user_serializer = RegisterSerializer(data=request.data)
        user = user_serializer.save()

        # 토큰 생성
        token = TokenObtainPairSerializer.get_token(user)
        refresh_token = str(token)
        access_token = str(token.access_token)
```
위 방식처럼 해도 되고, /api/token 으로 POST 요청을 보내도 되지만 굳이 요청 수를 늘리고 싶지 않았기 때문에 이렇게 했다😀
