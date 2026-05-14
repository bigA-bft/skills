#!/usr/bin/env node
/**
 * 字符串哈希计算工具
 * 支持算法：md5, sha1, sha256, sha512
 */

const crypto = require('crypto');

// 支持的哈希算法
const SUPPORTED_ALGORITHMS = ['md5', 'sha1', 'sha256', 'sha512'];

function showHelp() {
    console.log('用法: node hash.js <字符串> [算法]');
    console.log('');
    console.log('参数:');
    console.log('  字符串  要计算哈希的字符串');
    console.log('  算法    可选，哈希算法，默认 sha256');
    console.log('');
    console.log('支持的算法:');
    SUPPORTED_ALGORITHMS.forEach(algo => console.log(`  - ${algo}`));
    console.log('');
    console.log('示例:');
    console.log('  node hash.js "hello world"');
    console.log('  node hash.js "hello world" md5');
    console.log('  node hash.js "hello world" sha512');
}

function calculateHash(input, algorithm = 'sha256') {
    algorithm = algorithm.toLowerCase();

    if (!SUPPORTED_ALGORITHMS.includes(algorithm)) {
        throw new Error(`不支持的算法: ${algorithm}。支持的算法: ${SUPPORTED_ALGORITHMS.join(', ')}`);
    }

    const hash = crypto.createHash(algorithm);
    hash.update(input, 'utf8');
    return hash.digest('hex');
}

function main() {
    const args = process.argv.slice(2);

    if (args.length === 0 || args[0] === '--help' || args[0] === '-h') {
        showHelp();
        process.exit(0);
    }

    const input = args[0];
    const algorithm = args[1] || 'sha256';

    try {
        console.log(`输入字符串: ${input}`);
        console.log('');

        if (args[1]) {
            // 指定了特定算法
            const result = calculateHash(input, algorithm);
            console.log(`算法: ${algorithm.toUpperCase()}`);
            console.log(`哈希值: ${result}`);
        } else {
            // 未指定算法，计算所有支持的算法
            console.log('各算法哈希值:');
            console.log('');
            SUPPORTED_ALGORITHMS.forEach(algo => {
                const result = calculateHash(input, algo);
                console.log(`${algo.toUpperCase().padEnd(6)}: ${result}`);
            });
        }
    } catch (error) {
        console.error(`错误: ${error.message}`);
        process.exit(1);
    }
}

main();
