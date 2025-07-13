# Loki Analyzer

![Loki Analyzer Logo](icon.png)

**Loki Analyzer** é uma ferramenta avançada para análise superficial de jogos e softwares Windows.  
Desenvolvida em **Python 3, PyQt5, Lupa (Lua), YARA** e arquitetura modular, ela automatiza a inspeção de executáveis, DLLs, engines, linguagens, proteções, criptografia, heurísticas customizadas e muito mais — tudo em uma interface moderna, leve e fácil de usar.

---

## ⚡️ **Funcionalidades Principais**

- **Análise Profunda de Pastas de Jogos e Softwares**
  - Detecta executáveis, DLLs, engines gráficas, linguagens usadas, frameworks e scripts.
- **Detecção de Proteções & Ofuscação**
  - Anti-cheats (Themida, VMProtect, Easy Anti-Cheat, Battleye, etc)
  - Packing e virtualização de código.
- **Sinais de Criptografia**
  - AES, RSA, ECC, Blowfish, MD5, SHA1, SHA256, CRC32, etc.
- **Heurísticas Customizáveis via Lua**
  - Permite adicionar novas regras heurísticas facilmente.
- **Detecção de Engines Gráficas**
  - Unreal, Unity, Godot, Source, Frostbite, RPG Maker, etc.
- **Exportação de Resultados**
  - Salve resultados em JSON ou TXT.

---

## 🖥️ **Interface**

- Interface moderna, com tema escuro e elementos coloridos.
- Barra de progresso responsiva durante análise.
- Aba "Sobre" com informações do autor, versão e aviso legal.
- Ícone customizado para a aplicação.

![Screenshot Loki Analyzer](screenshots/loki_analyzer_1.png)

---

## 🚀 **Como Usar**

1. **Abra o Loki Analyzer**
2. Clique em **Selecionar pasta do jogo** e escolha a pasta a ser analisada.
3. Aguarde o processamento (barra de progresso mostrará o andamento).
4. Veja o relatório detalhado na tela.
5. Opcional: clique em **Exportar resultado** para salvar o relatório.

---

## 🔒 **Sobre Segurança & Distribuição**

- O programa pode ser distribuído em formato EXE (standalone, via PyInstaller).
- Scripts auxiliares (.lua, .yara) são embarcados no executável.
- Código protegido por empacotamento, ofuscação e/ou compilação binária.
- **Nota:** Nenhuma proteção é 100% inviolável, mas o Loki Analyzer utiliza as melhores práticas para dificultar engenharia reversa.

---

## 🛠️ **Como Gerar o Executável (Build)**

**Pré-requisitos:**  
- Python 3.11 ou 3.12 (recomendado)
- [PyInstaller](https://pyinstaller.org/)
- Dependências do projeto (ver `requirements.txt`)

**Comando exemplo:**

```bash
pyinstaller --onefile --noconsole --icon=ico.ico --name "Loki Analyzer" --add-data "yara_rules;./yara_rules" --add-data "scripts;./scripts" --add-data "lupa;./lupa" --add-data "version.txt;." --add-data "ico.ico;." main.py
