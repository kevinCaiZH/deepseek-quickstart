# 使用 Docker 部署和运行 PostgreSQL

整个过程主要分为三大部分：

1.  **在 Ubuntu 服务器上**：安装 Docker、拉取并运行 PostgreSQL 容器。
2.  **在 Ubuntu 服务器上**：配置防火墙，允许外部访问。
3.  **在本地 MacBook 上**：使用客户端工具连接到服务器上的 PostgreSQL，并创建表和插入数据。

请按照以下指令一步步操作。

---

### 第 1 步：在 Ubuntu 22 服务器上准备并运行 PostgreSQL

首先，SSH 登录到你的 Ubuntu 22 服务器。

#### 1.1 安装 Docker (如果尚未安装)

[Ubuntu 安装 Docker 和 Docker Compose 指南](../docs/docker.md)

#### 1.2 拉取并运行 PostgreSQL 容器

我们将使用一条 `docker run` 命令来完成所有操作：拉取镜像、创建并运行容器。

**关键点解释：**

*   `--name my-postgres`: 给容器起一个好记的名字。
*   `-e POSTGRES_PASSWORD=your_strong_password`: **设置 PostgreSQL 的 `postgres` 超级用户的密码。请务必替换 `your_strong_password` 为一个你自己的强密码。**
*   `-p 5432:5432`: **端口映射**。这是最关键的一步，它将服务器的 `5432` 端口映射到容器内部的 `5432` 端口，这样你的 MacBook 才能通过服务器 IP 访问。
*   `-v pgdata:/var/lib/postgresql/data`: **数据持久化**。创建一个名为 `pgdata` 的 Docker 卷 (Volume)，并挂载到容器内存储数据的目录。这样即使容器被删除，你的数据库数据也能保留下来。
*   `-d`: 后台运行容器。
*   `postgres:15`: 指定使用 PostgreSQL 的 15 版本镜像（你也可以选择 `postgres:latest` 或其他版本）。

**执行以下命令：**

```bash
# 请务必替换 your_strong_password
docker run --name my-postgres \
  -e POSTGRES_PASSWORD=your_strong_password \
  -p 5432:5432 \
  -v pgdata:/var/lib/postgresql/data \
  -d postgres:15
```

#### 1.3 验证容器是否成功运行

```bash
# 查看正在运行的容器
docker ps

# 你应该能看到类似下面的输出，STATUS 显示为 Up ...
# CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                    NAMES
# a1b2c3d4e5f6   postgres:15    "docker-entrypoint.s…"   3 seconds ago   Up 2 seconds   0.0.0.0:5432->5432/tcp   my-postgres
```

如果 `PORTS` 一栏显示 `0.0.0.0:5432->5432/tcp`，说明端口映射成功。

---

### 第 2 步：配置 Ubuntu 服务器防火墙

**⚠️云服务器直接配置网络安全组即可**

Ubuntu 默认使用 `ufw` 防火墙。你需要允许外部访问 `5432` 端口。

#### 2.1 检查防火墙状态

```bash
sudo ufw status
```

*   如果显示 `Status: inactive`，表示防火墙未开启，你可以跳到下一步。
*   如果显示 `Status: active`，你需要添加规则。

#### 2.2 允许 5432 端口

```bash
# 允许所有 IP 访问 5432 端口 (TCP协议)
sudo ufw allow 5432/tcp

# 重新加载防火墙规则使其生效
sudo ufw reload

# 再次检查状态，确保规则已添加
sudo ufw status
```

你现在应该能看到 `5432/tcp` 出现在允许列表中。

> **安全提示**：`allow 5432` 会对所有 IP 开放端口。如果你的 MacBook 有固定的公网 IP，更安全的做法是只对你的 IP 开放：`sudo ufw allow from <你的MacBook公网IP> to any port 5432`。

---

### 第 3 步：在 MacBook 上连接 PostgreSQL

现在，服务器端已经准备就绪。回到你的 MacBook 进行操作。

首先，你需要知道你的 **Ubuntu 服务器的公网 IP 地址**。在服务器上执行 `ip a` 或 `hostname -I` 可以查到。

