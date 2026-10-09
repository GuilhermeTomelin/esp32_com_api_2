# ESP32 com API + Streamlit

O ESP32 lê temperatura e umidade (DHT11), mostra no display OLED e expõe uma API HTTP.
Este projeto em Python consome essa API e mostra um painel no Streamlit.

## Estrutura

```
esp32_com_api/
├── app/
│   ├── main.py                  # painel Streamlit
│   ├── services/
│   │   └── weather_api.py       # cliente da API do ESP32
│   └── utils/
│       └── config.py            # IP, timeout e intervalo
├── codigo/
│   └── codigo.c++               # sketch do ESP32 (Arduino IDE)
└── requirements.txt
```

## Como rodar

1. Grave o sketch no ESP32 e abra o Serial Monitor (115200) para ver o **IP** dele.
2. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
3. Na pasta raiz do projeto, rode:
   ```
   streamlit run app/main.py
   ```
4. No painel, digite o IP do ESP32 na barra lateral (ou defina `ESP32_IP` antes de rodar).

O computador e o ESP32 precisam estar na **mesma rede Wi-Fi**.

## Rotas do ESP32

| Rota | Resposta |
|---|---|
| `GET /dados` | `{"temperatura": 25.00, "umidade": 60.00}` |
| `GET /temperatura` | `{"temperatura": 25.00}` |
| `GET /umidade` | `{"umidade": 60.00}` |

## Variáveis de ambiente (opcionais)

`ESP32_IP`, `ESP32_TIMEOUT`, `REFRESH_SECONDS`, `MAX_PONTOS`
