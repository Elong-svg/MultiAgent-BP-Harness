# Skill Integration Guide - Business Plan Creator

## 1. 子技能映射表（v4.0 完整版）

本 Skill 依赖 **10 个子技能** 协同工作，以下是各商业计划书章节与子技能的映射关系：

### 1.1 基础技能映射（7 个）

| 商业计划书章节 | 所需子技能 | 调用时机 | 数据要求 | 输出格式 |
|--------------|-----------|---------|---------|---------|
| **执行摘要** | Humanizer | Phase 5 | 各章节汇总内容 | 润色后的文本 |
| **公司概况** | finance-data-retrieval | Phase 1 | 公司名称/股票代码 | 公司基本信息、主营业务 |
| **财务分析** | finance + data | Phase 2-3 | 财务报表数据（年报/季报） | 财务指标表、趋势图 |
| **市场分析** | web_search | Phase 2 | 行业名称/关键词 | 行业规模、增长率、趋势 |
| **竞争分析** | web_search + data | Phase 2-3 | 竞品公司名称/股票代码 | 对比图表、竞争格局 |
| **战略分析** | - | Phase 2 | 公司公告、研报 | 战略定位、发展规划 |
| **风险评估** | finance-data-retrieval | Phase 2 | 财务风险指标 | 风险等级、应对措施 |
| **财务预测** | finance + data | Phase 3-4 | 历史财务数据 | 预测模型、敏感性分析 |
| **文档生成** | Word/PDF | Phase 5 | 所有章节内容 | .docx / .pdf |

### 1.2 新增专业子技能映射（3 个）

| 子技能 | 调用时机 | 输入数据 | 输出物 | 质量标准 |
|--------|---------|---------|--------|---------|
| **data-cleaner** | Phase 1 数据收集后 | finance-data-retrieval + PDF 年报 + web_search 数据 | cleaned_data.json + quality_report.json + data_dictionary.md | 质量评分 >= 80 分，A/B 级占比 >= 90% |
| **business-writer** | Phase 2 专家撰写时 | 专家分析结论 + 数据图表 | 各章节专业论述文本 | 三层论述结构正确，主旨式标题应用，AI 味消除 |
| **document-integrator** | Phase 3 整合阶段 | Claw 初步整合文档 + 图表锚点 | 整合后完整文档 + 整合报告 | 质量评分 >= 80 分，一致性检查通过 |

### 映射说明

- **Phase 1** - 数据收集阶段：获取公司基本信息和财务数据 → **data-cleaner 清洗**
- **Phase 2** - 分析阶段：财务分析、市场分析、竞争分析 → **business-writer 写作**
- **Phase 3** - 可视化阶段：生成图表和数据展示 → **document-integrator 整合**
- **Phase 4** - 预测阶段：财务预测和建模
- **Phase 5** - 整合阶段：文档生成和内容润色 → **Humanizer 润色**

---

## 2. 子技能详细调用指南

### 2.1 data-cleaner（v4.0 新增）

**用途**：数据清洗与标准化引擎，将多来源、多格式的杂乱原始数据清洗为干净、完整、结构化的标准化数据集

**典型调用场景**：

```typescript
// 场景 1：Phase 1 数据收集完成后自动调用
const cleanedData = await skill.call("data-cleaner", {
  workflow: "clean_and_merge",
  inputData: {
    financialData: incomeData,  // finance-data-retrieval 获取的财报数据
    marketData: industryData,   // web_search 获取的行业数据
    pdfData: parsedPdfData      // PDF 年报解析数据
  },
  options: {
    deduplicate: true,          // 去重合并
    handleMissing: true,        // 缺失值处理
    detectOutliers: true,       // 异常值检测
    rateReliability: true       // 可信度评级
  }
});

// 返回值
{
  cleaned_data: {...},          // 清洗后的结构化数据
  quality_report: {
    score: 92,                  // 质量评分（>=80 及格）
    reliability_grade: "A",     // 可信度评级（A/B/C/D/E）
    ab_ratio: 0.95              // A/B 级数据占比（>=90% 合格）
  },
  data_dictionary: {...}        // 数据字典
}
```

**数据清洗流程**：
1. **格式解析** - 支持 JSON/HTML/CSV/PDF/Excel 多格式
2. **去重合并** - 按可信度排序（官方财报>数据库>研报>媒体）
3. **缺失值处理** - 线性插值/行业均值/标记缺失
4. **异常值检测** - Z 分数/逻辑检查/趋势断裂
5. **标准化** - 单位统一/格式规范/结构重组
6. **可信度评级** - A/B/C/D/E 五级

