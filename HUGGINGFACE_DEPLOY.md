# 发布 LanguageMentor 到 HuggingFace Space

## 前置条件

1. 拥有 HuggingFace 账号（如果没有，请访问 https://huggingface.co/join 注册）
2. 已安装 Git 和 Git LFS（用于上传大文件）

## 发布步骤

### 方法一：通过 HuggingFace 网页界面（推荐）

1. **创建新的 Space**
   - 访问 https://huggingface.co/spaces
   - 点击 "Create new Space"
   - 填写信息：
     - **Space name**: `language-mentor`（或你喜欢的名称）
     - **SDK**: 选择 `Gradio`
     - **Hardware**: 选择 `CPU basic`（免费）或 `CPU upgrade`（需要付费）
     - **Visibility**: 选择 `Public`（公开）或 `Private`（私有）
   - 点击 "Create Space"

2. **上传文件**
   - 在 Space 页面，点击 "Files and versions" 标签
   - 点击 "Add file" → "Upload files"
   - 上传以下必需文件：
     - `app.py` - Gradio 应用主文件
     - `README_HF.md` - Space 描述文件（会自动识别为 README.md）
     - `requirements.txt` - Python 依赖
     - `config.json.example` - 配置文件示例
   - 上传 `src/` 目录下的所有 Python 文件

3. **设置环境变量（可选）**
   - 在 Space 设置页面，找到 "Repository secrets"
   - 添加以下环境变量（如果需要）：
     - `OPENAI_API_KEY`: 你的 OpenAI API Key
     - `DEEPSEEK_API_KEY`: 你的 DeepSeek API Key（如果使用）

4. **等待构建**
   - HuggingFace 会自动检测到文件并开始构建
   - 构建过程可能需要几分钟
   - 构建完成后，你的应用就可以访问了！

### 方法二：通过 Git 命令行

1. **克隆你的 Space 仓库**
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/language-mentor
   cd language-mentor
   ```

2. **复制项目文件**
   ```bash
   # 复制必需文件
   cp ../LanguageMentor/app.py .
   cp ../LanguageMentor/README_HF.md README.md
   cp ../LanguageMentor/requirements.txt .
   cp ../LanguageMentor/config.json.example .
   
   # 复制源代码
   cp -r ../LanguageMentor/src .
   ```

3. **提交并推送**
   ```bash
   git add .
   git commit -m "Initial commit: LanguageMentor v0.5"
   git push
   ```

4. **等待构建**
   - HuggingFace 会自动检测到推送并开始构建
   - 在 Space 页面查看构建日志

## 文件结构要求

HuggingFace Space 需要以下文件结构：

```
language-mentor/
├── app.py              # Gradio 应用主文件（必需）
├── README.md           # Space 描述（必需，我们使用 README_HF.md）
├── requirements.txt    # Python 依赖（必需）
├── config.json.example # 配置文件示例（可选）
└── src/                # 源代码目录
    ├── agents/
    ├── scenarios/
    ├── config.py
    └── scenario_manager.py
```

## 注意事项

1. **API Key 安全**
   - 不要在代码中硬编码 API Key
   - 使用环境变量或 HuggingFace Secrets
   - `config.json` 不应包含真实的 API Key

2. **依赖管理**
   - 确保 `requirements.txt` 包含所有必需的依赖
   - 避免使用过新的或不稳定的包版本

3. **资源限制**
   - 免费 Space 有 CPU 和内存限制
   - 如果应用响应慢，考虑升级到付费硬件

4. **构建时间**
   - 首次构建可能需要 5-10 分钟
   - 后续更新通常更快（2-5 分钟）

5. **日志查看**
   - 在 Space 页面可以查看构建日志和运行日志
   - 如果构建失败，检查日志中的错误信息

## 更新应用

当你需要更新应用时：

1. **通过网页界面**：直接上传新文件覆盖旧文件
2. **通过 Git**：
   ```bash
   git add .
   git commit -m "Update: description"
   git push
   ```

## 访问你的应用

构建完成后，你的应用可以通过以下 URL 访问：
```
https://huggingface.co/spaces/YOUR_USERNAME/language-mentor
```

## 故障排除

### 构建失败
- 检查 `requirements.txt` 中的依赖是否正确
- 查看构建日志中的错误信息
- 确保 `app.py` 中没有语法错误

### 运行时错误
- 检查环境变量是否正确设置
- 查看运行日志
- 确保 API Key 有效

### 应用无法访问
- 检查 Space 是否设置为 Public
- 确认构建已完成
- 查看 Space 状态页面

## 参考资源

- [HuggingFace Spaces 文档](https://huggingface.co/docs/hub/spaces)
- [Gradio 文档](https://gradio.app/docs/)
- [Space 示例](https://huggingface.co/spaces)

