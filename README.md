# WebServiceSubsystem

Introduction:</br>
Subsystem project for Knowledge Management and Service Platform for Chinese Cultural Relics Overseas

### How to build

#### Build conda environment

前端：Vue 后端：Flask

- 后端环境搭建：

```bash
conda create -n WebServiceSubsystem310 python=3.10
cd backend
pip install -r requirements.txt
python app.py
```

- 前端环境搭建

```bash
cd frontend
npm install
npm run serve
```

### 2025.4.26

- 完成知识图谱可视化：还需添加<u>搜索</u>展示功能
- 预计下次更新完成登陆注册（本地）、时间轴可视化