**质量标准**：
- ✅ 质量评分 >= 80 分
- ✅ A/B 级数据占比 >= 90%
- ✅ 异常值已标记并有处理记录
- ✅ 数据来源标注清晰

---

### 2.2 business-writer（v4.0 新增）

**用途**：商业写作引擎，将原始数据和分析结果转化为专业商业论述

**典型调用场景**：

```typescript
// 场景 1：行业研究员撰写行业分析章节
const industryChapter = await skill.call("business-writer", {
  workflow: "chapter_writing",
  chapterType: "industry_analysis",
  inputData: {
    analysisPoints: [
      {
        what: "行业规模 2024 年达到 5000 亿元",
        why: "受益于政策支持和消费升级",
        how: "预计未来 3 年保持 15% 复合增长"
      }
    ],
    data: industryData,
    charts: [chart1, chart2]
  },
  options: {
    applyThreeLayerStructure: true,  // What-Why-How 三层论述
    generateMainIdeaTitles: true,    // 主旨式标题
    optimizeTransitions: true,       // 段落衔接优化
    removeAIFlav: true               // AI 味消除
  }
});

// 场景 2：财务分析师撰写财务分析章节
const financialChapter = await skill.call("business-writer", {
  workflow: "chapter_writing",
  chapterType: "financial_analysis",
  inputData: {
    analysisPoints: financialRatios,
    data: financialStatements,
    charts: [revenueChart, profitChart]
  }
});
```

**写作标准**：
- ✅ **三层论述结构** - What（现象）-Why（原因）-How（趋势/建议）
- ✅ **主旨式标题** - 标题体现分析角度，不堆砌数据
- ✅ **段落式论述** - 禁止提纲式 1.2.3. 列表
- ✅ **字数控制** - 每章节 2000-3000 字
- ✅ **专业术语** - 财务术语使用准确
- ✅ **无 AI 味** - 文本自然流畅

**质量检查清单**：
- [ ] 三层论述结构应用正确
- [ ] 主旨式标题应用正确
- [ ] 无提纲式列表
- [ ] 字数达标（2000-3000 字）
- [ ] 数据来源已标注
- [ ] 无空话套话
- [ ] 逻辑连贯

---

### 2.3 document-integrator（v4.0 新增）

**用途**：文档智能整合引擎，解决多源文档合并时的图表定位、逻辑一致性、术语统一、格式规范等核心问题

**典型调用场景**：

```typescript
// 场景 1：Claw 初步整合后深度整合
const integratedDoc = await skill.call("document-integrator", {
  workflow: "full_integration",
  inputDoc: preliminaryDoc,       // Claw 初步整合的文档
  charts: allCharts,              // 所有图表文件
  tables: allTables,              // 所有表格
  options: {
    scanAnchors: true,            // 锚点扫描与注册
    validateCharts: true,         // 图表质量校验
    checkConsistency: true,       // 一致性检查（术语/数据/结论）
    stitchLogic: true,            // 逻辑缝合（生成过渡句）
    unifyFormat: true,            // 格式统一（标题层级/字体字号）
    calculateScore: true          // 质量评分（6 维度）
  }
});

// 返回值
{
  integrated_document: {...},     // 整合后完整文档
  integration_report: {
    quality_score: 87,            // 质量评分（>=80 及格）
    consistency_check: "PASS",    // 一致性检查结果
    anchor_mapping: {...},        // 锚点映射表
    change_log: [...]             // 变更日志
  },
  issues: [...]                   // 待处理问题清单
}
```

**核心机制**：
1. **锚点系统** - 使用 `{{}}` 包裹的标记连接文本与图表
2. **一致性检查** - 术语/数据/结论/引用跨章节校验
3. **逻辑缝合** - 自动生成章节过渡句
4. **格式统一** - 标题层级、字体字号、表格格式
5. **质量评分** - 6 维度加权评分（80 分及格）

**质量评分维度**：
| 维度 | 权重 | 检查内容 |
|------|------|---------|
| 术语一致性 | 15% | 同一术语全文表述统一 |
| 数据一致性 | 25% | 同一数据多处引用一致 |
| 结论一致性 | 20% | 前后结论无矛盾 |
| 图表质量 | 20% | 图表嵌入精准、标题完整 |
| 格式规范 | 10% | 标题层级、字体字号统一 |
| 逻辑连贯 | 10% | 章节过渡自然、逻辑流畅 |

**质量标准**：
- ✅ 质量评分 >= 80 分
- ✅ 术语一致性检查通过
- ✅ 数据一致性检查通过
- ✅ 图表锚点精准定位
- ✅ 无格式标记残留
- ✅ 无提示词泄露

---

