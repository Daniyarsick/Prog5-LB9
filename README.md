# **Сервис бонусной программы**

## **Аннануров Даниил Петрович ИВТ 1.2**

### **Задание** ЛБ 9 ПРОГ5
Реализуйте REST-сервис для просмотра текущего уровня бонусной программы, который дает определенный кешбэк пользователю и следующего уровня ("серебряный", "золотой", "платиновый" уровень при определенном объеме трат). Поскольку эти данные являются важными и критичными, каждый пользователь может видеть только информацию о своем кэшбеке. Для обеспечения безопасности потребуется реализовать метод, который по логину и паролю сотрудника будет выдавать секретный токен, действующий в течение определенного времени. Запрос данных о бонусной программе должен выдаваться только при предъявлении валидного токена пользователем. В модели данных и в интерфейсе соответственно должны быть отображены. Уровень трат и границы бонусных уровней

### Требования к решению

в качестве токена использовать JWT;
код размещен и доступен в публичном репозитории на GitHub / GitLab;
оформлена инструкция по запуску сервиса и взаимодействию с проектом (Markdown-файл с использованием конструкций разметки по необходимости);
сервис реализован на FastAPI или Django Rest Framework, Flask, Eve.

### **Установка**

Установить необходимые зависимости:

```bash
pip install fastapi uvicorn pyjwt
```

### **Запустить сервер FastAPI:**

```bash
uvicorn main:app --reload
```

### Использование

#### Получение токена

Чтобы получить токен, отправить POST-запрос на /token с именем пользователя и паролем:

**Пример запроса:**

```json
{
  "username": "user1",
  "password": "password1"
}
```
Пример ответа:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ1c2VyMSIsImV4cCI6MTczNDUzNjU2Nn0._Qx14-D_iHBL41-d8wCi9zZmVS13D-sGDcYEx8KKNOk",
  "token_type": "bearer"
}
```

### Получение информации о бонусах

Использовать полученный токен для доступа к информации о бонусах. Отправить GET-запрос на /bonus с заголовком Authorization: Bearer <token>.

Пример ответа:

```json
{
  "current_level": {
    "level": "Silver",
    "min_spending": 0,
    "cashback": 0.01
  },
  "next_level": {
    "level": "Gold",
    "min_spending": 10000,
    "cashback": 0.02
  }
}
```

Уровни бонусов
Silver: 0 - 9999 расходов, 1% кешбэк

Gold: 10000 - 19999 расходов, 2% кешбэк

Platinum: 20000+ расходов, 3% кешбэк

### Скриншоты

<img src="img_1.png" alt="img1png"></img>  <img src="img_2.png" alt="img2png"></img>