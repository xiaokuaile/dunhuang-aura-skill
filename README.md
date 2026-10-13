# Dunhuang Aura Skill

一个用于生成和修改敦煌矿物美学商业视觉及敦煌飞天人物的AI Skill，适合Codex、Claude Code及其他支持`SKILL.md`约定的智能体环境。

它不是一份简单的提示词合集。Skill会先判断交付物、比例、文字状态和构图模式，再约束色板、材质、光线、物体几何、敦煌元素密度及最终质检。

## 能做什么

- 5:2推特/X长文封面
- 无文字的全画幅商业主视觉
- 带精确标题的文章封面
- 敦煌风产品广告和电商主图
- AI图像工具、创意工作流主题封面
- 文化活动海报
- 手机和产品展示图
- 已有图片的去字、补满、平衡左右、降低装饰等局部修改
- 同一视觉系统下的多尺寸、多物料延展
- 3:4自然飞舞的敦煌飞天人物，传统服饰、飘带与壁画色彩
- 保留身份、面部特征、发型、原动作和构图的照片风格转换
- 明确要求后才生成弓箭或射箭场景，并检查弓、弦、箭与双手关系

## 两种视觉模式

商业任务继续使用原有商业模式，默认5:2。人物飞天任务使用独立的[飞天人物模式](references/apsara-mode.md)，新图默认3:4、自然飞舞或舞蹈姿态，不主动添加弓箭和射箭动作。商业模板中的“排除飞天”只适用于商业模式。

照片转换优先保留原图身份、面部特征、发型、未要求改变的动作、道具、构图与比例；只改画风时，不强行改成飞舞动作或裁成3:4。原图已有弓箭也不自动删除，但不增添弓箭或新射箭动作。明确要求射箭时，另用射箭模板检查结构。

## 商业模式视觉特征

- 炭黑洞窟和黑色岩石
- 沙色矿物壁画面板
- 朱砂、石绿、石青飘带
- 克制的赭石金光
- 陶瓷、玻璃、铜、石材的真实质感
- 前景产品、中景壁画、远景洞窟或山体的三层景深
- 敦煌元素服务商业主体，不使用宗教人物做装饰

![5:2无文字示例](assets/example-5x2-text-free.png)

## 安装

### Codex

```bash
git clone https://github.com/xiaokuaile/dunhuang-aura-skill.git ~/.codex/skills/dunhuang-aura
```

重启或重新打开Codex会话后调用：

```text
$dunhuang-aura 生成一张无文字的5:2商业封面，左右都要有明确主体，主题是AI图像生产。
```

### Claude Code

```bash
git clone https://github.com/xiaokuaile/dunhuang-aura-skill.git .claude/skills/dunhuang-aura
```

然后在任务中明确要求读取该Skill并生成或修改图片。

以上安装命令使用本 fork。PR 合并前，新增规则只在 PR 分支；已有安装需要确认来源、取得对应更新，并在生成流程中实际加载更新后的 Skill。仓库修改或 PR 合并不会自动安装 Skill，也不会自动改变当前聊天的图片生成能力。

## 使用示例

```text
使用 $dunhuang-aura 生成5:2横版封面。不要文字和留白。左侧是一只大型矿物彩陶瓷瓶和三层发光画框，右侧是护肤品与手机展示，中间保留水面景深通道。
```

```text
使用 $dunhuang-aura 修改这张图：删除所有文字，保留产品、光线、色板和构图，把原来的标题区补成完整的洞窟画廊。
```

```text
使用 $dunhuang-aura 为一个茶品牌做一张5:2产品主视觉。茶罐必须保持原图形状，右侧产品占画面35%，左侧保留标题区，敦煌元素只使用飘带和藻井边框。
```

```text
使用 $dunhuang-aura 生成一位正常的敦煌飞天，3:4，自然飞舞，传统服饰和飘带，敦煌壁画色彩，不要弓箭和射箭动作。
```

```text
使用 $dunhuang-aura 将上传照片改为敦煌飞天画风，保留人物身份、面部特征、发型、原动作、构图和比例，只改变服饰与画面材质。
```

```text
使用 $dunhuang-aura 生成一位拉弓瞄准的飞天，3:4。弓体连续，单根弓弦连接两端；箭尾搭弦，箭杆对齐支撑位置，持弓手和拉弦手动作连贯。
```

## 仓库结构

```text
dunhuang-aura/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── assets/
│   └── example-5x2-text-free.png
├── references/
│   ├── apsara-mode.md
│   ├── prompt-recipes.md
│   ├── qa-checklist.md
│   ├── style-system.md
│   └── workflows.md
├── scripts/
│   └── check_prompt.py
├── tests/
│   ├── invalid-vague.txt
│   ├── reference-existing-bow.txt
│   ├── test_check_prompt.py
│   └── valid-text-free.txt
├── LICENSE
└── README.md
```

## 提示词检查

```bash
python3 scripts/check_prompt.py your-prompt.txt --mode text-free --ratio 5:2
```

脚本会检查比例、文字禁用、敦煌色板、构图、材质、光线和常见AI套模板词。它只负责检查提示词完整度，不替代生成后的看图验收。

飞天人物提示词检查（省略比例时默认3:4）：

```bash
python3 scripts/check_prompt.py portrait.txt --scene apsara --mode text-free
```

照片转换使用原图比例；只有已明确要求新射箭场景时，才加射箭标记：

```bash
python3 scripts/check_prompt.py photo.txt --scene apsara --reference-photo --ratio 4:5
python3 scripts/check_prompt.py archery.txt --scene apsara --archery-requested --ratio 3:4
```

`--archery-requested` 是调用者记录用户明确要求的标记，检查器不能凭提示词替用户授权。射箭自动检查针对拉弓/瞄准模板；携弓、放箭等其他阶段按[飞天人物模式](references/apsara-mode.md)人工检查。`--mode` 仍支持 `text-free`、`exact-text` 和 `placeholder-free`，商业模式的原有调用方式保持兼容。

检查器是启发式文字检查，可能漏报或误报。提示词通过只说明部分规则在文字中出现；真实图片仍需检查身份相似度、人物结构、飘带遮挡，以及弓弦、箭尾、箭杆和双手的可见连接。未生成并查看图片时，图片验收必须标为“待执行”，不能写成“通过”。

运行单元测试：

```bash
python3 -m unittest discover -s tests -v
```

## 设计边界

商业模式默认排除佛像、菩萨、飞天、礼拜场景和直接复制的壁画人物。明确要求飞天人物时进入独立人物模式，不套用商业排除规则。

人物模式用于风格化创作，不宣称某个年代或洞窟的准确复原。若任务本身是考古复原、历史重建或宗教礼拜内容，应先提供具体年代、洞窟、图像依据和准确性要求，不能直接套用本 Skill。

## 作者与来源

原始 Skill 来自 [govin-ai/dunhuang-aura-skill](https://github.com/govin-ai/dunhuang-aura-skill)，作者署名为 Govin。本 fork 的扩展保留原有 MIT 许可证与 `Copyright (c) 2026 Govin`。

## License

MIT