### 2.4 finance-data-retrieval

**用途**：获取股票代码、财务报表、行业数据、市场指标

**典型调用场景**：

```typescript
// 场景1：获取公司基本信息
const companyInfo = await skill.call("finance-data-retrieval", {
  endpoint: "stock_basic",
  params: {
    ts_code: "600690.SH",  // 股票代码格式：代码.交易所后缀
    fields: "ts_code,name,industry,list_date,area"
  }
});

// 场景2：获取年报财务数据
const financialData = await skill.call("finance-data-retrieval", {
  endpoint: "income",  // 利润表
  params: {
    ts_code: "600690.SH",
    start_date: "20191231",
    end_date: "20231231",
    fields: "ts_code,ann_date,f_ann_date,end_date,total_revenue,operate_profit"
  }
});

// 场景3：获取资产负债表
const balanceSheet = await skill.call("finance-data-retrieval", {
  endpoint: "balancesheet",
  params: {
    ts_code: "600690.SH",
    start_date: "20191231",
    end_date: "20231231",
    fields: "ts_code,end_date,total_assets,total_liab,total_hldr_eqy"
  }
});

// 场景4：获取现金流量表
const cashFlow = await skill.call("finance-data-retrieval", {
  endpoint: "cashflow",
  params: {
    ts_code: "600690.SH",
    start_date: "20191231",
    end_date: "20231231",
    fields: "ts_code,end_date,n_cashflow_act,c_fr_sale_sg"
  }
});
```

**参数说明**：

| 参数 | 类型 | 说明 | 示例 |
|-----|------|------|------|
| `ts_code` | string | 股票代码（带交易所后缀） | "600690.SH", "000001.SZ" |
| `start_date` | string | 开始日期（YYYYMMDD格式） | "20190101" |
| `end_date` | string | 结束日期（YYYYMMDD格式） | "20231231" |
| `fields` | string | 返回字段列表，逗号分隔 | "ts_code,end_date,revenue" |

**返回值处理**：

```typescript
// 转换为 DataFrame 格式
import pandas as pd;

const df = pd.DataFrame(financialData.data.items, columns=financialData.data.fields);

// 数据类型转换
df['end_date'] = pd.to_datetime(df['end_date']);
df['total_revenue'] = df['total_revenue'].astype(float);

// 按日期排序
df = df.sort_values('end_date');
```

**常用 API 端点**：

| 端点 | 用途 | 返回数据 |
|-----|------|---------|
| `stock_basic` | 股票基本信息 | 公司名称、行业、上市日期 |
| `income` | 利润表 | 营收、利润、费用等 |
| `balancesheet` | 资产负债表 | 资产、负债、股东权益 |
| `cashflow` | 现金流量表 | 经营/投资/筹资现金流 |
| `daily` | 日线行情 | 开盘价、收盘价、成交量 |
| `fina_indicator` | 财务指标 | ROE、ROA、毛利率等 |

---

### 2.5 finance

**用途**：财务比率分析、趋势分析、杜邦分析

**典型调用场景**：

```typescript
// 场景1：ROE 分析（杜邦分析）
const roeAnalysis = await skill.call("finance", {
  workflow: "financial-analysis",
  data: balanceSheetData,
  analysisType: "dupont",
  metrics: ["roe", "roa", "gross_margin", "net_margin"]
});

// 场景2：偿债能力分析
const solvencyAnalysis = await skill.call("finance", {
  workflow: "financial-analysis",
  data: financialData,
  analysisType: "solvency",
  metrics: ["current_ratio", "quick_ratio", "debt_to_equity"]
});

// 场景3：盈利能力分析
const profitabilityAnalysis = await skill.call("finance", {
  workflow: "financial-analysis",
  data: incomeStatementData,
  analysisType: "profitability",
  metrics: ["gross_margin", "operating_margin", "net_margin", "roe"]
});

// 场景4：成长能力分析
const growthAnalysis = await skill.call("finance", {
  workflow: "financial-analysis",
  data: multiYearData,
  analysisType: "growth",
  metrics: ["revenue_growth", "profit_growth", "asset_growth"]
});
```

**数据要求**：

调用 finance 技能前，需准备以下财务数据：

| 数据类型 | 必需字段 | 数据来源 |
|---------|---------|---------|
| 利润表 | revenue, operating_profit, net_profit | finance-data-retrieval/income |
| 资产负债表 | total_assets, total_liabilities, equity | finance-data-retrieval/balancesheet |
| 现金流量表 | operating_cashflow, investing_cashflow | finance-data-retrieval/cashflow |

**输出示例**：

