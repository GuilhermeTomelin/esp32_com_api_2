"""Cliente da API HTTP que roda dentro do ESP32.

Rotas do ESP32:
    GET /dados        -> {"temperatura": 25.00, "umidade": 60.00}
    GET /temperatura  -> {"temperatura": 25.00}
    GET /umidade      -> {"umidade": 60.00}
Em caso de falha do sensor, o ESP32 responde HTTP 500 com {"erro": "..."}.
"""

import requests


class ESP32Error(Exception):
    """Erro ao falar com o ESP32 (rede, timeout, sensor ou resposta inválida)."""


class ESP32Client:
    def __init__(self, ip: str, timeout: float = 5.0):
        ip = ip.strip().removeprefix("http://").removeprefix("https://").rstrip("/")
        self.ip = ip
        self.base_url = f"http://{ip}"
        self.timeout = timeout

    def _get(self, rota: str) -> dict:
        url = f"{self.base_url}{rota}"

        try:
            resposta = requests.get(url, timeout=self.timeout)
        except requests.exceptions.Timeout as exc:
            raise ESP32Error(
                f"O ESP32 não respondeu em {self.timeout:.0f} s ({self.ip})."
            ) from exc
        except requests.exceptions.ConnectionError as exc:
            raise ESP32Error(
                f"Não foi possível conectar em {self.ip}. "
                "Confira o IP e se o computador está na mesma rede Wi-Fi."
            ) from exc
        except requests.exceptions.RequestException as exc:
            raise ESP32Error(f"Erro na requisição: {exc}") from exc

        try:
            dados = resposta.json()
        except ValueError as exc:
            raise ESP32Error("Resposta do ESP32 não é um JSON válido.") from exc

        if resposta.status_code != 200:
            raise ESP32Error(dados.get("erro", f"HTTP {resposta.status_code}"))

        return dados

    def get_dados(self) -> dict:
        """Lê temperatura e umidade de uma vez."""
        dados = self._get("/dados")

        try:
            return {
                "temperatura": float(dados["temperatura"]),
                "umidade": float(dados["umidade"]),
            }
        except (KeyError, TypeError, ValueError) as exc:
            raise ESP32Error(f"JSON inesperado do ESP32: {dados}") from exc
