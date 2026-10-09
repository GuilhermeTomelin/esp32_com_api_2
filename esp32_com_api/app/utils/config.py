"""Configurações do projeto.

Os valores podem ser mudados por variáveis de ambiente, sem mexer no código:
    ESP32_IP, ESP32_TIMEOUT, REFRESH_SECONDS, MAX_PONTOS
"""

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    # IP que o ESP32 mostra no Serial Monitor ao conectar no Wi-Fi
    esp32_ip: str = os.getenv("ESP32_IP", "192.168.0.50")

    # Tempo máximo de espera por uma resposta do ESP32 (segundos)
    timeout_s: float = float(os.getenv("ESP32_TIMEOUT", "5"))

    # Intervalo padrão entre leituras (o DHT11 precisa de pelo menos 1-2 s)
    refresh_s: int = int(os.getenv("REFRESH_SECONDS", "3"))

    # Quantas leituras guardar no histórico do gráfico
    max_pontos: int = int(os.getenv("MAX_PONTOS", "200"))


settings = Settings()