```json
{
  "analysis_type": "dupont",
  "results": {
    "roe": {
      "current": 0.156,
      "trend": "up",
      "yoy_change": 0.023,
      "interpretation": "净资产收益率15.6%，同比提升2.3个百分点"
    },
    "roa": {
      "current": 0.089,
      "trend": "stable",
      "yoy_change": 0.005
    }
  }
}
```

---

### 2.6 data

**用途**：数据可视化、统计分析、图表生成

**典型调用场景**：

```typescript
// 场景1：生成营收趋势图（Plotly 优先）
const revenueChart = await skill.call("data", {
  workflow: "visualization",
  chartType: "line",
  library: "plotly",
  data: {
    x: years,
    y: revenues,
    labels: revenueLabels
  },
  config: {
    title: "近5年营业收入趋势",
    xAxisLabel: "年度",
    yAxisLabel: "营业收入（亿元）",
    theme: "professional"
  }
});

// 场景2：生成利润结构对比图
const profitStructureChart = await skill.call("data", {
  workflow: "visualization",
  chartType: "stacked_bar",
  library: "plotly",
  data: {
    categories: years,
    series: [
      { name: "毛利润", values: grossProfits },
      { name: "营业利润", values: operatingProfits },
      { name: "净利润", values: netProfits }
    ]
  },
  config: {
    title: "利润结构对比",
    stacked: true
  }
});

// 场景3：生成资产负债结构饼图
const assetStructureChart = await skill.call("data", {
  workflow: "visualization",
  chartType: "pie",
  library: "plotly",
  data: {
    labels: ["流动资产", "非流动资产", "流动负债", "非流动负债", "股东权益"],
    values: [450, 380, 280, 120, 430]
  },
  config: {
    title: "资产负债结构（2023年）",
    donut: true
  }
});

// 场景4：生成竞争对手对比柱状图
const competitorChart = await skill.call("data", {
  workflow: "visualization",
  chartType: "grouped_bar",
  library: "plotly",
  data: {
    categories: ["海尔智家", "美的集团", "格力电器"],
    series: [
      { name: "营收（亿元）", values: [2614, 3737, 2050] },
      { name: "净利润（亿元）", values: [166, 337, 290] }
    ]
  },
  config: {
    title: "主要竞争对手财务对比（2023年）",
    legendPosition: "top"
  }
});
```

**图表类型推荐**：

| 商业计划书场景 | 推荐图表类型 | 推荐库 |
|--------------|------------|-------|
| 营收/利润趋势 | 折线图 (line) | plotly |
| 多年份对比 | 分组柱状图 (grouped_bar) | plotly |
| 结构占比 | 饼图/环形图 (pie/donut) | plotly |
| 累积趋势 | 堆叠面积图 (stacked_area) | plotly |
| 多指标对比 | 雷达图 (radar) | plotly |
| 相关性分析 | 散点图 (scatter) | plotly |

**图表输出处理**：

```typescript
// 保存图表为图片
const chartImage = await skill.call("data", {
  workflow: "export_chart",
  chart: revenueChart,
  format: "png",
  width: 1200,
  height: 600,
  outputPath: "./charts/revenue_trend.png"
});

// 或将图表嵌入文档
const chartHtml = revenueChart.to_html(full_html=false);
```

---

### 2.7 Word 文档生成

**用途**：生成 .docx 格式的商业计划书文档

**典型调用场景**：

```typescript
// 场景1：创建包含表格的文档
const wordDoc = await skill.call("Word 文档生成", {
  mode: "create",
  content: {
    title: "海尔智家商业计划书",
    sections: [
      {
        heading: "一、执行摘要",
        level: 1,
        content: executiveSummary
      },
      {
        heading: "二、公司概况",
        level: 1,
        content: companyOverview
      },
      {
        heading: "三、财务分析",
        level: 1,
        content: [
          {
            type: "text",
            content: "3.1 营收分析"
          },
          {
            type: "table",
            headers: ["年份", "营业收入", "同比增长", "毛利率"],
            rows: revenueData,
            style: "professional"
          },
          {
            type: "image",
            path: "./charts/revenue_trend.png",
            caption: "图3-1：近5年营收趋势"
          }
        ]
      }
    ]
  },
  outputPath: "./output/海尔智家商业计划书.docx",
  template: "professional_business_plan"
});

// 场景2：编辑现有文档
const editedDoc = await skill.call("Word 文档生成", {
  mode: "edit",
  filePath: "./output/海尔智家商业计划书.docx",
  edits: [
    {
      type: "replace",
      target: "{{COMPANY_NAME}}",
      content: "海尔智家股份有限公司"
    },
    {
      type: "insert_after",
      target: "## 财务分析",
      content: newFinancialContent
    }
  ]
});
```