我们提供两种连接方式：使用命令行工具 `psql` 和使用图形化界面工具 (推荐)。

---

#### 方式一：使用图形化界面工具 (如 DBeaver, TablePlus, Postico)

对于日常开发，使用 GUI 工具更方便。这里以 **DBeaver** (免费开源) 为例。

1.  **下载并安装 DBeaver**：访问 [DBeaver 官网](https://dbeaver.io/) 下载并安装。

2.  **创建新连接**：
    *   打开 DBeaver，点击左上角的 "新建连接" 图标 (插头形状)。
    *   在弹出的窗口中，选择 "PostgreSQL"，然后点击 "下一步"。

3.  **填写连接信息**：
    *   **主机 (Host)**: 填写你的 **`<服务器公网IP>`**。
    *   **端口 (Port)**: `5432` (这是默认值，一般不用改)。
    *   **数据库 (Database)**: `postgres` (这是默认创建的数据库)。
    *   **用户名 (Username)**: `postgres`。
    *   **密码 (Password)**: 填写你在第一步中为 `POSTGRES_PASSWORD` 设置的 `your_strong_password`。


4.  **测试并完成连接**：
    *   点击左下角的 "测试连接 (Test Connection)" 按钮。如果一切配置正确，会提示连接成功。
    *   点击 "完成 (Finish)"。现在你就可以在左侧的数据库导航器中看到你的 PostgreSQL 服务器了。


5.  **创建表和插入数据**：使用 SQL 编辑器 (推荐)
    *   在 DBeaver 顶部菜单栏，点击 **`SQL 编辑器` -> `新建 SQL 编辑器`** (或使用快捷键 `Cmd + [` )。
    *   确保编辑器顶部的连接指向的是你的 PostgreSQL 数据库。
    *   编写并执行 CREATE 和 INSERT 语句: [create.sql](create.sql)


#### 数据库设计说明

1. **产品表 (products)**
   - 包含100款护肤产品详细信息
   - SKU编码规则：XY+品类缩写+容量+版本标识
   - 成本与价格基于真实供应链数据模拟
   - 专利技术字段标注核心科技

2. **库存表 (inventory)**
   - 100个独立批次记录
   - 批次号规则：XY+生产年月日+序号
   - 包含三仓（北京/上海/广州）库存数据
   - 质检报告号符合企业标准格式

3. **成分表 (ingredients)**
   - 100种活性成分记录
   - 浓度标注符合《化妆品标签管理办法》
   - 供应商均为真实原料巨头企业
   - 功效说明匹配产品定位

### 数据特点
1. **真实性**：所有成本价、有效期、成分配比均符合行业标准
2. **可追溯性**：批次号与生产日期关联，支持全链路溯源
3. **业务导向**：库存量、仓库位置支持智能调拨决策
4. **扩展性**：专利号字段为技术保护提供法律依据


---

### 总结与排错

至此，你已成功在 Ubuntu 服务器上运行了 PostgreSQL，并从你的 MacBook 上连接成功。

**连接所需的核心信息：**
*   **服务器IP**: 你的 Ubuntu 服务器公网 IP
*   **端口**: `5432`
*   **用户名**: `postgres`
*   **密码**: 你在 `docker run` 命令中设置的密码
*   **数据库**: `postgres`

**如果连接失败，请检查：**
1.  **网络问题**: 能否 `ping <服务器公网IP>`？
2.  **防火墙问题**: 检查 `sudo ufw status`，确保 `5432/tcp` 是 `ALLOW` 状态。如果你用的是云服务器 (如阿里云、腾讯云、AWS)，请检查其控制台上的 **安全组 (Security Group)** 规则，确保入站方向的 `5432` 端口是开放的。
3.  **Docker 容器问题**: 在服务器上运行 `docker ps`，确保 `my-postgres` 容器正在运行，并且 `PORTS` 列显示 `0.0.0.0:5432->5432/tcp`。
4.  **密码错误**: 确认你输入的密码和创建容器时设置的 `-e POSTGRES_PASSWORD` 完全一致。
