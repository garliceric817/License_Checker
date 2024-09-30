# 使用官方的 Python 映像
FROM python:3.9-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends binutils && \
    rm -rf /var/lib/apt/lists/*

# 創建一用戶
RUN useradd -m -u 1001 user

# 設置工作目錄
WORKDIR /app

# 複製application
COPY --chown=user:user create_network_policy.py .

# 安裝依賴和 PyInstaller
RUN pip install kubernetes ldap3 pyinstaller

# compile
RUN pyinstaller --onefile create_network_policy.py

# 第二階短，打包主映象檔
FROM python:3.9-slim

# 創建一使用者
RUN useradd -m -u 1001 user

# workspace
WORKDIR /app

# 複製complied file
COPY --from=builder /app/dist/create_network_policy /app/

# 使用1001 UID
USER 1001

# 執行編譯程式
CMD ["./create_network_policy"]