**支持的元素类型**：

| 元素类型 | 说明 | 必需参数 |
|---------|------|---------|
| `text` | 普通文本段落 | `content` |
| `heading` | 标题 | `content`, `level` |
| `table` | 表格 | `headers`, `rows` |
| `image` | 图片 | `path` |
| `page_break` | 分页符 | - |
| `list` | 列表 | `items` |

---

### 2.8 PDF 文档生成

**用途**：生成专业排版的 PDF 格式商业计划书

**典型调用场景**：

```typescript
// 场景1：从 Markdown 生成 PDF
const pdfDoc = await skill.call("PDF 文档生成", {
  mode: "create",
  source: "markdown",
  content: markdownContent,
  outputPath: "./output/海尔智家商业计划书.pdf",
  design: {
    theme: "professional",
    fontFamily: "Source Han Sans SC",
    colorScheme: {
      primary: "#1a365d",
      secondary: "#2c5282",
      accent: "#3182ce"
    },
    pageSetup: {
      size: "A4",
      orientation: "portrait",
      margins: { top: "2cm", bottom: "2cm", left: "2.5cm", right: "2.5cm" }
    }
  },
  include: {
    coverPage: true,
    toc: true,
    header: true,
    footer: true,
    pageNumbers: true
  }
});

// 场景2：从 Word 转换 PDF
const pdfFromWord = await skill.call("PDF 文档生成", {
  mode: "convert",
  sourceFile: "./output/海尔智家商业计划书.docx",
  outputPath: "./output/海尔智家商业计划书.pdf",
  quality: "high"
});
```

**设计系统参数**：

| 参数 | 选项 | 适用场景 |
|-----|------|---------|
| `theme` | professional / minimal / modern / corporate | 商业计划书推荐 professional |
| `fontFamily` | Source Han Sans SC / Microsoft YaHei / SimSun | 中文文档推荐 Source Han Sans SC |
| `colorScheme.primary` | 任意 HEX 色值 | 主色调（标题、重点） |
| `colorScheme.secondary` | 任意 HEX 色值 | 副色调（副标题、边框） |

---

### 2.9 Humanizer

**用途**：去除 AI 生成内容的机器感，提升文本的自然度和可读性

**典型调用场景**：

```typescript
// 场景1：润色整篇商业计划书
const humanizedContent = await skill.call("Humanizer", {
  content: originalContent,
  tone: "professional",
  intensity: "medium",  // light / medium / heavy
  targetAudience: "investor",
  focus: ["reduce_ai_patterns", "improve_flow", "add_personality"]
});

// 场景2：逐章节润色
const sections = ["executive_summary", "market_analysis", "financial_analysis"];
const humanizedSections = {};

for (const section of sections) {
  humanizedSections[section] = await skill.call("Humanizer", {
    content: draftContent[section],
    tone: section === "executive_summary" ? "persuasive" : "professional",
    intensity: "light"
  });
}
```

**润色参数说明**：

| 参数 | 选项 | 说明 |
|-----|------|------|
| `tone` | professional / persuasive / conversational / formal | 根据章节选择语气 |
| `intensity` | light / medium / heavy | light=轻度润色，保留原意；heavy=深度改写 |
| `targetAudience` | investor / executive / technical / general | 目标读者类型 |

**调用时机**：

- **Phase 5 最后一步**：所有内容撰写完成后统一润色
- **优势**：保持全文风格一致、避免重复润色造成信息丢失
- **注意**：润色前保存原始版本，便于对比

---

## 3. 技能调用编排示例

### 3.1 标准流程：生成完整商业计划书

