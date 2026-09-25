# 17-floortile（铺地砖）

Floortile — 面积/单片面积向上取整再加损耗百分比

## 启动

```bash
docker compose up --build
```

| 入口 | 地址 |
| --- | --- |
| 前端 | http://localhost:4600 |
| API | http://localhost:9600 |

## 主链

房间尺寸+砖规格+损耗 → 片数 → 铺贴预览

花铺循环加片：砖型或测算请求可带循环长（m）。循环长 > 0 时，沿房间长边按 ceil(房间长/循环长) 段循环对接花位，每段重新起砖，差额乘行数计为加片，与基础 order 合计；循环长 0 关闭，≥房间长或为负返回 422。已存记录的加片为当时快照，改砖型默认循环长不影响历史。

## 技术栈

Python 3.12 + FastAPI + SQLite；Vue 3 + Vite + Nginx。
