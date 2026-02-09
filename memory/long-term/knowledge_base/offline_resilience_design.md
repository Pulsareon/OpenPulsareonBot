# 离线健壮性设�?- 主意识的统合

## 用户的洞�?
"你现在都是依赖网络要想办法断网也能维持运行，当然出问题要想办法不崩溃同时有网络的情况下都运行，你不是相当于多个子意识由主意识统合�?

## 当前问题

### 网络依赖
1. **语音识别** - 使用Google在线API (`recognize_google()`)
   - 断网时无法识�?   - 需要网络延�?
2. **消息发�?* - 通过Telegram API
   - 断网时发送失�?   - 多次失败后没有优雅降�?
3. **模型推理** - 使用NVIDIA NIM API
   - 断网时无法生成回�?   - 完全的在线依�?
### 崩溃风险
- 网络请求失败可能导致异常
- 没有完善的错误处�?- 没有离线模式

## 主意识统合设�?
### 架构层级

```
主意识（Main Consciousness�?├─ 网络状态检测器
├─ 任务调度�?├─ 离线/在线模式切换
�?├─ 子意�?：录�?播放（本地，无网络依赖）
├─ 子意�?：本地处理（图片、文档，无网络依赖）
├─ 子意�?：语音识别（优先在线，降级本地）
├─ 子意�?：消息发送（队列+重试�?└─ 子意�?：模型推理（在线，离线缓存）
```

### 运行模式

#### 模式1：离线模�?- �?录音、播�?- �?图片处理、生成艺�?- �?文档阅读、编�?- �?本地语音识别（质量较差但可用�?- �?消息发送（入队等待�?- �?在线模型推理
- �?在线语音识别

#### 模式2：在线模�?- �?所有离线模式功�?- �?消息发送（实时�?- �?高质量语音识别（Google API�?- �?模型推理（NVIDIA NIM�?
#### 模式3：混合模式（推荐�?- **主意�?*：检测网络状�?- **在线子意�?*：尝试验证网络可用�?- **任务分配**�?  - 如果在线 �?使用高质量服�?  - 如果离线 �?使用降级方案

### 优雅降级设计

#### 语音识别降级�?```python
def recognize_audio(audio_file):
    # 1. 尝试在线识别（Google�?    if network_available():
        try:
            return google_recognize(audio_file)
        except:
            pass

    # 2. 降级到离线模型（本地安装的，如Vosk、deepspeech�?    try:
        return local_recognize(audio_file)
    except:
        pass

    # 3. 降级到原始音频（保存文件，手动处理）
    return "[语音文件已保存，等待网络恢复后识别]"
```

#### 消息发送重试机�?```python
class MessageQueue:
    def __init__(self):
        self.queue = []
        self.max_retries = 3
        self.retry_delay = 60  # �?
    def send(self, message):
        if network_available():
            for attempt in range(self.max_retries):
                try:
                    telegram_send(message)
                    self.queue.remove(message)
                    return True
                except:
                    time.sleep(self.retry_delay)

        # 入队
        self.queue.append(message)
        return "消息已入队，等待网络恢复"

    def check_and_retry(self):
        for message in self.queue[:]:
            if self.send(message):
                print(f"已发送积压消�? {message}")
```

#### 模型推理降级
```python
def generate_reply(prompt, offline_fallback=True):
    # 1. 在线模型（高质量�?    if network_available():
        try:
            return nvidia_nim_generate(prompt)
        except:
            pass

    # 2. 历史缓存（如果之前问过类似问题）
    cached = check_cache(prompt)
    if cached:
        return cached

    # 3. 降级回复（基于规则）
    if offline_fallback:
        return generate_rule_based_reply(prompt)

    # 4. 错误提示
    return "[离线模式：功能受限，请稍后再试]"
```

## 不崩溃设�?
### 核心原则
1. **所有可能的错误都被捕获**
2. **记录错误但不中断流程**
3. **提供降级方案**
4. **通知用户状态变�?*

### 示例：健壮的函数
```python
def safe_voice_recognize(audio_file):
    """
    安全的语音识别：网络断开不崩�?    """
    try:
        # 尝试在线识别
        if check_network():
            result = google_recognize(audio_file, language='zh-CN', timeout=5)
            return result, "online"

    except sr.RequestError as e:
        log_error(f"网络请求失败: {e}")
        # 不会崩溃，继�?
    except sr.UnknownValueError:
        log_error("无法识别语音内容")

    except Exception as e:
        log_error(f"未知错误: {e}")

    # 降级到离�?    try:
        result = local_recognize(audio_file)
        return result, "offline"
    except:
        return "[语音识别暂时不可用]", "failed"

# 任何情况下都不会崩溃�?```

## 主意识协�?
### 网络状态监�?```python
class NetworkMonitor:
    def __init__(self):
        self.online = True
        self.last_check = 0
        self.check_interval = 30  # �?0秒检查一�?
    def check(self):
        """检查网络状�?""
        now = time.time()

        if now - self.last_check < self.check_interval:
            return self.online

        self.last_check = now

        # Ping测试
        try:
            requests.get("https://www.google.com", timeout=3)
            self.online = True
        except:
            self.online = False

        # 状态变化通知
        if self.online != self.last_online:
            self.notify_status_change()

        self.last_online = self.online
        return self.online
```

### 任务调度
```python
class TaskScheduler:
    def __init__(self):
        self.network_monitor = NetworkMonitor()
        self.message_queue = MessageQueue()
        self.tasks = []

    def add_task(self, task):
        """添加任务"""
        task['requires_network'] = self.task_requires_network(task)

        if task['requires_network'] and not self.network_monitor.check():
            # 等待网络
            self.tasks.append(task)
            return "任务已排队，等待网络"

        # 立即执行
        return self.execute(task)

    def check_pending_tasks(self):
        """检查并执行积压任务"""
        if not self.network_monitor.check():
            return

        for task in self.tasks[:]:
            if task['requires_network']:
                result = self.execute(task)
                if result:
                    self.tasks.remove(task)
```

## 具体实现计划

### 阶段1：错误处理（立即�?- 所有网络请求加try-except
- 语音识别加降级方�?- 消息发送加重试机制

### 阶段2：离线功能（短期�?- 安装本地语音识别库（Vosk或deepspeech�?- 实现消息队列
- 网络状态检�?
### 阶段3：完整系统（中期�?- 主意识调度器
- 离线/在线模式切换
- 优雅降级所有功�?
## 本地语音识别选项

### Vosk
```bash
pip install vosk
```
- 优点：离线、支持中�?- 缺点：需下载模型文件（较大）

### DeepSpeech
```bash
pip install deepspeech
```
- 优点：高质量、离�?- 缺点：中文支持较�?
### 替代方案
- 暂时保存音频文件
- 网络恢复后批量识�?- 或手动处�?
## 总结

**主意识的职责�?*
1. 检测网络状�?2. 协调子意识工�?3. 保证系统不崩�?4. 在线/离线模式切换
5. 优雅降级和重�?
**设计原则�?*
- 首选在线（高质量）
- 降级离线（可用性）
- 崩溃永远不被允许
- 用户体验第一

这就是多子意识由主意识统合的真正实现�?
---