```typescript
/**
 * 完整商业计划书生成流程
 * 以海尔智家（600690.SH）为例
 */

async function generateBusinessPlan(companyCode: string, companyName: string) {
  const workflow = {
    companyCode: companyCode,      // "600690.SH"
    companyName: companyName,      // "海尔智家"
    outputDir: `./output/${companyName}_商业计划书`
  };

  // ========== Phase 1: 数据收集 ==========
  console.log("Phase 1: 收集基础数据...");
  
  // Step 1.1: 获取公司基本信息
  const companyBasic = await skill.call("finance-data-retrieval", {
    endpoint: "stock_basic",
    params: { ts_code: workflow.companyCode }
  });
  
  // Step 1.2: 获取财务报表（5年数据）
  const incomeData = await skill.call("finance-data-retrieval", {
    endpoint: "income",
    params: {
      ts_code: workflow.companyCode,
      start_date: "20190101",
      end_date: "20231231"
    }
  });
  
  const balanceData = await skill.call("finance-data-retrieval", {
    endpoint: "balancesheet",
    params: {
      ts_code: workflow.companyCode,
      start_date: "20190101",
      end_date: "20231231"
    }
  });
  
  const cashflowData = await skill.call("finance-data-retrieval", {
    endpoint: "cashflow",
    params: {
      ts_code: workflow.companyCode,
      start_date: "20190101",
      end_date: "20231231"
    }
  });
  
  // Step 1.3: 获取行业数据
  const industryData = await skill.call("web_search", {
    query: `${companyBasic.industry}行业规模 市场增长率 2024`
  });

  // ========== Phase 2: 数据分析 ==========
  console.log("Phase 2: 执行财务分析...");
  
  // Step 2.1: 财务比率分析
  const financialRatios = await skill.call("finance", {
    workflow: "financial-analysis",
    data: { income: incomeData, balance: balanceData, cashflow: cashflowData },
    analysisTypes: ["profitability", "solvency", "growth", "dupont"]
  });
  
  // Step 2.2: 生成分析文本
  const analysisText = generateAnalysisText(financialRatios);

  // ========== Phase 3: 可视化 ==========
  console.log("Phase 3: 生成图表...");
  
  // Step 3.1: 营收趋势图
  const revenueChart = await skill.call("data", {
    workflow: "visualization",
    chartType: "line",
    library: "plotly",
    data: { x: years, y: revenues },
    config: { title: `${workflow.companyName}近5年营收趋势` }
  });
  
  // Step 3.2: 利润结构图
  const profitChart = await skill.call("data", {
    workflow: "visualization",
    chartType: "stacked_bar",
    library: "plotly",
    data: profitStructureData,
    config: { title: "利润结构对比" }
  });
  
  // Step 3.3: 财务指标对比图
  const ratioChart = await skill.call("data", {
    workflow: "visualization",
    chartType: "radar",
    library: "plotly",
    data: ratioComparisonData,
    config: { title: "核心财务指标雷达图" }
  });
  
  // 保存所有图表
  await saveCharts([revenueChart, profitChart, ratioChart], workflow.outputDir);

  // ========== Phase 4: 财务预测 ==========
  console.log("Phase 4: 财务预测建模...");
  
  const forecast = await skill.call("finance", {
    workflow: "forecast",
    historicalData: incomeData,
    method: "arima",  // 或 "linear", "growth_rate"
    years: 3
  });

  // ========== Phase 5: 文档生成 ==========
  console.log("Phase 5: 生成文档...");
  
  // Step 5.1: 生成 Word 初稿
  const wordDoc = await skill.call("Word 文档生成", {
    mode: "create",
    content: {
      title: `${workflow.companyName}商业计划书`,
      sections: buildSections({
        companyBasic,
        financialRatios,
        analysisText,
        industryData,
        forecast
      })
    },
    outputPath: `${workflow.outputDir}/${workflow.companyName}_商业计划书_初稿.docx`
  });
  
  // Step 5.2: 润色内容
  console.log("Phase 5.2: 内容润色...");
  const humanizedDoc = await skill.call("Humanizer", {
    content: wordDoc.content,
    tone: "professional",
    intensity: "medium"
  });
  
  // Step 5.3: 生成最终 Word 文档
  const finalWord = await skill.call("Word 文档生成", {
    mode: "create",
    content: humanizedDoc,
    outputPath: `${workflow.outputDir}/${workflow.companyName}_商业计划书.docx`
  });
  
  // Step 5.4: 生成 PDF 版本
  const finalPdf = await skill.call("PDF 文档生成", {
    mode: "convert",
    sourceFile: finalWord.path,
    outputPath: `${workflow.outputDir}/${workflow.companyName}_商业计划书.pdf`
  });
  
  console.log("✅ 商业计划书生成完成！");
  console.log(`Word版本: ${finalWord.path}`);
  console.log(`PDF版本: ${finalPdf.path}`);
  
  return {
    wordPath: finalWord.path,
    pdfPath: finalPdf.path
  };
}

// 执行生成
generateBusinessPlan("600690.SH", "海尔智家");
```

### 3.2 快速流程：仅生成财务分析章节

```typescript
/**
 * 快速流程：仅生成财务分析部分
 * 适用于补充现有文档
 */

async function generateFinancialAnalysisOnly(companyCode: string) {
  // Step 1: 获取数据
  const financialData = await skill.call("finance-data-retrieval", {
    endpoint: "income",
    params: { ts_code: companyCode, start_date: "20190101", end_date: "20231231" }
  });
  
  // Step 2: 分析
  const analysis = await skill.call("finance", {
    workflow: "financial-analysis",
    data: financialData,
    analysisTypes: ["profitability", "growth"]
  });
  
  // Step 3: 生成图表
  const chart = await skill.call("data", {
    workflow: "visualization",
    chartType: "line",
    data: financialData,
    config: { title: "营收趋势" }
  });
  
  // Step 4: 输出章节
  return {
    content: analysis.narrative,
    chart: chart
  };
}
```

