## Определение популярности геолокации для размещения банкомата
<p align="center" width="100%">
    <img width="15%" src="https://i.imgur.com/PwMDaLx.png"> 
</p>

----
[![Build Status](https://github.com/yugorshkov/atms_popularity/actions/workflows/github_runners_lint_test.yml/badge.svg?branch=main)](https://github.com/yugorshkov/atms_popularity/actions/workflows/github_runners_lint_test.yml)

### Учебный проект курса "MLOps и production подход к ML исследованиям"
***
Модель определения популярности места расположения банкомата

Описание проекта на [Кью](https://yandex.ru/q/ "Яндекс Кью")

### Использование сервиса
Запустить контейнер.  
*Вместо порта 5001 можно использовать любой доступный*
```sh
docker run -p 5001:8080 laggerkrd/atms_popularity
```

Скачать [тестовые файлы](examples "Необязательная подсказка")

```python
import requests
import pandas as pd

test_df = pd.read_csv("examples/test1.csv")
test_df.set_index("id", inplace=True)

host = '127.0.0.1'
port = '5001'

url = f'http://{host}:{port}/invocations'
headers = {'Content-Type': 'application/json'}
http_data = test_df.to_json(orient='split')

response = requests.post(url=url, headers=headers, data=http_data)

print(f'Predictions: {response.text}')
```
