---
name: hash-calculator
description: 字符串哈希计算工具，支持 MD5、SHA1、SHA256、SHA512 等常用哈希算法。当用户需要计算字符串哈希值、验证数据完整性、生成校验码时使用。可计算单个算法或同时计算多种算法的哈希值。
---

# 哈希计算器技能

## 功能

- 计算字符串的哈希值
- 支持多种算法：MD5、SHA1、SHA256、SHA512
- 可同时输出所有算法的哈希值
- 也可指定特定算法计算

## 使用方法

### 基本用法（计算所有算法）

```bash
node .claude/skills/hash-calculator/scripts/hash.js "字符串"
```

### 指定算法

```bash
node .claude/skills/hash-calculator/scripts/hash.js "字符串" <算法>
```

支持的算法：`md5`、`sha1`、`sha256`、`sha512`

## 示例

### 示例 1：计算所有哈希值
用户："计算 hello world 的哈希值"

```bash
node .claude/skills/hash-calculator/scripts/hash.js "hello world"
```

输出：
```
输入字符串: hello world

各算法哈希值:

MD5   : 5eb63bbbe01eeed093cb22bb8f5acdc3
SHA1  : 2aae6c35c94fcfb415dbe95f408b9ce91ee846ed
SHA256: b94d27b9934d3e08a52e52d7da7dabfac484efe37a5380ee9088f7ace2efcde9
SHA512: 309ecc489c12d6eb4cc40f50c902f2b4d0ed77ee511a7c7a9bcd3ca86d4cd86f989dd35bc5ff499670da34255b45b0cfd830e81f605dcf7dc5542e93ae9cd76f
```

### 示例 2：只计算 MD5
用户："hello world 的 MD5 是多少"

```bash
node .claude/skills/hash-calculator/scripts/hash.js "hello world" md5
```

输出：
```
输入字符串: hello world

算法: MD5
哈希值: 5eb63bbbe01eeed093cb22bb8f5acdc3
```

### 示例 3：计算 SHA256
用户："计算 '123456' 的 SHA256"

```bash
node .claude/skills/hash-calculator/scripts/hash.js "123456" sha256
```

输出：
```
输入字符串: 123456

算法: SHA256
哈希值: 8d969eef6ecad3c29a3a629280e686cf0c3f5d5a86aff3ca12020c923adc6c92
```

## 注意事项

1. 字符串区分大小写，`Hello` 和 `hello` 的哈希值不同
2. 默认使用 UTF-8 编码处理字符串
3. 输出结果为小写十六进制字符串
4. 如需计算文件哈希，需要先读取文件内容为字符串