### 3.3 并行流程：多公司对比分析

```typescript
/**
 * 并行流程：生成多家公司的对比分析
 */

async function generateCompetitorAnalysis(companyCodes: string[]) {
  // 并行获取所有公司数据
  const dataPromises = companyCodes.map(code => 
    skill.call("finance-data-retrieval", {
      endpoint: "income",
      params: { ts_code: code, start_date: "20230101", end_date: "20231231" }
    })
  );
  
  const allData = await Promise.all(dataPromises);
  
  // 生成对比图表
  const comparisonChart = await skill.call("data", {
    workflow: "visualization",
    chartType: "grouped_bar",
    data: {
      categories: companyCodes.map(c => c.split('.')[0]),
      series: [
        { name: "营收", values: allData.map(d => d.revenue) },
        { name: "净利润", values: allData.map(d => d.net_profit) }
      ]
    },
    config: { title: "竞争对手财务对比" }
  });
  
  return comparisonChart;
}
```

---

## 4. 错误处理指南

### 4.1 数据获取失败处理

```typescript
/**
 * 数据获取失败时的降级策略
 */

async function getFinancialDataWithFallback(companyCode: string) {
  try {
    // 首选：获取年报数据
    const data = await skill.call("finance-data-retrieval", {
      endpoint: "income",
      params: { ts_code: companyCode }
    });
    return { success: true, data, source: "annual_report" };
  } catch (error) {
    console.warn("年报数据获取失败，尝试获取季报数据...");
    
    try {
      // 备选：获取季报数据
      const quarterlyData = await skill.call("finance-data-retrieval", {
        endpoint: "income_vip",  // 或尝试其他端点
        params: { ts_code: companyCode }
      });
      return { success: true, data: quarterlyData, source: "quarterly_report" };
    } catch (fallbackError) {
      console.error("所有数据源均失败");
      return { 
        success: false, 
        error: "数据获取失败，请手动提供财务数据",
        manualInputRequired: true 
      };
    }
  }
}
```

**数据获取失败处理策略**：

| 失败场景 | 备选方案 | 降级策略 |
|---------|---------|---------|
| 年报数据不可用 | 使用季报数据 | 提示用户数据粒度变化 |
| 财务数据不完整 | 使用最近3年数据 | 在分析中注明数据范围 |
| 公司信息查询失败 | 使用用户输入的公司名称 | 要求用户确认信息 |
| 行业数据获取失败 | 使用通用行业描述 | 从文档中删除具体数值 |

### 4.2 API 限制处理

```typescript
/**
 * API 限流处理
 */

async function callWithRateLimit(skillName: string, params: object, maxRetries = 3) {
  for (let attempt = 1; attempt <= maxRetries; attempt++) {
    try {
      return await skill.call(skillName, params);
    } catch (error) {
      if (error.code === "RATE_LIMITED" && attempt < maxRetries) {
        const delay = Math.pow(2, attempt) * 1000;  // 指数退避
        console.log(`API限流，${delay}ms后重试 (${attempt}/${maxRetries})...`);
        await sleep(delay);
      } else {
        throw error;
      }
    }
  }
}
```

**API 限制处理策略**：

| 限制类型 | 处理方式 | 说明 |
|---------|---------|------|
| 频率限制 | 指数退避重试 | 2s → 4s → 8s |
| 每日配额 | 缓存已有数据 | 使用本地缓存避免重复调用 |
| 并发限制 | 串行化处理 | 避免并行调用同一API |
| 权限不足 | 降级到公开数据 | 使用web_search替代 |

### 4.3 数据不完整处理

```typescript
/**
 * 数据完整性检查与处理
 */

function validateDataCompleteness(data: any, requiredFields: string[]) {
  const missingFields = requiredFields.filter(field => 
    !data[field] || data[field] === null || data[field] === undefined
  );
  
  if (missingFields.length > 0) {
    console.warn(`数据不完整，缺失字段: ${missingFields.join(", ")}`);
    
    return {
      isComplete: false,
      missingFields,
      recommendation: missingFields.length > 2 
        ? "建议手动补充数据" 
        : "可使用估算值继续"
    };
  }
  
  return { isComplete: true };
}

// 使用示例
const validation = validateDataCompleteness(financialData, [
  "total_revenue", "net_profit", "total_assets", "total_liabilities"
]);

if (!validation.isComplete) {
  // 处理缺失数据
  handleMissingData(validation.missingFields);
}
```

**数据不完整应对方法**：

| 缺失数据类型 | 应对方法 | 文档标注 |
|-------------|---------|---------|
| 单年度数据缺失 | 使用插值估算 | "该年度数据为估算值" |
| 某项指标缺失 | 从其他指标推导 | "根据XX数据推算" |
| 整表缺失 | 从web_search获取 | "数据来源：公开信息" |
| 历史数据不完整 | 缩短分析周期 | "基于近X年数据分析" |

### 4.4 错误恢复流程

```typescript
/**
 * 全局错误恢复策略
 */

class BusinessPlanGenerator {
  private errors: any[] = [];
  private warnings: any[] = [];
  
  async generateWithRecovery(config: any) {
    try {
      // Phase 1: 数据收集
      const data = await this.collectData(config).catch(err => {
        this.handleDataError(err, "Phase 1");
        return this.getMinimalData(config);  // 使用最小数据集继续
      });
      
      // Phase 2: 分析
      const analysis = await this.analyze(data).catch(err => {
        this.handleAnalysisError(err, "Phase 2");
        return { skipped: true, reason: err.message };
      });
      
      // Phase 3-5: 继续执行...
      
      // 生成错误报告
      if (this.errors.length > 0) {
        await this.generateErrorReport();
      }
      
      return {
        success: this.errors.length === 0,
        document: finalDoc,
        errors: this.errors,
        warnings: this.warnings
      };
    } catch (fatalError) {
      return {
        success: false,
        error: fatalError.message,
        partialOutput: this.getPartialOutput()
      };
    }
  }
  
  private handleDataError(error: any, phase: string) {
    this.errors.push({ phase, error, timestamp: new Date() });
    console.error(`[${phase}] 数据错误: ${error.message}`);
  }
}
```

---

## 5. 最佳实践

### 5.1 数据缓存策略

```typescript
/**
 * 建议：对频繁使用的数据进行缓存
 */

const cache = {
  companyData: new Map(),
  industryData: new Map(),
  
  get(key: string) {
    const item = this.companyData.get(key);
    if (item && Date.now() - item.timestamp < 3600000) {  // 1小时缓存
      return item.data;
    }
    return null;
  },
  
  set(key: string, data: any) {
    this.companyData.set(key, { data, timestamp: Date.now() });
  }
};
```

### 5.2 日志记录规范

```typescript
/**
 * 建议：记录完整的调用链路
 */

const logger = {
  info: (msg: string, meta?: object) => {
    console.log(`[INFO] ${msg}`, meta || '');
  },
  
  skillCall: (skillName: string, params: object) => {
    console.log(`[SKILL] Calling ${skillName}`, { params });
  },
  
  skillResult: (skillName: string, success: boolean, duration: number) => {
    console.log(`[SKILL] ${skillName} ${success ? '✓' : '✗'} (${duration}ms)`);
  }
};
```

### 5.3 性能优化建议

| 优化点 | 方法 | 效果 |
|-------|------|------|
| 数据获取 | 并行调用独立API | 减少总耗时 |
| 图表生成 | 延迟加载非关键图表 | 提升响应速度 |
| 文档生成 | 分段生成再合并 | 避免内存溢出 |
| 重复调用 | 使用缓存 | 减少API调用次数 |

---

## 6. 附录

### 6.1 常用股票代码格式

| 市场 | 代码格式 | 示例 |
|-----|---------|------|
| 上海证券交易所 | XXXXXX.SH | 600690.SH |
| 深圳证券交易所 | XXXXXX.SZ | 000001.SZ |
| 北京证券交易所 | XXXXXX.BJ | 430047.BJ |
| 香港交易所 | XXXXXX.HK | 09999.HK |
| 美股 | 代码.US | AAPL.US |

### 6.2 财务指标速查表

| 指标 | 计算公式 | 数据来源 |
|-----|---------|---------|
| ROE | 净利润 / 净资产 | balancesheet + income |
| ROA | 净利润 / 总资产 | balancesheet + income |
| 毛利率 | (营收-成本) / 营收 | income |
| 净利率 | 净利润 / 营收 | income |
| 资产负债率 | 总负债 / 总资产 | balancesheet |

### 6.3 版本记录

| 版本 | 日期 | 更新内容 |
|-----|------|---------|
| v1.0 | 2026-03-29 | 初始版本，包含6个子技能的完整调用指南 |

---

*文档生成时间：2026-03-31*
*适用 Skill 版本：business-plan-creator v4.0+*